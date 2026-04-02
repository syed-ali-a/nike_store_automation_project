from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_invalid_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            reset_app_state()

            page.goto("http://127.0.0.1:8000/")
            page.fill("#username", "wronguser")
            page.fill("#password", "wrongpass")
            page.click("#login-button")

            assert page.locator("#login-error").is_visible()
            assert "Invalid username or password" in page.locator("#login-error").inner_text()

            print("Invalid Login UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_invalid_login")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_invalid_login()