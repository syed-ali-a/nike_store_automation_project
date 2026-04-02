from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_remove_specific_variant():
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

            size_dropdown = page.locator("#selected-size")
            color_dropdown = page.locator("#selected-color")

            # Add first variant
            size_dropdown.select_option(index=1)
            first_size = size_dropdown.input_value()

            color_dropdown.select_option(index=0)
            first_color = color_dropdown.input_value()

            page.click("#add-to-cart-details")
            page.wait_for_url("**/cart")

            # Back to same product
            page.goto("http://127.0.0.1:8000/products")
            page.locator(".product-image").first.click()
            page.wait_for_url("**/product/**")

            size_dropdown = page.locator("#selected-size")
            color_dropdown = page.locator("#selected-color")

            # Add second variant: try different size first
            option_count = size_dropdown.locator("option").count()
            if option_count > 2:
                size_dropdown.select_option(index=2)
            else:
                size_dropdown.select_option(index=1)
            second_size = size_dropdown.input_value()

            # If size didn't change, force different color
            color_option_count = color_dropdown.locator("option").count()
            if second_size == first_size and color_option_count > 1:
                for i in range(color_option_count):
                    value = color_dropdown.locator("option").nth(i).get_attribute("value")
                    if value != first_color:
                        color_dropdown.select_option(value)
                        break

            second_color = color_dropdown.input_value()

            # Ensure second variant is actually different
            assert (second_size != first_size) or (second_color != first_color)

            page.click("#add-to-cart-details")
            page.wait_for_url("**/cart")

            rows = page.locator("#cart-body tr")
            rows_before = rows.count()
            assert rows_before >= 2

            # Capture first row text before remove
            first_row_text_before = rows.nth(0).inner_text()

            # Remove first row
            page.locator("button[id^='remove-item']").first.click()
            page.wait_for_timeout(1000)

            rows_after_locator = page.locator("#cart-body tr")
            rows_after = rows_after_locator.count()

            # Row count should reduce by 1, or cart may become empty if only one matched item existed
            assert rows_after == rows_before - 1 or page.locator("#empty-cart").count() == 1

            # If one row still exists, it should not be identical to removed first row
            if rows_after > 0:
                remaining_first_row_text = rows_after_locator.nth(0).inner_text()
                assert remaining_first_row_text != first_row_text_before

            print("Remove Specific Variant Test Passed")

        except Exception:
            save_failure_screenshot(page, "test_remove_specific_variant")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_remove_specific_variant()