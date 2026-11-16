"""Build ../v12/index.html: v11 store (store.tpl.html + products.json) with a
Riverstone-style editorial layer (full-bleed photo hero + visit booking,
airy serif headings, image band, calm About + branches). v11 stays untouched.
Run: python3 src/build_v12.py  (after build.py if the store template changed)."""
import pathlib, re

here = pathlib.Path(__file__).parent
s = (here / "store.tpl.html").read_text(encoding="utf-8")
s = s.replace("__DATA__", (here / "products.json").read_text(encoding="utf-8").strip())
s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
# shared v11 images live one level up
s = re.sub(r'(?<![\w./])img/', '../img/', s)


def cut(src, start, end, new):
    i = src.index(start)
    j = src.index(end, i) + len(end)
    return src[:i] + new + src[j:]


def swap(src, old, new):
    assert old in src, old[:60]
    return src.replace(old, new, 1)


s = swap(s, '<link rel="preload" as="image" href="../img/x-carrera-room-lg.webp">',
         '<link rel="preload" as="image" href="img/hero-terrace.webp" media="(min-width:821px)">\n'
         '<link rel="preload" as="image" href="img/hero-terrace-sm.webp" media="(max-width:820px)">')
s = swap(s, "family=Readex+Pro:wght@300;400;500;600&",
         "family=Readex+Pro:wght@300;400;500;600&family=Noto+Naskh+Arabic:wght@500;600&")

HERO = """<section class="rv-hero" aria-labelledby="h-hero">
  <picture>
    <source media="(max-width:820px)" srcset="img/hero-terrace-sm.webp">
    <img src="img/hero-terrace.webp" alt="تراس بأرضية بورسلين رمادي فاتح وإطلالة على المدينة" width="1920" height="1075" fetchpriority="high">
  </picture>
  <div class="wrap rv-in">
    <p class="rv-k">سيراميك · بورسلين · أدوات صحية</p>
    <h1 id="h-hero">مساحات هادية،<br>بخامات تعيش معاك.</h1>
    <p class="rv-sub">وكلاء وموزعين لكبرى الشركات المحلية والمستوردة. اتفرّج على اللون والملمس والمقاس بعينك في أي معرض من معارضنا التلاتة.</p>
    <div class="rv-cta"><a class="rv-b solid" href="#visit">احجز زيارة للمعرض</a><a class="rv-b ghost" href="#tiles">تسوّق الآن</a></div>
  </div>
  <div class="wrap rv-bk-wrap">
    <form class="rv-bk" id="visit" aria-label="احجز زيارة خاصة للمعرض">
      <label>الفرع<select id="vBr"><option>الهرم، الطالبية</option><option>المريوطية</option><option>المعادي حلوان (المعصرة)</option></select></label>
      <label>اليوم<select id="vDay"></select></label>
      <label>الوقت<select id="vTime"><option>الصبح (١٠:٣٠ – ١ ظ)</option><option>بعد الضهر (١ – ٥ م)</option><option selected>بالليل (٥ – ١٠:٣٠ م)</option></select></label>
      <button type="submit">احجز على واتساب</button>
    </form>
    <p class="rv-note">بنرتّب لك زيارة مع مهندس المعرض، ونجهّز العينات اللي سألت عليها قبل ما توصل.</p>
  </div>
</section>

<section class="rv-intro wrap" aria-label="عن معارض الرضوان">
  <p class="rv-big">من الطالبية للمعصرة، <span>٣ معارض</span> بتعرض أكبر الماركات، عشان تختار الأرضية والحمام والمطبخ وانت شايفهم قدامك، مش من صورة.</p>
  <div class="brands rv-brands"><span>Cleopatra</span><span>GROHE</span><span>DURAVIT</span><span>Ideal Standard</span><span>Red Sea</span><span>ALPHA</span><span>Infinity</span></div>
</section>

<main class="wrap">
  <div class="hero">"""
