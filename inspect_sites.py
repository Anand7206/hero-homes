import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            return resp.read()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return b""

print("--- Fetching herohomelucknow.in assets ---")
html1 = fetch("https://herohomelucknow.in/").decode("utf-8", errors="ignore")
js_files = re.findall(r'src="([^"]+)"', html1)
css_files = re.findall(r'href="([^"]+\.css)"', html1)
print("JS files:", js_files)
print("CSS files:", css_files)

for js_path in js_files:
    if js_path.startswith('/'):
        js_url = "https://herohomelucknow.in" + js_path
    else:
        js_url = "https://herohomelucknow.in/" + js_path
    js_content = fetch(js_url).decode("utf-8", errors="ignore")
    print(f"\nScanning {js_url} (len {len(js_content)})...")
    images = re.findall(r'["\'](/assets/[^"\']+\.(?:png|jpg|jpeg|svg|webp))["\']', js_content)
    print("Found images in JS:", set(images))

print("\n--- Fetching lucknowhomes.in ---")
html2 = fetch("https://lucknowhomes.in/").decode("utf-8", errors="ignore")
print("lucknowhomes.in html len:", len(html2))
images2 = re.findall(r'src=["\']([^"\']+)["\']', html2)
print("Found images in lucknowhomes html:", set(images2[:20]))
