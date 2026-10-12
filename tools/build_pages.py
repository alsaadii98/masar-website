#!/usr/bin/env python3
"""Build the site pages in ar, en and ckb: the Waze-alternative landing page and the
store pages (privacy, terms, delete-account, support), plus robots.txt, sitemap.xml
and .well-known (app links).

Arabic is the default and lives at the site root (/privacy). English and Kurdish
live under /en/ and /ckb/. GitHub Pages serves privacy.html at /privacy, so the
URLs stay clean. Run from the repo root:  python3 tools/build_pages.py
"""
from html import escape
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
ORIGIN = "https://masarmaps.com"
# Hostinger alias: support@ delivers to ali@masarmaps.com.
EMAIL = "support@masarmaps.com"

LANGS = {
    "ar": {"dir": "rtl", "prefix": "", "label": "العربية", "brand": "مسار"},
    "en": {"dir": "ltr", "prefix": "/en", "label": "English", "brand": "Masar"},
    "ckb": {"dir": "rtl", "prefix": "/ckb", "label": "کوردی", "brand": "مسار"},
}
PAGES = ["privacy", "terms", "delete-account", "support"]


def url(lang, page):
    return f"{LANGS[lang]['prefix']}/{page}"


def mail_link():
    return f'<a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>'


def inline_mail():
    return f'<a href="mailto:{EMAIL}"><bdi>{EMAIL}</bdi></a>'


def path(*steps, rtl):
    arrow = " ← " if rtl else " → "
    return '<span class="path">' + arrow.join(steps) + "</span>"


# --------------------------------------------------------------------------
# Content. Blocks: str -> <p>; ("ul", [..]) / ("ol", [..]); ("h3", str);
# ("mail",) -> big mail button. Strings may hold trusted inline HTML.
# --------------------------------------------------------------------------

