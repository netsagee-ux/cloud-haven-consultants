"""Build the enamel colour map from public-domain Natural Earth 1:110m coastlines.
Pass land-110m.json (and optionally countries-110m.json) from world-atlas 2.0.2.
"""
from pathlib import Path
import json
import sys
from PIL import Image, ImageDraw, ImageFont

W,H=4096,2048
def px(lon,lat):return ((lon+180)*W/360,(90-lat)*H/180)
def geometries(path):
    data=json.loads(Path(path).read_text())
    tr=data['transform']
    arcs=[]
    for source in data['arcs']:
        x=y=0
        arc=[]
        for dx,dy in source:
            x+=dx;y+=dy
            arc.append(px(tr['translate'][0]+x*tr['scale'][0],tr['translate'][1]+y*tr['scale'][1]))
        arcs.append(arc)
    polys=[]
    for obj in next(iter(data['objects'].values()))['geometries']:
        for poly in (obj['arcs'] if obj['type']=='MultiPolygon' else [obj['arcs']]):
            rings=[]
            for ring in poly:
                coords=[]
                for it in ring:
                    pts=arcs[it] if it>=0 else arcs[~it][::-1]
                    coords.extend(pts if not coords else pts[1:])
                rings.append(coords)
            polys.append(rings)
    return polys

base=Image.new('RGB',(W,H),(24,63,63))
land=Image.new('L',(W,H),0)
d=ImageDraw.Draw(land)
polys=geometries(sys.argv[1])
for rings in polys:
    for i,ring in enumerate(rings):
        d.polygon(ring,fill=255 if i==0 else 0)
base.paste((181,191,165),(0,0,W,H),land)
d=ImageDraw.Draw(base)
for rings in polys:
    for ring in rings:
        d.line(ring,(147,175,161),width=2)
if len(sys.argv)>2:
    for rings in geometries(sys.argv[2]):
        for ring in rings:
            d.line(ring,(138,158,143),width=1)
grid=Image.new('RGBA',(W,H))
g=ImageDraw.Draw(grid)
for lon in range(-180,181,10):
    x=px(lon,0)[0]; g.line([(x,0),(x,H)],fill=(200,216,192,75 if lon%30==0 else 33),width=2)
for lat in range(-80,81,10):
    y=px(0,lat)[1];g.line([(0,y),(W,y)],fill=(203,218,197,72 if lat%30==0 else 35),width=3 if lat==0 else 2)
for lat in (-23.45,23.45):
    y=px(0,lat)[1]
    for x in range(0,W,20):g.line([(x,y),(x+10,y)],fill=(203,218,197,70),width=2)
base=Image.alpha_composite(base.convert('RGBA'),grid)
d=ImageDraw.Draw(base)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
for label,x,y,c in [('EUROPE',26,51,'#50695e'),('AFRICA',17,-3,'#50695e'),('ASIA',92,51,'#50695e'),('INDIAN OCEAN',73,-20,'#9aafa1'),('PACIFIC OCEAN',-144,-2,'#9aafa1'),('ATLANTIC OCEAN',-36,16,'#9aafa1'),('AUSTRALIA',133,-25,'#50695e'),('NORTH AMERICA',-99,48,'#50695e'),('SOUTH AMERICA',-61,-13,'#50695e')]:
    d.text(px(x,y),' '.join(label),font=font,fill=c,anchor='mm')
base.resize((2048,1024),Image.Resampling.LANCZOS).convert('RGB').save(Path(__file__).with_name('globe-enamel.jpg'),quality=88,subsampling=0,optimize=True)
