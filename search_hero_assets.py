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
css_content = fetch("https://herohomelucknow.in/assets/index-B9Lvfb7N.css").decode("utf-8", errors="ignore")

print("--- Searching images/svgs in JS content ---")
matches = re.findall(r'/[a-zA-Z0-9_\-/\.]+\.(?:png|jpg|jpeg|svg|webp|ico)', js_content)
print("Matches in JS:", set(matches))

matches_css = re.findall(r'/[a-zA-Z0-9_\-/\.]+\.(?:png|jpg|jpeg|svg|webp|ico)', css_content)
print("Matches in CSS:", set(matches_css))

print("\n--- Checking common logo URLs on herohomelucknow.in ---")
candidates = [
    "https://herohomelucknow.in/assets/logo.svg",
    "https://herohomelucknow.in/assets/logo.png",
    "https://herohomelucknow.in/logo.svg",
    "https://herohomelucknow.in/logo.png",
    "https://herohomelucknow.in/favicon.ico",
    "https://herohomelucknow.in/assets/hero-logo.svg",
    "https://herohomelucknow.in/assets/hero-logo.png",
]
for c in candidates:
    res = fetch(c)
    if res:
        print(f"Found candidate {c} : {len(res)} bytes")