def content(lang):
    L = lambda page: url(lang, page)
    M = inline_mail()

    if lang == "en":
        app_path = path("Settings", "My account", "Delete account", rtl=False)
        return {
            "nav": {"privacy": "Privacy", "terms": "Terms", "delete-account": "Delete account", "support": "Support"},
            "home": "Home",
            "effective": "Effective 12 October 2026",
            "osm": 'Map data © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
            "privacy": {
                "title": "Privacy Policy",
                "lead": "Masar is a navigation app for Iraq. Here is what we collect, and why.",
                "sections": [
                    ("In short", [("ul", [
                        "No ads.",
                        "We never sell your data.",
                        "No tracking across apps. No advertising ID (IDFA or AAID).",
                        "You can use Masar without an account.",
                    ])]),
                    ("Account (optional)", [
                        "You can browse the map, navigate and post road reports as a guest.",
                        "If you log in, you use your Iraqi mobile number. We send a one-time code by WhatsApp through our provider, eSITE gateway. We store your phone number encrypted, for your account.",
                    ]),
                    ("Location", [("ul", [
                        "Masar uses your location only while the app is open or while you navigate. It never tracks you in the background otherwise.",
                        "During a trip, the app sends anonymous GPS points (position, speed, heading) to compute live traffic.",
                        "These points carry a trip token that changes every trip. They are never linked to your account or phone number.",
                        "Raw points are deleted within 24 hours. We keep only average road speeds.",
                    ])]),
                    ("Road reports", [
                        "Reports (traffic, police, accident, hazard, road closed, checkpoint, flood, bad weather, speed bump, map error) show their place, type and time to other drivers.",
                        "We never show who posted a report. Guest reports carry a random device ID to stop abuse. Logged-in users earn points.",
                    ]),
                    ("Saved places", [
                        "Home, work and favourites stay on your phone while you are a guest. Once you log in, we store them on our server so they follow your account.",
                    ]),
                    ("Notifications", [
                        "To send notifications, we keep a Firebase Cloud Messaging token with your app language, platform and app version. It is linked to your account if you are logged in.",
                        "You can turn notifications off in your phone settings.",
                    ]),
                    ("Crash reports and analytics", [
                        "We use Google Firebase Crashlytics and Analytics to fix bugs and improve the app. They receive the app version, language, device model, crash details and which screens and features are used.",
                        "We never send your location, phone number or searches. No advertising ID, no tracking. Firebase may estimate a rough region from your IP address.",
                    ]),
                    ("Maps", [
                        "Maps and routes come from our own servers, built on OpenStreetMap data (© OpenStreetMap contributors, ODbL). We do not use Google or Apple maps for map data or routing.",
                    ]),
                    ("Where your data is kept", [
                        "On our own servers. All connections use HTTPS, and personal data is encrypted at rest.",
                    ]),
                    ("Delete your account", [
                        f"In the app: {app_path}. This removes your phone number, saved places, push tokens and points.",
                        f'You can also ask by email. See <a href="{L("delete-account")}">Delete account</a>.',
                    ]),
                    ("Children", ["Masar is not directed at children under 13."]),
                    ("Changes", ["If we change this policy, we update this page and the date above."]),
                    ("Contact", [("mail",)]),
                ],
            },
            "terms": {
                "title": "Terms of Use",
                "lead": "Short rules for using Masar.",
                "sections": [
                    ("Drive safely", [("ul", [
                        "Follow traffic laws and road signs. The real road always comes first.",
                        "Do not use the app while driving. Set your route before you go, or let a passenger do it.",
                    ])]),
                    ("Routes are guidance", [
                        "Routes, times and alerts are guidance only and can be wrong. You are responsible for how you drive.",
                    ]),
                    ("Reports must be true", [
                        "Post only real, current road reports. No false, offensive or personal content.",
                    ]),
                    ("Our rights", [
                        "We may remove false or abusive reports, and block devices or accounts that misuse Masar.",
                    ]),
                    ("Map data", [
                        'Map data © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>, available under the Open Database License (ODbL).',
                    ]),
                    ("Privacy", [f'See our <a href="{L("privacy")}">Privacy Policy</a>.']),
                    ("Contact", [("mail",)]),
                ],
            },
            "delete-account": {
                "title": "Delete your account",
                "lead": "You can delete your Masar account at any time.",
                "sections": [
                    ("In the app", [("ol", [
                        "Open Masar.",
                        f"Go to {path('Settings', 'My account', rtl=False)}.",
                        "Tap <strong>Delete account</strong>, then <strong>Delete for good</strong>.",
                    ])]),
                    ("By email", [
                        "Can't use the app? Email us with the phone number on your account. We may contact you to confirm the account is yours. We handle requests within 30 days.",
                        ("mail",),
                    ]),
                    ("What we delete", [("ul", [
                        "Your phone number and name",
                        "Your saved places",
                        "Your push notification tokens",
                        "Your points and level",
                    ])]),
                    ("What we keep", [("ul", [
                        "Anonymous traffic data (average road speeds). It is not linked to you.",
                        "Your past road reports stay on the map, without your name.",
                    ])]),
                    ("Guests", [
                        "Without an account we hold no account data. Uninstalling the app removes your saved places from the phone.",
                    ]),
                ],
            },
            "support": {
                "title": "Support",
                "lead": "Questions about Masar? We're here to help.",
                "sections": [
                    ("Contact us", [("mail",)]),
                    ("Questions", [
                        ("h3", "Do I need an account?"),
                        "No. You can search, navigate and post reports as a guest. Log in only to keep points and sync your saved places.",
                        ("h3", "How do road reports work?"),
                        "Tap <strong>Report</strong> and pick a type. Drivers nearby see it on the map with its place and time. Your name is never shown.",
                        ("h3", "Does Masar work with CarPlay and Android Auto?"),
                        "Yes. Connect your phone to your car and open Masar on the car screen.",
                        ("h3", "How do I delete my account?"),
                        f'In the app: {app_path}. Or see <a href="{L("delete-account")}">Delete account</a>.',
                    ]),
                ],
            },
        }

    if lang == "ar":
        app_path = path("الإعدادات", "حسابي", "حذف الحساب", rtl=True)
        return {
            "nav": {"privacy": "الخصوصية", "terms": "الشروط", "delete-account": "حذف الحساب", "support": "الدعم"},
            "home": "الرئيسية",
            "effective": "تاريخ السريان: 12 تشرين الأول 2026",
            "osm": 'بيانات الخريطة © <a href="https://www.openstreetmap.org/copyright">مساهمو OpenStreetMap</a>',
            "privacy": {
                "title": "سياسة الخصوصية",
                "lead": "مسار تطبيق ملاحة للعراق. هذا ما نجمعه ولماذا.",
                "sections": [
                    ("باختصار", [("ul", [
                        "لا إعلانات.",
                        "لا نبيع بياناتك أبداً.",
                        "لا تتبّع بين التطبيقات، ولا معرّف إعلاني (IDFA أو AAID).",
                        "تستطيع استخدام مسار بدون حساب.",
                    ])]),
                    ("الحساب (اختياري)", [
                        "تستطيع تصفّح الخريطة والملاحة ونشر البلاغات كضيف.",
                        "إذا سجّلت الدخول، تستخدم رقم هاتفك العراقي. نرسل لك رمزاً لمرة واحدة عبر واتساب من خلال مزوّدنا eSITE gateway. نحفظ رقم هاتفك مشفّراً لحسابك.",
                    ]),
                    ("الموقع", [("ul", [
                        "يستخدم مسار موقعك فقط والتطبيق مفتوح أو أثناء الملاحة، ولا يتتبّعك في الخلفية غير ذلك أبداً.",
                        "أثناء الرحلة يرسل التطبيق نقاط GPS مجهولة (الموقع والسرعة والاتجاه) لحساب الزحمة المباشرة.",
                        "ترتبط هذه النقاط برمز رحلة يتغيّر مع كل رحلة، ولا ترتبط أبداً بحسابك أو رقم هاتفك.",
                        "نحذف النقاط الخام خلال 24 ساعة، ونحتفظ فقط بمعدّل سرعة الطرق.",
                    ])]),
                    ("البلاغات", [
                        "البلاغات (زحمة، شرطة، حادث، خطر، طريق مغلق، سيطرة، فيضان، طقس سيئ، مطب، خطأ بالخريطة) تُظهر مكانها ونوعها ووقتها للسائقين الآخرين.",
                        "لا نُظهر أبداً من نشر البلاغ. بلاغات الضيوف تحمل معرّف جهاز عشوائياً للحماية من الإساءة. المستخدمون المسجّلون يكسبون نقاطاً.",
                    ]),
                    ("الأماكن المحفوظة", [
                        "البيت والعمل والمفضّلة تبقى على هاتفك ما دمت ضيفاً. بعد تسجيل الدخول نحفظها على خادمنا لتبقى مع حسابك.",
                    ]),
                    ("الإشعارات", [
                        "لإرسال الإشعارات نحفظ رمز Firebase Cloud Messaging مع لغة التطبيق ونظام التشغيل وإصدار التطبيق، ويرتبط بحسابك إذا كنت مسجّلاً.",
                        "تستطيع إيقاف الإشعارات من إعدادات هاتفك.",
                    ]),
                    ("تقارير الأعطال والإحصاءات", [
                        "نستخدم Google Firebase Crashlytics و Analytics لإصلاح الأخطاء وتحسين التطبيق. تصلها نسخة التطبيق واللغة وطراز الجهاز وتفاصيل الأعطال والشاشات والميزات المستخدمة.",
                        "لا نرسل أبداً موقعك أو رقم هاتفك أو ما تبحث عنه. لا معرّف إعلاني ولا تتبّع. قد يقدّر Firebase منطقة تقريبية من عنوان IP.",
                    ]),
                    ("الخرائط", [
                        "الخرائط والمسارات من خوادمنا الخاصة، مبنية على بيانات OpenStreetMap (© مساهمو OpenStreetMap، رخصة ODbL). لا نستخدم خرائط Google أو Apple لبيانات الخريطة أو المسارات.",
                    ]),
                    ("أين تُحفظ بياناتك", [
                        "على خوادمنا الخاصة. كل الاتصالات عبر HTTPS، والبيانات الشخصية مشفّرة أثناء التخزين.",
                    ]),
                    ("حذف حسابك", [
                        f"من التطبيق: {app_path}. يحذف ذلك رقم هاتفك وأماكنك المحفوظة ورموز الإشعارات ونقاطك.",
                        f'تستطيع أيضاً الطلب عبر البريد. راجع صفحة <a href="{L("delete-account")}">حذف الحساب</a>.',
                    ]),
                    ("الأطفال", ["مسار غير موجّه للأطفال دون 13 سنة."]),
                    ("التغييرات", ["إذا غيّرنا هذه السياسة نحدّث هذه الصفحة والتاريخ أعلاه."]),
                    ("تواصل معنا", [("mail",)]),
                ],
            },
            "terms": {
                "title": "شروط الاستخدام",
                "lead": "قواعد قصيرة لاستخدام مسار.",
                "sections": [
                    ("قُد بأمان", [("ul", [
                        "التزم بقوانين المرور وإشارات الطريق. الطريق الفعلي يأتي أولاً دائماً.",
                        "لا تستخدم التطبيق أثناء القيادة. حدّد مسارك قبل الانطلاق، أو اطلب ذلك من مرافقك.",
                    ])]),
                    ("المسارات للإرشاد فقط", [
                        "المسارات والأوقات والتنبيهات للإرشاد فقط وقد تكون غير دقيقة. أنت المسؤول عن طريقة قيادتك.",
                    ]),
                    ("البلاغات يجب أن تكون صحيحة", [
                        "انشر فقط بلاغات حقيقية وحالية. لا محتوى كاذباً أو مسيئاً أو شخصياً.",
                    ]),
                    ("حقوقنا", [
                        "قد نحذف البلاغات الكاذبة أو المسيئة، ونحظر الأجهزة أو الحسابات التي تسيء استخدام مسار.",
                    ]),
                    ("بيانات الخريطة", [
                        'بيانات الخريطة © <a href="https://www.openstreetmap.org/copyright">مساهمو OpenStreetMap</a>، متاحة برخصة قاعدة البيانات المفتوحة (ODbL).',
                    ]),
                    ("الخصوصية", [f'راجع <a href="{L("privacy")}">سياسة الخصوصية</a>.']),
                    ("تواصل معنا", [("mail",)]),
                ],
            },
            "delete-account": {
                "title": "حذف الحساب",
                "lead": "تستطيع حذف حسابك في مسار في أي وقت.",
                "sections": [
                    ("من التطبيق", [("ol", [
                        "افتح مسار.",
                        f"اذهب إلى {path('الإعدادات', 'حسابي', rtl=True)}.",
                        "اضغط <strong>حذف الحساب</strong>، ثم <strong>حذف الحساب نهائياً</strong>.",
                    ])]),
                    ("عبر البريد", [
                        "لا تستطيع استخدام التطبيق؟ راسلنا مع رقم الهاتف المرتبط بحسابك. قد نتواصل معك للتأكد أن الحساب لك. ننفّذ الطلب خلال 30 يوماً.",
                        ("mail",),
                    ]),
                    ("ما نحذفه", [("ul", [
                        "رقم هاتفك واسمك",
                        "أماكنك المحفوظة",
                        "رموز الإشعارات",
                        "نقاطك ومستواك",
                    ])]),
                    ("ما نحتفظ به", [("ul", [
                        "بيانات الزحمة المجهولة (معدّل سرعة الطرق)، وهي غير مرتبطة بك.",
                        "بلاغاتك السابقة تبقى على الخريطة بدون اسمك.",
                    ])]),
                    ("الضيوف", [
                        "بدون حساب لا نحتفظ بأي بيانات حساب. حذف التطبيق يحذف أماكنك المحفوظة من الهاتف.",
                    ]),
                ],
            },
            "support": {
                "title": "الدعم",
                "lead": "عندك سؤال عن مسار؟ نحن هنا للمساعدة.",
                "sections": [
                    ("تواصل معنا", [("mail",)]),
                    ("أسئلة شائعة", [
                        ("h3", "هل أحتاج حساباً؟"),
                        "لا. تستطيع البحث والملاحة ونشر البلاغات كضيف. سجّل الدخول فقط لجمع النقاط ومزامنة أماكنك المحفوظة.",
                        ("h3", "كيف تعمل البلاغات؟"),
                        "اضغط <strong>بلّغ</strong> واختر النوع. يظهر البلاغ على الخريطة للسائقين القريبين مع مكانه ووقته. لا يظهر اسمك أبداً.",
                        ("h3", "هل يعمل مسار مع CarPlay و Android Auto؟"),
                        "نعم. اربط هاتفك بالسيارة وافتح مسار على شاشة السيارة.",
                        ("h3", "كيف أحذف حسابي؟"),
                        f'من التطبيق: {app_path}. أو راجع صفحة <a href="{L("delete-account")}">حذف الحساب</a>.',
                    ]),
                ],
            },
        }

    # ckb — Kurdish (Sorani). Needs native review before store submission.
    app_path = path("ڕێکخستنەکان", "هەژمارەکەم", "سڕینەوەی هەژمار", rtl=True)
    return {
        "nav": {"privacy": "تایبەتمەندی", "terms": "مەرجەکان", "delete-account": "سڕینەوەی هەژمار", "support": "پشتگیری"},
        "home": "سەرەتا",
        "effective": "بەرواری کارپێکردن: 12ی تشرینی یەکەمی 2026",
        "osm": 'داتای نەخشە © <a href="https://www.openstreetmap.org/copyright">بەشداربووانی OpenStreetMap</a>',
        "privacy": {
            "title": "سیاسەتی تایبەتمەندی",
            "lead": "مسار ئەپێکی ڕێنیشاندەرە بۆ عێراق. ئەمە ئەوەیە کە کۆی دەکەینەوە و بۆچی.",
            "sections": [
                ("بە کورتی", [("ul", [
                    "هیچ ڕیکلامێک نییە.",
                    "هەرگیز زانیارییەکانت نافرۆشین.",
                    "شوێنکەوتن لە نێوان ئەپەکاندا نییە، و ناسنامەی ڕیکلام (IDFA یان AAID) بەکارناهێنین.",
                    "دەتوانیت بەبێ هەژمار مسار بەکاربهێنیت.",
                ])]),
                ("هەژمار (ئارەزوومەندانە)", [
                    "دەتوانیت وەک میوان نەخشە ببینیت، ڕێنیشاندەر بەکاربهێنیت و ڕاپۆرت بنێریت.",
                    "ئەگەر بچیتە ژوورەوە، ژمارەی مۆبایلی عێراقیت بەکاردەهێنیت. کۆدێکی یەکجاری لە ڕێگەی واتسئاپەوە بە هۆی دابینکەرەکەمان eSITE gateway بۆت دەنێرین. ژمارەی مۆبایلەکەت بە شفرەکراوی بۆ هەژمارەکەت هەڵدەگرین.",
                ]),
                ("شوێن", [("ul", [
                    "مسار تەنها کاتێک شوێنەکەت بەکاردەهێنێت کە ئەپەکە کراوەیە یان لە کاتی ڕێنیشانداندا. جگە لەوە هەرگیز لە پاشبنەمادا بەدواتدا ناچێت.",
                    "لە کاتی گەشتدا، ئەپەکە خاڵی GPSی بێناو (شوێن، خێرایی، ئاراستە) دەنێرێت بۆ ژماردنی قەرەباڵغی ڕاستەوخۆ.",
                    "ئەم خاڵانە نیشانەیەکی گەشتیان پێوەیە کە لە هەر گەشتێکدا دەگۆڕێت. هەرگیز بە هەژمار یان ژمارەی مۆبایلەکەتەوە نابەسترێنەوە.",
                    "خاڵە خاوەکان لە ماوەی 24 کاتژمێردا دەسڕینەوە. تەنها تێکڕای خێرایی ڕێگاکان هەڵدەگرین.",
                ])]),
                ("ڕاپۆرتەکان", [
                    "ڕاپۆرتەکان (قەرەباڵغی، پۆلیس، ڕووداو، مەترسی، ڕێگای داخراو، سەیتەرە، لافاو، کەشوهەوای خراپ، بەربەستی خێرایی، هەڵەی نەخشە) شوێن و جۆر و کاتیان بۆ شۆفێرانی تر پیشان دەدرێت.",
                    "هەرگیز پیشانی نادەین کێ ڕاپۆرتەکەی ناردووە. ڕاپۆرتی میوانەکان ناسنامەیەکی هەڕەمەکیی ئامێریان پێوەیە بۆ ڕێگرتن لە خراپ بەکارهێنان. ئەوانەی چوونەتە ژوورەوە خاڵ کۆدەکەنەوە.",
                ]),
                ("شوێنە پاشەکەوتکراوەکان", [
                    "ماڵ، کار و دڵخوازەکان لەسەر مۆبایلەکەت دەمێننەوە تا میوان بیت. دوای چوونەژوورەوە لەسەر سێرڤەرەکەمان هەڵیاندەگرین تا لەگەڵ هەژمارەکەتدا بن.",
                ]),
                ("ئاگادارکردنەوەکان", [
                    "بۆ ناردنی ئاگادارکردنەوە، نیشانەیەکی Firebase Cloud Messaging لەگەڵ زمانی ئەپ، سیستەم و وەشانی ئەپ هەڵدەگرین. ئەگەر چووبیتە ژوورەوە بە هەژمارەکەتەوە دەبەسترێتەوە.",
                    "دەتوانیت لە ڕێکخستنەکانی مۆبایلەکەتەوە ئاگادارکردنەوەکان بکوژێنیتەوە.",
                ]),
                ("ڕاپۆرتی تێکچوون و ئامار", [
                    "Google Firebase Crashlytics و Analytics بەکاردەهێنین بۆ چاککردنی هەڵەکان و باشترکردنی ئەپەکە. وەشانی ئەپ، زمان، مۆدێلی ئامێر، وردەکاریی تێکچوون و ئەو شاشە و تایبەتمەندییانەی بەکاردێن وەردەگرن.",
                    "هەرگیز شوێن، ژمارەی مۆبایل یان گەڕانەکانت نانێرین. ناسنامەی ڕیکلام و شوێنکەوتن نییە. لەوانەیە Firebase ناوچەیەکی نزیکەیی لە ناونیشانی IPەوە بخەمڵێنێت.",
                ]),
                ("نەخشەکان", [
                    "نەخشە و ڕێگاکان لە سێرڤەرەکانی خۆمانەوە دێن و لەسەر داتای OpenStreetMap دروستکراون (© بەشداربووانی OpenStreetMap، مۆڵەتی ODbL). نەخشەی Google یان Apple بۆ داتای نەخشە یان ڕێگا بەکارناهێنین.",
                ]),
                ("زانیارییەکانت لە کوێ هەڵدەگیرێن", [
                    "لەسەر سێرڤەرەکانی خۆمان. هەموو پەیوەندییەکان بە HTTPSن، و زانیارییە کەسییەکان لە کاتی هەڵگرتندا شفرەکراون.",
                ]),
                ("سڕینەوەی هەژمارەکەت", [
                    f"لە ئەپەکەدا: {app_path}. ئەمە ژمارەی مۆبایل، شوێنە پاشەکەوتکراوەکان، نیشانەکانی ئاگادارکردنەوە و خاڵەکانت دەسڕێتەوە.",
                    f'دەتوانیت بە ئیمەیڵیش داوا بکەیت. سەیری <a href="{L("delete-account")}">سڕینەوەی هەژمار</a> بکە.',
                ]),
                ("منداڵان", ["مسار بۆ منداڵانی خوار 13 ساڵ ئامادە نەکراوە."]),
                ("گۆڕانکاری", ["ئەگەر ئەم سیاسەتە بگۆڕین، ئەم پەڕەیە و بەروارەکەی سەرەوە نوێ دەکەینەوە."]),
                ("پەیوەندیمان پێوە بکە", [("mail",)]),
            ],
        },
        "terms": {
            "title": "مەرجەکانی بەکارهێنان",
            "lead": "چەند ڕێسایەکی کورت بۆ بەکارهێنانی مسار.",
            "sections": [
                ("بە سەلامەتی لێبخوڕە", [("ul", [
                    "پابەندی یاساکانی هاتوچۆ و نیشانەکانی ڕێگا بە. ڕێگای ڕاستەقینە هەمیشە لە پێشەوەیە.",
                    "لە کاتی لێخوڕیندا ئەپەکە بەکارمەهێنە. پێش ڕۆیشتن ڕێگاکەت دیاری بکە، یان با هاوڕێکەت بیکات.",
                ])]),
                ("ڕێگاکان تەنها ڕێنمایین", [
                    "ڕێگا، کات و ئاگادارکردنەوەکان تەنها بۆ ڕێنماییین و لەوانەیە هەڵە بن. تۆ بەرپرسیاری شێوەی لێخوڕینەکەتیت.",
                ]),
                ("ڕاپۆرتەکان دەبێت ڕاست بن", [
                    "تەنها ڕاپۆرتی ڕاستەقینە و ئێستایی بنێرە. ناوەڕۆکی درۆ، سووکایەتیئامێز یان کەسی مەنێرە.",
                ]),
                ("مافەکانمان", [
                    "لەوانەیە ڕاپۆرتی درۆ یان خراپ بسڕینەوە، و ئەو ئامێر یان هەژمارانە بلۆک بکەین کە خراپ مسار بەکاردەهێنن.",
                ]),
                ("داتای نەخشە", [
                    'داتای نەخشە © <a href="https://www.openstreetmap.org/copyright">بەشداربووانی OpenStreetMap</a>، بە مۆڵەتی Open Database License (ODbL).',
                ]),
                ("تایبەتمەندی", [f'سەیری <a href="{L("privacy")}">سیاسەتی تایبەتمەندی</a> بکە.']),
                ("پەیوەندیمان پێوە بکە", [("mail",)]),
            ],
        },
        "delete-account": {
            "title": "سڕینەوەی هەژمار",
            "lead": "هەر کاتێک بتەوێت دەتوانیت هەژمارەکەت لە مسار بسڕیتەوە.",
            "sections": [
                ("لە ئەپەکەدا", [("ol", [
                    "مسار بکەرەوە.",
                    f"بڕۆ بۆ {path('ڕێکخستنەکان', 'هەژمارەکەم', rtl=True)}.",
                    "<strong>سڕینەوەی هەژمار</strong> دابگرە، پاشان <strong>سڕینەوەی هەمیشەیی</strong>.",
                ])]),
                ("بە ئیمەیڵ", [
                    "ناتوانیت ئەپەکە بەکاربهێنیت؟ ئیمەیڵمان بۆ بنێرە لەگەڵ ئەو ژمارە مۆبایلەی کە هەژمارەکەتی پێوەیە. لەوانەیە پەیوەندیت پێوە بکەین بۆ دڵنیابوون لەوەی هەژمارەکە هی تۆیە. لە ماوەی 30 ڕۆژدا داواکارییەکە جێبەجێ دەکەین.",
                    ("mail",),
                ]),
                ("ئەوەی دەیسڕینەوە", [("ul", [
                    "ژمارەی مۆبایل و ناوت",
                    "شوێنە پاشەکەوتکراوەکانت",
                    "نیشانەکانی ئاگادارکردنەوە",
                    "خاڵ و ئاستەکەت",
                ])]),
                ("ئەوەی هەڵیدەگرین", [("ul", [
                    "داتای بێناوی قەرەباڵغی (تێکڕای خێرایی ڕێگاکان)، کە بە تۆوە نەبەستراوەتەوە.",
                    "ڕاپۆرتە کۆنەکانت بەبێ ناوت لەسەر نەخشە دەمێننەوە.",
                ])]),
                ("میوانەکان", [
                    "بەبێ هەژمار هیچ زانیارییەکی هەژمارمان لا نییە. سڕینەوەی ئەپەکە شوێنە پاشەکەوتکراوەکانت لە مۆبایلەکە دەسڕێتەوە.",
                ]),
            ],
        },
        "support": {
            "title": "پشتگیری",
            "lead": "پرسیارت دەربارەی مسار هەیە؟ ئێمە لێرەین بۆ یارمەتیدان.",
            "sections": [
                ("پەیوەندیمان پێوە بکە", [("mail",)]),
                ("پرسیارە باوەکان", [
                    ("h3", "پێویستم بە هەژمار هەیە؟"),
                    "نەخێر. دەتوانیت وەک میوان بگەڕێیت، ڕێنیشاندەر بەکاربهێنیت و ڕاپۆرت بنێریت. تەنها بۆ کۆکردنەوەی خاڵ و هاوکاتکردنی شوێنە پاشەکەوتکراوەکان بچۆ ژوورەوە.",
                    ("h3", "ڕاپۆرتەکان چۆن کار دەکەن؟"),
                    "<strong>ڕاپۆرت بکە</strong> دابگرە و جۆرێک هەڵبژێرە. شۆفێرانی نزیک لەسەر نەخشە دەیبینن لەگەڵ شوێن و کاتەکەی. هەرگیز ناوت پیشان نادرێت.",
                    ("h3", "مسار لەگەڵ CarPlay و Android Auto کار دەکات؟"),
                    "بەڵێ. مۆبایلەکەت بە ئۆتۆمبێلەکەتەوە ببەستە و مسار لەسەر شاشەی ئۆتۆمبێلەکە بکەرەوە.",
                    ("h3", "چۆن هەژمارەکەم بسڕمەوە؟"),
                    f'لە ئەپەکەدا: {app_path}. یان سەیری <a href="{L("delete-account")}">سڕینەوەی هەژمار</a> بکە.',
                ]),
            ],
        },
    }


