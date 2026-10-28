"""Build ../index.html from store.tpl.html + products.json (standalone, RTL)."""
import pathlib
here = pathlib.Path(__file__).parent
s = (here / "store.tpl.html").read_text(encoding="utf-8")
s = s.replace("__DATA__", (here / "products.json").read_text(encoding="utf-8").strip())
s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
head = ('<!doctype html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<meta name="description" content="الرضوان للسيراميك والبورسلين والأدوات الصحية: ٣ معارض في الهرم والمريوطية وحلوان.">\n'
        '<link rel="icon" href="img/logo.png">\n')
i = s.index("</style>") + len("</style>")
s = head + s[:i] + "\n<style>html,body{margin:0}img{max-width:100%}</style>\n</head>\n<body>\n" + s[i:] + "\n</body>\n</html>\n"
(here.parent / "index.html").write_text(s, encoding="utf-8")