s = swap(s, '<main class="wrap">\n  <div class="hero">', HERO)

# old hero left column: becomes a search block (keeps hform/hq/chips for JS)
s = cut(s, '<p class="rate">', '</h1>',
        '<p class="kicker">ابدأ من هنا</p>\n      <h2 class="rv-h2" style="margin-top:8px">دوّر على اللي في بالك</h2>')
# remove the old feature duo + wide banner (the hero replaces them)
s = cut(s, '<div class="duo">', '</a>\n  </div>', '')
s = cut(s, '<a class="bn wide"', '</div>\n  </a>', '')

BAND = """<section class="rv-band" aria-labelledby="h-band">
    <picture><source media="(max-width:820px)" srcset="img/band-bath-sm.webp"><img src="img/band-bath.webp" alt="حمام بحوائط رخام فاتح وبانيو قائم ومراية مضيئة" width="1920" height="1072" loading="lazy"></picture>
    <div class="rv-band-tx"><p class="rv-k">الحمامات</p><h2 id="h-band">الهدوء بيبان<br>في التفاصيل.</h2><a class="rv-b solid" href="#bath">أدوات صحية وخلاطات</a></div>
  </section>

  <section id="bath\""""
s = swap(s, '<section id="bath"', BAND)

# drop the old brands strip (moved to the intro) and the old about box
s = cut(s, '<section aria-label="الماركات">', '</section>', '')
s = cut(s, '<section class="about"', '</section>', '')

ABOUT = """<section class="rv-about" aria-labelledby="h-about">
    <div class="rv-about-img"><img src="img/about-ivory.webp" alt="حمام بأرضية بورسلين عاجي وحوض من الخشب" width="1200" height="672" loading="lazy"></div>
    <div class="rv-about-tx">
      <p class="rv-k">عن الرضوان</p>
      <h2 id="h-about">خبرة المعرض،<br>وسهولة الأونلاين.</h2>
      <p>الرضوان للسيراميك والبورسلين والأدوات الصحية، وكلاء وموزعين لكبرى الشركات المحلية والمستوردة. بنبيع سيراميك وبورسلين وأطقم حمامات وخلاطات وبانيوهات وأحواض مطبخ من كليوباترا وجروهي وديورافيت وأيديال ستاندرد، وبنخدم الجيزة و٦ أكتوبر والقاهرة وحلوان.</p>
      <dl class="rv-stats">
        <div><dt>٣</dt><dd>معارض في الجيزة وحلوان</dd></div>
        <div><dt>١٣١ ألف</dt><dd>متابع على فيسبوك</dd></div>
        <div><dt>١٠٠٪</dt><dd>بيرشّحونا من ٧٨٠ تقييم</dd></div>
        <div><dt>٧+</dt><dd>ماركات محلية ومستوردة</dd></div>
      </dl>
    </div>
  </section>

  <section id="branches\""""
s = swap(s, '<section id="branches"', ABOUT)
s = cut(s, '<div class="stats">', '</div>\n    </div>', '')
s = swap(s, '<h2 id="h-br">اتفرّج على الطبيعة في معارضنا</h2>', '<p class="rv-k">المعارض</p><h2 id="h-br">اتفرّج على الطبيعة،<br>في أقرب معرض ليك.</h2>')

