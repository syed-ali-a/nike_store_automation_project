from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_product_image_change_by_color():
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

            image = page.locator("#product-image")
            color_dropdown = page.locator("#selected-color")

            # Get initial image
            initial_src = image.get_attribute("src")

            options = color_dropdown.locator("option")

            if options.count() > 1:
                for i in range(options.count()):
                    value = options.nth(i).get_attribute("value")

                    color_dropdown.select_option(value)
                    page.wait_for_timeout(500)

                    new_src = image.get_attribute("src")

                    if new_src != initial_src:
                        break

                assert new_src != initial_src

            print("Product Image Change Test Passed")

        except Exception:
            save_failure_screenshot(page, "test_product_image_change_by_color")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_product_image_change_by_color()