# --------------------------------------------------------------------------

def render_block(b):
    if isinstance(b, str):
        return f"<p>{b}</p>"
    kind = b[0]
    if kind in ("ul", "ol"):
        items = "".join(f"<li>{i}</li>" for i in b[1])
        return f"<{kind}>{items}</{kind}>"
    if kind == "h3":
        return f"<h3>{b[1]}</h3>"
    if kind == "mail":
        return f"<p>{mail_link()}</p>"
    raise ValueError(kind)




# --------------------------------------------------------------------------
# Landing page: "Waze alternative in Iraq". Targets the searches around the
# October 2026 ban (بديل ويز في العراق، حظر تطبيق ويز، مصطفى سند تطبيق ويز).
# Ban facts are attributed to press reports and cited; update if the date moves.
# --------------------------------------------------------------------------

SOURCES = [
    ("Kurdistan24", "https://www.kurdistan24.net/en/story/944372"),
    ("Al Jazeera", "https://www.aljazeera.com/news/2026/10/9/why-has-iraq-decided-to-ban-online-map-service-waze"),
    ("The National", "https://www.thenationalnews.com/news/mena/2026/10/07/iraq-to-ban-waze-navigation-app-over-israeli-links/"),
]


def sources_line(label):
    joined = " · ".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in SOURCES)
    return f'<p class="sources">{label}: {joined}</p>'


