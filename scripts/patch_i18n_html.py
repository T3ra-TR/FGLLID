# -*- coding: utf-8 -*-
"""One-shot: add data-i18n markers + i18n.js script include."""
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "index.html"
html = p.read_text(encoding="utf-8")

if 'src="i18n.js"' not in html:
    html = html.replace(
        '<script src="app.js"></script>',
        '<script src="i18n.js"></script>\n    <script src="app.js"></script>',
    )

replacements = [
    (
        "            အထူးဖော်ပြချက်များ\n          </span>",
        '            <span data-i18n="ticker.label">အထူးဖော်ပြချက်များ</span>\n          </span>',
    ),
    (
        '              <span class="mx-5">တရားဝင် သတင်းများ တင်နေပါသည်…</span>',
        '              <span class="mx-5" data-i18n="ticker.loading">တရားဝင် သတင်းများ တင်နေပါသည်…</span>',
    ),
    (
        """                <h2
                  class="home-soft-title home-anim home-anim-d1 text-2xl sm:text-3xl lg:text-4xl font-bold leading-snug"
                >
                  ဌာန၏ <span class="accent">ပင်မလုပ်ငန်း</span> တာဝန်များ
                </h2>""",
        """                <h2
                  class="home-soft-title home-anim home-anim-d1 text-2xl sm:text-3xl lg:text-4xl font-bold leading-snug"
                  data-i18n-html="home.title"
                >
                  ဌာန၏ <span class="accent">ပင်မလုပ်ငန်း</span> တာဝန်များ
                </h2>""",
    ),
    (
        """                <p
                  class="home-soft-copy home-anim home-anim-d2 text-sm sm:text-base max-w-2xl leading-relaxed mt-4"
                >
                  အလုပ်သမားဝန်ကြီးဌာန လက်အောက်ရှိ ဦးစီးဌာနတစ်ခုဖြစ်ပြီး အလုပ်ရှင်နှင့် အလုပ်သမားကြား
                  ဥပဒေနှင့်အညီ လိုက်နာဆောင်ရွက်စေရန် စနစ်တကျ တာဝန်ယူ ဆောင်ရွက်လျက်ရှိပါသည်။
                </p>""",
        """                <p
                  class="home-soft-copy home-anim home-anim-d2 text-sm sm:text-base max-w-2xl leading-relaxed mt-4"
                  data-i18n="home.copy"
                >
                  အလုပ်သမားဝန်ကြီးဌာန လက်အောက်ရှိ ဦးစီးဌာနတစ်ခုဖြစ်ပြီး အလုပ်ရှင်နှင့် အလုပ်သမားကြား
                  ဥပဒေနှင့်အညီ လိုက်နာဆောင်ရွက်စေရန် စနစ်တကျ တာဝန်ယူ ဆောင်ရွက်လျက်ရှိပါသည်။
                </p>""",
    ),
    (
        'class="classic-btn classic-btn-gold">တိုင်ကြားစာ ပေးပို့ရန်</a>',
        'class="classic-btn classic-btn-gold" data-i18n="home.cta.complaint">တိုင်ကြားစာ ပေးပို့ရန်</a>',
    ),
    (
        'class="classic-btn home-soft-outline">ဥပဒေများ လေ့လာရန်</a>',
        'class="classic-btn home-soft-outline" data-i18n="home.cta.laws">ဥပဒေများ လေ့လာရန်</a>',
    ),
    (
        '<div class="dir-head">အမြန် လမ်းညွှန်</div>',
        '<div class="dir-head" data-i18n="home.dir.head">အမြန် လမ်းညွှန်</div>',
    ),
    (
        '<div class="dir-meta">၂၄ နာရီ တိုင်ကြားနိုင်သည့် ဖုန်း</div>',
        '<div class="dir-meta" data-i18n="home.dir.hotline.meta">၂၄ နာရီ တိုင်ကြားနိုင်သည့် ဖုန်း</div>',
    ),
    (
        '<div class="dir-title">ဟော့လိုင်း ၁၈၁၁</div>',
        '<div class="dir-title" data-i18n="home.dir.hotline.title">ဟော့လိုင်း ၁၈၁၁</div>',
    ),
    (
        '<div class="dir-meta">၂၀၁၉ ခုနှစ်</div>',
        '<div class="dir-meta" data-i18n="home.dir.law.meta">၂၀၁၉ ခုနှစ်</div>',
    ),
    (
        '<div class="dir-title">လုပ်ငန်းခွင် ဥပဒေ</div>',
        '<div class="dir-title" data-i18n="home.dir.law.title">လုပ်ငန်းခွင် ဥပဒေ</div>',
    ),
    (
        '<div class="dir-meta">တိုင်း/ပြည်နယ် ခရိုင်ရုံးများ</div>',
        '<div class="dir-meta" data-i18n="home.dir.office.meta">တိုင်း/ပြည်နယ် ခရိုင်ရုံးများ</div>',
    ),
    (
        '<div class="dir-title">ရုံးခွဲ ၁၅ ခုနှင့် ဆက်သွယ်ရန်</div>',
        '<div class="dir-title" data-i18n="home.dir.office.title">ရုံးခွဲ ၁၅ ခုနှင့် ဆက်သွယ်ရန်</div>',
    ),
]

# Intro panels — replace paragraph blocks uniquely
intro = [
    (
        """            <button type="button" class="intro-panel active" role="tab" aria-selected="true">
              <h3>Vision</h3>
              <p>
                ခေတ်မီပြီး ဘေးအန္တရာယ်ကင်းရှင်းသော၊ အလုပ်သမားအခွင့်အရေး ပြည့်ဝစွာရရှိသည့်
                စံပြလုပ်ငန်းခွင် ပတ်ဝန်းကျင် တည်ဆောက်ရန်။
              </p>
            </button>""",
        """            <button type="button" class="intro-panel active" role="tab" aria-selected="true">
              <h3>Vision</h3>
              <p data-i18n="intro.vision">
                ခေတ်မီပြီး ဘေးအန္တရာယ်ကင်းရှင်းသော၊ အလုပ်သမားအခွင့်အရေး ပြည့်ဝစွာရရှိသည့်
                စံပြလုပ်ငန်းခွင် ပတ်ဝန်းကျင် တည်ဆောက်ရန်။
              </p>
            </button>""",
    ),
    (
        """            <button type="button" class="intro-panel" role="tab" aria-selected="false">
              <h3>Mission</h3>
              <p>
                အလုပ်ရှင်နှင့် အလုပ်သမားကြား ဥပဒေနှင့်အညီ လိုက်နာဆောင်ရွက်စေရန် စနစ်တကျ
                စစ်ဆေးကြပ်မတ်ခြင်း။
              </p>
            </button>""",
        """            <button type="button" class="intro-panel" role="tab" aria-selected="false">
              <h3>Mission</h3>
              <p data-i18n="intro.mission">
                အလုပ်ရှင်နှင့် အလုပ်သမားကြား ဥပဒေနှင့်အညီ လိုက်နာဆောင်ရွက်စေရန် စနစ်တကျ
                စစ်ဆေးကြပ်မတ်ခြင်း။
              </p>
            </button>""",
    ),
    (
        """            <button type="button" class="intro-panel" role="tab" aria-selected="false">
              <h3>OSH</h3>
              <p>
                ၂၀၁၉ ခုနှစ် လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေးနှင့် ကျန်းမာရေးဥပဒေအရ
                ကာကွယ်စောင့်ရှောက်ခြင်း။
              </p>
            </button>""",
        """            <button type="button" class="intro-panel" role="tab" aria-selected="false">
              <h3>OSH</h3>
              <p data-i18n="intro.osh">
                ၂၀၁၉ ခုနှစ် လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေးနှင့် ကျန်းမာရေးဥပဒေအရ
                ကာကွယ်စောင့်ရှောက်ခြင်း။
              </p>
            </button>""",
    ),
    (
        """            <button type="button" class="intro-panel" role="tab" aria-selected="false">
              <h3>Services</h3>
              <p>
                စက်ရုံမှတ်ပုံတင်၊ လုပ်ခ/အလုပ်ချိန် စစ်ဆေးခြင်းနှင့် အငြင်းပွားမှု ညှိနှိုင်းဖြေရှင်းခြင်း။
              </p>
            </button>""",
        """            <button type="button" class="intro-panel" role="tab" aria-selected="false">
              <h3>Services</h3>
              <p data-i18n="intro.services">
                စက်ရုံမှတ်ပုံတင်၊ လုပ်ခ/အလုပ်ချိန် စစ်ဆေးခြင်းနှင့် အငြင်းပွားမှု ညှိနှိုင်းဖြေရှင်းခြင်း။
              </p>
            </button>""",
    ),
]

