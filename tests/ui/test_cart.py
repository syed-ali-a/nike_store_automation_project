from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_cart_flow():
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

            # Open first product
            page.locator(".product-image").first.click()
            page.wait_for_url("**/product/**")

            # Select size
            size_dropdown = page.locator("#selected-size")
            size_dropdown.select_option(index=1)
            selected_size = size_dropdown.input_value()

            # Select color
            color_dropdown = page.locator("#selected-color")
            selected_color = color_dropdown.input_value()

            # Change color if possible
            options = color_dropdown.locator("option")
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

            # Validate table exists
            table = page.locator("#cart-table")
            assert table.is_visible()

            # Get first row
            rows = page.locator("#cart-body tr")
            assert rows.count() > 0

            first_row = rows.first

            # Validate product name
            product_text = first_row.inner_text()
            assert "Nike" in product_text

            # Validate size
            assert selected_size in product_text

            # Validate color
            assert selected_color in product_text

            # Validate image
            cart_image = first_row.locator("img")
            cart_image_src = cart_image.get_attribute("src")

            assert cart_image_src is not None
            assert cart_image_src == expected_image

            print("Cart UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_cart")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_cart_flow()