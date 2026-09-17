import os
from PIL import Image, ImageDraw, ImageFont

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

# Convert PNG logo to WebP as well
img = Image.open("assets/hero-homes-logo.png")
img.save("assets/hero-homes-logo.webp", "WEBP", quality=90)
print("Saved assets/hero-homes-logo.webp")

# Create Hero Township Gate Desktop (1920x1080)
def create_hero_render(width, height, is_mobile=False):
    # Create dark luxury dusk background with gold/navy tones & arch/gate rendering
    im = Image.new("RGB", (width, height), (11, 31, 58)) # Navy #0B1F3A
    draw = ImageDraw.Draw(im)
    
    # Gradient overlay / sky at dusk
    for y in range(height):
        r = int(11 + (40 - 11) * (y / height))
        g = int(31 + (50 - 31) * (y / height))
        b = int(58 + (90 - 58) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Draw stylized township gate & lush landscape outline
    # Gate Pillars
    p_w = int(width * 0.08)
    p_h = int(height * 0.45)
    center_x = width // 2
    gate_y = height - p_h - 100
    
    # Left pillar
    draw.rectangle([center_x - p_w*3, gate_y, center_x - p_w*2, height - 100], fill=(20, 45, 80), outline=(201, 162, 39), width=3)
    # Right pillar
    draw.rectangle([center_x + p_w*2, gate_y, center_x + p_w*3, height - 100], fill=(20, 45, 80), outline=(201, 162, 39), width=3)
    # Grand Arch connecting pillars
    draw.arc([center_x - p_w*3, gate_y - 100, center_x + p_w*3, gate_y + 100], 180, 360, fill=(201, 162, 39), width=6)
    
    # Warm glow lighting inside gate
    draw.ellipse([center_x - 150, gate_y + 50, center_x + 150, gate_y + 350], fill=(242, 208, 107, 40))
    
    # Road leading in
    draw.polygon([(center_x - 100, height - 100), (center_x + 100, height - 100), (center_x + 400, height), (center_x - 400, height)], fill=(15, 25, 45))
    
    # Text overlay placeholder info
    title = "HERO HOMES TOWNSHIP GATE (1920x1080 Dusk Render)" if not is_mobile else "HERO HOMES TOWNSHIP GATE (800x1000 Dusk Render)"
    try:
        font = ImageFont.truetype("arial.ttf", 28 if not is_mobile else 20)
    except:
        font = ImageFont.load_default()
    
    draw.text((width//2 - 250, height - 50), title, fill=(201, 162, 39), font=font)
    
    return im

hero_desktop = create_hero_render(1920, 1080)
hero_desktop.save("assets/hero-township-gate-desktop.webp", "WEBP", quality=85)
hero_desktop.save("assets/hero-township-gate-desktop.jpg", "JPEG", quality=85)

hero_mobile = create_hero_render(800, 1000, is_mobile=True)
hero_mobile.save("assets/hero-township-gate-mobile.webp", "WEBP", quality=85)
hero_mobile.save("assets/hero-township-gate-mobile.jpg", "JPEG", quality=85)
print("Created hero background desktop & mobile renders (WebP + JPG)")

# Create Map Static Thumbnail (800x500)
map_img = Image.new("RGB", (800, 500), (240, 237, 230))
map_draw = ImageDraw.Draw(map_img)
# Grid lines for map
for x in range(0, 800, 80):
    map_draw.line([(x, 0), (x, 500)], fill=(220, 215, 200), width=1)
for y in range(0, 500, 80):
    map_draw.line([(0, y), (800, y)], fill=(220, 215, 200), width=1)
# Major road NH-27 / Kanpur Road line
map_draw.line([(50, 450), (750, 50)], fill=(201, 162, 39), width=12)
map_draw.text((380, 220), "Kanpur Road / NH-27", fill=(11, 31, 58))
# Pin marker
map_draw.ellipse([480, 140, 520, 180], fill=(225, 11, 24), outline=(11, 31, 58), width=3)
map_draw.text((430, 110), "Hero Homes Township", fill=(11, 31, 58))
map_draw.text((250, 460), "Click to Load Interactive Google Map", fill=(201, 162, 39))

map_img.save("assets/map-location-thumb.webp", "WEBP", quality=85)
map_img.save("assets/map-location-thumb.jpg", "JPEG", quality=85)
print("Created map static thumbnails (WebP + JPG)")

# Create Social / OG Image (1200x630 JPG — NEVER WEBP)
og_img = Image.new("RGB", (1200, 630), (11, 31, 58))
og_draw = ImageDraw.Draw(og_img)
# Gold border accent
og_draw.rectangle([20, 20, 1180, 610], outline=(201, 162, 39), width=4)
# Header text
og_draw.text((80, 100), "HERO HOMES LUCKNOW", fill=(242, 208, 107))
og_draw.text((80, 180), "Upcoming 52-Acre Township on Kanpur Road", fill=(255, 255, 255))
og_draw.text((80, 250), "Premium Living & Prime Investment | Pre-Launch Plots from 125 sq. yds", fill=(200, 210, 225))
og_draw.text((80, 350), "Expected Price: Rs 65,000 / sq. yd (approx.)", fill=(242, 208, 107))
og_draw.text((80, 420), "Expected Launch: Oct - Nov 2026", fill=(255, 255, 255))
og_draw.text((80, 520), "Marketed by Lucknow Homes — Authorised Channel Partner", fill=(180, 190, 200))

og_img.save("assets/og-image.jpg", "JPEG", quality=90)
print("Created OG image assets/og-image.jpg (1200x630 JPG)")

# Favicon SVG
svg_favicon = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="12" fill="#0B1F3A"/>
  <path d="M16 48V16h8v12h16V16h8v32h-8V34H24v14z" fill="url(#goldGrad)"/>
  <defs>
    <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#C9A227"/>
      <stop offset="100%" stop-color="#F2D06B"/>
    </linearGradient>
  </defs>
</svg>"""

with open("assets/favicon.svg", "w", encoding="utf-8") as f:
    f.write(svg_favicon)

# Apple Touch Icon PNG (180x180)
apple_icon = Image.new("RGB", (180, 180), (11, 31, 58))
apple_draw = ImageDraw.Draw(apple_icon)
apple_draw.rectangle([10, 10, 170, 170], outline=(201, 162, 39), width=4)
apple_draw.text((35, 75), "HERO", fill=(242, 208, 107))
apple_icon.save("assets/apple-touch-icon.png", "PNG")

# Favicon.ico (32x32)
ico_img = Image.new("RGB", (32, 32), (11, 31, 58))
ico_draw = ImageDraw.Draw(ico_img)
ico_draw.text((6, 8), "H", fill=(242, 208, 107))
ico_img.save("assets/favicon.ico")

print("Created favicons (SVG, ICO, PNG)")
