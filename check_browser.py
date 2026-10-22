import os
from playwright.sync_api import sync_playwright

html_path = os.path.abspath('frontend/index.html')
file_url = f'file:///{html_path.replace(os.sep, "/")}'

print('Opening:', file_url)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    errors = []
    page.on('console', lambda msg: errors.append(f'[{msg.type}] {msg.text}') if msg.type in ['error', 'warning'] else None)
    page.on('pageerror', lambda exc: errors.append(f'[PAGE ERROR] {exc}'))

    page.goto(file_url)
    page.wait_for_timeout(3000)

    print('Captured console messages/errors:')
    for err in errors:
        print('  ', err)

    # Check #app text content and visible
    app_el = page.query_selector('#app')
    if app_el:
        is_visible = app_el.is_visible()
        text = app_el.inner_text()
        print(f'#app is_visible: {is_visible}')
        print(f'#app inner_text length: {len(text)}')
        print(f'#app preview: {repr(text[:200])}')
    else:
        print('#app element NOT FOUND!')

    browser.close()

