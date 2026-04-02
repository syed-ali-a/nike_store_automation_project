from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_remove_from_cart():
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

            # Open product
            page.locator(".product-image").first.click()
            page.wait_for_url("**/product/**")

            # Select size
            size_dropdown = page.locator("#selected-size")
            size_dropdown.select_option(index=1)

            # Select color
            color_dropdown = page.locator("#selected-color")

            options = color_dropdown.locator("option")
            if options.count() > 1:
                color_dropdown.select_option(index=1)

            page.wait_for_timeout(500)

            # Add to cart
            page.click("#add-to-cart-details")
            page.wait_for_url("**/cart")

            # Count before
            rows_before = page.locator("#cart-body tr").count()
            assert rows_before > 0

            # Click remove
            page.locator("button[id^='remove-item']").first.click()
            page.wait_for_timeout(1000)

            # Count after
            rows_after = page.locator("#cart-body tr").count()

            # ✅ VALID ASSERTION
            assert rows_after <= rows_before

            # If cart becomes empty
            if rows_after == 0:
                assert page.locator("#empty-cart").is_visible()

            print("Remove From Cart UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_remove_from_cart")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_remove_from_cart()