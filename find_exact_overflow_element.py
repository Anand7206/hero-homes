from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 360, 'height': 800})
    page.goto('http://localhost:8080/')
    page.wait_for_load_state('networkidle')

    bad_els = page.evaluate("""() => {
        const els = document.querySelectorAll('*');
        const list = [];
        els.forEach(el => {
            const style = window.getComputedStyle(el);
            if (style.overflowX !== 'auto' && style.overflowX !== 'scroll' && el.tagName !== 'HTML' && el.tagName !== 'BODY') {
                const rect = el.getBoundingClientRect();
                if (rect.width > 360 || rect.right > 360) {
                    list.push({
                        tag: el.tagName,
                        id: el.id,
                        className: el.className,
                        rectRight: rect.right,
                        rectWidth: rect.width,
                        scrollWidth: el.scrollWidth,
                        text: el.innerText ? el.innerText.substring(0, 40) : ''
                    });
                }
            }
        });
        return list;
    }""")

    print(f"Non-scrollable elements exceeding 360px (count {len(bad_els)}):")
    for item in bad_els:
        print(item)

    browser.close()