more = [
    ('            <h2>ဦးဆောင်မှုနှင့် နှုတ်ခွန်းဆက်စကား</h2>',
     '            <h2 data-i18n="admin.head">ဦးဆောင်မှုနှင့် နှုတ်ခွန်းဆက်စကား</h2>'),
    ('            <p>ညွှန်ကြားရေးမှူးချုပ်နှင့် ဦးစီးဌာန ဦးဆောင်အရာရှိများ</p>',
     '            <p data-i18n="admin.sub">ညွှန်ကြားရေးမှူးချုပ်နှင့် ဦးစီးဌာန ဦးဆောင်အရာရှိများ</p>'),
    ('                <button type="button" class="bio-tab is-active" data-bio="bio" role="tab" aria-selected="true">\n                  Biography\n                </button>',
     '                <button type="button" class="bio-tab is-active" data-bio="bio" role="tab" aria-selected="true" data-i18n="admin.tab.bio">\n                  Biography\n                </button>'),
    ('                <button type="button" class="bio-tab" data-bio="greet" role="tab" aria-selected="false">\n                  နှုတ်ခွန်းဆက်\n                </button>',
     '                <button type="button" class="bio-tab" data-bio="greet" role="tab" aria-selected="false" data-i18n="admin.tab.greet">\n                  နှုတ်ခွန်းဆက်\n                </button>'),
    ('                        <p class="dg-caption-role">ညွှန်ကြားရေးမှူးချုပ်</p>',
     '                        <p class="dg-caption-role" data-i18n="admin.dg.role">ညွှန်ကြားရေးမှူးချုပ်</p>'),
    ("""                        <p class="dg-caption-org">
                          အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန · အလုပ်သမားဝန်ကြီးဌာန
                        </p>""",
     """                        <p class="dg-caption-org" data-i18n="admin.dg.org">
                          အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန · အလုပ်သမားဝန်ကြီးဌာန
                        </p>"""),
    ('                      <h4 class="bio-slide-title">အတ္ထုပ္ပတ္တိ (Biography)</h4>',
     '                      <h4 class="bio-slide-title" data-i18n="admin.bio.title">အတ္ထုပ္ပတ္တိ (Biography)</h4>'),
    ("""                      <p class="bio-slide-text bio-clamp">
                        အလုပ်သမားရေးရာ စစ်ဆေးကြပ်မတ်မှု၊ လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေး (OSH)
                        နှင့် အလုပ်သမားဥပဒေ လိုက်နာဆောင်ရွက်မှု မြှင့်တင်ရေးတို့တွင် ဦးဆောင်တာဝန်
                        ယူဆောင်ရွက်လျက်ရှိပါသည်။ တိုင်း/ပြည်နယ် ရုံးခွဲများနှင့် ညှိနှိုင်း၍
                        ပြည်သူ့ဝန်ဆောင်မှု ပိုမိုကောင်းမွန်ရေးကို အလေးထား ဆောင်ရွက်ပါသည်။
                      </p>""",
     """                      <p class="bio-slide-text bio-clamp" data-i18n="admin.bio.text">
                        အလုပ်သမားရေးရာ စစ်ဆေးကြပ်မတ်မှု၊ လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေး (OSH)
                        နှင့် အလုပ်သမားဥပဒေ လိုက်နာဆောင်ရွက်မှု မြှင့်တင်ရေးတို့တွင် ဦးဆောင်တာဝန်
                        ယူဆောင်ရွက်လျက်ရှိပါသည်။ တိုင်း/ပြည်နယ် ရုံးခွဲများနှင့် ညှိနှိုင်း၍
                        ပြည်သူ့ဝန်ဆောင်မှု ပိုမိုကောင်းမွန်ရေးကို အလေးထား ဆောင်ရွက်ပါသည်။
                      </p>"""),
    ('                      <h4 class="bio-slide-title">ညွှန်ကြားရေးမှူးချုပ်၏ နှုတ်ခွန်းဆက်</h4>',
     '                      <h4 class="bio-slide-title" data-i18n="admin.greet.title">ညွှန်ကြားရေးမှူးချုပ်၏ နှုတ်ခွန်းဆက်</h4>'),
    ('                      <p class="dg-caption-role" style="margin-bottom: 0.65rem">အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန</p>',
     '                      <p class="dg-caption-role" style="margin-bottom: 0.65rem" data-i18n="admin.greet.org">အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန</p>'),
    ("""                      <p class="bio-slide-text bio-clamp">
                        ကျနော်တို့ ဦးစီးဌာနအနေဖြင့် စက်ရုံ၊ အလုပ်ရုံများတွင် အလုပ်သမားများ
                        ဘေးကင်းလုံခြုံစွာ လုပ်ကိုင်နိုင်ရေးအတွက် ဥပဒေနှင့်အညီ တန်းတူညီမျှ
                        စစ်ဆေးကြပ်မတ် လျက်ရှိပါသည်။ အလုပ်ရှင်နှင့် အလုပ်သမား အပြန်အလှန်
                        လေးစားယုံကြည်မှုရှိသော လုပ်ငန်းခွင် ပတ်ဝန်းကျင် တည်ဆောက်ရေးကို
                        ဦးတည်ဆောင်ရွက်ပါသည်။
                      </p>""",
     """                      <p class="bio-slide-text bio-clamp" data-i18n="admin.greet.text">
                        ကျနော်တို့ ဦးစီးဌာနအနေဖြင့် စက်ရုံ၊ အလုပ်ရုံများတွင် အလုပ်သမားများ
                        ဘေးကင်းလုံခြုံစွာ လုပ်ကိုင်နိုင်ရေးအတွက် ဥပဒေနှင့်အညီ တန်းတူညီမျှ
                        စစ်ဆေးကြပ်မတ် လျက်ရှိပါသည်။ အလုပ်ရှင်နှင့် အလုပ်သမား အပြန်အလှန်
                        လေးစားယုံကြည်မှုရှိသော လုပ်ငန်းခွင် ပတ်ဝန်းကျင် တည်ဆောက်ရေးကို
                        ဦးတည်ဆောင်ရွက်ပါသည်။
                      </p>"""),
    ('                <h4 class="font-bold text-navy-900 text-sm mb-1">ဒုတိယညွှန်ကြားရေးမှူးချုပ်</h4>',
     '                <h4 class="font-bold text-navy-900 text-sm mb-1" data-i18n="deputy1.title">ဒုတိယညွှန်ကြားရေးမှူးချုပ်</h4>'),
    ("""                <p class="text-[11px] text-slate-500 mt-1.5 leading-relaxed">
                  စစ်ဆေးရေးနှင့် OSH ကဏ္ဍ ကြီးကြပ်မှု ကူညီဆောင်ရွက်ခြင်း
                </p>""",
     """                <p class="text-[11px] text-slate-500 mt-1.5 leading-relaxed" data-i18n="deputy1.desc">
                  စစ်ဆေးရေးနှင့် OSH ကဏ္ဍ ကြီးကြပ်မှု ကူညီဆောင်ရွက်ခြင်း
                </p>"""),
    ('                <h4 class="font-bold text-navy-900 text-sm mb-1">ညွှန်ကြားရေးမှူး (စီမံ)</h4>',
     '                <h4 class="font-bold text-navy-900 text-sm mb-1" data-i18n="deputy2.title">ညွှန်ကြားရေးမှူး (စီမံ)</h4>'),
    ("""                <p class="text-[11px] text-slate-500 mt-1.5 leading-relaxed">
                  စီမံခန့်ခွဲရေးနှင့် ရုံးလုပ်ငန်း စနစ်တကျ ဆောင်ရွက်ခြင်း
                </p>""",
     """                <p class="text-[11px] text-slate-500 mt-1.5 leading-relaxed" data-i18n="deputy2.desc">
                  စီမံခန့်ခွဲရေးနှင့် ရုံးလုပ်ငန်း စနစ်တကျ ဆောင်ရွက်ခြင်း
                </p>"""),
]