CSS = """
/* ===== v12: Riverstone-style editorial layer ===== */
:root{--serif:"Noto Naskh Arabic","Readex Pro",serif}
section{padding-block:104px 0}
.sh{margin-bottom:36px}
.sh h2,.rv-h2{font-family:var(--serif);font-weight:500;font-size:clamp(28px,3.4vw,46px);line-height:1.35}
.sh p{font-size:15px;margin-top:8px}
.rv-k{font-size:13px;letter-spacing:.02em;color:var(--accent);font-weight:500}
.rv-b{display:inline-flex;align-items:center;justify-content:center;height:52px;padding:0 28px;border-radius:999px;font-weight:500;font-size:15px;transition:background .25s,color .25s}
.rv-b.solid{background:var(--accent);color:#fff}.rv-b.solid:hover{background:#5b1f75}
.rv-b.ghost{background:rgba(255,255,255,.16);color:#fff;border:1px solid rgba(255,255,255,.55);backdrop-filter:blur(6px)}.rv-b.ghost:hover{background:#fff;color:var(--ink)}
.rv-hero{position:relative;min-height:max(560px,calc(100svh - 190px));max-height:860px;display:flex;flex-direction:column;justify-content:flex-end;padding:0;color:#fff;overflow:hidden;margin:16px max(16px,env(safe-area-inset-left,0px)) 0;border-radius:calc(var(--r) + 10px)}
.rv-hero picture,.rv-hero picture img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.rv-hero picture img{animation:rvz 18s ease-out both}
@keyframes rvz{from{transform:scale(1.08)}to{transform:scale(1)}}
.rv-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,14,24,.05) 30%,rgba(20,14,24,.62) 100%),linear-gradient(270deg,rgba(20,14,24,.35),transparent 60%)}
.rv-in,.rv-bk-wrap{position:relative;z-index:1;width:100%;box-sizing:border-box}
.rv-in{padding-top:96px;padding-inline:clamp(20px,5vw,72px)}
.rv-hero .rv-k{color:rgba(255,255,255,.85)}
.rv-hero h1{font-family:var(--serif);font-weight:500;font-size:clamp(38px,6vw,84px);line-height:1.25;margin-top:14px;text-shadow:0 2px 30px rgba(0,0,0,.25)}
.rv-sub{max-width:52ch;margin-top:18px;font-size:clamp(15px,1.3vw,18px);color:rgba(255,255,255,.9)}
.rv-cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.rv-bk-wrap{padding:40px clamp(20px,5vw,72px) clamp(20px,3vw,36px)}
.rv-bk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) auto;gap:8px;align-items:end;background:rgba(255,255,255,.94);color:var(--ink);border-radius:22px;padding:10px;backdrop-filter:blur(10px);box-shadow:0 20px 60px -30px rgba(0,0,0,.5)}
.rv-bk label{display:flex;flex-direction:column;font-size:12px;color:var(--muted);padding:8px 14px;border-radius:14px;background:var(--stone)}
.rv-bk select{border:0;background:transparent;font:500 15px var(--body);color:var(--ink);padding:4px 0 2px;margin-inline-start:-2px;cursor:pointer}
.rv-bk select:focus{outline:none}
.rv-bk button{height:58px;padding:0 30px;border:0;border-radius:16px;background:var(--accent);color:#fff;font-weight:500;font-size:15px;cursor:pointer}
.rv-bk button:hover{background:#5b1f75}
.rv-note{font-size:13px;color:rgba(255,255,255,.85);margin-top:12px}
.rv-intro{padding-block:120px 8px;text-align:center}
.rv-big{font-family:var(--serif);font-weight:500;font-size:clamp(24px,3vw,40px);line-height:1.6;max-width:30ch;margin-inline:auto;color:var(--ink)}
.rv-big span{color:var(--accent)}
.rv-brands{margin-top:56px;border:0;justify-content:center}
.hero{padding-block:104px 0;align-items:center}
.rv-band{position:relative;margin-top:104px;padding:0;min-height:560px;border-radius:calc(var(--r) + 10px);overflow:hidden;display:flex;align-items:flex-end}
.rv-band picture,.rv-band img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.rv-band::after{content:"";position:absolute;inset:0;background:linear-gradient(270deg,rgba(20,14,24,.55),transparent 65%)}
.rv-band-tx{position:relative;z-index:1;color:#fff;padding:clamp(24px,5vw,64px)}
.rv-band-tx .rv-k{color:rgba(255,255,255,.85)}
.rv-band h2{font-family:var(--serif);font-weight:500;font-size:clamp(30px,4.4vw,60px);line-height:1.3;margin:10px 0 26px}
.rv-about{display:grid;grid-template-columns:1.1fr 1fr;gap:clamp(32px,6vw,96px);align-items:center}
.rv-about-img{border-radius:calc(var(--r) + 10px);overflow:hidden;aspect-ratio:4/5}
.rv-about-img img{width:100%;height:100%;object-fit:cover;object-position:35% 50%}
.rv-about h2{font-family:var(--serif);font-weight:500;font-size:clamp(30px,3.6vw,50px);line-height:1.35;margin:12px 0 22px}
.rv-about-tx>p:not(.rv-k){color:var(--muted);font-size:16px;line-height:1.95;max-width:52ch}
.rv-stats{display:grid;grid-template-columns:1fr 1fr;margin:40px 0 0;border-top:1px solid var(--line)}
.rv-stats div{padding:22px 0;border-bottom:1px solid var(--line)}
.rv-stats div:nth-child(odd){padding-inline-end:20px;border-inline-end:1px solid var(--line)}
.rv-stats div:nth-child(even){padding-inline-start:24px}
.rv-stats dt{font-family:var(--serif);font-size:clamp(30px,3vw,42px);color:var(--accent);line-height:1.2}
.rv-stats dd{margin:4px 0 0;font-size:13.5px;color:var(--muted)}
#branches .bc{border:0;background:var(--stone)}
@media (max-width:900px){
  section{padding-block:72px 0}
  .rv-hero{min-height:0;margin-top:10px}
  .rv-in{padding-top:96px}
  .rv-bk{grid-template-columns:1fr 1fr}
  .rv-bk label:first-child{grid-column:1/-1}
  .rv-bk button{grid-column:1/-1;height:52px}
  .rv-bk-wrap{padding-top:28px}
  .rv-intro{padding-block:80px 0}
  .rv-brands{margin-top:36px}
  .hero{padding-block:72px 0}
  .rv-band{min-height:440px;margin-top:72px}
  .rv-about{grid-template-columns:1fr}
  .rv-about-img{aspect-ratio:4/3}
}
@media (prefers-reduced-motion:reduce){.rv-hero picture img{animation:none}}
"""
s = swap(s, "</style>", CSS + "</style>")

