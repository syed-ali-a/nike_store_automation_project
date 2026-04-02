from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_dashboard_update_after_cancel():
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

            # Go to first product
            page.locator(".product-image").first.click()
            page.wait_for_url("**/product/**")

            # Select size and color
            page.select_option("#selected-size", index=1)
            page.select_option("#selected-color", index=1)

            # Add to cart
            page.click("#add-to-cart-details")
            page.wait_for_url("**/cart")

            # Checkout -> dashboard
            page.click("#checkout-button")
            page.wait_for_url("**/dashboard")

            # Read dashboard values after checkout
            total_orders_after_checkout = int(page.locator("#total-orders").inner_text())
            total_products_after_checkout = int(page.locator("#total-products").inner_text())

            assert total_orders_after_checkout >= 1
            assert total_products_after_checkout >= 1

            # Go to orders and cancel
            page.goto("http://127.0.0.1:8000/orders")

            cancel_buttons = page.locator(".cancel-btn")
            assert cancel_buttons.count() > 0

            cancel_buttons.first.click()
            page.wait_for_url("**/dashboard")

            # Read dashboard values after cancel
            total_orders_after_cancel = int(page.locator("#total-orders").inner_text())
            total_products_after_cancel = int(page.locator("#total-products").inner_text())

            # Dashboard should reduce because cancelled orders are excluded
            assert total_orders_after_cancel < total_orders_after_checkout
            assert total_products_after_cancel < total_products_after_checkout

            print("Dashboard Update After Cancel UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_dashboard_update_after_cancel")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_dashboard_update_after_cancel()