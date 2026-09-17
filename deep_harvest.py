import json
import re
import urllib.request
import ssl
from playwright.sync_api import sync_playwright

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def harvest_with_playwright():
    print("=== HARVESTING FROM https://herohomeslucknow.in/ VIA PLAYWRIGHT ===")
    
    harvest_data = {
        'url': 'https://herohomeslucknow.in/',
        'title': '',
        'phone_numbers': [],
        'whatsapp_numbers': [],
        'map_iframes': [],
        'images': [],
        'text_blocks': [],
        'logo_candidates': [],
        'rera_text': []
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto("https://herohomeslucknow.in/", timeout=30000, wait_until="networkidle")
        except Exception as e:
            print(f"Page load warning: {e}")
            page.goto("https://herohomeslucknow.in/", timeout=30000, wait_until="domcontentloaded")
        
        harvest_data['title'] = page.title()
        
        # 1. Map iframes
        iframes = page.query_selector_all("iframe")
        for f in iframes:
            src = f.get_attribute("src")
            if src:
                harvest_data['map_iframes'].append(src)
        
        # 2. Extract images
        imgs = page.query_selector_all("img")
        for img in imgs:
            src = img.get_attribute("src") or img.get_attribute("data-src")
            alt = img.get_attribute("alt") or ""
            natural_w = img.evaluate("el => el.naturalWidth")
            natural_h = img.evaluate("el => el.naturalHeight")
            if src:
                harvest_data['images'].append({
                    'src': src,
                    'alt': alt,
                    'width': natural_w,
                    'height': natural_h
                })
        
        # 3. Extract phone / whatsapp links
        links = page.query_selector_all("a")
        for a in links:
            href = a.get_attribute("href") or ""
            text = a.inner_text().strip()
            if href.startswith("tel:"):
                harvest_data['phone_numbers'].append({'href': href, 'text': text})
            elif "wa.me" in href or "whatsapp" in href or "api.whatsapp.com" in href:
                harvest_data['whatsapp_numbers'].append({'href': href, 'text': text})
        
        # 4. Body text snippets
        body_text = page.inner_text("body")
        phones_found = re.findall(r'(?:\+91[\s\-]?)?[6-9]\d{9}', body_text)
        harvest_data['text_phones'] = list(set(phones_found))
        
        rera_matches = re.findall(r'RERA[^.\n]+', body_text, re.IGNORECASE)
        harvest_data['rera_text'] = list(set(rera_matches))
        
        # Take full page screenshot for reference
        page.screenshot(path="harvest_herohomeslucknow.png", full_page=True)
        print("Saved harvest screenshot to harvest_herohomeslucknow.png")
        
        browser.close()

    return harvest_data

if __name__ == "__main__":
    data = harvest_with_playwright()
    with open("harvest_result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Harvest complete. Saved to harvest_result.json")