def landing(lang):
    L = lambda page: url(lang, page)
    if lang == "ar":
        return {
            "nav": "بديل ويز",
            "seo_title": "بديل ويز في العراق: مسار، تطبيق ملاحة عراقي",
            "description": "بعد قرار حظر تطبيق ويز في العراق، مسار تطبيق ملاحة عراقي فيه زحمة مباشرة وبلاغات الطريق وإرشاد صوتي بالعربي والكوردي. قريباً على App Store و Google Play.",
            "title": "بديل ويز في العراق",
            "lead": "مسار تطبيق ملاحة عراقي، مصنوع للعراق. قريباً على App Store و Google Play.",
            "sections": [
                ("حظر تطبيق ويز في العراق", [
                    "في تشرين الأول 2026 أعلن وزير الاتصالات مصطفى سند حظر تطبيق ويز (Waze) في العراق، وقال إن السبب أن التطبيق إسرائيلي المنشأ. حُدّد الحظر أولاً مطلع 2027، ثم قُدّم موعده إلى نهاية كانون الأول 2026، بحسب تقارير صحفية.",
                    ("raw", sources_line("المصادر")),
                ]),
                ("مسار: بديل عراقي لويز", [("ul", [
                    "زحمة مباشرة على الطرق، تتحدّث كل دقيقة.",
                    "إرشاد صوتي خطوة بخطوة، وإعادة توجيه تلقائية إذا خرجت عن المسار.",
                    "بلاغات السائقين: حوادث، زحمة، طرق مغلقة، فيضانات، مطبات وغيرها.",
                    "بحث بالعربي والكوردي والإنكليزي، وحتى العربي المكتوب بحروف لاتينية.",
                    "مشاركة وقت الوصول عبر واتساب وتيليغرام.",
                    "يعمل مع CarPlay و Android Auto.",
                    "بدون إعلانات، وبدون حساب.",
                ])]),
                ("خصوصيتك أولاً", [
                    f'لا نبيع بياناتك أبداً. نقاط GPS مجهولة وتُحذف خلال 24 ساعة. خرائطنا من OpenStreetMap على خوادمنا الخاصة، بدون Google أو Apple. اقرأ <a href="{L("privacy")}">سياسة الخصوصية</a>.',
                ]),
            ],
            "faq_title": "أسئلة شائعة",
            "faq": [
                ("هل سيتم حظر تطبيق ويز في العراق؟", "نعم. أعلن وزير الاتصالات مصطفى سند حظر تطبيق ويز في العراق، والموعد المعلن نهاية كانون الأول 2026."),
                ("متى يبدأ حظر ويز في العراق؟", "كان الموعد مطلع 2027، ثم قُدّم إلى نهاية كانون الأول 2026، بحسب ما نقلته وسائل الإعلام عن الوزير."),
                ("ما هو بديل ويز في العراق؟", "مسار تطبيق ملاحة عراقي فيه ما تحتاجه من ويز: زحمة مباشرة وبلاغات الطريق وإرشاد صوتي، بالعربي والكوردي والإنكليزي."),
                ("هل مسار تطبيق عراقي؟", "نعم. مسار تطبيق عراقي، خرائطه من OpenStreetMap على خوادمه الخاصة، ولا يعتمد على ويز أو خرائط Google."),
                ("متى يتوفر مسار؟", "قريباً على App Store و Google Play. تابعنا على masarmaps.com."),
                ("هل أحتاج حساباً لاستخدام مسار؟", "لا. تستطيع البحث والملاحة ونشر البلاغات بدون حساب."),
            ],
        }
    if lang == "en":
        return {
            "nav": "Waze alternative",
            "seo_title": "Waze alternative in Iraq: Masar, the Iraqi navigation app",
            "description": "Iraq is banning Waze. Masar is an Iraqi navigation app with live traffic, road reports and voice guidance in Arabic, Kurdish and English. Coming soon to the App Store and Google Play.",
            "title": "The Waze alternative for Iraq",
            "lead": "Masar is an Iraqi navigation app, made for Iraq. Coming soon to the App Store and Google Play.",
            "sections": [
                ("Iraq's Waze ban", [
                    "In October 2026, Iraq's Communications Minister Mustafa Sanad announced a ban on the Waze app in Iraq, citing the app's Israeli origin. The ban was first set for the start of 2027, then brought forward to the end of December 2026, according to press reports.",
                    ("raw", sources_line("Sources")),
                ]),
                ("Masar: an Iraqi alternative to Waze", [("ul", [
                    "Live traffic on the roads, updated every minute.",
                    "Turn-by-turn voice guidance, with automatic rerouting if you leave the route.",
                    "Driver reports: accidents, traffic, closed roads, floods, speed bumps and more.",
                    "Search in Arabic, Kurdish and English, even Arabic typed in Latin letters.",
                    "Share your arrival time on WhatsApp and Telegram.",
                    "Works with CarPlay and Android Auto.",
                    "No ads, no account needed.",
                ])]),
                ("Privacy first", [
                    f'We never sell your data. GPS points are anonymous and deleted within 24 hours. Our maps come from OpenStreetMap on our own servers, without Google or Apple. Read our <a href="{L("privacy")}">Privacy Policy</a>.',
                ]),
            ],
            "faq_title": "Questions",
            "faq": [
                ("Is Waze being banned in Iraq?", "Yes. Communications Minister Mustafa Sanad announced a ban on Waze in Iraq. The announced date is the end of December 2026."),
                ("When does the Waze ban start in Iraq?", "It was first set for the start of 2027, then brought forward to the end of December 2026, according to press reports quoting the minister."),
                ("What is the alternative to Waze in Iraq?", "Masar is an Iraqi navigation app with what you use Waze for: live traffic, road reports and voice guidance, in Arabic, Kurdish and English."),
                ("Is Masar an Iraqi app?", "Yes. Masar is an Iraqi app. Its maps come from OpenStreetMap on its own servers, and it does not depend on Waze or Google Maps."),
                ("When is Masar available?", "Coming soon to the App Store and Google Play. Follow masarmaps.com."),
                ("Do I need an account to use Masar?", "No. You can search, navigate and post reports without an account."),
            ],
        }
    return {
        "nav": "جێگرەوەی ویز",
        "seo_title": "جێگرەوەی ویز لە عێراق: مسار، ئەپی ڕێنیشاندەری عێراقی",
        "description": "دوای بڕیاری قەدەغەکردنی ویز لە عێراق، مسار ئەپێکی ڕێنیشاندەری عێراقییە بە قەرەباڵغی ڕاستەوخۆ، ڕاپۆرتی ڕێگا و ڕێنمایی دەنگی بە کوردی و عەرەبی. بەم زووانە لە App Store و Google Play.",
        "title": "جێگرەوەی ویز لە عێراق",
        "lead": "مسار ئەپێکی ڕێنیشاندەری عێراقییە، بۆ عێراق دروستکراوە. بەم زووانە لە App Store و Google Play.",
        "sections": [
            ("قەدەغەکردنی ویز لە عێراق", [
                "لە تشرینی یەکەمی 2026دا، وەزیری پەیوەندییەکانی عێراق مستەفا سەند قەدەغەکردنی ئەپی ویز (Waze)ی لە عێراق ڕاگەیاند، و گوتی هۆکارەکەی ئەوەیە کە ئەپەکە بنەچەی ئیسرائیلییە. سەرەتا بۆ سەرەتای 2027 دیاری کرا، پاشان بۆ کۆتایی کانوونی یەکەمی 2026 پێشخرا، بەپێی ڕاپۆرتە ڕۆژنامەوانییەکان.",
                ("raw", sources_line("سەرچاوەکان")),
            ]),
            ("مسار: جێگرەوەیەکی عێراقی بۆ ویز", [("ul", [
                "قەرەباڵغی ڕاستەوخۆ لەسەر ڕێگاکان، هەر خولەکێک نوێ دەبێتەوە.",
                "ڕێنمایی دەنگی هەنگاو بە هەنگاو، و گۆڕینی ڕێگا بە خۆکار ئەگەر لە ڕێگاکە دەرچوویت.",
                "ڕاپۆرتی شۆفێران: ڕووداو، قەرەباڵغی، ڕێگای داخراو، لافاو، بەربەستی خێرایی و زیاتر.",
                "گەڕان بە کوردی و عەرەبی و ئینگلیزی.",
                "هاوبەشکردنی کاتی گەیشتن لە واتسئاپ و تێلێگرام.",
                "لەگەڵ CarPlay و Android Auto کار دەکات.",
                "بێ ڕیکلام، بێ هەژمار.",
            ])]),
            ("تایبەتمەندیت لە پێشەوەیە", [
                f'هەرگیز زانیارییەکانت نافرۆشین. خاڵەکانی GPS بێناون و لە ماوەی 24 کاتژمێردا دەسڕدرێنەوە. نەخشەکانمان لە OpenStreetMapەوەن لەسەر سێرڤەرەکانی خۆمان، بەبێ Google یان Apple. <a href="{L("privacy")}">سیاسەتی تایبەتمەندی</a> بخوێنەوە.',
            ]),
        ],
        "faq_title": "پرسیارە باوەکان",
        "faq": [
            ("ئایا ویز لە عێراق قەدەغە دەکرێت؟", "بەڵێ. وەزیری پەیوەندییەکان مستەفا سەند قەدەغەکردنی ویزی لە عێراق ڕاگەیاند. بەرواری ڕاگەیەندراو کۆتایی کانوونی یەکەمی 2026یە."),
            ("قەدەغەکردنی ویز لە عێراق کەی دەست پێدەکات؟", "سەرەتا بۆ سەرەتای 2027 بوو، پاشان بۆ کۆتایی کانوونی یەکەمی 2026 پێشخرا، بەپێی ڕاپۆرتەکان."),
            ("جێگرەوەی ویز لە عێراق چییە؟", "مسار ئەپێکی ڕێنیشاندەری عێراقییە بە قەرەباڵغی ڕاستەوخۆ، ڕاپۆرتی ڕێگا و ڕێنمایی دەنگی، بە کوردی و عەرەبی و ئینگلیزی."),
            ("ئایا مسار ئەپێکی عێراقییە؟", "بەڵێ. مسار ئەپێکی عێراقییە، نەخشەکانی لە OpenStreetMapەوەن لەسەر سێرڤەرەکانی خۆی، و پشت بە ویز یان نەخشەی Google نابەستێت."),
            ("مسار کەی بەردەست دەبێت؟", "بەم زووانە لە App Store و Google Play. masarmaps.com بەدوادا بچۆ."),
            ("پێویستم بە هەژمار هەیە بۆ بەکارهێنانی مسار؟", "نەخێر. دەتوانیت بەبێ هەژمار بگەڕێیت، ڕێنیشاندەر بەکاربهێنیت و ڕاپۆرت بنێریت."),
        ],
    }


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

