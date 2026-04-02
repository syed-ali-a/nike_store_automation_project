from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_different_variant_separate_line():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            reset_app_state()

            # Login
            page.goto("http://127.0.0.1:8000/")
            page.fill('input[name="username"]', "nikeuser")
            page.fill('input[name="password"]', "1234")
            page.click('button[type="submit"]')
            page.wait_for_url("**/products")

            # Open same product first time
            page.click('a[href="/product/1"]')
            page.wait_for_url("**/product/**")

            # Add variant 1: Size 8, Black
            page.select_option('select[name="selected_size"]', "8")
            page.select_option('select[name="selected_color"]', "Black")
            page.click('button[type="submit"]')
            page.wait_for_url("**/cart")

            # Open same product second time
            page.goto("http://127.0.0.1:8000/product/1")

            # Add variant 2: Size 9, Black
            page.select_option('select[name="selected_size"]', "9")
            page.select_option('select[name="selected_color"]', "Black")
            page.click('button[type="submit"]')
            page.wait_for_url("**/cart")

            # Validate cart now has 2 separate rows
            rows = page.locator("#cart-body tr")
            row_count = rows.count()
            assert row_count == 2

            # Validate sizes are different
            first_size = rows.nth(0).locator("td:nth-child(2)").inner_text()
            second_size = rows.nth(1).locator("td:nth-child(2)").inner_text()

            assert first_size != second_size
            assert {"8", "9"} == {first_size, second_size}

            print("Different Variant Separate Line UI test passed")

        except Exception:
            save_failure_screenshot(page, "test_different_variant_separate_line")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_different_variant_separate_line()