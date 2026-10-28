from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import sys
out=sys.argv[1]
jobs=[('/tmp/claude-0/dl-giza/giza.jpg',(270,185,1270,810),0.82,'branch-haram'),
      ('/tmp/claude-0/dl-helwan/helwan.jpg',(110,215,1530,1102),0.8,'branch-helwan'),
      ('/tmp/claude-0/dl-mar/mar.jpg',(40,60,1540,997),1.0,'branch-mariouteya')]
for src,box,g,name in jobs:
    im=Image.open(src).convert('RGB').crop(box)
    im=ImageOps.autocontrast(im,cutoff=0.6)
    if g!=1.0:
        lut=[int(255*((i/255)**g)) for i in range(256)]*3; im=im.point(lut)
    im=ImageEnhance.Color(im).enhance(1.12); im=ImageEnhance.Contrast(im).enhance(1.05)
    im=im.resize((1200,int(1200*im.size[1]/im.size[0])),Image.LANCZOS)
    im=im.filter(ImageFilter.UnsharpMask(radius=1.2,percent=60,threshold=3))
    im.save(f'{out}/{name}.webp',quality=80); print(name,im.size)
