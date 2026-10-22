/* FGLLID site data — load / merge / apply / file-import helpers */
(function (global) {
  const STORAGE_KEY = "fgllid_site_v1";
  const SITE_JSON = "data/site.json";

  function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  function fileBaseName(name) {
    return String(name || "")
      .replace(/\.[^.]+$/, "")
      .replace(/[_-]+/g, " ")
      .trim() || "Untitled";
  }

  function readFileAsDataURL(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(reader.error || new Error("read failed"));
      reader.readAsDataURL(file);
    });
  }

  function readFileAsText(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(String(reader.result || ""));
      reader.onerror = () => reject(reader.error || new Error("read failed"));
      reader.readAsText(file, "UTF-8");
    });
  }

  async function fetchDefaultSite() {
    const res = await fetch(SITE_JSON, { cache: "no-store" });
    if (!res.ok) throw new Error("site.json load failed");
    return res.json();
  }

  function loadLocalOverride() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }

  function saveLocal(data) {
    const next = deepClone(data);
    next.updatedAt = new Date().toISOString();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    return next;
  }

  function clearLocal() {
    localStorage.removeItem(STORAGE_KEY);
  }

  async function getSiteData() {
    const base = await fetchDefaultSite();
    const override = loadLocalOverride();
    return override ? { ...deepClone(base), ...deepClone(override), version: override.version || base.version } : base;
  }

  function downloadJson(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json;charset=utf-8",
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename || "site.json";
    a.click();
    URL.revokeObjectURL(a.href);
  }

  /** Import one or more files → mutate site data (no manual typing). */
  async function importFilesIntoSite(files, site) {
    const data = deepClone(site || {});
    data.gallery = Array.isArray(data.gallery) ? data.gallery : [];
    data.publications = Array.isArray(data.publications) ? data.publications : [];
    data.media = Array.isArray(data.media) ? data.media : [];
    const report = { json: 0, images: 0, text: 0, skipped: 0 };

    for (const file of [...files]) {
      const name = file.name || "";
      const lower = name.toLowerCase();

      if (lower.endsWith(".json")) {
        const text = await readFileAsText(file);
        const parsed = JSON.parse(text);
        Object.assign(data, parsed);
        data.gallery = Array.isArray(data.gallery) ? data.gallery : [];
        data.publications = Array.isArray(data.publications) ? data.publications : [];
        data.media = Array.isArray(data.media) ? data.media : [];
        report.json += 1;
        continue;
      }

      if (/\.(png|jpe?g|gif|webp|svg)$/i.test(lower)) {
        const src = await readFileAsDataURL(file);
        const label = fileBaseName(name);
        const tag = label.split(/\s+/)[0] || "Photo";
        /* DG photo by filename hint */
        if (/^dg|director|ညွှန်ကြား|photo-dg/i.test(name)) {
          data.dg = data.dg || {};
          data.dg.photo = src;
        } else {
          data.gallery.unshift({ src, label, tag, fromFile: name });
        }
        report.images += 1;
        continue;
      }

      if (/\.(txt|md|csv)$/i.test(lower)) {
        const text = await readFileAsText(file);
        const title = fileBaseName(name);
        data.publications.unshift({
          code: String(data.publications.length + 1).padStart(2, "0"),
          title: title.slice(0, 80),
          body: text.slice(0, 4000),
          fromFile: name,
        });
        report.text += 1;
        continue;
      }

      report.skipped += 1;
    }

    data.updatedAt = new Date().toISOString();
    return { data, report };
  }

  /** Apply site.json fields onto the public index DOM (best-effort). */
  function applySiteToDom(data) {
    if (!data || typeof data !== "object") return;

    if (data.hotline) {
      const label = document.querySelector("[data-i18n='top.hotline']");
      if (label && data.hotline.label) label.textContent = data.hotline.label;
      const hotline = document.querySelector(".topbar-hotline");
      if (hotline && data.hotline.primary) {
        hotline.textContent = data.hotline.primary;
        hotline.href = `tel:${String(data.hotline.primary).replace(/\D/g, "")}`;
      }
      const phone = document.querySelector(".topbar-phone");
      if (phone && (data.hotline.officeDisplay || data.hotline.office)) {
        phone.textContent = data.hotline.officeDisplay || data.hotline.office;
        phone.href = `tel:${String(data.hotline.office || "").replace(/\D/g, "")}`;
      }
    }

    if (data.dg) {
      const img = document.querySelector(".dg-frame img");
      if (img && data.dg.photo) {
        img.src = data.dg.photo;
        img.alt = `${data.dg.name || ""} — ${data.dg.role || ""}`.trim();
      }
      const nameEl = document.querySelector(".dg-caption h4");
      if (nameEl) {
        const lang = document.documentElement.dataset.lang || "mm";
        const nm =
          lang === "en"
            ? data.dg.nameEn || data.dg.name
            : data.dg.name || data.dg.nameEn;
        if (nm) {
          nameEl.textContent = nm;
          nameEl.setAttribute("data-i18n", "admin.dg.name");
        }
      }
      const bio = document.querySelector('[data-i18n="admin.bio.text"]');
      if (bio && data.dg.bio) bio.textContent = data.dg.bio;
      const greet = document.querySelector('[data-i18n="admin.greet.text"]');
      if (greet && data.dg.greet) greet.textContent = data.dg.greet;
    }

    if (Array.isArray(data.deputies)) {
      document.querySelectorAll(".deputy-row-card").forEach((card, i) => {
        const d = data.deputies[i];
        if (!d) return;
        const init = card.querySelector(".deputy-initials");
        const frame = card.querySelector(".deputy-photo-frame");
        if (d.photo && frame) {
          frame.innerHTML = `<img src="${d.photo}" alt="" />`;
        } else if (init && d.initial) {
          init.textContent = d.initial;
        }
        const h4 = card.querySelector("h4");
        if (h4 && d.title) h4.textContent = d.title;
        const ps = card.querySelectorAll(".deputy-text p");
        if (ps[1] && d.desc) ps[1].textContent = d.desc;
      });
    }

    const pubsList = document.getElementById("pubs-list");
    if (pubsList && Array.isArray(data.publications) && data.publications.length) {
      pubsList.innerHTML = data.publications
        .map((p, i) => {
          const isExtra = !!(p.extra || i >= 8);
          const cls = isExtra ? "pub-cover pub-extra" : "pub-cover";
          const popup = isExtra ? ' data-popup="1"' : "";
          return `<div class="${cls}"${popup}><strong>${escapeHtml(p.code || String(i + 1).padStart(2, "0"))}</strong> ${escapeHtml(p.title || "")}</div>`;
        })
        .join("");
    }

    const galleryList = document.getElementById("gallery-list");
    if (galleryList && Array.isArray(data.gallery) && data.gallery.length) {
      galleryList.innerHTML = data.gallery
        .map((g, i) => {
          const isExtra = !!(g.extra || i >= 8);
          const cls = isExtra
            ? "pub-cover gallery-tile pub-extra"
            : "pub-cover gallery-tile";
          const popup = isExtra ? ' data-popup="1"' : "";
          const src = escapeHtml(g.src || "");
          const tag = escapeHtml(g.tag || "Photo");
          const label = escapeHtml(g.label || "");
          return `<div class="${cls}"${popup} style="background-image:url('${src}')"><strong>${tag}</strong> ${label}</div>`;
        })
        .join("");
    }

    document.dispatchEvent(new CustomEvent("fgllid:site-applied", { detail: data }));
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  global.FGLLID_SITE = {
    STORAGE_KEY,
    SITE_JSON,
    fetchDefaultSite,
    loadLocalOverride,
    saveLocal,
    clearLocal,
    getSiteData,
    downloadJson,
    importFilesIntoSite,
    applySiteToDom,
    deepClone,
    fileBaseName,
  };
})(window);
