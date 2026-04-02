from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_dashboard_flow():
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

            page.locator(".product-image").first.click()
            page.wait_for_url("**/product/**")

            page.select_option("#selected-size", index=1)
            page.select_option("#selected-color", index=1)

            page.click("#add-to-cart-details")
            page.wait_for_url("**/cart")

            page.click("#checkout-button")
            page.wait_for_url("**/dashboard")

            assert page.locator("#total-orders").is_visible()
            assert page.locator("#total-products").is_visible()
            assert page.locator("#total-money").is_visible()
            assert page.locator("#cart-count").is_visible()

            assert page.locator("#most-ordered-category").is_visible()
            assert page.locator("#rewards-points").is_visible()
            assert page.locator("#most-product").is_visible()
            assert page.locator("#avg-order-value").is_visible()

            total_orders = page.inner_text("#total-orders")
            assert int(total_orders) >= 1

            print("Dashboard UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_dashboard")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_dashboard_flow()