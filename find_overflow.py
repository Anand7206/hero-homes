from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 360, 'height': 800})
    page.goto("http://localhost:8080/")
    page.wait_for_load_state("networkidle")

    overflowing = page.evaluate("""() => {
        const results = [];
        const docW = window.innerWidth;
        const els = document.querySelectorAll('*');
        els.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.right > docW + 1) {
                results.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    right: rect.right,
                    width: rect.width,
                    text: el.innerText ? el.innerText.substring(0, 30) : ''
                });
            }
        });
        return results;
    }""")

    print(f"Elements overflowing 360px viewport (count: {len(overflowing)}):")
    for item in overflowing[:15]:
        print(item)

    browser.close()