LANDING = "waze-alternative"
ALL_PAGES = [LANDING] + PAGES
OG_IMAGE = ORIGIN + "/assets/og-image.png"
LOGO_PNG = ORIGIN + "/assets/masar-logo-512.png"
OG_LOCALE = {"ar": "ar_IQ", "en": "en_US", "ckb": "ckb_IQ"}
APP_NAME = {"ar": "مسار", "en": "Masar", "ckb": "مسار"}


def page_content(lang):
    c = content(lang)
    lp = landing(lang)
    c["nav"] = {LANDING: lp["nav"], **c["nav"]}
    c[LANDING] = lp
    return c


def organization():
    return {
        "@type": "Organization",
        "@id": ORIGIN + "/#org",
        "name": "Masar Maps",
        "alternateName": ["مسار", "Masar"],
        "url": ORIGIN + "/",
        "logo": LOGO_PNG,
        "email": EMAIL,
    }


def mobile_app(lang, description):
    return {
        "@type": "MobileApplication",
        "@id": ORIGIN + "/#app",
        "name": APP_NAME[lang],
        "alternateName": ["Masar", "مسار", "Masar Maps"],
        "operatingSystem": "iOS, Android",
        "applicationCategory": "TravelApplication",
        "description": description,
        "inLanguage": ["ar", "ckb", "en"],
        "areaServed": {"@type": "Country", "name": "Iraq"},
        "publisher": {"@id": ORIGIN + "/#org"},
        "image": OG_IMAGE,
    }


