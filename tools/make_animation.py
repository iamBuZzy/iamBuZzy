#!/usr/bin/env python3
"""Generate a GitHub-ready animated cyber HUD banner from the supplied base art.

Dependencies: pip install pillow
Usage: python tools/make_animation.py

The banner base is assets/profile-scan-source.png. If changing your name/details,
edit or replace that base image before regenerating the animation.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets'
BASE = ASSETS / 'profile-scan-source.png'
STILL = ASSETS / 'profile-scan.png'
OUTPUT = ASSETS / 'profile-scan.gif'

# 1200 px stays detailed but remains light enough for GitHub.
WIDTH = 1120
FRAME_COUNT = 28
DURATION_MS = 105

src = Image.open(BASE).convert('RGB')
h = round(src.height * WIDTH / src.width)
base = src.resize((WIDTH, h), Image.Resampling.LANCZOS)
base.save(STILL, optimize=True)

# Repeated overlays are generated at output resolution to save space.
frames=[]
for i in range(FRAME_COUNT):
    t=i/FRAME_COUNT
    frame=base.copy().convert('RGBA')
    # Soft, gently-moving holographic scanner across the ASCII identity panel.
    x=round(42 + (515-42)*t)
    y0,y1=58,h-35
    glow=Image.new('RGBA', (WIDTH,h),(0,0,0,0))
    gd=ImageDraw.Draw(glow,'RGBA')
    gd.rectangle([x-4,y0,x+4,y1],fill=(4,255,216,75))
    glow=glow.filter(ImageFilter.GaussianBlur(12))
    frame=Image.alpha_composite(frame,glow)
    scan=Image.new('RGBA',(WIDTH,h),(0,0,0,0))
    sd=ImageDraw.Draw(scan,'RGBA')
    for delta in range(-32,33):
        strength=max(0,1-abs(delta)/33)
        alpha=int((3+20*strength**2)*strength)
        sd.line([(x+delta,y0),(x+delta,y1)],fill=(0,255,215,alpha),width=1)
    sd.line([(x,y0),(x,y1)],fill=(131,255,240,105),width=2)
    sd.line([(x-2,y0),(x-2,y1)],fill=(2,210,193,45),width=1)
    frame=Image.alpha_composite(frame,scan)
    lights=Image.new('RGBA',(WIDTH,h),(0,0,0,0))
    d=ImageDraw.Draw(lights,'RGBA')
    # Moving light streak at the top border.
    lx=int(270+670*t)
    d.line([(lx,25),(lx+52,25)], fill=(82,255,234,110),width=2)
    # Pulse the HUD's online indicators and segmented loading bars.
    strength=(1+math.sin(2*math.pi*t*2))/2
    a=int(70+145*strength)
    d.ellipse((1048,17,1053,22),fill=(10,255,214,a))
    d.ellipse((1063,17,1068,22),fill=(10,255,214,int(a*.6)))
    d.ellipse((1078,17,1083,22),fill=(10,255,214,int(a*.35)))
    # Loading pulse: underline at bottom-left of the scanner display.
    bar_x=63+int(92*t)
    d.rounded_rectangle([bar_x,h-60,bar_x+9,h-57],radius=1,fill=(70,255,229,145))
    # Tiny digital artifacts; predictable per frame, not random screen noise.
    for k in range(11):
        px=180+((i*17+k*97)%315)
        py=77+((i*7+k*41)%(h-128))
        alpha=25+int(30*(.5+.5*math.sin(i*.4+k)))
        d.point((px,py),fill=(69,255,229,alpha))
    # Blend light sources; draw directly on RGBA would produce dark stripes.
    frame=Image.alpha_composite(frame,lights)
    frames.append(frame.convert('RGB'))

# Shared palette = less visual flickering during GIF animation.
# Quantizing first frame to adaptive palette & reusing yields better consistency.
palette=frames[0].quantize(colors=112,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
indexed[0].save(OUTPUT,save_all=True,append_images=indexed[1:],duration=DURATION_MS,
                loop=0,optimize=True,disposal=2)
print(f'Created: {OUTPUT} ({OUTPUT.stat().st_size/1024/1024:.2f} MiB)')
print(f'Created: {STILL} ({STILL.stat().st_size/1024/1024:.2f} MiB)')
