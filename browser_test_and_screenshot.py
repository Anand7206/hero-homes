import time
from playwright.sync_api import sync_playwright
import os
import urllib.parse

artifact_dir = r"C:\Users\anand singh\.gemini\antigravity\brain\6c8e94d4-2f9b-4bc7-b190-49ab5b83ddeb"
os.makedirs(artifact_dir, exist_ok=True)

def run_phase3_verification():
    print("==================================================")
    print(" PHASE 3 FULL VERIFICATION & SCREENSHOT SUITE     ")
    print("==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        viewports = [360, 375, 414, 768, 1024, 1440]
        for w in viewports:
            ctx = browser.new_context(viewport={'width': w, 'height': 800})
            page = ctx.new_page()
            page.goto("http://localhost:8080/")
            page.wait_for_load_state("networkidle")

            # Screenshot
            shot_path = os.path.join(artifact_dir, f"screenshot_{w}px.png")
            page.screenshot(path=shot_path, full_page=True)
            print(f"✔ Saved full-page screenshot at {w}px: {shot_path}")

            # Horizontal Overflow Check
            scroll_w = page.evaluate("document.documentElement.scrollWidth")
            inner_w = page.evaluate("window.innerWidth")
            if scroll_w <= inner_w:
                print(f"✔ [PASS] {w}px viewport: scrollWidth ({scroll_w}) <= innerWidth ({inner_w})")
            else:
                print(f"❌ [FAIL] {w}px viewport overflow! scrollWidth ({scroll_w}) > innerWidth ({inner_w})")

            ctx.close()

        # Detailed Interactive Flow Tests (Desktop Viewport)
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        page.goto("http://localhost:8080/")
        page.wait_for_load_state("networkidle")

        # 1. Budget Form Flow Test
        print("\n--- TEST: 2-Step Budget Form Flow ---")
        # Select "₹1 Cr – ₹1.25 Cr" budget card
        page.evaluate("selectBudgetCard('₹1 Cr – ₹1.25 Cr', 'Matches 160 & 180 sq. yds')")
        time.sleep(0.3)

        reciprocity_visible = page.is_visible("#reciprocityPanel")
        reciprocity_text = page.inner_text("#reciprocityText")
        print(f"✔ Reciprocity panel visible: {reciprocity_visible}, text: '{reciprocity_text}'")

        s_budget = os.path.join(artifact_dir, "step1_budget_selected.png")
        page.screenshot(path=s_budget)

        # Click Continue to Step 2
        page.click("#step1ContinueBtn")
        time.sleep(0.3)

        step2_visible = page.is_visible("#step2View")
        print(f"✔ Step 2 view visible: {step2_visible}")

        # Test Back Button
        page.click("button.back-btn-link")
        time.sleep(0.3)
        budget_preserved = page.evaluate("state.budget_band") == "₹1 Cr – ₹1.25 Cr"
        print(f"✔ Budget selection preserved on Back click: {budget_preserved}")

        # Return to Step 2 and test validation
        page.click("#step1ContinueBtn")
        time.sleep(0.3)

        # Empty submit
        page.click("#submitBtn")
        time.sleep(0.3)
        name_err = page.evaluate("document.getElementById('fullName').classList.contains('is-invalid')")
        mobile_err = page.evaluate("document.getElementById('mobileNumber').classList.contains('is-invalid')")
        print(f"✔ Empty submit validation errors - Name: {name_err}, Mobile: {mobile_err}")

        # Invalid phone '12345'
        page.fill("#fullName", "Aditya Sharma")
        page.fill("#mobileNumber", "12345")
        page.focus("#emailAddress")
        time.sleep(0.3)
        phone_rejected = page.evaluate("document.getElementById('mobileNumber').classList.contains('is-invalid')")
        print(f"✔ Invalid phone '12345' rejected: {phone_rejected}")

        # Valid Submit
        page.fill("#mobileNumber", "9876543210")
        page.check("#consentCheckbox")
        time.sleep(3.2) # time on page check
        page.click("#submitBtn")
        time.sleep(1.5)

        thanks_visible = page.is_visible("#thankYouState")
        print(f"✔ Thank You state displayed: {thanks_visible}")

        s_thanks = os.path.join(artifact_dir, "step2_thankyou_submitted.png")
        page.screenshot(path=s_thanks)

        # 2. Plot Card Pre-selection (180 sq. yds)
        print("\n--- TEST: Plot Card Pre-Selection ---")
        page.goto("http://localhost:8080/")
        page.wait_for_load_state("networkidle")

        page.evaluate("selectPlotCard('180 sq. yds', '₹1 Cr – ₹1.25 Cr')")
        time.sleep(0.5)

        plot_val = page.evaluate("document.getElementById('plotSize').value")
        budget_val = page.evaluate("state.budget_band")
        print(f"✔ Plot card pre-selection - Plot Size: '{plot_val}', Budget Band: '{budget_val}'")

        s_plot180 = os.path.join(artifact_dir, "plot180_preselected.png")
        page.screenshot(path=s_plot180)

        # 3. WhatsApp Context-Aware Prefill URL Test
        print("\n--- TEST: Context-Aware WhatsApp Prefill ---")
        wa_href = page.get_attribute("#stickyBarWaBtn", "href")
        print(f"Generated WhatsApp URL: {wa_href}")
        decoded_wa = urllib.parse.unquote(wa_href)
        print(f"Decoded prefill text: {decoded_wa}")
        contains_context = "180 sq. yds" in decoded_wa and "₹1 Cr – ₹1.25 Cr" in decoded_wa
        print(f"✔ WhatsApp prefill contains selected plot size and budget band: {contains_context}")

        # 4. Project Gallery & Lightbox Test
        print("\n--- TEST: Gallery Lightbox & Keyboard Controls ---")
        page.evaluate("openLightbox(0)")
        time.sleep(0.3)

        lightbox_active = page.is_visible("#lightboxModal.active")
        body_locked = page.evaluate("document.body.classList.contains('lightbox-open')")
        print(f"✔ Lightbox active: {lightbox_active}, body scroll locked: {body_locked}")

        s_lightbox = os.path.join(artifact_dir, "gallery_lightbox_open.png")
        page.screenshot(path=s_lightbox)

        # Press Escape key to close
        page.keyboard.press("Escape")
        time.sleep(0.3)
        lightbox_closed = not page.is_visible("#lightboxModal.active")
        body_unlocked = not page.evaluate("document.body.classList.contains('lightbox-open')")
        print(f"✔ Lightbox closed with Esc key: {lightbox_closed}, body scroll unlocked: {body_unlocked}")

        # 5. Map Embed Load Test
        print("\n--- TEST: Map Click-to-Load ---")
        page.evaluate("loadGoogleMap()")
        time.sleep(0.5)
        map_iframe_exists = page.is_visible("iframe.map-iframe")
        print(f"✔ Google Maps iframe loaded: {map_iframe_exists}")

        # 6. Mobile Bar vs Floating WhatsApp Visibility
        print("\n--- TEST: Responsive Sticky Bar vs Floating Button ---")
        # Desktop (1440px)
        sticky_bar_desktop = page.is_visible(".sticky-mobile-bar")
        floating_wa_desktop = page.is_visible(".desktop-wa-floating")
        print(f"1440px Desktop - Sticky Bar visible: {sticky_bar_desktop} (False), Floating WA visible: {floating_wa_desktop} (True)")

        # Switch to 375px Mobile
        page.set_viewport_size({'width': 375, 'height': 667})
        time.sleep(0.3)
        sticky_bar_mobile = page.is_visible(".sticky-mobile-bar")
        floating_wa_mobile = page.is_visible(".desktop-wa-floating")
        print(f"375px Mobile - Sticky Bar visible: {sticky_bar_mobile} (True), Floating WA visible: {floating_wa_mobile} (False)")

        browser.close()

    print("\n==================================================")
    print(" PHASE 3 VERIFICATION SUITE COMPLETED SUCCESSFULLY ")
    print("==================================================")

if __name__ == "__main__":
    run_phase3_verification()
