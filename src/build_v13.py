"""Build ../v13/index.html from v13.html + products.json. Run: python3 src/build_v13.py"""
import pathlib
here = pathlib.Path(__file__).parent
s = (here / "v13.html").read_text(encoding="utf-8")
s = s.replace("__DATA__", (here / "products.json").read_text(encoding="utf-8").strip())
(here.parent / "v13" / "index.html").write_text(s, encoding="utf-8")
print("ok", len(s))
