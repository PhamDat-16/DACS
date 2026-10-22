import time
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\LENOVO\.gemini\antigravity\brain\601e0b20-16bd-443a-b67d-50412978d4fc"

def run_slot_slider_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 950})
        page = context.new_page()

        page.on("dialog", lambda dialog: dialog.accept())
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}", flush=True))
        page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}", flush=True))

        print("1. Opening http://127.0.0.1:8000...", flush=True)
        page.goto("http://127.0.0.1:8000")
        page.wait_for_timeout(1000)

        # Login as Customer using quick fill
        print("2. Clicking Customer: demo quick fill...", flush=True)
        page.click('button:has-text("Customer:")')
        page.wait_for_timeout(400)

        print("3. Submitting Sign In...", flush=True)
        page.click('button[type="submit"]')
        page.wait_for_timeout(2000)

        # Navigate to My Bookings
        print("4. Navigating to My Bookings...", flush=True)
        page.click('button:has-text("My Bookings")')
        page.wait_for_timeout(1000)

        # Verify Slot Slider
        print("5. Verifying Slot Slider Track...", flush=True)
        slider_track = page.locator("#slotSliderTrack")
        assert slider_track.is_visible(), "Slot slider track is not visible!"

        total_slots = page.locator("#slotSliderTrack > div").count()
        print(f"Total slots rendered in slider: {total_slots}", flush=True)
        assert total_slots >= 10, f"Expected at least 10 slots in slider, got {total_slots}"

        # Test sliding with right arrow
        print("6. Clicking Right Arrow on Slider (#btnScrollSlotRight)...", flush=True)
        btn_right = page.locator("#btnScrollSlotRight")
        assert btn_right.is_visible(), "Scroll right button is not visible!"
        btn_right.click()
        page.wait_for_timeout(400)
        btn_right.click()
        page.wait_for_timeout(400)

        # Select slot B-001 on the slider
        print("7. Clicking slot B-001 on the slider...", flush=True)
        slot_b001 = page.locator("#slot-item-B-001")
        assert slot_b001.is_visible(), "Slot B-001 item is not visible on slider!"
        slot_b001.click()
        page.wait_for_timeout(500)

        # Take screenshot of the customer booking form with the slot slider
        screenshot_path = f"{ARTIFACT_DIR}\\customer_slot_slider_verified.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}", flush=True)

        # Verify selected slot code
        selected_text = page.locator("text='Vị trí bạn đã chọn:'").locator("..").inner_text()
        print(f"Selected slot text: {selected_text}", flush=True)
        assert "B-001" in selected_text, f"Expected B-001 to be selected, found: {selected_text}"

        print("=== ALL TESTS PASSED! THE CUSTOMER SLOT SLIDER IS WORKING PERFECTLY! ===", flush=True)
        browser.close()

if __name__ == "__main__":
    run_slot_slider_verification()
