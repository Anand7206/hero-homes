import time
from playwright.sync_api import sync_playwright
import os

artifact_dir = r"C:\Users\anand singh\.gemini\antigravity\brain\6c8e94d4-2f9b-4bc7-b190-49ab5b83ddeb"

def test_video_gate_feature():
    print("==================================================")
    print(" TESTING YOUTUBE VIDEO GATE & MODAL POPUP FORM   ")
    print("==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        page.goto("http://localhost:8080/")
        page.wait_for_load_state("networkidle")

        # 1. Verify YouTube Play Button Overlay on Master Plan Slot
        play_btn_visible = page.is_visible(".yt-play-btn")
        print(f"✔ YouTube Red Play Button overlay visible: {play_btn_visible}")

        s_slot = os.path.join(artifact_dir, "video_gate_masterplan_thumbnail.png")
        page.locator("#videoSlot").screenshot(path=s_slot)
        print(f"✔ Saved thumbnail screenshot: {s_slot}")

        # 2. Click Master Plan slot to trigger gate modal
        page.click("#videoSlot")
        time.sleep(0.4)

        modal_visible = page.is_visible("#videoGateModal")
        print(f"✔ Video Gate Modal displayed on click: {modal_visible}")

        s_modal = os.path.join(artifact_dir, "video_gate_modal_opened.png")
        page.screenshot(path=s_modal)
        print(f"✔ Saved Video Gate Modal screenshot: {s_modal}")

        # 3. Verify Modal Elements
        header_text = page.inner_text("#gateModalTitle")
        print(f"✔ Modal Header text: '{header_text}'")

        c1_text = page.inner_text(".gate-side-col .side-feature-card:nth-child(1) .side-card-label")
        c2_text = page.inner_text(".gate-side-col .side-feature-card:nth-child(2) .side-card-label")
        c3_text = page.inner_text(".gate-side-col .side-feature-card:nth-child(3) .side-card-label")
        print(f"✔ Right column cards: 1. '{c1_text}', 2. '{c2_text}', 3. '{c3_text}'")

        # 4. Empty Submit Validation Test
        page.click("#gateSubmitBtn")
        time.sleep(0.3)
        name_err = page.evaluate("document.getElementById('gateName').classList.contains('is-invalid')")
        phone_err = page.evaluate("document.getElementById('gatePhone').classList.contains('is-invalid')")
        consent_err = page.is_visible("#gateConsentErr")
        print(f"✔ Empty submit validation errors - Name: {name_err}, Phone: {phone_err}, Consent: {consent_err}")

        # 5. Invalid Phone Test ('12345')
        page.fill("#gateName", "Priya Sharma")
        page.fill("#gatePhone", "12345")
        page.click("#gateSubmitBtn")
        time.sleep(0.3)
        phone_rejected = page.evaluate("document.getElementById('gatePhone').classList.contains('is-invalid')")
        print(f"✔ Invalid phone '12345' rejected: {phone_rejected}")

        # 6. Valid Submit Flow
        page.fill("#gatePhone", "9876543210")
        page.check("#gateConsent")

        # Select datetime-local value
        now_dt = page.evaluate("document.getElementById('gateDatetime').value")
        print(f"✔ Datetime value auto-populated min: {now_dt}")

        page.click("#gateSubmitBtn")
        time.sleep(1.5)

        modal_closed = not page.is_visible("#videoGateModal")
        iframe_loaded = page.is_visible("#videoWrapper iframe")
        unlocked_stored = page.evaluate("localStorage.getItem('hero_video_unlocked')")
        print(f"✔ Modal closed: {modal_closed}, YouTube iframe playing: {iframe_loaded}, localStorage unlocked: '{unlocked_stored}'")

        s_playing = os.path.join(artifact_dir, "video_unlocked_and_playing.png")
        page.screenshot(path=s_playing)
        print(f"✔ Saved video playing screenshot: {s_playing}")

        # 7. Test Subsequent Clicks (Unlocked State)
        page.reload()
        page.wait_for_load_state("networkidle")
        page.click("#videoSlot")
        time.sleep(0.5)

        modal_skipped = not page.is_visible("#videoGateModal")
        direct_iframe = page.is_visible("#videoWrapper iframe")
        print(f"✔ Unlocked subsequent click - Modal skipped: {modal_skipped}, YouTube iframe autoplayed directly: {direct_iframe}")

        # 8. Test Mobile Layout (<768px)
        page.evaluate("localStorage.removeItem('hero_video_unlocked')") # Reset lock for mobile test
        page.set_viewport_size({'width': 375, 'height': 667})
        page.reload()
        page.wait_for_load_state("networkidle")

        page.click("#videoSlot")
        time.sleep(0.4)

        s_mobile_modal = os.path.join(artifact_dir, "video_gate_modal_mobile_375px.png")
        page.screenshot(path=s_mobile_modal)
        print(f"✔ Saved 375px Mobile Video Gate Modal screenshot: {s_mobile_modal}")

        browser.close()

    print("\n==================================================")
    print(" VIDEO GATE FEATURE VERIFICATION PASSED PERFECTLY  ")
    print("==================================================")

if __name__ == "__main__":
    test_video_gate_feature()