svc = [
    ('              <h2>အဓိက ဆောင်ရွက်ပေးလျက်ရှိသော ဝန်ဆောင်မှုများ</h2>',
     '              <h2 data-i18n="svc.head">အဓိက ဆောင်ရွက်ပေးလျက်ရှိသော ဝန်ဆောင်မှုများ</h2>'),
    ('              <p>ပြည်သူများနှင့် လုပ်ငန်းရှင်များအတွက် စုံစမ်းလျှောက်ထားနိုင်သည့် ဝန်ဆောင်မှုများ</p>',
     '              <p data-i18n="svc.sub">ပြည်သူများနှင့် လုပ်ငန်းရှင်များအတွက် စုံစမ်းလျှောက်ထားနိုင်သည့် ဝန်ဆောင်မှုများ</p>'),
    ('                <h3>စက်ရုံ/အလုပ်ရုံ အသိအမှတ်ပြုခြင်း</h3>',
     '                <h3 data-i18n="svc1.title">စက်ရုံ/အလုပ်ရုံ အသိအမှတ်ပြုခြင်း</h3>'),
    ('                <p>စက်ရုံသစ်များ စတင်ဖွင့်လှစ်ခြင်းနှင့် စက်ပစ္စည်း တပ်ဆင်မှုများကို ဥပဒေနှင့်အညီ မှတ်ပုံတင် စစ်ဆေးပေးခြင်း။</p>',
     '                <p data-i18n="svc1.desc">စက်ရုံသစ်များ စတင်ဖွင့်လှစ်ခြင်းနှင့် စက်ပစ္စည်း တပ်ဆင်မှုများကို ဥပဒေနှင့်အညီ မှတ်ပုံတင် စစ်ဆေးပေးခြင်း။</p>'),
    ('                <h3>အနိမ့်ဆုံးအခကြေးငွေ စစ်ဆေးခြင်း</h3>',
     '                <h3 data-i18n="svc2.title">အနိမ့်ဆုံးအခကြေးငွေ စစ်ဆေးခြင်း</h3>'),
    ('                <p>သတ်မှတ် အနိမ့်ဆုံး အခကြေးငွေ နှုန်းထားများအတိုင်း ပေးချေခြင်း ရှိ/မရှိ ကွင်းဆင်း စစ်ဆေးခြင်း။</p>',
     '                <p data-i18n="svc2.desc">သတ်မှတ် အနိမ့်ဆုံး အခကြေးငွေ နှုန်းထားများအတိုင်း ပေးချေခြင်း ရှိ/မရှိ ကွင်းဆင်း စစ်ဆေးခြင်း။</p>'),
    ('                <h3>အလုပ်ချိန်နှင့် ခွင့်ရက်များ စစ်ဆေးခြင်း</h3>',
     '                <h3 data-i18n="svc3.title">အလုပ်ချိန်နှင့် ခွင့်ရက်များ စစ်ဆေးခြင်း</h3>'),
    ('                <p>အလုပ်ချိန် သတ်မှတ်ချက်နှင့် ခွင့်ရက်များ မှန်ကန်စွာ ခံစားခွင့်ပေးရေး ကြပ်မတ်ခြင်း။</p>',
     '                <p data-i18n="svc3.desc">အလုပ်ချိန် သတ်မှတ်ချက်နှင့် ခွင့်ရက်များ မှန်ကန်စွာ ခံစားခွင့်ပေးရေး ကြပ်မတ်ခြင်း။</p>'),
]

# replace first 3 svc detail buttons only in services section - use count
# History / laws / media / complaints / qr / offices / news / footer

