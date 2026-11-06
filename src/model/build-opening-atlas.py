"""Render the opening globe from the same Natural Earth texture as the 3D atlas."""
from math import cos, sin, radians, pi
from pathlib import Path
from PIL import Image

folder = Path(__file__).resolve().parent
with Image.open(folder / 'globe-enamel.jpg') as image:
    texture = image.convert('RGB')
width, height = texture.size
radius = 280
tilt = radians(21)
meridian = 27

def project(lon, lat):
    longitude, latitude = radians(lon - meridian), radians(lat)
    a = cos(latitude) * cos(longitude)
    depth = a * cos(tilt) + sin(latitude) * sin(tilt)
    x = radius * cos(latitude) * sin(longitude)
    y = radius * (a * sin(tilt) - sin(latitude) * cos(tilt))
    return x, y, depth

def visible_line(coordinates):
    path = []
    pen_down = False
    for lon, lat in coordinates:
        x, y, depth = project(lon, lat)
        if depth >= 0:
            path.append(('L' if pen_down else 'M') + f'{x:.1f} {y:.1f}')
        pen_down = depth >= 0
    return ''.join(path)

grid = [visible_line((lon, lat) for lat in range(-90, 91, 2)) for lon in range(-180, 180, 20)]
grid += [visible_line((lon, lat) for lon in range(-180, 181, 2)) for lat in range(-75, 76, 15)]
dots = []
for lat in range(-81, 82, 2):
    count = max(1, round(180 * cos(radians(lat))))
    for i in range(count):
        lon = 360 * ((i + (lat % 4) / 4) % count) / count - 180
        x, y, depth = project(lon, lat)
        px = int((lon + 180) / 360 * width) % width
        py = min(height - 1, int((90 - lat) / 180 * height))
        if depth > 0 and texture.getpixel((px, py))[0] > 123:
            dots.append(f'M{x:.1f} {y:.1f}h.1')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-400 -355 800 710" fill="none">
<defs>
  <radialGradient id="surface" cx="70%" cy="23%" r="85%"><stop stop-color="#263e31"/><stop offset=".54" stop-color="#15291f"/><stop offset="1" stop-color="#0a1512"/></radialGradient>
  <linearGradient id="rim" x2=".9" y2=".6" gradientUnits="objectBoundingBox"><stop stop-color="#3b5040"/><stop offset=".45" stop-color="#b4ab7c"/><stop offset="1" stop-color="#586c52"/></linearGradient>
</defs>
<g transform="rotate(-17)"><ellipse rx="368" ry="108" stroke="#a99e70" stroke-opacity=".64"/><circle r="280" fill="url(#surface)" stroke="url(#rim)" stroke-width="1.6"/>
<path d="{''.join(grid)}" stroke="#9aaf87" stroke-width=".65" opacity=".37"/>
<path d="{''.join(dots)}" stroke="#b2be8b" stroke-linecap="round" stroke-width="2.4" opacity=".89"/>
<path d="M-368 0a368 108 0 0 0 736 0" stroke="#b8aa78" stroke-width="1.35"/>
<circle cx="320" cy="53" r="3" fill="#dfd5a4"/></g></svg>'''
(folder.parents[1] / 'dist/assets/opening-atlas.svg').write_text(svg)
