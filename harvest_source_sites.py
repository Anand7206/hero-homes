import urllib.request
import ssl
import re
import os
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def check_url(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read()
            return {
                'status': resp.status,
                'final_url': resp.url,
                'length': len(data),
                'content': data.decode('utf-8', errors='ignore')
            }
    except Exception as e:
        return {'status': 'ERROR', 'error': str(e)}

print("=== CHECKING SOURCE SITES ===")
site1 = check_url("https://herohomeslucknow.in/")
print(f"1. herohomeslucknow.in : status={site1.get('status')}, len={site1.get('length', 0)}, error={site1.get('error')}")

site2 = check_url("https://herohomelucknow.in/")
print(f"2. herohomelucknow.in  : status={site2.get('status')}, len={site2.get('length', 0)}, error={site2.get('error')}")

site3 = check_url("https://lucknowhomes.in/")
print(f"3. lucknowhomes.in     : status={site3.get('status')}, len={site3.get('length', 0)}, error={site3.get('error')}")
