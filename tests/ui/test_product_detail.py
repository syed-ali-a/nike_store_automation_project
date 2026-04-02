from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_product_detail_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            reset_app_state()

            # Open login page
            page.goto("http://127.0.0.1:8000/")

            # Login
            page.fill("#username", "nikeuser")
            page.fill("#password", "1234")
            page.click("#login-button")
            page.wait_for_url("**/products")

            # Open first product
            page.locator(".product-image").first.click()
            page.wait_for_url("**/product/**")

            # Validate product name visible
            assert page.locator("#product-name").is_visible()

            # Validate product image visible
            product_image = page.locator("#product-image")
            assert product_image.is_visible()

            # Capture default image src
            default_src = product_image.get_attribute("src")
            assert default_src is not None
            assert default_src != ""

            # Validate size dropdown
            size_dropdown = page.locator("#selected-size")
            assert size_dropdown.is_visible()
            size_dropdown.select_option(index=1)

            # Validate color dropdown
            color_dropdown = page.locator("#selected-color")
            assert color_dropdown.is_visible()

            # Validate default selected color exists
            default_color = color_dropdown.input_value()
            assert default_color is not None
            assert default_color != ""

            # Change color only if there is more than one option
            options = color_dropdown.locator("option")
            option_count = options.count()
            assert option_count > 0

            if option_count > 1:
                current_value = color_dropdown.input_value()

                new_value = None
                for i in range(option_count):
                    value = options.nth(i).get_attribute("value")
                    if value != current_value:
                        new_value = value
                        break

                assert new_value is not None

                color_dropdown.select_option(new_value)
                page.wait_for_timeout(500)

                updated_src = product_image.get_attribute("src")
                assert updated_src is not None
                assert updated_src != ""

                # Image should change when color changes
                assert updated_src != default_src

            # Validate add to cart button
            assert page.locator("#add-to-cart-details").is_visible()

            print("Product Detail UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_product_detail")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_product_detail_page()