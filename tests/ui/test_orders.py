from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_orders_flow():
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

            page.goto("http://127.0.0.1:8000/orders")

            assert "/orders" in page.url
            assert page.locator("#orders-table").is_visible()

            row_count = page.locator("#orders-body tr").count()
            assert row_count > 0

            print("Orders UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_orders")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_orders_flow()