JS = """
// v12: visit booking -> prefilled WhatsApp message
(()=>{const d=document.getElementById("vDay"),N=["الأحد","الاتنين","التلات","الأربع","الخميس","الجمعة","السبت"],t=new Date();
for(let i=0;i<7;i++){const x=new Date(t);x.setDate(t.getDate()+i);const o=document.createElement("option");
o.textContent=i===0?"النهارده":i===1?"بكرة":`${N[x.getDay()]} ${x.getDate().toLocaleString("ar-EG")}/${(x.getMonth()+1).toLocaleString("ar-EG")}`;d.append(o)}
document.getElementById("visit").addEventListener("submit",e=>{e.preventDefault();
const m=`السلام عليكم، عايز أحجز زيارة لمعرض الرضوان.\\nالفرع: ${vBr.value}\\nاليوم: ${vDay.value}\\nالوقت: ${vTime.value}`;
window.open("https://wa.me/201007559300?text="+encodeURIComponent(m),"_blank","noopener")})})();
</script>"""
k = s.rindex("</script>")
s = s[:k] + JS + s[k + len("</script>"):]

head = ('<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="description" content="الرضوان للسيراميك والبورسلين والأدوات الصحية: ٣ معارض في الهرم والمريوطية وحلوان. احجز زيارة للمعرض أو تسوّق أونلاين.">\n'
        '<link rel="icon" href="../img/logo.png">\n')
i = s.index("</style>") + len("</style>")
s = head + s[:i] + "\n<style>html,body{margin:0}img{max-width:100%}</style>\n</head>\n<body>\n" + s[i:] + "\n</body>\n</html>\n"
out = here.parent / "v12" / "index.html"
out.write_text(s, encoding="utf-8")
print("wrote", out, len(s))
