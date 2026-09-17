import urllib.request
import os
import re
import xml.etree.ElementTree as ET

def run_verification():
    print("==================================================")
    print(" HERO HOMES LUCKNOW - PHASE 3 VERIFICATION SUITE  ")
    print("==================================================")

    # 1. Fetch HTML from localhost server
    url = "http://localhost:8080/"
    try:
        req = urllib.request.urlopen(url)
        html = req.read().decode('utf-8')
        print(f"✔ [TEST 1 PASS] Local HTTP server responding at {url} (Code 200, {len(html)} bytes)")
    except Exception as e:
        print(f"❌ [TEST 1 FAIL] Local HTTP server error: {e}")
        return

    # 2. Case-sensitivity audit
    print("\n--- TEST 2: Case-Sensitivity & File Existence Audit ---")
    assets_dir = "assets"
    actual_files = os.listdir(assets_dir)
    print(f"Actual files in ./assets/: {actual_files}")

    # Find all referenced assets in HTML
    asset_refs = re.findall(r'(?:src|href|srcset)=["\']\./assets/([^"\'\s,]+)', html)
    # Clean up srcset multipliers like ' 1x' or ' 2x'
    cleaned_refs = []
    for ref in asset_refs:
        ref_clean = ref.split()[0]
        cleaned_refs.append(ref_clean)
    
    unique_refs = set(cleaned_refs)
    mismatches = []
    missing = []
    
    for ref in unique_refs:
        if ref not in actual_files:
            # Check case-insensitive match
            matching_ic = [f for f in actual_files if f.lower() == ref.lower()]
            if matching_ic:
                mismatches.append((ref, matching_ic[0]))
            else:
                missing.append(ref)
    
    if not mismatches and not missing:
        print(f"✔ [TEST 2 PASS] All {len(unique_refs)} referenced assets exist in ./assets/ with EXACT case matching!")
    else:
        if mismatches:
            print(f"❌ [TEST 2 FAIL] Case mismatches found: {mismatches}")
        if missing:
            print(f"❌ [TEST 2 FAIL] Missing asset files: {missing}")

    # 3. External dependencies / Hotlink check
    print("\n--- TEST 3: Zero External JS & Hotlink Audit ---")
    external_scripts = re.findall(r'<script[^>]+src=["\'](http[^"\']+)["\']', html)
    external_imgs = re.findall(r'<img[^>]+src=["\'](http[^"\']+)["\']', html)
    
    print(f"External script tags: {external_scripts}")
    print(f"External image tags: {external_imgs}")

    if not external_scripts and not external_imgs:
        print("✔ [TEST 3 PASS] Zero external JS scripts or hotlinked images detected!")
    else:
        print("❌ [TEST 3 FAIL] External dependencies found!")

    # 4. Image attributes check (width, height, alt, loading, decoding)
    print("\n--- TEST 4: Image Attributes & Picture Fallback Audit ---")
    img_tags = re.findall(r'<img[^>]+>', html)
    print(f"Found {len(img_tags)} <img> tags.")

    img_issues = []
    for img in img_tags:
        has_width = 'width=' in img
        has_height = 'height=' in img
        has_alt = 'alt=' in img
        has_loading = 'loading=' in img
        has_decoding = 'decoding=' in img

        if not (has_width and has_height and has_alt):
            img_issues.append((img, f"width:{has_width}, height:{has_height}, alt:{has_alt}"))

    if not img_issues:
        print("✔ [TEST 4 PASS] All <img> tags have explicit width, height, and alt attributes!")
    else:
        print(f"❌ [TEST 4 FAIL] <img> attribute issues: {img_issues}")

    # 5. Open Graph / Social Image Audit
    print("\n--- TEST 5: Open Graph Image Format Audit ---")
    og_image_match = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', html)
    if og_image_match:
        og_url = og_image_match.group(1)
        print(f"Found og:image URL: {og_url}")
        is_absolute = og_url.startswith("http://") or og_url.startswith("https://")
        is_jpg_png = og_url.lower().endswith(".jpg") or og_url.lower().endswith(".jpeg") or og_url.lower().endswith(".png")
        is_not_webp = not og_url.lower().endswith(".webp")

        if is_absolute and is_jpg_png and is_not_webp:
            print("✔ [TEST 5 PASS] og:image is an absolute URL and strictly JPG/PNG (NOT WebP)!")
        else:
            print(f"❌ [TEST 5 FAIL] og:image check failed: absolute={is_absolute}, jpg/png={is_jpg_png}")
    else:
        print("❌ [TEST 5 FAIL] og:image meta tag not found!")

    # 6. Mandatory Disclosure Text Audit
    print("\n--- TEST 6: Mandatory Content Integrity Audit ---")
    d1 = "Marketed by Lucknow Homes — Authorised Channel Partner. This is not the official website of the developer."
    d2 = "Project RERA registration awaited ({{UP_RERA_NUMBER}}). All information is indicative and subject to change. Prices, sizes and launch dates do not constitute an offer or contract."
    d3 = "one of India's most trusted real estate brands"

    has_d1 = d1 in html
    has_d2 = d2 in html
    has_d3 = d3 in html

    print(f"Co-brand disclosure present: {has_d1}")
    print(f"Footer RERA disclosure present: {has_d2}")
    print(f"Developer phrasing present: {has_d3}")

    if has_d1 and has_d2 and has_d3:
        print("✔ [TEST 6 PASS] All mandatory disclosure strings and developer phrasing are present verbatim!")
    else:
        print("❌ [TEST 6 FAIL] Missing mandatory content strings!")

    # 7. Sticky Mobile Bar & Form ID Check
    print("\n--- TEST 7: Mobile Bar & Core Elements Audit ---")
    has_mobile_bar = 'class="sticky-mobile-bar"' in html
    has_enquire_id = 'id="enquire"' in html
    has_plot_sizes = '125 sq. yds' in html and '160 sq. yds' in html and '180 sq. yds' in html and '200 sq. yds' in html
    
    print(f"Sticky Mobile Bar present: {has_mobile_bar}")
    print(f"Lead Form id='enquire' present: {has_enquire_id}")
    print(f"Plot sizes cards present: {has_plot_sizes}")

    if has_mobile_bar and has_enquire_id and has_plot_sizes:
        print("✔ [TEST 7 PASS] Sticky mobile bar, lead form container, and plot size cards verified!")
    else:
        print("❌ [TEST 7 FAIL] Missing core layout elements!")

    print("\n==================================================")
    print(" VERIFICATION SUITE COMPLETE                      ")
    print("==================================================")

if __name__ == "__main__":
    run_verification()
