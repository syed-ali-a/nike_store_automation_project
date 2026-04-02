from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_cart_selected_color_image():
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

            # Select color
            color_dropdown = page.locator("#selected-color")
            options = color_dropdown.locator("option")

            selected_color = color_dropdown.input_value()

            if options.count() > 1:
                for i in range(options.count()):
                    value = options.nth(i).get_attribute("value")
                    if value != selected_color:
                        color_dropdown.select_option(value)
                        selected_color = value
                        break

            page.wait_for_timeout(500)

            # Capture expected image
            expected_image = page.locator("#product-image").get_attribute("src")

            # Add to cart
            page.click("#add-to-cart-details")
            page.wait_for_url("**/cart")

            # Get cart image
            row = page.locator("#cart-body tr").first
            cart_image = row.locator("img").get_attribute("src")

            assert cart_image == expected_image

            print("Cart Selected Color Image Test Passed")

        except Exception:
            save_failure_screenshot(page, "test_cart_selected_color_image")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_cart_selected_color_image()