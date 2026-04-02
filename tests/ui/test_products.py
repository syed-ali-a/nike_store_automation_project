from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_products_page():
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

            first_product_image = page.locator(".product-image").first
            assert first_product_image.is_visible()

            first_product_image.click()
            page.wait_for_url("**/product/**")

            assert "/product/" in page.url
            assert page.locator("#product-name").is_visible()

            print("Products UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_products")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_products_page()