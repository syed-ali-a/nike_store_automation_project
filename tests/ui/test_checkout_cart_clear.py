from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_checkout_cart_clear():
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

            # Go to product
            page.locator(".product-image").first.click()
            page.wait_for_url("**/product/**")

            # Select size & color
            page.select_option("#selected-size", index=1)
            page.select_option("#selected-color", index=1)

            # Add to cart
            page.click("#add-to-cart-details")
            page.wait_for_url("**/cart")

            # Ensure cart has items
            row_count_before = page.locator("#cart-body tr").count()
            assert row_count_before > 0

            # Click checkout
            page.click("#checkout-button")

            # Should redirect to dashboard
            page.wait_for_url("**/dashboard")
            assert "/dashboard" in page.url

            # Go back to cart
            page.goto("http://127.0.0.1:8000/cart")

            # Validate empty cart message
            assert page.locator("#empty-cart").is_visible()

            print("Checkout Cart Clear UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_checkout_cart_clear")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_checkout_cart_clear()