def json_ld(lang, page, p, title, description, canonical):
    import json
    graph = [organization()]
    webpage = {
        "@type": "WebPage",
        "@id": canonical + "#page",
        "url": canonical,
        "name": title,
        "description": description,
        "inLanguage": lang,
        "isPartOf": {"@type": "WebSite", "@id": ORIGIN + "/#site", "url": ORIGIN + "/", "name": "Masar Maps"},
        "publisher": {"@id": ORIGIN + "/#org"},
    }
    if page == LANDING:
        webpage["about"] = {"@id": ORIGIN + "/#app"}
        graph.append(mobile_app(lang, description))
        graph.append({
            "@type": "FAQPage",
            "@id": canonical + "#faq",
            "inLanguage": lang,
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in p["faq"]
            ],
        })
    graph.insert(0, webpage)
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f'  <script type="application/ld+json">\n{data}\n  </script>'


def render(lang, page):
    meta = LANGS[lang]
    c = page_content(lang)
    p = c[page]
    title = p.get("seo_title") or f"{p['title']} — {meta['brand']}"
    description = p.get("description") or p["lead"]
    canonical = ORIGIN + url(lang, page)
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{l}" href="{ORIGIN + url(l, page)}">' for l in LANGS
    ) + f'\n  <link rel="alternate" hreflang="x-default" href="{ORIGIN + url("ar", page)}">'
    og_alt = "\n".join(
        f'  <meta property="og:locale:alternate" content="{OG_LOCALE[l]}">' for l in LANGS if l != lang
    )
    langs = "".join(
        f'<a href="{url(l, page)}" lang="{l}" hreflang="{l}"'
        + (' aria-current="page"' if l == lang else "")
        + f">{LANGS[l]['label']}</a>"
        for l in LANGS
    )
    blocks_html = []
    for h, blocks in p["sections"]:
        blocks_html.append(
            f"      <section>\n        <h2>{h}</h2>\n        "
            + "\n        ".join(b[1] if isinstance(b, tuple) and b[0] == "raw" else render_block(b) for b in blocks)
            + "\n      </section>"
        )
    if "faq" in p:
        faq = "\n        ".join(f"<h3>{q}</h3>\n        <p>{a}</p>" for q, a in p["faq"])
        blocks_html.append(f"      <section>\n        <h2>{p['faq_title']}</h2>\n        {faq}\n      </section>")
    sections = "\n".join(blocks_html)
    show_date = page in ("privacy", "terms")
    date = f'\n      <p class="date">{c["effective"]}</p>' if show_date else ""
    footer_links = "".join(
        f'<a href="{url(lang, pg)}"' + (' aria-current="page"' if pg == page else "") + f">{c['nav'][pg]}</a>"
        for pg in ALL_PAGES
    )
    return f"""<!doctype html>
<html lang="{lang}" dir="{meta['dir']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#31C6F7">
  <meta name="color-scheme" content="light">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{canonical}">
{alternates}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Masar Maps">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="{OG_LOCALE[lang]}">
{og_alt}
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="/assets/masar-logo.svg">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/{'Vazirmatn-Regular' if lang == 'ckb' else 'ReadexPro-Regular'}.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/pages.css">
{json_ld(lang, page, p, title, description, canonical)}
</head>
<body>
  <header>
    <div class="wrap">
      <a class="brand" href="/" aria-label="{c['home']}"><img src="/assets/masar-logo.svg" alt="" width="40" height="40"><span>{meta['brand']}</span></a>
      <nav class="langs" aria-label="Language">{langs}</nav>
    </div>
  </header>
  <main class="wrap">
    <article class="card">
      <h1>{p['title']}</h1>
      <p class="lead">{p['lead']}</p>{date}
{sections}
    </article>
  </main>
  <footer class="wrap">
    <nav aria-label="{c['nav']['support']}">{footer_links}</nav>
    <p>{c['osm']} · <bdi>masarmaps.com</bdi></p>
  </footer>
</body>
</html>
"""


