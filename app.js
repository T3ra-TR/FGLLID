(async () => {
  const menuToggle = document.getElementById("menu-toggle");
  const mobileNav = document.getElementById("mobile-nav");
  const liveTime = document.getElementById("live-time");
  const langBtn = document.getElementById("lang-btn");
  const langBtnText = document.getElementById("lang-btn-text");
  const ticker = document.getElementById("official-ticker");
  const tickerWrap = document.getElementById("official-ticker-wrap");
  const newsGrid = document.getElementById("news-grid");
  const newsSource = document.getElementById("news-source");
  const newsViewAll = document.getElementById("news-view-all");
  const newsPrev = document.getElementById("newsPrev");
  const newsNext = document.getElementById("newsNext");
  const introPanels = document.querySelectorAll(".intro-panel");

  const NEWS_JSON = "data/news.json";
  const FALLBACK_IMG =
    "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80";

  let newsIndex = 0;
  let newsSlideCount = 0;

  if (menuToggle && mobileNav) {
    menuToggle.addEventListener("click", () => {
      const open = mobileNav.classList.toggle("hidden") === false;
      menuToggle.setAttribute("aria-expanded", String(open));
    });
    mobileNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        mobileNav.classList.add("hidden");
        menuToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* —— Page views: home vs administration (footer always visible) —— */
  const pages = {
    home: document.getElementById("page-home"),
    administration: document.getElementById("page-administration"),
  };
  const ADMIN_HASHES = new Set([
    "administration",
    "admin",
    "about",
    "history",
    "org",
    "leadership",
  ]);

  function parseHash() {
    const raw = (location.hash || "#home").replace(/^#/, "").split(/[/?]/)[0];
    if (ADMIN_HASHES.has(raw)) {
      return { page: "administration", anchor: raw === "administration" ? "#admin" : `#${raw}` };
    }
    return {
      page: "home",
      anchor: raw && raw !== "home" ? `#${raw}` : null,
    };
  }

  function showPage(name, { scrollTop = true, anchor = null } = {}) {
    const page = name === "administration" ? "administration" : "home";
    Object.entries(pages).forEach(([key, el]) => {
      if (!el) return;
      const on = key === page;
      el.classList.toggle("is-active", on);
      if (on) el.removeAttribute("hidden");
      else el.setAttribute("hidden", "");
    });
    document.body.dataset.page = page;
    document.querySelectorAll("#primary-nav a, #mobile-nav a").forEach((a) => {
      const linkPage = a.getAttribute("data-page-link");
      const isAbout = linkPage === "administration";
      const on =
        (page === "administration" && isAbout) ||
        (page === "home" && linkPage === "home" && a.getAttribute("href") === "#home");
      a.classList.toggle("active", Boolean(on));
    });
    if (anchor) {
      window.setTimeout(() => {
        document.querySelector(anchor)?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 40);
    } else if (scrollTop) {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  function applyHashRoute({ scrollTop = true } = {}) {
    const { page, anchor } = parseHash();
    showPage(page, { scrollTop: scrollTop && !anchor, anchor });
  }

  window.addEventListener("hashchange", () => applyHashRoute());

  document.addEventListener("click", (e) => {
    const link = e.target.closest("[data-page-link]");
    if (!link) return;
    const page = link.getAttribute("data-page-link");
    if (!page || !pages[page]) return;
    const href = link.getAttribute("href") || "";
    if (!href.startsWith("#")) return;
    e.preventDefault();
    if (location.hash === href) applyHashRoute();
    else location.hash = href;
  });

  applyHashRoute({ scrollTop: false });

  /* —— EN / MM i18n (default: mm) —— */
  const I18N = window.FGLLID_I18N || { defaultLang: "mm", strings: {} };
  const LANG_KEY = "fgllid_lang";
  let currentLang =
    localStorage.getItem(LANG_KEY) === "en" ? "en" : I18N.defaultLang || "mm";

  function t(key, fallbackText) {
    const pack = I18N.strings?.[currentLang] || {};
    const mm = I18N.strings?.mm || {};
    const val = pack[key] ?? mm[key];
    if (val != null && val !== "") return val;
    return fallbackText != null ? fallbackText : key;
  }

  function applyLang(lang) {
    currentLang = lang === "en" ? "en" : "mm";
    localStorage.setItem(LANG_KEY, currentLang);
    document.documentElement.lang = currentLang === "en" ? "en" : "my";
    document.documentElement.dataset.lang = currentLang;
    document.body.classList.toggle("is-en", currentLang === "en");
    document.body.classList.toggle("is-mm", currentLang === "mm");

    const title = t("doc.title");
    if (title && title !== "doc.title") document.title = title;

    document.querySelectorAll("[data-i18n]").forEach((el) => {
      const key = el.getAttribute("data-i18n");
      if (!key) return;
      const pack = I18N.strings?.[currentLang] || {};
      const mm = I18N.strings?.mm || {};
      const val = pack[key] ?? mm[key];
      /* Never paint raw keys like "top.hotline" over real copy */
      if (val == null || val === "") return;
      el.textContent = val;
    });
    document.querySelectorAll("[data-i18n-html]").forEach((el) => {
      const key = el.getAttribute("data-i18n-html");
      if (!key) return;
      const pack = I18N.strings?.[currentLang] || {};
      const mm = I18N.strings?.mm || {};
      const val = pack[key] ?? mm[key];
      if (val == null || val === "") return;
      el.innerHTML = val;
    });
    document.querySelectorAll("[data-i18n-aria]").forEach((el) => {
      const key = el.getAttribute("data-i18n-aria");
      if (!key) return;
      const val = t(key);
      if (val === key) return;
      el.setAttribute("aria-label", val);
    });
    document.querySelectorAll("[data-i18n-alt]").forEach((el) => {
      const key = el.getAttribute("data-i18n-alt");
      if (!key) return;
      const val = t(key);
      if (val === key) return;
      el.setAttribute("alt", val);
    });

    const switchLabel = t("lang.switchTo");
    if (langBtnText && switchLabel !== "lang.switchTo") {
      langBtnText.textContent = switchLabel;
    }
    const langAria = t("lang.aria");
    if (langBtn && langAria !== "lang.aria") {
      langBtn.setAttribute("aria-label", langAria);
    }

    /* Feature rotator texts refresh on next tick via currentLang */
    if (typeof window.__fgllidRefreshFeatures === "function") {
      window.__fgllidRefreshFeatures();
    }
    tickClock();
  }

  function tickClock() {
    if (!liveTime) return;
    const locale = currentLang === "en" ? "en-GB" : "my-MM";
    liveTime.textContent = new Date().toLocaleString(locale, {
      weekday: "short",
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }
  setInterval(tickClock, 30_000);

  if (langBtn) {
    langBtn.addEventListener("click", () => {
      applyLang(currentLang === "mm" ? "en" : "mm");
    });
  }
  applyLang(currentLang);

  /* —— Notifications popup —— */
  const notiBtn = document.getElementById("noti-btn");
  const notiPanel = document.getElementById("noti-panel");
  const notiDot = document.getElementById("noti-dot");
  const notiMark = document.getElementById("noti-mark");
  const NOTI_KEY = "fgllid_noti_read";

  function syncNotiDot() {
    const unread = document.querySelectorAll(".noti-item.is-unread").length;
    if (notiDot) notiDot.classList.toggle("is-off", unread === 0);
  }

  const notiBackdrop = document.getElementById("noti-backdrop");

  function openNoti(open) {
    if (!notiPanel || !notiBtn) return;
    notiPanel.hidden = !open;
    notiBtn.setAttribute("aria-expanded", String(open));
    document.body.classList.toggle("noti-open", open);
    if (notiBackdrop) {
      notiBackdrop.hidden = !open;
      notiBackdrop.setAttribute("aria-hidden", String(!open));
    }
    if (open) {
      notiPanel.style.animation = "none";
      void notiPanel.offsetWidth;
      notiPanel.style.animation = "";
    }
  }

  if (localStorage.getItem(NOTI_KEY) === "1") {
    document.querySelectorAll(".noti-item").forEach((el) => el.classList.remove("is-unread"));
  }
  syncNotiDot();

  notiBtn?.addEventListener("click", (e) => {
    e.stopPropagation();
    openNoti(notiPanel?.hidden !== false);
  });
  notiMark?.addEventListener("click", () => {
    document.querySelectorAll(".noti-item").forEach((el) => el.classList.remove("is-unread"));
    localStorage.setItem(NOTI_KEY, "1");
    syncNotiDot();
  });
  notiPanel?.addEventListener("click", (e) => e.stopPropagation());
  notiBackdrop?.addEventListener("click", () => openNoti(false));
  document.addEventListener("click", (e) => {
    if (e.target.closest("#noti-btn, #noti-panel")) return;
    openNoti(false);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") openNoti(false);
  });
  notiPanel?.querySelector(".noti-footer")?.addEventListener("click", () => openNoti(false));

  /* —— Dark mode —— */
  const themeBtn = document.getElementById("theme-btn");
  const themeIcon = document.getElementById("theme-icon");
  const THEME_KEY = "fgllid_theme";

  function applyTheme(mode) {
    const dark = mode === "dark";
    document.documentElement.classList.toggle("theme-dark", dark);
    document.body.classList.toggle("theme-dark", dark);
    localStorage.setItem(THEME_KEY, dark ? "dark" : "light");
    if (themeIcon) {
      themeIcon.className = dark ? "fa-solid fa-sun" : "fa-solid fa-moon";
    }
    if (themeBtn) {
      themeBtn.setAttribute(
        "aria-label",
        t(dark ? "theme.aria.light" : "theme.aria.dark")
      );
    }
  }

  applyTheme(localStorage.getItem(THEME_KEY) === "dark" ? "dark" : "light");
  themeBtn?.addEventListener("click", () => {
    const next = document.body.classList.contains("theme-dark") ? "light" : "dark";
    applyTheme(next);
  });

  /* site.json / localStorage — after i18n so data wins for content fields */
  if (window.FGLLID_SITE) {
    try {
      const siteData = await window.FGLLID_SITE.getSiteData();
      window.FGLLID_SITE.applySiteToDom(siteData);
      window.__fgllidSiteData = siteData;
    } catch (err) {
      console.warn("site data:", err);
    }
  }

  const pauseTicker = () => ticker?.classList.add("is-paused");
  const resumeTicker = () => ticker?.classList.remove("is-paused");
  if (ticker) {
    ticker.addEventListener("touchstart", pauseTicker, { passive: true });
    ticker.addEventListener("touchend", resumeTicker, { passive: true });
  }
  if (tickerWrap) {
    tickerWrap.addEventListener("mouseenter", pauseTicker);
    tickerWrap.addEventListener("mouseleave", resumeTicker);
  }

  introPanels.forEach((panel) => {
    panel.addEventListener("click", () => {
      introPanels.forEach((p) => {
        p.classList.remove("active");
        p.setAttribute("aria-selected", "false");
      });
      panel.classList.add("active");
      panel.setAttribute("aria-selected", "true");
    });
  });

  const navLinks = document.querySelectorAll(".primary-nav-boxed a");
  const sections = [...navLinks]
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);

  if (navLinks.length && sections.length && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const id = `#${entry.target.id}`;
          navLinks.forEach((link) => {
            link.classList.toggle("active", link.getAttribute("href") === id);
          });
        });
      },
      { rootMargin: "-35% 0px -55% 0px", threshold: 0 }
    );
    sections.forEach((section) => observer.observe(section));
  }

  /* Pubs / gallery: scroll 4→8, >8 blur see-more opens popup */
  const seeMoreModal = document.getElementById("see-more-modal");
  const seeMoreBody = document.getElementById("see-more-body");
  const seeMoreTitle = document.getElementById("see-more-title");

  function openSeeMore(wrap, title) {
    if (!seeMoreModal || !seeMoreBody) return;
    const extras = wrap.querySelectorAll(".pub-extra");
    seeMoreBody.className = "see-more-body pubs pubs-list";
    seeMoreBody.innerHTML = "";
    extras.forEach((el) => {
      seeMoreBody.appendChild(el.cloneNode(true));
    });
    if (seeMoreTitle) seeMoreTitle.textContent = title;
    seeMoreModal.hidden = false;
    document.body.style.overflow = "hidden";
  }

  function closeSeeMore() {
    if (!seeMoreModal) return;
    seeMoreModal.hidden = true;
    document.body.style.overflow = "";
  }

  seeMoreModal?.querySelectorAll("[data-close]").forEach((el) => {
    el.addEventListener("click", closeSeeMore);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeSeeMore();
  });

  function wireSeeMore(wrapId, btnId, title) {
    const wrap = document.getElementById(wrapId);
    const btn = document.getElementById(btnId);
    if (!wrap || !btn) return;
    const viewport = wrap.querySelector(".pubs-viewport");
    const list = wrap.querySelector(".pubs-list");
    const extras = wrap.querySelectorAll(".pub-extra");
    const hasExtra = extras.length > 0;
    const scrollables = [
      ...(list
        ? list.querySelectorAll(":scope > .pub-cover:not(.pub-extra)")
        : []),
    ];
    const canPastFour = scrollables.length > 4;

    if (hasExtra && canPastFour) {
      wrap.classList.add("has-extra");
      btn.hidden = false;
    } else {
      wrap.classList.remove("has-extra", "see-more-visible");
      btn.hidden = true;
    }

    const syncSeeMore = () => {
      if (!viewport || !hasExtra || !canPastFour) {
        wrap.classList.remove("see-more-visible");
        return;
      }
      /* Past first ~4 tiles (2 rows) → blur See more animates in */
      const rowH =
        scrollables[0]?.getBoundingClientRect().height || 118;
      const gap = 10;
      const pastFour = viewport.scrollTop >= rowH + gap * 0.5;
      const nearBottom =
        viewport.scrollTop + viewport.clientHeight >=
        viewport.scrollHeight - 12;
      wrap.classList.toggle("see-more-visible", pastFour || nearBottom);
    };

    viewport?.addEventListener("scroll", syncSeeMore, { passive: true });
    requestAnimationFrame(syncSeeMore);
    btn.addEventListener("click", () =>
      openSeeMore(wrap, typeof title === "function" ? title() : title)
    );
  }
  wireSeeMore("pubs-wrap", "pubs-see-more", () => t("pubs.modal"));
  wireSeeMore("gallery-wrap", "gallery-see-more", () => t("gallery.modal"));

  function openTextMore(title, body) {
    if (!seeMoreModal || !seeMoreBody) return;
    seeMoreBody.className = "see-more-body admin-more-body";
    seeMoreBody.innerHTML = `<p>${escapeHtml(body)}</p>`;
    if (seeMoreTitle) seeMoreTitle.textContent = title;
    seeMoreModal.hidden = false;
    document.body.style.overflow = "hidden";
  }

  document.querySelectorAll(".admin-view-more").forEach((btn) => {
    btn.addEventListener("click", () => {
      const title =
        currentLang === "en"
          ? btn.dataset.moreTitleEn || btn.dataset.moreTitle
          : btn.dataset.moreTitle;
      const body =
        currentLang === "en"
          ? btn.dataset.moreBodyEn || btn.dataset.moreBody
          : btn.dataset.moreBody;
      openTextMore(title || t("svc.detail"), body || "");
    });
  });

  /* Complaint QR */
  const qrImg = document.getElementById("complaint-qr-img");
  const qrLink = document.getElementById("complaint-qr-link");
  if (qrImg) {
    const base = `${location.origin}${location.pathname.replace(/[^/]*$/, "")}`;
    const formUrl = `${base}#complaint-qr`;
    const qrSrc = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(formUrl)}`;
    qrImg.src = qrSrc;
    if (qrLink) qrLink.href = formUrl;
  }

  /* Admin bio pager — soft tabs + left/right slide */
  const bioTrack = document.getElementById("bio-track");
  const bioTabsWrap = document.querySelector(".bio-tabs");
  const bioTabs = document.querySelectorAll(".bio-tab");
  const bioPrev = document.getElementById("bioPrev");
  const bioNext = document.getElementById("bioNext");
  let bioIndex = 0;

  function goBio(index, dir) {
    if (!bioTrack) return;
    const slides = bioTrack.querySelectorAll(".bio-slide");
    if (!slides.length) return;
    bioIndex = ((index % slides.length) + slides.length) % slides.length;
    bioTrack.style.transform = `translateX(-${bioIndex * 50}%)`;
    slides.forEach((s, i) => s.classList.toggle("is-active", i === bioIndex));
    bioTabs.forEach((t, i) => {
      t.classList.toggle("is-active", i === bioIndex);
      t.setAttribute("aria-selected", String(i === bioIndex));
    });
    bioTabsWrap?.setAttribute("data-active", String(bioIndex));
    bioTrack.classList.remove("from-left", "from-right");
    if (dir) bioTrack.classList.add(dir === 1 ? "from-right" : "from-left");
  }

  bioTabs.forEach((tab, i) => {
    tab.addEventListener("click", () => goBio(i, i > bioIndex ? 1 : -1));
  });
  bioPrev?.addEventListener("click", () => goBio(bioIndex - 1, -1));
  bioNext?.addEventListener("click", () => goBio(bioIndex + 1, 1));
  bioTabsWrap?.setAttribute("data-active", "0");

  /* History story reveal on scroll */
  const historyStory = document.getElementById("history-story");
  if (historyStory && "IntersectionObserver" in window) {
    const histObs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            historyStory.classList.add("is-inview");
            histObs.disconnect();
          }
        });
      },
      { threshold: 0.28 }
    );
    histObs.observe(historyStory);
  } else {
    historyStory?.classList.add("is-inview");
  }

  /* Feature popup — rotating transitions (not long list) */
  const featureItems = [
    { href: "#services", key: "feature.1" },
    { href: "#laws", key: "feature.2" },
    { href: "#about", key: "feature.3" },
    { href: "#complaints", key: "feature.4" },
    { href: "#news", key: "feature.5" },
    { href: "#services", key: "feature.6" },
    { href: "#laws", key: "feature.7" },
  ];
  const featureFx = ["pop-fade", "pop-zoom", "pop-flip", "pop-slide", "pop-rise"];
  const featureCard = document.getElementById("feature-card");
  const featureLink = document.getElementById("feature-link");
  const featureDots = document.getElementById("feature-dots");
  let featureIdx = 0;

  if (featureDots) {
    featureDots.innerHTML = featureItems
      .map((_, i) => `<button type="button" data-i="${i}" aria-label="Feature ${i + 1}"></button>`)
      .join("");
    featureDots.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => showFeature(Number(btn.dataset.i)));
    });
  }

  function showFeature(index) {
    if (!featureCard || !featureLink) return;
    featureIdx = ((index % featureItems.length) + featureItems.length) % featureItems.length;
    const item = featureItems[featureIdx];
    const fx = featureFx[featureIdx % featureFx.length];
    featureLink.href = item.href;
    featureLink.textContent = t(item.key);
    featureCard.classList.remove(...featureFx);
    void featureCard.offsetWidth;
    featureCard.classList.add(fx);
    featureDots?.querySelectorAll("button").forEach((b, i) => {
      b.classList.toggle("is-on", i === featureIdx);
    });
  }

  window.__fgllidRefreshFeatures = () => showFeature(featureIdx);

  if (featureCard && featureLink) {
    showFeature(0);
    setInterval(() => showFeature(featureIdx + 1), 3800);
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  const MY_MONTHS = [
    "ဇန်နဝါရီ",
    "ဖေဖော်ဝါရီ",
    "မတ်",
    "ဧပြီ",
    "မေ",
    "ဇွန်",
    "ဇူလိုင်",
    "ဩဂုတ်",
    "စက်တင်ဘာ",
    "အောက်တိုဘာ",
    "နိုဝင်ဘာ",
    "ဒီဇင်ဘာ",
  ];
  const MY_DIGITS = "၀၁၂၃၄၅၆၇၈၉";

  function toMyanmarDigits(value) {
    return String(value).replace(/\d/g, (d) => MY_DIGITS[Number(d)]);
  }

  function formatDate(iso) {
    if (!iso) return "";
    const d = new Date(iso.length === 10 ? `${iso}T00:00:00` : iso);
    if (Number.isNaN(d.getTime())) return iso;
    if (currentLang === "en") {
      return d.toLocaleDateString("en-GB", {
        day: "numeric",
        month: "short",
        year: "numeric",
      });
    }
    const day = toMyanmarDigits(d.getDate());
    const month = MY_MONTHS[d.getMonth()];
    const year = toMyanmarDigits(d.getFullYear());
    return `${day} ${month} ${year}`;
  }

  function renderTicker(titles) {
    if (!ticker || !titles?.length) return;
    ticker.innerHTML = titles
      .map((title) => `<span class="mx-5">${escapeHtml(title)}</span>`)
      .join("");
  }

  const newsDots = document.getElementById("newsDots");
  const PER_PAGE = 1;
  const NEWS_BADGES_MM = ["သတင်း", "ကြေညာချက်", "စစ်ဆေးရေး"];
  const NEWS_BADGES_EN = ["News", "Notice", "Inspection"];
  let newsItems = [];

  function cardHtml(item, payload, idx) {
    const img = item.image || FALLBACK_IMG;
    const href = item.link || payload.fgllidNewsUrl || "#news";
    const badges = currentLang === "en" ? NEWS_BADGES_EN : NEWS_BADGES_MM;
    const badge = badges[idx % badges.length];
    const source =
      item.source ||
      (idx % 2 === 0
        ? "FGLLI · အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန"
        : "အလုပ်သမားဝန်ကြီးဌာန · တရားဝင် ထုတ်ပြန်ချက်");
    const title = item.title || "";
    return `
      <a class="news-card" href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer" data-title="${escapeHtml(title)}">
        <div class="news-cover">
          <img src="${escapeHtml(img)}" alt="" loading="lazy" onerror="this.onerror=null;this.src='${FALLBACK_IMG}'" />
          <span class="news-badge">${escapeHtml(badge)}</span>
        </div>
        <div class="news-body">
          <span class="news-date">${escapeHtml(formatDate(item.datetime || item.date))}</span>
          <h3 class="news-title" aria-label="${escapeHtml(title)}"></h3>
          <p class="news-excerpt">${escapeHtml(source)}</p>
        </div>
      </a>`;
  }

  function visiblePerPage() {
    return PER_PAGE;
  }

  let newsTypeTimer = 0;
  let newsAutoTimer = 0;

  function stopNewsType() {
    if (newsTypeTimer) {
      clearInterval(newsTypeTimer);
      newsTypeTimer = 0;
    }
  }

  function playNewsEnter(card) {
    if (!card) return;
    const img = card.querySelector(".news-cover img");
    const titleEl = card.querySelector(".news-title");
    const full = card.dataset.title || titleEl?.getAttribute("aria-label") || "";

    card.classList.remove("is-entering");
    void card.offsetWidth;
    card.classList.add("is-entering");

    if (img) {
      img.classList.remove("news-img-pop");
      void img.offsetWidth;
      img.classList.add("news-img-pop");
    }

    stopNewsType();
    if (!titleEl) return;
    const reduce =
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {
      titleEl.textContent = full;
      titleEl.classList.remove("is-typing");
      return;
    }
    titleEl.textContent = "";
    titleEl.classList.add("is-typing");
    let i = 0;
    const step = Math.max(1, Math.ceil(full.length / 55));
    newsTypeTimer = setInterval(() => {
      i = Math.min(full.length, i + step);
      titleEl.textContent = full.slice(0, i);
      if (i >= full.length) {
        stopNewsType();
        titleEl.classList.remove("is-typing");
      }
    }, 28);
  }

  function paintDots() {
    if (!newsDots) return;
    newsDots.innerHTML = Array.from({ length: newsSlideCount }, (_, i) =>
      `<button type="button" aria-label="Page ${i + 1}"${i === newsIndex ? ' class="is-active"' : ""}></button>`
    ).join("");
    newsDots.querySelectorAll("button").forEach((b, i) => {
      b.addEventListener("click", () => goNews(i));
    });
  }

  function goNews(index) {
    if (!newsGrid || newsSlideCount < 1) return;
    newsIndex = ((index % newsSlideCount) + newsSlideCount) % newsSlideCount;
    const cards = newsGrid.querySelectorAll(".news-card");
    if (!cards.length) return;
    const per = visiblePerPage();
    const cardW = cards[0].getBoundingClientRect().width;
    const offset = newsIndex * per * cardW;
    newsGrid.style.transform = `translateX(-${offset}px)`;
    newsDots?.querySelectorAll("button").forEach((b, i) => {
      b.classList.toggle("is-active", i === newsIndex);
    });
    cards.forEach((c, i) => c.classList.toggle("is-active", i === newsIndex));
    playNewsEnter(cards[newsIndex]);
    resetNewsAuto();
  }

  function resetNewsAuto() {
    if (newsAutoTimer) clearInterval(newsAutoTimer);
    if (newsSlideCount < 2) return;
    newsAutoTimer = setInterval(() => goNews(newsIndex + 1), 6500);
  }

  function syncNewsPages() {
    const per = visiblePerPage();
    newsSlideCount = Math.max(1, Math.ceil(newsItems.length / per));
    if (newsIndex >= newsSlideCount) newsIndex = newsSlideCount - 1;
    paintDots();
    goNews(newsIndex);
  }

  function renderNews(payload) {
    if (!newsGrid) return;
    newsItems = (payload.items || []).slice(0, 9);

    if (newsViewAll && payload.fgllidNewsUrl) {
      newsViewAll.href = payload.fgllidNewsUrl;
    }

    if (newsSource) {
      const when = payload.fetchedAt
        ? new Date(payload.fetchedAt).toLocaleString("en-GB")
        : "";
      newsSource.textContent = when
        ? `အရင်းအမြစ် — mol.gov.mm · FGLLID-News · sync ${when}`
        : "အရင်းအမြစ် — mol.gov.mm · FGLLID-News";
    }

    renderTicker(
      payload.ticker?.length ? payload.ticker : newsItems.map((i) => i.title)
    );

    if (!newsItems.length) {
      newsGrid.innerHTML = `<p class="news-empty">${t("news.empty")}</p>`;
      newsSlideCount = 0;
      if (newsDots) newsDots.innerHTML = "";
      return;
    }

    newsGrid.innerHTML = newsItems
      .map((item, i) => cardHtml(item, payload, i))
      .join("");
    newsIndex = 0;
    requestAnimationFrame(() => syncNewsPages());
  }

  newsPrev?.addEventListener("click", () => goNews(newsIndex - 1));
  newsNext?.addEventListener("click", () => goNews(newsIndex + 1));
  const newsCarousel = document.getElementById("news-vslider");
  newsCarousel?.addEventListener("mouseenter", () => {
    if (newsAutoTimer) clearInterval(newsAutoTimer);
  });
  newsCarousel?.addEventListener("mouseleave", () => resetNewsAuto());
  let resizeTimer = 0;
  window.addEventListener("resize", () => {
    if (!newsItems.length) return;
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => syncNewsPages(), 120);
  });

  async function loadNews() {
    try {
      const res = await fetch(NEWS_JSON, { cache: "no-store" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      renderNews(await res.json());
    } catch (err) {
      console.warn("news.json load failed", err);
      if (newsGrid) {
        newsGrid.innerHTML =
          `<p class="news-empty">${t("news.error")}</p>`;
      }
    }
  }

  loadNews();

  document.getElementById("scroll-top")?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  /* Footer visitor counter (localStorage demo viewer) */
  const viewerEl = document.getElementById("ft-viewer-count");
  if (viewerEl) {
    const KEY = "fgllid_viewer_count";
    let n = Number(localStorage.getItem(KEY) || "12840");
    if (!Number.isFinite(n) || n < 1) n = 12840;
    n += 1;
    localStorage.setItem(KEY, String(n));
    viewerEl.textContent = n.toLocaleString("en-US");
  }

  /* YouTube media slider — left / right animation */
  const mediaTrack = document.getElementById("media-slider-track");
  const mediaPrev = document.getElementById("mediaPrev");
  const mediaNext = document.getElementById("mediaNext");
  const mediaDots = document.getElementById("media-slider-dots");
  const mediaMetaTopic = document.getElementById("media-meta-topic");
  const mediaMetaCount = document.getElementById("media-meta-count");
  const mediaViewport = document.querySelector(".media-slider-viewport");
  let mediaIndex = 0;
  let mediaBusy = false;

  function mediaSlides() {
    return mediaTrack ? [...mediaTrack.querySelectorAll(".media-slide")] : [];
  }

  function stopAllMediaEmbeds() {
    mediaSlides().forEach((slide) => {
      const play = slide.querySelector(".media-video-play");
      const frame = slide.querySelector(".media-video-frame");
      if (frame) {
        frame.hidden = true;
        frame.innerHTML = "";
      }
      if (play) play.hidden = false;
    });
  }

  function syncMediaMeta(slide) {
    if (!slide) return;
    const topicKey = slide.dataset.topicKey;
    if (mediaMetaTopic && topicKey) {
      mediaMetaTopic.setAttribute("data-i18n", topicKey);
      mediaMetaTopic.textContent = t(topicKey);
    }
    if (mediaMetaCount) {
      mediaMetaCount.textContent = `${mediaIndex + 1} / ${mediaSlides().length}`;
    }
  }

  function goMedia(index, dir) {
    const slides = mediaSlides();
    if (!mediaTrack || !slides.length || mediaBusy) return;
    const next =
      ((index % slides.length) + slides.length) % slides.length;
    if (next === mediaIndex && dir == null) {
      syncMediaMeta(slides[mediaIndex]);
      return;
    }

    mediaBusy = true;
    stopAllMediaEmbeds();
    const prev = mediaIndex;
    const goingRight = dir === "next" || (dir == null && next > prev);
    slides[prev]?.classList.remove("is-active", "is-enter-left", "is-enter-right");
    slides[prev]?.classList.add(goingRight ? "is-exit-left" : "is-exit-right");

    mediaIndex = next;
    mediaTrack.style.transform = `translateX(-${mediaIndex * 100}%)`;

    slides[mediaIndex]?.classList.remove("is-exit-left", "is-exit-right");
    slides[mediaIndex]?.classList.add(
      "is-active",
      goingRight ? "is-enter-right" : "is-enter-left"
    );

    mediaDots?.querySelectorAll("button").forEach((b, i) => {
      b.classList.toggle("is-on", i === mediaIndex);
      b.setAttribute("aria-selected", String(i === mediaIndex));
    });
    syncMediaMeta(slides[mediaIndex]);

    window.setTimeout(() => {
      slides.forEach((s) =>
        s.classList.remove(
          "is-exit-left",
          "is-exit-right",
          "is-enter-left",
          "is-enter-right"
        )
      );
      slides[mediaIndex]?.classList.add("is-active");
      mediaBusy = false;
    }, 520);
  }

  if (mediaTrack) {
    const slides = mediaSlides();
    if (mediaDots) {
      mediaDots.innerHTML = slides
        .map(
          (_, i) =>
            `<button type="button" role="tab" aria-label="Video ${i + 1}" aria-selected="${i === 0}"></button>`
        )
        .join("");
      mediaDots.querySelectorAll("button").forEach((btn, i) => {
        btn.addEventListener("click", () =>
          goMedia(i, i > mediaIndex ? "next" : "prev")
        );
      });
    }

    slides.forEach((slide) => {
      const ytId = slide.dataset.ytId;
      const play = slide.querySelector(".media-video-play");
      const frame = slide.querySelector(".media-video-frame");
      const poster = slide.querySelector(".media-video-poster");
      if (poster && ytId) {
        poster.src = `https://i.ytimg.com/vi/${ytId}/hqdefault.jpg`;
      }
      play?.addEventListener("click", () => {
        if (!ytId || !frame) return;
        play.hidden = true;
        frame.hidden = false;
        frame.innerHTML = `<iframe
          src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(ytId)}?autoplay=1&rel=0"
          title="FGLLID YouTube video"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowfullscreen
          loading="lazy"
        ></iframe>`;
      });
    });

    mediaPrev?.addEventListener("click", () => goMedia(mediaIndex - 1, "prev"));
    mediaNext?.addEventListener("click", () => goMedia(mediaIndex + 1, "next"));

    /* Touch / swipe */
    let touchX = null;
    mediaViewport?.addEventListener(
      "touchstart",
      (e) => {
        touchX = e.changedTouches[0]?.clientX ?? null;
      },
      { passive: true }
    );
    mediaViewport?.addEventListener(
      "touchend",
      (e) => {
        if (touchX == null) return;
        const dx = (e.changedTouches[0]?.clientX ?? touchX) - touchX;
        touchX = null;
        if (Math.abs(dx) < 48) return;
        if (dx < 0) goMedia(mediaIndex + 1, "next");
        else goMedia(mediaIndex - 1, "prev");
      },
      { passive: true }
    );

    /* Auto-advance (pause while embed playing) */
    window.setInterval(() => {
      const active = mediaSlides()[mediaIndex];
      const embedding = active && !active.querySelector(".media-video-frame")?.hidden;
      if (embedding || document.hidden) return;
      goMedia(mediaIndex + 1, "next");
    }, 7000);

    mediaTrack.style.transform = "translateX(0)";
    slides.forEach((s, i) => s.classList.toggle("is-active", i === 0));
    mediaDots?.querySelectorAll("button").forEach((b, i) => {
      b.classList.toggle("is-on", i === 0);
    });
    syncMediaMeta(slides[0]);
  }
})().catch((err) => console.error(err));
