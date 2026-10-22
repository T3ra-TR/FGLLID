(() => {
  const S = window.FGLLID_SITE;
  if (!S) {
    console.error("site-data.js missing");
    return;
  }

  let site = null;

  const $ = (id) => document.getElementById(id);
  const statusEl = $("import-status");
  const dropZone = $("drop-zone");
  const fileInput = $("file-input");

  function setStatus(msg) {
    if (statusEl) statusEl.textContent = msg || "";
  }

  function syncFormFromSite() {
    if (!site) return;
    $("f-hotline-label").value = site.hotline?.label || "";
    $("f-hotline-primary").value = site.hotline?.primary || "";
    $("f-hotline-office").value = site.hotline?.office || "";
    $("f-dg-name").value = site.dg?.name || "";
    $("f-dg-role").value = site.dg?.role || "";
    $("f-dg-photo").value = site.dg?.photo || "";
    $("f-dg-bio").value = site.dg?.bio || "";
    $("raw-json").value = JSON.stringify(site, null, 2);

    const prev = $("dg-preview");
    if (prev) {
      prev.style.backgroundImage = site.dg?.photo ? `url("${site.dg.photo}")` : "";
    }

    const gal = site.gallery || [];
    $("gallery-count").textContent = `(${gal.length})`;
    $("gallery-thumbs").innerHTML = gal
      .map(
        (g) =>
          `<div class="ad-thumb" style="background-image:url('${String(g.src || "").replace(/'/g, "%27")}')"><span>${escapeText(g.tag || "")} ${escapeText(g.label || "")}</span></div>`
      )
      .join("");

    const pubs = site.publications || [];
    $("pubs-count").textContent = `(${pubs.length})`;
    $("pubs-list-admin").innerHTML = pubs
      .map(
        (p) =>
          `<div class="ad-list-item"><strong>${escapeText(p.code || "")}</strong><span>${escapeText(p.title || "")}</span></div>`
      )
      .join("");
  }

  function escapeText(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function readFormIntoSite() {
    if (!site) site = {};
    site.hotline = site.hotline || {};
    site.hotline.label = $("f-hotline-label").value.trim();
    site.hotline.primary = $("f-hotline-primary").value.trim();
    site.hotline.office = $("f-hotline-office").value.trim();
    site.dg = site.dg || {};
    site.dg.name = $("f-dg-name").value.trim();
    site.dg.role = $("f-dg-role").value.trim();
    site.dg.photo = $("f-dg-photo").value.trim();
    site.dg.bio = $("f-dg-bio").value.trim();
    try {
      const raw = JSON.parse($("raw-json").value);
      /* Prefer raw JSON as source of truth if valid; keep form hotline/dg overlays */
      site = { ...raw, hotline: { ...raw.hotline, ...site.hotline }, dg: { ...raw.dg, ...site.dg } };
    } catch {
      /* keep form-based site if raw invalid */
    }
    return site;
  }

  async function handleFiles(fileList) {
    if (!fileList?.length) return;
    readFormIntoSite();
    try {
      const { data, report } = await S.importFilesIntoSite(fileList, site);
      site = data;
      S.saveLocal(site);
      syncFormFromSite();
      setStatus(
        `တင်ပြီး: JSON ${report.json} · ပုံ ${report.images} · စာသား ${report.text}` +
          (report.skipped ? ` · ကျော် ${report.skipped}` : "") +
          " — Save လုပ်ပြီး index တွင် ကြည့်ပါ"
      );
    } catch (err) {
      console.error(err);
      setStatus("ဖိုင်တင်မရပါ: " + (err.message || err));
    }
  }

  async function boot() {
    try {
      site = await S.getSiteData();
      syncFormFromSite();
      setStatus(S.loadLocalOverride() ? "Local override တင်ထားသည်" : "data/site.json မှ တင်ထားသည်");
    } catch (err) {
      setStatus("site.json မဖတ်နိုင်ပါ — local server လိုအပ်သည်");
      console.error(err);
      site = { version: 1, hotline: {}, dg: {}, gallery: [], publications: [] };
      syncFormFromSite();
    }
  }

  $("btn-pick")?.addEventListener("click", () => fileInput?.click());
  fileInput?.addEventListener("change", () => {
    handleFiles(fileInput.files);
    fileInput.value = "";
  });

  ["dragenter", "dragover"].forEach((ev) => {
    dropZone?.addEventListener(ev, (e) => {
      e.preventDefault();
      dropZone.classList.add("is-drag");
    });
  });
  ["dragleave", "drop"].forEach((ev) => {
    dropZone?.addEventListener(ev, (e) => {
      e.preventDefault();
      dropZone.classList.remove("is-drag");
    });
  });
  dropZone?.addEventListener("drop", (e) => {
    handleFiles(e.dataTransfer?.files);
  });

  $("btn-save")?.addEventListener("click", () => {
    readFormIntoSite();
    S.saveLocal(site);
    syncFormFromSite();
    setStatus("LocalStorage သို့ သိမ်းပြီး — index.html refresh လုပ်ပါ");
  });

  $("btn-export")?.addEventListener("click", () => {
    readFormIntoSite();
    S.downloadJson(site, "site.json");
    setStatus("site.json download လုပ်ပြီး — data/site.json အဖြစ် ထားပါ");
  });

  $("btn-reset")?.addEventListener("click", async () => {
    if (!confirm("Local override ဖျက်ပြီး site.json သို့ ပြန်သွားမလား?")) return;
    S.clearLocal();
    site = await S.fetchDefaultSite();
    syncFormFromSite();
    setStatus("Reset ပြီး — data/site.json");
  });

  $("btn-clear-gallery")?.addEventListener("click", () => {
    if (!site) return;
    site.gallery = [];
    syncFormFromSite();
    setStatus("Gallery ရှင်းပြီး — Save နှိပ်ပါ");
  });

  boot();
})();