hist = [
    ('              <h2>သမိုင်းအကျဉ်းနှင့် ဖွဲ့စည်းပုံ</h2>',
     '              <h2 data-i18n="hist.head">သမိုင်းအကျဉ်းနှင့် ဖွဲ့စည်းပုံ</h2>'),
    ('              <p>ဦးစီးဌာန၏ နောက်ခံသမိုင်းနှင့် အုပ်ချုပ်မှု ဖွဲ့စည်းပုံ</p>',
     '              <p data-i18n="hist.sub">ဦးစီးဌာန၏ နောက်ခံသမိုင်းနှင့် အုပ်ချုပ်မှု ဖွဲ့စည်းပုံ</p>'),
    ('                    <h3>သမိုင်းအကျဉ်း</h3>',
     '                    <h3 data-i18n="hist.story">သမိုင်းအကျဉ်း</h3>'),
    ('                  <h3>ဖွဲ့စည်းပုံ</h3>',
     '                  <h3 data-i18n="org.head">ဖွဲ့စည်းပုံ</h3>'),
    ('                  <h3>နောက်ဆုံးထုတ်ဝေမှုများ</h3>',
     '                  <h3 data-i18n="pubs.head">နောက်ဆုံးထုတ်ဝေမှုများ</h3>'),
    ('              <h2>အလုပ်သမားဆိုင်ရာ တည်ဆဲဥပဒေများ</h2>',
     '              <h2 data-i18n="laws.head">အလုပ်သမားဆိုင်ရာ တည်ဆဲဥပဒေများ</h2>'),
    ('                <h3>၁၉၅၁ ခုနှစ် အလုပ်ရုံများ ဥပဒေ</h3>',
     '                <h3 data-i18n="law1.title">၁၉၅၁ ခုနှစ် အလုပ်ရုံများ ဥပဒေ</h3>'),
    ('                <p>စက်ရုံ/အလုပ်ရုံများ၏ လုံခြုံရေးနှင့် လုပ်ငန်းခွင် စံချိန်စံညွှန်းများ။</p>',
     '                <p data-i18n="law1.desc">စက်ရုံ/အလုပ်ရုံများ၏ လုံခြုံရေးနှင့် လုပ်ငန်းခွင် စံချိန်စံညွှန်းများ။</p>'),
    ('                <h3>၂၀၁၉ ခုနှစ် OSH ဥပဒေ</h3>',
     '                <h3 data-i18n="law2.title">၂၀၁၉ ခုနှစ် OSH ဥပဒေ</h3>'),
    ('                <p>လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေးနှင့် ကျန်းမာရေးဆိုင်ရာ တာဝန်ဝတ္တရားများ။</p>',
     '                <p data-i18n="law2.desc">လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေးနှင့် ကျန်းမာရေးဆိုင်ရာ တာဝန်ဝတ္တရားများ။</p>'),
    ('                <h3>၂၀၁၃ ခုနှစ် အနည်းဆုံး အခကြေးငွေ ဥပဒေ</h3>',
     '                <h3 data-i18n="law3.title">၂၀၁၃ ခုနှစ် အနည်းဆုံး အခကြေးငွေ ဥပဒေ</h3>'),
    ('                <p>သတ်မှတ် အနည်းဆုံး အခကြေးငွေနှုန်းထားများ လိုက်နာပေးချေရေး။</p>',
     '                <p data-i18n="law3.desc">သတ်မှတ် အနည်းဆုံး အခကြေးငွေနှုန်းထားများ လိုက်နာပေးချေရေး။</p>'),
    ('              <h2>အသိပညာပေး ဗီဒီယို</h2>',
     '              <h2 data-i18n="media.head">အသိပညာပေး ဗီဒီယို</h2>'),
    ('              <p>YouTube မှ ကြည့်ရှုနိုင်ပါသည် — လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေး အသိပညာပေး</p>',
     '              <p data-i18n="media.sub">YouTube မှ ကြည့်ရှုနိုင်ပါသည် — လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေး အသိပညာပေး</p>'),
    ('                  <span class="media-video-caption">YouTube တွင် ကြည့်ရန်</span>',
     '                  <span class="media-video-caption" data-i18n="media.caption">YouTube တွင် ကြည့်ရန်</span>'),
    ('                  >YouTube တွင် ဖွင့်ရန် ›</a',
     '                  data-i18n="media.open">YouTube တွင် ဖွင့်ရန် ›</a'),
    ('                <span class="complaint-band-tag">အရေးပေါ် · Hotline</span>',
     '                <span class="complaint-band-tag" data-i18n="complaint.tag">အရေးပေါ် · Hotline</span>'),
    ('                <h2>ထိခိုက်နစ်နာမှု <span>တိုင်ကြားစာ</span></h2>',
     '                <h2 data-i18n-html="complaint.title">ထိခိုက်နစ်နာမှု <span>တိုင်ကြားစာ</span></h2>'),
    ('                  <a class="lu-btn lu-btn-gold" href="tel:1811">ဟော့လိုင်း ၁၈၁၁</a>',
     '                  <a class="lu-btn lu-btn-gold" href="tel:1811" data-i18n="complaint.hotline">ဟော့လိုင်း ၁၈၁၁</a>'),
    ('                  <a class="lu-btn lu-btn-ghost" href="#complaint-qr">QR ဖြင့် ပေးပို့ရန်</a>',
     '                  <a class="lu-btn lu-btn-ghost" href="#complaint-qr" data-i18n="complaint.qrBtn">QR ဖြင့် ပေးပို့ရန်</a>'),
    ('                <span class="complaint-band-dial-label">ခေါ်ဆိုရန်</span>',
     '                <span class="complaint-band-dial-label" data-i18n="complaint.call">ခေါ်ဆိုရန်</span>'),
    ('              <span class="classic-label">အွန်လိုင်း ဝန်ဆောင်မှု • DEMO</span>',
     '              <span class="classic-label" data-i18n="qr.label">အွန်လိုင်း ဝန်ဆောင်မှု • DEMO</span>'),
    ('              <h2>တိုင်ကြားစာ ပေးပို့ခြင်း</h2>',
     '              <h2 data-i18n="qr.head">တိုင်ကြားစာ ပေးပို့ခြင်း</h2>'),
    ('              <h3 class="font-bold text-navy-900 text-lg mb-2">ထိခိုက်နစ်နာမှု တိုင်ကြားစာ (QR)</h3>',
     '              <h3 class="font-bold text-navy-900 text-lg mb-2" data-i18n="qr.cardTitle">ထိခိုက်နစ်နာမှု တိုင်ကြားစာ (QR)</h3>'),
    ('              <h2>တိုင်းနှင့်ပြည်နယ် ဦးစီးဌာန ရုံးများ</h2>',
     '              <h2 data-i18n="offices.head">တိုင်းနှင့်ပြည်နယ် ဦးစီးဌာန ရုံးများ</h2>'),
    ('                <h3>နေပြည်တော် ရုံးချုပ်</h3>',
     '                <h3 data-i18n="office1.title">နေပြည်တော် ရုံးချုပ်</h3>'),
    ('                <p>ရုံးအမှတ် (၅၁)၊ အလုပ်သမားဝန်ကြီးဌာန၊ နေပြည်တော်။ ဖုန်း: ၀၆၇-၃၄၃၀၁၈၄</p>',
     '                <p data-i18n="office1.desc">ရုံးအမှတ် (၅၁)၊ အလုပ်သမားဝန်ကြီးဌာန၊ နေပြည်တော်။ ဖုန်း: ၀၆၇-၃၄၃၀၁၈၄</p>'),
    ('                <h3>ရန်ကုန်တိုင်းဒေသကြီး</h3>',
     '                <h3 data-i18n="office2.title">ရန်ကုန်တိုင်းဒေသကြီး</h3>'),
    ('                <p>စက်ရုံဇုန်များ စစ်ဆေးရေးနှင့် OSH ကြီးကြပ်မှု ဝန်ဆောင်မှုများ။</p>',
     '                <p data-i18n="office2.desc">စက်ရုံဇုန်များ စစ်ဆေးရေးနှင့် OSH ကြီးကြပ်မှု ဝန်ဆောင်မှုများ။</p>'),
    ('                <h3>မန္တလေးတိုင်းဒေသကြီး</h3>',
     '                <h3 data-i18n="office3.title">မန္တလေးတိုင်းဒေသကြီး</h3>'),
    ('                <p>တိုင်းဒေသကြီးအတွင်း အလုပ်ရုံ စစ်ဆေးရေးနှင့် တိုင်ကြားစာ လက်ခံခြင်း။</p>',
     '                <p data-i18n="office3.desc">တိုင်းဒေသကြီးအတွင်း အလုပ်ရုံ စစ်ဆေးရေးနှင့် တိုင်ကြားစာ လက်ခံခြင်း။</p>'),
    ('                  <h2>အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန</h2>',
     '                  <h2 data-i18n="news.head">အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန</h2>'),
    ('                  <p class="tagline">လုံခြုံကျန်းမာသော လုပ်ငန်းခွင်၊ တက်ကြွထုတ်လုပ်နိုင်သော အလုပ်သမား</p>',
     '                  <p class="tagline" data-i18n="news.tagline">လုံခြုံကျန်းမာသော လုပ်ငန်းခွင်၊ တက်ကြွထုတ်လုပ်နိုင်သော အလုပ်သမား</p>'),
    ('                    <p class="news-loading">တရားဝင် သတင်းများ ဆွဲယူနေပါသည်…</p>',
     '                    <p class="news-loading" data-i18n="news.loading">တရားဝင် သတင်းများ ဆွဲယူနေပါသည်…</p>'),
    ('                    >အားလုံးကြည့်ရန်</a',
     '                    data-i18n="news.viewAll">အားလုံးကြည့်ရန်</a'),
    ('                    <h3 class="news-below-title">ဝန်ဆောင်မှုများ</h3>',
     '                    <h3 class="news-below-title" data-i18n="news.svcHead">ဝန်ဆောင်မှုများ</h3>'),
    ('                    <a class="news-below-more" href="#services">အားလုံးကြည့်ရန် ›</a>',
     '                    <a class="news-below-more" href="#services" data-i18n="news.svcMore">အားလုံးကြည့်ရန် ›</a>'),
    ('                  <h3>အထူးဖော်ပြချက်များ</h3>',
     '                  <h3 data-i18n="aside.features">အထူးဖော်ပြချက်များ</h3>'),
    ('          <h3 id="see-more-title">ပိုမိုကြည့်ရန်</h3>',
     '          <h3 id="see-more-title" data-i18n="modal.more">ပိုမိုကြည့်ရန်</h3>'),
    ('          <button type="button" class="see-more-x" data-close="1" aria-label="Close">×</button>',
     '          <button type="button" class="see-more-x" data-close="1" aria-label="Close" data-i18n-aria="modal.close">×</button>'),
    ('            <h4>အသုံးဝင်သော လင့်ခ်များ</h4>',
     '            <h4 data-i18n="ft.links">အသုံးဝင်သော လင့်ခ်များ</h4>'),
    ('            <a href="https://www.mol.gov.mm/" target="_blank" rel="noopener noreferrer">အလုပ်သမားဝန်ကြီးဌာန</a>',
     '            <a href="https://www.mol.gov.mm/" target="_blank" rel="noopener noreferrer" data-i18n="ft.mol">အလုပ်သမားဝန်ကြီးဌာန</a>'),
    ('            <a href="https://www.mol.gov.mm/category/news-fgllid/" target="_blank" rel="noopener noreferrer">FGLLID သတင်း</a>',
     '            <a href="https://www.mol.gov.mm/category/news-fgllid/" target="_blank" rel="noopener noreferrer" data-i18n="ft.news">FGLLID သတင်း</a>'),
    ('            <a href="#admin">ညွှန်ကြားရေးမှူးချုပ် ရုံး</a>',
     '            <a href="#admin" data-i18n="ft.dgOffice">ညွှန်ကြားရေးမှူးချုပ် ရုံး</a>'),
    ('            <a href="#history">သမိုင်းနှင့် ဖွဲ့စည်းပုံ</a>',
     '            <a href="#history" data-i18n="ft.history">သမိုင်းနှင့် ဖွဲ့စည်းပုံ</a>'),
    ('            <h4 class="ft-sub">ဝန်ဆောင်မှုများ</h4>',
     '            <h4 class="ft-sub" data-i18n="ft.svc">ဝန်ဆောင်မှုများ</h4>'),
    ('            <a href="#services">စက်ရုံ မှတ်ပုံတင်</a>',
     '            <a href="#services" data-i18n="ft.reg">စက်ရုံ မှတ်ပုံတင်</a>'),
    ('            <a href="#services">OSH စစ်ဆေးရေး</a>',
     '            <a href="#services" data-i18n="ft.osh">OSH စစ်ဆေးရေး</a>'),
    ('            <a href="#complaints">တိုင်ကြားစာ</a>',
     '            <a href="#complaints" data-i18n="ft.complaint">တိုင်ကြားစာ</a>'),
]

