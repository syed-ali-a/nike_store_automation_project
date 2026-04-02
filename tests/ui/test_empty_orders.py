from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_empty_orders():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Reset app → ensures NO orders
            reset_app_state()

            # Login
            page.goto("http://127.0.0.1:8000/")
            page.fill("#username", "nikeuser")
            page.fill("#password", "1234")
            page.click("#login-button")
            page.wait_for_url("**/products")

            # Go directly to orders page
            page.goto("http://127.0.0.1:8000/orders")

            # Validate empty state is visible
            assert page.locator("#empty-orders").is_visible()

            # Validate table is NOT present
            assert page.locator("#orders-table").count() == 0

            print("Empty Orders UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_empty_orders")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_empty_orders()