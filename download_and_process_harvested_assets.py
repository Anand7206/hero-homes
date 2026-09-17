import urllib.request
import ssl
import os
from PIL import Image, ImageDraw, ImageFont

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0'}

os.makedirs("assets", exist_ok=True)

def download(url, path):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = resp.read()
            with open(path, 'wb') as f:
                f.write(data)
            print(f"Downloaded {url} -> {path} ({len(data)} bytes)")
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

print("=== DOWNLOADING HARVESTED ASSETS ===")
# 1. Logos
download("https://herohomeslucknow.in/images/logo.webp", "assets/hero-homes-logo.webp")
download("https://lucknowhomes.in/images/Homes-Logo.webp", "assets/lucknow-homes-logo.webp")

# Convert logo to PNG fallback
try:
    im_logo = Image.open("assets/hero-homes-logo.webp")
    im_logo.save("assets/hero-homes-logo.png", "PNG")
    print("Created assets/hero-homes-logo.png fallback")
except Exception as e:
    print(f"Logo PNG error: {e}")

# 2. Main Township Dusk Render (slider-1.webp)
if download("https://herohomeslucknow.in/images/slider-1.webp", "assets/township-gate-dusk.webp"):
    im = Image.open("assets/township-gate-dusk.webp")
    im.save("assets/township-gate-dusk.jpg", "JPEG", quality=85)
    mobile_crop = im.resize((800, 1000))
    mobile_crop.save("assets/township-gate-dusk-mobile.webp", "WEBP", quality=85)
    mobile_crop.save("assets/township-gate-dusk-mobile.jpg", "JPEG", quality=85)
    print("Processed township-gate-dusk (desktop & mobile WebP + JPG)")

# 3. Township Overview (about.webp)
if download("https://herohomeslucknow.in/images/about.webp", "assets/township-overview.webp"):
    im = Image.open("assets/township-overview.webp")
    im.save("assets/township-overview.jpg", "JPEG", quality=85)

# 4. Master Plan Layout (walkthrough.webp)
if download("https://herohomeslucknow.in/images/walkthrough.webp", "assets/master-plan-layout.webp"):
    im = Image.open("assets/master-plan-layout.webp")
    im.save("assets/master-plan-layout.jpg", "JPEG", quality=85)

# 5. Villa Elevation (costing.jpeg)
if download("https://herohomeslucknow.in/images/costing.jpeg", "assets/plot-villa-elevation-src.jpg"):
    im = Image.open("assets/plot-villa-elevation-src.jpg")
    im.save("assets/plot-villa-elevation.webp", "WEBP", quality=85)
    im.save("assets/plot-villa-elevation.jpg", "JPEG", quality=85)
    if os.path.exists("assets/plot-villa-elevation-src.jpg"):
        os.remove("assets/plot-villa-elevation-src.jpg")

# 6. Additional Gallery Items (Clubhouse & Sports)
def create_gallery_render(width, height, title, color_bg, path_base):
    im = Image.new("RGB", (width, height), color_bg)
    draw = ImageDraw.Draw(im)
    draw.rectangle([20, 20, width-20, height-20], outline=(201, 162, 39), width=3)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    draw.text((width//2 - 120, height//2 - 12), title, fill=(242, 208, 107), font=font)
    im.save(f"{path_base}.webp", "WEBP", quality=85)
    im.save(f"{path_base}.jpg", "JPEG", quality=85)

create_gallery_render(800, 500, "Grand Clubhouse Render", (11, 31, 58), "assets/grand-clubhouse")
create_gallery_render(800, 500, "Sports & Recreation Zone", (20, 45, 80), "assets/sports-recreation-zone")

# 7. Map Thumbnail Poster
map_img = Image.new("RGB", (800, 500), (240, 237, 230))
map_draw = ImageDraw.Draw(map_img)
for x in range(0, 800, 80): map_draw.line([(x, 0), (x, 500)], fill=(220, 215, 200), width=1)
for y in range(0, 500, 80): map_draw.line([(0, y), (800, y)], fill=(220, 215, 200), width=1)
map_draw.line([(50, 450), (750, 50)], fill=(201, 162, 39), width=12)
map_draw.text((380, 220), "Kanpur Road / NH-27", fill=(11, 31, 58))
map_draw.ellipse([480, 140, 520, 180], fill=(225, 11, 24), outline=(11, 31, 58), width=3)
map_draw.text((430, 110), "Hero Homes Lucknow", fill=(11, 31, 58))

map_img.save("assets/map-location-thumb.webp", "WEBP", quality=85)
map_img.save("assets/map-location-thumb.jpg", "JPEG", quality=85)

# 8. OG Social Image (1200x630 JPG)
og_img = Image.new("RGB", (1200, 630), (11, 31, 58))
og_draw = ImageDraw.Draw(og_img)
og_draw.rectangle([20, 20, 1180, 610], outline=(201, 162, 39), width=4)
og_draw.text((80, 100), "HERO HOMES LUCKNOW", fill=(242, 208, 107))
og_draw.text((80, 180), "Upcoming 52-Acre Township on Kanpur Road", fill=(255, 255, 255))
og_draw.text((80, 250), "Pre-Launch Residential Plots 125-200 sq. yds from Rs 65,000 / sq. yd", fill=(200, 210, 225))
og_draw.text((80, 520), "Marketed by Lucknow Homes — Authorised Channel Partner", fill=(180, 190, 200))
og_img.save("assets/og-image.jpg", "JPEG", quality=90)

# 9. Favicons
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

apple_icon = Image.new("RGB", (180, 180), (11, 31, 58))
apple_draw = ImageDraw.Draw(apple_icon)
apple_draw.rectangle([10, 10, 170, 170], outline=(201, 162, 39), width=4)
apple_draw.text((35, 75), "HERO", fill=(242, 208, 107))
apple_icon.save("assets/apple-touch-icon.png", "PNG")

ico_img = Image.new("RGB", (32, 32), (11, 31, 58))
ico_draw = ImageDraw.Draw(ico_img)
ico_draw.text((6, 8), "H", fill=(242, 208, 107))
ico_img.save("assets/favicon.ico")

print("=== ALL ASSETS DOWNLOADED AND PROCESSED ===")
