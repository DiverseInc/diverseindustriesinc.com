"""
Generate a 1200x630 Open Graph image for diverseindustriesinc.com.
Uses the 512px DI master logo on a dark navy background with the tagline below.
Output: assets/og-image.png
"""
from PIL import Image, ImageDraw, ImageFont
import os

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
LOGO_512 = os.path.join(ASSETS, "diverse-logo-512.png")
OUT = os.path.join(ASSETS, "og-image.png")

# Canvas
W, H = 1200, 630
NAVY = (10, 37, 64)        # dark navy brand
GOLD = (245, 166, 35)      # gold brand
WHITE = (255, 255, 255)
MUTED = (147, 161, 184)    # muted slate

# Build background
img = Image.new("RGB", (W, H), NAVY)

# Subtle radial-style gradient via overlay rectangles (cheap effect)
overlay = Image.new("RGB", (W, H), NAVY)
for r in range(0, 500, 4):
    alpha = max(0, 30 - r // 16)
    for x in range(W):
        for y in range(H):
            dx, dy = x - W // 2, y - int(H * 0.18)
            d = (dx * dx + dy * dy) ** 0.5
            if abs(d - r) < 2:
                a = overlay.getpixel((x, y))
                overlay.putpixel((x, y), (min(255, a[0] + alpha), min(255, a[1] + alpha), min(255, a[2] + alpha)))
img.paste(overlay, (0, 0))

# Logo (centered upper third)
logo = Image.open(LOGO_512).convert("RGBA")
LOGO_SIZE = 280
logo = logo.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
logo_x = (W - LOGO_SIZE) // 2
logo_y = 110
img.paste(logo, (logo_x, logo_y), logo)

draw = ImageDraw.Draw(img)

# Pick a font. Try several fallbacks.
def load_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\verdana.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

font_h1 = load_font(60, bold=True)
font_sub = load_font(34, bold=False)
font_url = load_font(26, bold=False)

# Brand name (h1)
brand = "Diverse Industries Inc."
sub = "Software & AI Tools  ·  28 apps, 1 purchase"
url = "diverseindustriesinc.com"

def center_text(text, y, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((W - w) // 2, y), text, font=font, fill=fill)

center_text(brand, 430, font_h1, WHITE)
center_text(sub, 505, font_sub, GOLD)
center_text(url, 555, font_url, MUTED)

# Gold accent bar
bar_w = 80
draw.rectangle([(W // 2 - bar_w // 2, 415), (W // 2 + bar_w // 2, 419)], fill=GOLD)

img.save(OUT, "PNG", optimize=True)
print(f"Saved: {OUT}  ({os.path.getsize(OUT)} bytes)")