ok = 0
fail = 0
for old, new in replacements + intro + more + svc + hist:
    if old in html:
        html = html.replace(old, new, 1)
        ok += 1
    else:
        fail += 1
        print("MISS:", old[:80].replace("\n", " "))

# history paragraphs
hblocks = [
    ("""                  <p class="history-lead">
                    အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာနသည် အလုပ်သမားဝန်ကြီးဌာနအောက်တွင်
                    စက်ရုံ၊ အလုပ်ရုံများ၏ လုံခြုံရေး၊ လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေးနှင့်
                    အလုပ်သမားဥပဒေ လိုက်နာဆောင်ရွက်မှုများကို စစ်ဆေးကြပ်မတ်ရန် ဖွဲ့စည်းထားသော
                    ဦးစီးဌာန ဖြစ်ပါသည်။
                  </p>""",
     """                  <p class="history-lead" data-i18n="hist.p1">
                    အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာနသည် အလုပ်သမားဝန်ကြီးဌာနအောက်တွင်
                    စက်ရုံ၊ အလုပ်ရုံများ၏ လုံခြုံရေး၊ လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေးနှင့်
                    အလုပ်သမားဥပဒေ လိုက်နာဆောင်ရွက်မှုများကို စစ်ဆေးကြပ်မတ်ရန် ဖွဲ့စည်းထားသော
                    ဦးစီးဌာန ဖြစ်ပါသည်။
                  </p>"""),
    ("""                  <p class="history-lead">
                    အစဉ်အဆက် ပြဋ္ဌာန်းခဲ့သော အလုပ်ရုံများဆိုင်ရာ ဥပဒေများ၊ လုပ်ငန်းခွင်
                    ဘေးအန္တရာယ်ကင်းရှင်းရေးနှင့် ကျန်းမာရေး (OSH) ဆိုင်ရာ ပြဋ္ဌာန်းချက်များအရ
                    ကွင်းဆင်းစစ်ဆေးခြင်း၊ အသိပညာပေးခြင်းနှင့် ပြည်သူ့ဝန်ဆောင်မှုများ
                    ဆောင်ရွက်လျက်ရှိပါသည်။
                  </p>""",
     """                  <p class="history-lead" data-i18n="hist.p2">
                    အစဉ်အဆက် ပြဋ္ဌာန်းခဲ့သော အလုပ်ရုံများဆိုင်ရာ ဥပဒေများ၊ လုပ်ငန်းခွင်
                    ဘေးအန္တရာယ်ကင်းရှင်းရေးနှင့် ကျန်းမာရေး (OSH) ဆိုင်ရာ ပြဋ္ဌာန်းချက်များအရ
                    ကွင်းဆင်းစစ်ဆေးခြင်း၊ အသိပညာပေးခြင်းနှင့် ပြည်သူ့ဝန်ဆောင်မှုများ
                    ဆောင်ရွက်လျက်ရှိပါသည်။
                  </p>"""),
    ('                        <span class="history-era">အစောပိုင်းကာလ</span>',
     '                        <span class="history-era" data-i18n="hist.era1">အစောပိုင်းကာလ</span>'),
    ('                        <p>အလုပ်ရုံ စစ်ဆေးရေးနှင့် မှတ်ပုံတင် လုပ်ငန်းများ စတင်</p>',
     '                        <p data-i18n="hist.era1.desc">အလုပ်ရုံ စစ်ဆေးရေးနှင့် မှတ်ပုံတင် လုပ်ငန်းများ စတင်</p>'),
    ('                        <span class="history-era">ခေတ်သစ် ပြုပြင်ပြောင်းလဲမှု</span>',
     '                        <span class="history-era" data-i18n="hist.era2">ခေတ်သစ် ပြုပြင်ပြောင်းလဲမှု</span>'),
    ('                        <p>OSH နှင့် အနည်းဆုံးအခကြေးငွေ စစ်ဆေးမှု တိုးချဲ့</p>',
     '                        <p data-i18n="hist.era2.desc">OSH နှင့် အနည်းဆုံးအခကြေးငွေ စစ်ဆေးမှု တိုးချဲ့</p>'),
    ('                        <span class="history-era">ယနေ့</span>',
     '                        <span class="history-era" data-i18n="hist.era3">ယနေ့</span>'),
    ('                        <p>တိုင်း/ပြည်နယ် ရုံးများနှင့် ချိတ်ဆက်၍ တစ်နိုင်ငံလုံး စစ်ဆေးကြပ်မတ်</p>',
     '                        <p data-i18n="hist.era3.desc">တိုင်း/ပြည်နယ် ရုံးများနှင့် ချိတ်ဆက်၍ တစ်နိုင်ငံလုံး စစ်ဆေးကြပ်မတ်</p>'),
    ('                    <div class="org-node org-node-top">ညွှန်ကြားရေးမှူးချုပ်</div>',
     '                    <div class="org-node org-node-top" data-i18n="org.dg">ညွှန်ကြားရေးမှူးချုပ်</div>'),
    ('                      <div class="org-node">ဒုတိယညွှန်ကြားရေးမှူးချုပ်</div>',
     '                      <div class="org-node" data-i18n="org.ddg">ဒုတိယညွှန်ကြားရေးမှူးချုပ်</div>'),
    ('                      <div class="org-node">ညွှန်ကြားရေးမှူး (စီမံ)</div>',
     '                      <div class="org-node" data-i18n="org.dir">ညွှန်ကြားရေးမှူး (စီမံ)</div>'),
    ('                      <div class="org-node org-node-sm">စစ်ဆေးရေး</div>',
     '                      <div class="org-node org-node-sm" data-i18n="org.insp">စစ်ဆေးရေး</div>'),
    ('                      <div class="org-node org-node-sm">OSH</div>',
     '                      <div class="org-node org-node-sm" data-i18n="org.osh">OSH</div>'),
    ('                      <div class="org-node org-node-sm">တိုင်း/ပြည်နယ် ရုံးများ</div>',
     '                      <div class="org-node org-node-sm" data-i18n="org.offices">တိုင်း/ပြည်နယ် ရုံးများ</div>'),
]

