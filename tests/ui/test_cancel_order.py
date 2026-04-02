from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_cancel_order():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            reset_app_state()

            # Login
            page.goto("http://127.0.0.1:8000/")
            page.fill("#username", "nikeuser")
            page.fill("#password", "1234")
            page.click("#login-button")
            page.wait_for_url("**/products")

            # Add product
            page.locator(".product-image").first.click()
            page.wait_for_url("**/product/**")

            page.select_option("#selected-size", index=1)
            page.select_option("#selected-color", index=1)

            page.click("#add-to-cart-details")
            page.wait_for_url("**/cart")

            # Checkout
            page.click("#checkout-button")
            page.wait_for_url("**/dashboard")

            # Go to orders
            page.goto("http://127.0.0.1:8000/orders")

            # Ensure orders exist
            row_count = page.locator("#orders-body tr").count()
            assert row_count > 0

            # Click cancel on first cancellable order
            cancel_buttons = page.locator(".cancel-btn")
            assert cancel_buttons.count() > 0

            cancel_buttons.first.click()

            # App redirects to dashboard after cancel
            page.wait_for_url("**/dashboard")

            # Go back to orders page to validate cancelled status
            page.goto("http://127.0.0.1:8000/orders")

            cancelled_status = page.locator(".status-cancelled")
            assert cancelled_status.count() > 0
            assert cancelled_status.first.is_visible()

            print("Cancel Order UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_cancel_order")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_cancel_order()