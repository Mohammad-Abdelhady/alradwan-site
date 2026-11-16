"""Build ../v14/index.html from v14.html + products.json. Run: python3 src/build_v14.py"""
import pathlib
here = pathlib.Path(__file__).parent
s = (here / "v14.html").read_text(encoding="utf-8")
s = s.replace("__DATA__", (here / "products.json").read_text(encoding="utf-8").strip())
(here.parent / "v14" / "index.html").write_text(s, encoding="utf-8")
print("ok", len(s))
