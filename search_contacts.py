import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request("https://herohomeslucknow.in/", headers=headers)
html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8', errors='ignore')

# Search tel: links or 10-digit numbers
tels = re.findall(r'tel:([0-9\+\s\-]+)', html)
wa = re.findall(r'wa\.me/([0-9]+)', html)
numbers = re.findall(r'\+?91[\s\-]?[6-9]\d{9}', html)

print("Tel links:", tels)
print("WhatsApp links:", wa)
print("Regex 10-digit numbers:", set(numbers))

# Check for RERA strings
rera = re.findall(r'RERA[^<]+', html, re.IGNORECASE)
print("RERA strings:", set(rera))
