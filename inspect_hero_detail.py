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

js_content = fetch("https://herohomelucknow.in/assets/index-Bbr9BEa8.js").decode("utf-8", errors="ignore")

# Find all image-like strings
all_imgs = re.findall(r'["\']([^"\']+\.(?:png|jpg|jpeg|svg|webp|ico))["\']', js_content)
print("All img strings in JS:", set(all_imgs))

# Find developer phrasing & color codes
colors = re.findall(r'#[0-9a-fA-F]{3,8}', js_content)
print("Colors found in JS:", set(colors[:20]))

# Search text snippets in JS
text_snippets = re.findall(r'["\']([^"\']*(?:Hero|Lucknow|Kanpur|Township|Developer|Homes)[^"\']*)["\']', js_content, re.IGNORECASE)
print("\nSample text snippets:")
for t in list(set(text_snippets))[:15]:
    if len(t) < 150:
        print("- ", t)