for old, new in hblocks:
    if old in html:
        html = html.replace(old, new, 1)
        ok += 1
    else:
        fail += 1
        print("MISS2:", old[:70].replace("\n", " "))

# complaint copy
old_c = """                <p>
                  လုပ်ငန်းခွင် မတော်တဆမှုနှင့် အလုပ်သမားရေးရာ တိုင်ကြားချက်များကို ပေးပို့နိုင်ပါသည်။
                  အရေးပေါ် ဟော့လိုင်း <strong>1811</strong>။
                </p>"""
new_c = """                <p data-i18n-html="complaint.copy">
                  လုပ်ငန်းခွင် မတော်တဆမှုနှင့် အလုပ်သမားရေးရာ တိုင်ကြားချက်များကို ပေးပို့နိုင်ပါသည်။
                  အရေးပေါ် ဟော့လိုင်း <strong>1811</strong>။
                </p>"""
if old_c in html:
    html = html.replace(old_c, new_c, 1)
    ok += 1
else:
    fail += 1
    print("MISS complaint copy")

# QR sub
old_q = """              <p>
                ဤနေရာသည် သရုပ်ပြ (demo) ဖြစ်ပါသည်။ ဤနေရာတွင် ဖြည့်သွင်းသော အချက်အလက်များကို
                အစိုးရဌာနသို့ တကယ် ပေးပို့မည် မဟုတ်ပါ။
              </p>"""
new_q = """              <p data-i18n="qr.sub">
                ဤနေရာသည် သရုပ်ပြ (demo) ဖြစ်ပါသည်။ ဤနေရာတွင် ဖြည့်သွင်းသော အချက်အလက်များကို
                အစိုးရဌာနသို့ တကယ် ပေးပို့မည် မဟုတ်ပါ။
              </p>"""
if old_q in html:
    html = html.replace(old_q, new_q, 1)
    ok += 1
else:
    fail += 1
    print("MISS qr sub")

old_qd = """              <p class="text-sm text-slate-600 mb-4 leading-relaxed">
                QR စကင်ဖတ်၍ တိုင်ကြားစာ ပုံစံ ဖွင့်နိုင်ပါသည်၊ ပြည့်ပြီးသား ဒေတာကို Database တွင်
                ကြည့်ရှုနိုင်သည်။
              </p>"""
new_qd = """              <p class="text-sm text-slate-600 mb-4 leading-relaxed" data-i18n="qr.cardDesc">
                QR စကင်ဖတ်၍ တိုင်ကြားစာ ပုံစံ ဖွင့်နိုင်ပါသည်၊ ပြည့်ပြီးသား ဒေတာကို Database တွင်
                ကြည့်ရှုနိုင်သည်။
              </p>"""
if old_qd in html:
    html = html.replace(old_qd, new_qd, 1)
    ok += 1
else:
    fail += 1
    print("MISS qr desc")

# View more buttons — add data-i18n class-wide via replace
html = html.replace(
    'class="admin-view-more"',
    'class="admin-view-more" data-i18n="admin.viewMore"',
)
# svc detail links
html = html.replace(
    'class="lu-btn lu-btn-outline" href="#services">အသေးစိတ်</a>',
    'class="lu-btn lu-btn-outline" href="#services" data-i18n="svc.detail">အသေးစိတ်</a>',
)

# news below svc cards (h4 + p) — duplicate of services
html = html.replace(
    "<h4>စက်ရုံ/အလုပ်ရုံ အသိအမှတ်ပြုခြင်း</h4>",
    '<h4 data-i18n="svc1.title">စက်ရုံ/အလုပ်ရုံ အသိအမှတ်ပြုခြင်း</h4>',
)
html = html.replace(
    "<h4>အနိမ့်ဆုံးအခကြေးငွေ စစ်ဆေးခြင်း</h4>",
    '<h4 data-i18n="svc2.title">အနိမ့်ဆုံးအခကြေးငွေ စစ်ဆေးခြင်း</h4>',
)
html = html.replace(
    "<h4>အလုပ်ချိန်နှင့် ခွင့်ရက်များ စစ်ဆေးခြင်း</h4>",
    '<h4 data-i18n="svc3.title">အလုပ်ချိန်နှင့် ခွင့်ရက်များ စစ်ဆေးခြင်း</h4>',
)

