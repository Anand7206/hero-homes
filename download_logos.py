import urllib.request
import ssl
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def download_file(url, target_path):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            data = resp.read()
            with open(target_path, 'wb') as f:
                f.write(data)
            print(f"Downloaded {url} -> {target_path} ({len(data)} bytes)")
            return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

# Download Hero Homes Logo
download_file("https://herohomelucknow.in/images/logo.png", "assets/hero-homes-logo.png")

# Download Lucknow Homes Logo
download_file("https://lucknowhomes.in/images/Homes-Logo.webp", "assets/lucknow-homes-logo.webp")

# Let's also check if there are other logo variants like svg or webp on herohomelucknow.in
download_file("https://herohomelucknow.in/images/logo.svg", "assets/hero-homes-logo-check.svg")
download_file("https://herohomelucknow.in/images/logo.webp", "assets/hero-homes-logo-check.webp")
