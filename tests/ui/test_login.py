from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            reset_app_state()

            page.goto("http://127.0.0.1:8000/")
            page.fill("#username", "nikeuser")
            page.fill("#password", "1234")
            page.click("#login-button")
            page.wait_for_url("**/products")

            assert "products" in page.url.lower()
            print("Login UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_login")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_login()