# footer remaining
ft = [
    ('            <h4>ဌာနခွဲများ</h4>', '            <h4 data-i18n="ft.depts">ဌာနခွဲများ</h4>'),
    ('            <a href="#offices">တိုင်း/ပြည်နယ် ရုံးများ</a>',
     '            <a href="#offices" data-i18n="ft.offices">တိုင်း/ပြည်နယ် ရုံးများ</a>'),
    ('            <a href="#laws">ဥပဒေနှင့် နည်းဥပဒေများ</a>',
     '            <a href="#laws" data-i18n="ft.laws">ဥပဒေနှင့် နည်းဥပဒေများ</a>'),
    ('            <a href="#news">သတင်းနှင့် ထုတ်ပြန်ချက်</a>',
     '            <a href="#news" data-i18n="ft.newsPress">သတင်းနှင့် ထုတ်ပြန်ချက်</a>'),
    ('            <h4 class="ft-sub">စီမံခန့်ခွဲမှု</h4>',
     '            <h4 class="ft-sub" data-i18n="ft.mgmt">စီမံခန့်ခွဲမှု</h4>'),
    ('            <a href="#offices">ရုံးချုပ် နေပြည်တော်</a>',
     '            <a href="#offices" data-i18n="ft.hq">ရုံးချုပ် နေပြည်တော်</a>'),
    ('            <h4>အရေးပေါ် ခေါ်ဆိုရန်</h4>',
     '            <h4 data-i18n="ft.emergency">အရေးပေါ် ခေါ်ဆိုရန်</h4>'),
    ('            <a href="tel:1811">ဟော့လိုင်း <span class="gold">1811</span></a>',
     '            <a href="tel:1811" data-i18n-html="ft.hotline">ဟော့လိုင်း <span class="gold">1811</span></a>'),
    ('            <a href="tel:0673430184">ရုံးချုပ် ၀၆၇-၃၄၃၀၁၈၄</a>',
     '            <a href="tel:0673430184" data-i18n="ft.hqPhone">ရုံးချုပ် ၀၆၇-၃၄၃၀၁၈၄</a>'),
    ('            <a href="tel:191">မီးဘေး ၁၉၁</a>',
     '            <a href="tel:191" data-i18n="ft.fire">မီးဘေး ၁၉၁</a>'),
    ('            <h4 class="ft-sub">အချက်အလက်</h4>',
     '            <h4 class="ft-sub" data-i18n="ft.info">အချက်အလက်</h4>'),
    ('            <h4>Map · ရုံးတည်နေရာ</h4>',
     '            <h4 data-i18n="ft.map">Map · ရုံးတည်နေရာ</h4>'),
    ('              >OpenStreetMap တွင် ဖွင့်ရန် ›</a',
     '              data-i18n="ft.mapOpen">OpenStreetMap တွင် ဖွင့်ရန် ›</a'),
    ('            <p class="ft-addr">ရုံးအမှတ် (၅၁)၊ အလုပ်သမားဝန်ကြီးဌာန၊ နေပြည်တော်</p>',
     '            <p class="ft-addr" data-i18n="ft.addr">ရုံးအမှတ် (၅၁)၊ အလုပ်သမားဝန်ကြီးဌာန၊ နေပြည်တော်</p>'),
    ('              <span>လည်ပတ်သူ</span>',
     '              <span data-i18n="ft.viewer">လည်ပတ်သူ</span>'),
    ('              <strong>အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန</strong>',
     '              <strong data-i18n="ft.brand">အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန</strong>'),
    ('            <a href="#home">ပင်မ</a>',
     '            <a href="#home" data-i18n="nav.home">ပင်မ</a>'),
    ('            <a href="#services">ဝန်ဆောင်မှု</a>',
     '            <a href="#services" data-i18n="nav.services">ဝန်ဆောင်မှု</a>'),
    ('            <a href="#news">သတင်း</a>',
     '            <a href="#news" data-i18n="nav.news">သတင်း</a>'),
    ('          <div class="ft-copy">© ၂၀၂၆ FGLLID · အလုပ်သမားဝန်ကြီးဌာန · All rights reserved</div>',
     '          <div class="ft-copy" data-i18n="ft.copy">© ၂၀၂၆ FGLLID · အလုပ်သမားဝန်ကြီးဌာန · All rights reserved</div>'),
    ('    <button type="button" class="ft-top" id="scroll-top" aria-label="အပေါ်သို့">',
     '    <button type="button" class="ft-top" id="scroll-top" aria-label="အပေါ်သို့" data-i18n-aria="scroll.top">'),
    ('                <button type="button" class="media-video-play" id="media-video-play" aria-label="ဗီဒီယို ဖွင့်ရန်">',
     '                <button type="button" class="media-video-play" id="media-video-play" aria-label="ဗီဒီယို ဖွင့်ရန်" data-i18n-aria="media.playAria">'),
]

for old, new in ft:
    if old in html:
        html = html.replace(old, new, 1)
        ok += 1
    else:
        fail += 1
        print("MISS ft:", old[:70].replace("\n", " "))

# footer complaint link — may already be done; bottom one
if 'data-i18n="ft.complaint"' not in html:
    html = html.replace(
        '<a href="#complaints">တိုင်ကြားစာ</a>',
        '<a href="#complaints" data-i18n="ft.complaint">တိုင်ကြားစာ</a>',
        1,
    )

# bottom complaints in ft-bottom-links
html = html.replace(
    """            <a href="#complaints">တိုင်ကြားစာ</a>
          </div>
          <div class="ft-copy" """,
    """            <a href="#complaints" data-i18n="nav.complaints">တိုင်ကြားစာ</a>
          </div>
          <div class="ft-copy" """,
)

