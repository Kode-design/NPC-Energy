from playwright.sync_api import Page, expect, sync_playwright

def verify_fixes(page: Page):
    page.goto("http://localhost:8000/index.html")

    # Start Game
    page.get_by_role("button", name="START GAME").click()
    page.wait_for_timeout(1000)

    # Skip dialogue
    for _ in range(15):
        if page.locator("#dialogue-box").is_visible():
            if page.locator(".choice-btn").count() > 0:
                 page.locator(".choice-btn").first.click()
            else:
                 page.keyboard.press("Space")
            page.wait_for_timeout(200)
        else:
            break

    # Move to Bed (Target X=500. Start=200. Delta=300. Speed=3. Frames=100)
    for _ in range(100):
        page.keyboard.press("ArrowRight")

    # Interact with Backpack
    page.keyboard.press("Space")
    page.wait_for_timeout(1000)

    # Skip "Backpack Acquired" dialogue
    for _ in range(5):
        if page.locator("#dialogue-box").is_visible():
             page.keyboard.press("Space")
             page.wait_for_timeout(200)
        else:
            break

    # Take screenshot to verify backpack is GONE
    page.screenshot(path="verification/3_backpack_gone.png")

    # Move to exit (Target > 600. Current ~500. Delta=150. Frames=50)
    for _ in range(60):
        page.keyboard.press("ArrowRight")

    # Wait for transition (1000ms fade)
    page.wait_for_timeout(2000)

    # Verify we are outside.
    # Outside background is blue #85c1e9. Home is #d7bde2.
    # We can just take a screenshot.
    page.screenshot(path="verification/4_scene_outside.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            verify_fixes(page)
            print("Verification script completed successfully.")
        except Exception as e:
            print(f"Verification failed: {e}")
        finally:
            browser.close()
