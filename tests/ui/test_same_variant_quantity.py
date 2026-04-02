from playwright.sync_api import sync_playwright
from test_utils import save_failure_screenshot, reset_app_state


def test_same_variant_quantity():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            reset_app_state()

            page.goto("http://127.0.0.1:8000/")
            page.fill('input[name="username"]', "nikeuser")
            page.fill('input[name="password"]', "1234")
            page.click('button[type="submit"]')
            page.wait_for_url("**/products")

            page.click('a[href="/product/1"]')
            page.select_option('select[name="selected_size"]', "8")
            page.select_option('select[name="selected_color"]', "Black")
            page.click('button[type="submit"]')
            page.wait_for_timeout(1000)

            page.goto("http://127.0.0.1:8000/product/1")
            page.select_option('select[name="selected_size"]', "8")
            page.select_option('select[name="selected_color"]', "Black")
            page.click('button[type="submit"]')

            page.goto("http://127.0.0.1:8000/cart")

            rows = page.locator("#cart-body tr")
            row_count = rows.count()
            assert row_count == 1

            quantity_text = rows.nth(0).locator("td:nth-child(5)").inner_text()
            assert quantity_text == "2"

            print("Same Variant Quantity Test Passed")

        except Exception:
            save_failure_screenshot(page, "test_same_variant_quantity")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    test_same_variant_quantity()