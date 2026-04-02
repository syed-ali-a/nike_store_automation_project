from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_empty_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            reset_app_state()

            page.goto("http://127.0.0.1:8000/")
            page.click("#login-button")

            assert page.url == "http://127.0.0.1:8000/"

            username_valid = page.locator("#username").evaluate("el => el.checkValidity()")
            password_valid = page.locator("#password").evaluate("el => el.checkValidity()")

            assert username_valid is False
            assert password_valid is False

            print("Empty Login UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_empty_login")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_empty_login()