# EN attrs for admin view-more
en_more = [
    (
        'data-more-title="ဦးဇော်လင်းထွဋ် · Biography"',
        'data-more-title="ဦးဇော်လင်းထွဋ် · Biography" data-more-title-en="U Zaw Lin Htut · Biography"',
    ),
    (
        'data-more-body="ဦးဇော်လင်းထွဋ်သည် အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန၏ ညွှန်ကြားရေးမှူးချုပ်အဖြစ် တာဝန်ထမ်းဆောင်လျက်ရှိပါသည်။ အလုပ်သမားရေးရာ စစ်ဆေးကြပ်မတ်မှု၊ လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေး (OSH) နှင့် အလုပ်သမားဥပဒေ လိုက်နာဆောင်ရွက်မှု မြှင့်တင်ရေးတို့တွင် ဦးဆောင်တာဝန် ယူဆောင်ရွက်လျက်ရှိပါသည်။ တိုင်း/ပြည်နယ် ရုံးခွဲများနှင့် ညှိနှိုင်း၍ ပြည်သူ့ဝန်ဆောင်မှု ပိုမိုကောင်းမွန်ရေး၊ စက်ရုံ/အလုပ်ရုံများတွင် ဘေးကင်းလုံခြုံသော လုပ်ငန်းခွင် ပတ်ဝန်းကျင် တည်ဆောက်ရေးကို အလေးထား ဆောင်ရွက်ပါသည်။"',
        'data-more-body="ဦးဇော်လင်းထွဋ်သည် အလုပ်ရုံနှင့် အလုပ်သမားဥပဒေစစ်ဆေးရေးဦးစီးဌာန၏ ညွှန်ကြားရေးမှူးချုပ်အဖြစ် တာဝန်ထမ်းဆောင်လျက်ရှိပါသည်။ အလုပ်သမားရေးရာ စစ်ဆေးကြပ်မတ်မှု၊ လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေး (OSH) နှင့် အလုပ်သမားဥပဒေ လိုက်နာဆောင်ရွက်မှု မြှင့်တင်ရေးတို့တွင် ဦးဆောင်တာဝန် ယူဆောင်ရွက်လျက်ရှိပါသည်။ တိုင်း/ပြည်နယ် ရုံးခွဲများနှင့် ညှိနှိုင်း၍ ပြည်သူ့ဝန်ဆောင်မှု ပိုမိုကောင်းမွန်ရေး၊ စက်ရုံ/အလုပ်ရုံများတွင် ဘေးကင်းလုံခြုံသော လုပ်ငန်းခွင် ပတ်ဝန်းကျင် တည်ဆောက်ရေးကို အလေးထား ဆောင်ရွက်ပါသည်။" data-more-body-en="U Zaw Lin Htut serves as Director General of FGLLID. He leads labour inspection, OSH, and labour-law compliance, working with State/Region offices to improve public service and safe workplaces."',
    ),
    (
        'data-more-title="ညွှန်ကြားရေးမှူးချုပ်၏ နှုတ်ခွန်းဆက်"',
        'data-more-title="ညွှန်ကြားရေးမှူးချုပ်၏ နှုတ်ခွန်းဆက်" data-more-title-en="Message from the Director General"',
    ),
    (
        'data-more-body="ကျနော်တို့ ဦးစီးဌာနအနေဖြင့် စက်ရုံ၊ အလုပ်ရုံများတွင် အလုပ်သမားများ ဘေးကင်းလုံခြုံစွာ လုပ်ကိုင်နိုင်ရေးအတွက် ဥပဒေနှင့်အညီ တန်းတူညီမျှ စစ်ဆေးကြပ်မတ် လျက်ရှိပါသည်။ အလုပ်ရှင်နှင့် အလုပ်သမား အပြန်အလှန် လေးစားယုံကြည်မှုရှိသော လုပ်ငန်းခွင် ပတ်ဝန်းကျင် တည်ဆောက်ရေးကို ဦးတည်ဆောင်ရွက်ပါသည်။ အလုပ်သမားအခွင့်အရေး ကာကွယ်ရေးနှင့် ဥပဒေလိုက်နာမှု မြှင့်တင်ရေးသည် ကျနော်တို့၏ အဓိက ရည်မှန်းချက် ဖြစ်ပါသည်။"',
        'data-more-body="ကျနော်တို့ ဦးစီးဌာနအနေဖြင့် စက်ရုံ၊ အလုပ်ရုံများတွင် အလုပ်သမားများ ဘေးကင်းလုံခြုံစွာ လုပ်ကိုင်နိုင်ရေးအတွက် ဥပဒေနှင့်အညီ တန်းတူညီမျှ စစ်ဆေးကြပ်မတ် လျက်ရှိပါသည်။ အလုပ်ရှင်နှင့် အလုပ်သမား အပြန်အလှန် လေးစားယုံကြည်မှုရှိသော လုပ်ငန်းခွင် ပတ်ဝန်းကျင် တည်ဆောက်ရေးကို ဦးတည်ဆောင်ရွက်ပါသည်။ အလုပ်သမားအခွင့်အရေး ကာကွယ်ရေးနှင့် ဥပဒေလိုက်နာမှု မြှင့်တင်ရေးသည် ကျနော်တို့၏ အဓိက ရည်မှန်းချက် ဖြစ်ပါသည်။" data-more-body-en="Our department inspects factories so workers can work safely under the law. We aim for workplaces built on mutual respect, protecting workers\' rights and promoting legal compliance."',
    ),
    (
        'data-more-title="ဒုတိယညွှန်ကြားရေးမှူးချုပ်"',
        'data-more-title="ဒုတိယညွှန်ကြားရေးမှူးချုပ်" data-more-title-en="Deputy Director General"',
    ),
    (
        'data-more-body="ဒုတိယညွှန်ကြားရေးမှူးချုပ်သည် စစ်ဆေးရေးနှင့် OSH ကဏ္ဍ ကြီးကြပ်မှုတွင် ကူညီဆောင်ရွက်ပါသည်။ တိုင်း/ပြည်နယ် ရုံးများနှင့် ညှိနှိုင်း၍ စက်ရုံ စစ်ဆေးရေး၊ လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေး စံချိန်စံညွှန်းများ လိုက်နာမှု မြှင့်တင်ရေးတို့ကို ပံ့ပိုးဆောင်ရွက်ပါသည်။"',
        'data-more-body="ဒုတိယညွှန်ကြားရေးမှူးချုပ်သည် စစ်ဆေးရေးနှင့် OSH ကဏ္ဍ ကြီးကြပ်မှုတွင် ကူညီဆောင်ရွက်ပါသည်။ တိုင်း/ပြည်နယ် ရုံးများနှင့် ညှိနှိုင်း၍ စက်ရုံ စစ်ဆေးရေး၊ လုပ်ငန်းခွင် ဘေးအန္တရာယ်ကင်းရှင်းရေး စံချိန်စံညွှန်းများ လိုက်နာမှု မြှင့်တင်ရေးတို့ကို ပံ့ပိုးဆောင်ရွက်ပါသည်။" data-more-body-en="The Deputy Director General supports oversight of inspection and OSH, coordinating with State/Region offices on factory inspection and workplace safety standards."',
    ),
    (
        'data-more-title="ညွှန်ကြားရေးမှူး (စီမံ)"',
        'data-more-title="ညွှန်ကြားရေးမှူး (စီမံ)" data-more-title-en="Director (Admin)"',
    ),
    (
        'data-more-body="ညွှန်ကြားရေးမှူး (စီမံ) သည် စီမံခန့်ခွဲရေးနှင့် ရုံးလုပ်ငန်းများကို စနစ်တကျ ဆောင်ရွက်ပါသည်။ ဝန်ထမ်းရေးရာ၊ ရုံးစနစ်၊ မှတ်တမ်းထိန်းသိမ်းမှုနှင့် အတွင်းရေးရာ ညှိနှိုင်းဆောင်ရွက်မှုများတွင် တာဝန်ယူပါသည်။"',
        'data-more-body="ညွှန်ကြားရေးမှူး (စီမံ) သည် စီမံခန့်ခွဲရေးနှင့် ရုံးလုပ်ငန်းများကို စနစ်တကျ ဆောင်ရွက်ပါသည်။ ဝန်ထမ်းရေးရာ၊ ရုံးစနစ်၊ မှတ်တမ်းထိန်းသိမ်းမှုနှင့် အတွင်းရေးရာ ညှိနှိုင်းဆောင်ရွက်မှုများတွင် တာဝန်ယူပါသည်။" data-more-body-en="The Director (Admin) manages administration and office operations, including HR, office systems, records, and internal coordination."',
    ),
]
for old, new in en_more:
    if old in html:
        html = html.replace(old, new, 1)
        ok += 1
    else:
        fail += 1
        print("MISS en:", old[:60])

p.write_text(html, encoding="utf-8")
print(f"OK={ok} FAIL={fail}")
print("i18n.js" in html, html.count("data-i18n"))