# --------------------------------------------------------------------------
# robots.txt, sitemap.xml and .well-known
# --------------------------------------------------------------------------

LASTMOD = "2026-10-12"

# Fill these when the store accounts exist, then rebuild:
#   APPLE_TEAM_ID  — Apple Developer → Membership → Team ID (10 chars).
#   ANDROID_SHA256 — Play Console → App integrity → App signing key certificate
#                    → SHA-256 (add the upload key too for local release builds).
APPLE_TEAM_ID = ""
ANDROID_SHA256 = []
BUNDLE_ID = "com.masarmaps"


def write_seo_files():
    import json
    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://masarmaps.com/sitemap.xml\n", encoding="utf-8"
    )
    urls = [("/", "1.0")] + [
        (url(l, pg), "0.9" if pg == LANDING else "0.5") for pg in ALL_PAGES for l in LANGS
    ]
    entries = []
    for loc, prio in urls:
        alts = ""
        page = loc.rsplit("/", 1)[-1]
        if page in ALL_PAGES:
            alts = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{ORIGIN + url(l, page)}"/>' for l in LANGS
            ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN + url("ar", page)}"/>'
        entries.append(
            f"  <url>\n    <loc>{ORIGIN + loc}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n    <priority>{prio}</priority>{alts}\n  </url>"
        )
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries) + "\n</urlset>\n",
        encoding="utf-8",
    )

    wk = SITE / ".well-known"
    wk.mkdir(exist_ok=True)
    # Android App Links / Credential Manager. Empty fingerprints = no association yet.
    assetlinks = [{
        "relation": ["delegate_permission/common.handle_all_urls", "delegate_permission/common.get_login_creds"],
        "target": {"namespace": "android_app", "package_name": BUNDLE_ID, "sha256_cert_fingerprints": ANDROID_SHA256},
    }]
    (wk / "assetlinks.json").write_text(json.dumps(assetlinks, indent=2) + "\n", encoding="utf-8")
    # iOS associated domains. No paths open the app yet, so web pages always stay on the web.
    app_ids = [f"{APPLE_TEAM_ID}.{BUNDLE_ID}"] if APPLE_TEAM_ID else []
    aasa = {
        "applinks": {"details": [{"appIDs": app_ids, "components": []}] if app_ids else []},
        "webcredentials": {"apps": app_ids},
    }
    (wk / "apple-app-site-association").write_text(json.dumps(aasa, indent=2) + "\n", encoding="utf-8")
    if not APPLE_TEAM_ID or not ANDROID_SHA256:
        print("note: .well-known files have no app ids yet (set APPLE_TEAM_ID / ANDROID_SHA256)")


def main():
    for lang, meta in LANGS.items():
        out_dir = SITE / meta["prefix"].lstrip("/") if meta["prefix"] else SITE
        out_dir.mkdir(parents=True, exist_ok=True)
        for page in ALL_PAGES:
            (out_dir / f"{page}.html").write_text(render(lang, page), encoding="utf-8")
            print("wrote", (out_dir / f"{page}.html").relative_to(SITE.parent))
    write_seo_files()
    print("wrote robots.txt, sitemap.xml, .well-known/")


if __name__ == "__main__":
    main()
