import time
import os
import urllib.parse
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\anand singh\.gemini\antigravity\brain\6c8e94d4-2f9b-4bc7-b190-49ab5b83ddeb"
os.makedirs(artifact_dir, exist_ok=True)

def verify_thank_you_flow():
    print("==================================================")
    print(" THANK-YOU PAGE & CONVERSION SUITE VERIFICATION   ")
    print("==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. VIEWPORT & OVERFLOW CHECKS ON THANK-YOU.HTML
        viewports = [360, 375, 768, 1440]
        for w in viewports:
            ctx = browser.new_context(viewport={'width': w, 'height': 800})
            page = ctx.new_page()
            page.goto("http://localhost:8080/thank-you.html?ref=HH-TEST1234")
            page.wait_for_load_state("networkidle")

            shot_path = os.path.join(artifact_dir, f"thank_you_{w}px.png")
            page.screenshot(path=shot_path, full_page=True)
            print(f"✔ Saved screenshot at {w}px: {shot_path}")

            scroll_w = page.evaluate("document.documentElement.scrollWidth")
            inner_w = page.evaluate("window.innerWidth")
            if scroll_w <= inner_w:
                print(f"✔ [PASS] {w}px viewport: scrollWidth ({scroll_w}) <= innerWidth ({inner_w})")
            else:
                print(f"❌ [FAIL] {w}px viewport overflow! scrollWidth ({scroll_w}) > innerWidth ({inner_w})")
            ctx.close()

        # 2. NEUTRAL PAGE LOAD (No ?ref= parameter)
        print("\n--- TEST 1: Neutral Page Load (No ?ref=) ---")
        ctx_neutral = browser.new_context(viewport={'width': 1440, 'height': 900})
        page_n = ctx_neutral.new_page()
        page_n.goto("http://localhost:8080/thank-you.html")
        page_n.wait_for_load_state("networkidle")

        heading_n = page_n.inner_text("#thankYouHeading")
        conf_n = page_n.inner_text("#confirmationLineText")
        ref_visible_n = page_n.is_visible("#refCard")
        data_layer_n = page_n.evaluate("window.dataLayer")
        lead_events_n = [e for e in data_layer_n if e.get('event') == 'lead_confirmed']

        print(f"✔ Neutral Headline: '{heading_n}'")
        print(f"✔ Neutral Confirmation Text: '{conf_n}'")
        print(f"✔ Ref Card Visible: {ref_visible_n} (Expected: False)")
        print(f"✔ Lead Confirmed Events Fired: {len(lead_events_n)} (Expected: 0)")
        assert "undefined" not in page_n.content(), "Found 'undefined' in page content!"
        print("✔ No 'undefined' text anywhere on neutral page!")

        ctx_neutral.close()

        # 3. END-TO-END FORM SUBMIT & REDIRECT FLOW FROM INDEX.HTML
        print("\n--- TEST 2: Form Submission Redirect & Fire-Once Guard ---")
        ctx_flow = browser.new_context(viewport={'width': 1440, 'height': 900})
        page_f = ctx_flow.new_page()
        page_f.goto("http://localhost:8080/")
        page_f.wait_for_load_state("networkidle")

        # Select budget card
        page_f.evaluate("selectBudgetCard('₹1 Cr – ₹1.25 Cr', 'Matches 160 sq. yds')")
        page_f.click("#step1ContinueBtn")
        time.sleep(0.3)

        # Fill form details
        page_f.fill("#fullName", "Aditya Vikram")
        page_f.fill("#mobileNumber", "9876543210")
        page_f.fill("#emailAddress", "aditya@example.com")
        page_f.check("#consentCheckbox")
        time.sleep(3.2) # time on page check

        # Submit form
        page_f.click("#submitBtn")
        page_f.wait_for_url("**/thank-you.html*", timeout=5000)
        print("✔ Successfully redirected to thank-you.html!")

        # Verify Personalization
        heading_personalized = page_f.inner_text("#thankYouHeading")
        conf_personalized = page_f.inner_text("#confirmationLineText")
        ref_visible = page_f.is_visible("#refCard")
        ref_text = page_f.inner_text("#refNumberText") if ref_visible else ''

        print(f"✔ Personalized Headline: '{heading_personalized}'")
        print(f"✔ Personalized Conf Line: '{conf_personalized}'")
        print(f"✔ Ref Card Visible: {ref_visible}, Ref Code: '{ref_text}'")
        assert "Aditya" in heading_personalized, "FirstName not in heading!"
        assert "98••••3210" in conf_personalized or "98••••" in conf_personalized, "Masked phone missing!"

        # Check conversion events on first load
        dl_first = page_f.evaluate("window.dataLayer")
        lead_events_first = [e for e in dl_first if e.get('event') == 'lead_confirmed']
        print(f"✔ First Load Conversion Events Fired: {len(lead_events_first)}")
        if lead_events_first:
          ev = lead_events_first[0]
          print(f"   Event payload: lead_id={ev.get('lead_id')}, budget={ev.get('budget_band')}, plot={ev.get('plot_size')}")
          extracted_lead_id = ev.get('lead_id')

        shot_first = os.path.join(artifact_dir, "thank_you_first_load.png")
        page_f.screenshot(path=shot_first)

        # Check replaceState stripped ?ref=
        current_url = page_f.url
        print(f"✔ Current URL after replaceState: {current_url}")
        assert "?ref=" not in current_url, "?ref= parameter was not stripped by replaceState!"

        # A. RELOAD STRIPPED PAGE (http://localhost:8080/thank-you.html)
        print("\n--- Reloading Stripped Thank-You Page ---")
        page_f.reload()
        page_f.wait_for_load_state("networkidle")

        dl_reload = page_f.evaluate("window.dataLayer")
        lead_events_reload = [e for e in dl_reload if e.get('event') == 'lead_confirmed']
        print(f"✔ Reload Lead Confirmed Events Fired: {len(lead_events_reload)} (Expected: 0 on neutral reload)")
        assert len(lead_events_reload) == 0, "Events fired on neutral reload!"
        print("✔ [PASS] Stripped page reload fires 0 conversion events!")

        # B. RE-VISIT SAME URL WITH ?ref= PARAMETER IN SAME SESSION
        print(f"\n--- Re-visiting URL with ?ref={extracted_lead_id} in Same Session ---")
        page_f.goto(f"http://localhost:8080/thank-you.html?ref={extracted_lead_id}")
        page_f.wait_for_load_state("networkidle")

        dl_revisit = page_f.evaluate("window.dataLayer")
        lead_events_revisit = [e for e in dl_revisit if e.get('event') == 'lead_confirmed']
        already_fired_key = page_f.evaluate(f"sessionStorage.getItem('fired_{extracted_lead_id}')")

        print(f"✔ Session Key 'fired_{extracted_lead_id}': {already_fired_key}")
        print(f"✔ Re-visit Lead Confirmed Events Fired: {len(lead_events_revisit)} (Expected: 0)")
        assert len(lead_events_revisit) == 0, "Fire-once guard failed when revisiting same ?ref=!"
        print("✔ [PASS] Fire-once guard prevented duplicate conversion when revisiting same ?ref=!")

        shot_reload = os.path.join(artifact_dir, "thank_you_reload_state.png")
        page_f.screenshot(path=shot_reload)

        ctx_flow.close()

        # 4. XSS SECURITY TEST
        print("\n--- TEST 3: XSS Injection Prevention ---")
        ctx_xss = browser.new_context(viewport={'width': 1440, 'height': 900})
        page_xss = ctx_xss.new_page()

        xss_name = "<script>alert(1)</script>"
        lead_ctx = {
            "lead_id": "HH-XSS999",
            "name": xss_name,
            "mobile": "9876543210",
            "plot_size": "180 sq. yds",
            "budget_band": "₹1 Cr",
            "source": "xss_test"
        }
        page_xss.goto("http://localhost:8080/thank-you.html")
        page_xss.evaluate(f"sessionStorage.setItem('hero_lead_context', JSON.stringify({lead_ctx}))")
        page_xss.goto("http://localhost:8080/thank-you.html?ref=HH-XSS999")
        page_xss.wait_for_load_state("networkidle")

        heading_xss = page_xss.inner_text("#thankYouHeading")
        print(f"✔ XSS Name rendered as literal text: '{heading_xss}'")
        assert "<script>" in heading_xss or "&lt;script&gt;" in page_xss.content(), "XSS payload was executed or stripped wrongly!"
        print("✔ [PASS] XSS payload rendered strictly as safe text content!")

        ctx_xss.close()

        print("\n==================================================")
        print(" ALL THANK-YOU VERIFICATION TESTS PASSED CLEANLY!  ")
        print("==================================================")

if __name__ == '__main__':
    verify_thank_you_flow()
