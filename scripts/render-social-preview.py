#!/usr/bin/env python3
"""Render assets/profile-social-preview.png to match profile-social-preview.svg."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
BG_TOP = (13, 17, 23)
BG_BOT = (22, 27, 34)
ACCENT = (111, 59, 228)
ACCENT2 = (34, 211, 238)
PURPLE_TXT = (183, 156, 255)
FG = (240, 246, 252)
MUTED = (139, 148, 158)
DIM = (110, 118, 129)
FAINT = (72, 79, 88)

SANS_B = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/liberation-sans-fonts/LiberationSans-Regular.ttf"
MONO_R = "/usr/share/fonts/liberation-mono-fonts/LiberationMono-Regular.ttf"

img = Image.new("RGB", (W, H), BG_TOP)
d = ImageDraw.Draw(img)

# Diagonal background gradient
for y in range(H):
    t = y / (H - 1)
    d.line(
        [(0, y), (W, y)],
        fill=tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3)),
    )

# Dot grid
for x in range(0, W, 28):
    for y in range(0, H, 28):
        d.ellipse([x, y, x + 2, y + 2], fill=(44, 51, 59))

# Purple radial glow (top-right corner, subtle)
cx, cy, r = 1230, 0, 520
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=70)
glow = glow.filter(__import__("PIL.ImageFilter", fromlist=["x"]).GaussianBlur(120))
purple = Image.new("RGB", (W, H), ACCENT)
img = Image.composite(purple, img, glow)
d = ImageDraw.Draw(img)

# Top accent bar (gradient)
bar = Image.new("RGB", (W, 6))
bd = ImageDraw.Draw(bar)
for x in range(W):
    t = x / (W - 1)
    bd.line(
        [(x, 0), (x, 6)],
        fill=tuple(int(ACCENT[i] + (ACCENT2[i] - ACCENT[i]) * t) for i in range(3)),
    )
img.paste(bar, (0, 0))
d = ImageDraw.Draw(img)

f_name = ImageFont.truetype(SANS_B, 88)
f_role = ImageFont.truetype(SANS_B, 36)
f_loc = ImageFont.truetype(SANS_R, 28)
f_sub = ImageFont.truetype(SANS_R, 24)
f_mono = ImageFont.truetype(MONO_R, 22)
f_mono_sm = ImageFont.truetype(MONO_R, 22)

d.text((88, 170), "Alexis Fiolleau", font=f_name, fill=FG)

# Accent underline
d.rounded_rectangle([88, 292, 158, 297], radius=3, fill=ACCENT)
d.text((176, 276), "Full-Stack Developer", font=f_role, fill=PURPLE_TXT)

d.text((88, 350), "Nantes, France", font=f_loc, fill=MUTED)
d.text(
    (88, 398),
    "Freelance & agency founder - sites web, apps mobiles, automatisations",
    font=f_sub,
    fill=DIM,
)
d.text((88, 486), "next.js  typescript  kotlin  swift  python", font=f_mono, fill=MUTED)

gh = "github.com/Potowai"
w = d.textlength(gh, font=f_mono_sm)
d.text((1192 - w, 88), gh, font=f_mono_sm, fill=FAINT)

img.save("assets/profile-social-preview.png", "PNG", optimize=True)
print("wrote assets/profile-social-preview.png", img.size)
