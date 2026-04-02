import subprocess
import sys
import time
from generate_report import generate_reports


TEST_GROUPS = {
    # ================= UI TESTS =================
    "UI-1": [("tests/ui/test_login.py", "UI - Login", "Valid login and redirect to products page")],
    "UI-2": [("tests/ui/test_invalid_login.py", "UI - Invalid Login", "Invalid credentials should show error")],
    "UI-3": [("tests/ui/test_empty_login.py", "UI - Empty Login", "Empty login should show validation message")],
    "UI-4": [("tests/ui/test_products.py", "UI - Products", "Products page loads with items")],
    "UI-5": [("tests/ui/test_product_detail.py", "UI - Product Detail", "Product detail page loads correctly")],
    "UI-6": [("tests/ui/test_product_image_change_by_color.py", "UI - Product Image Change By Color", "Image updates when color changes")],
    "UI-7": [("tests/ui/test_cart.py", "UI - Cart", "Product can be added to cart")],
    "UI-8": [("tests/ui/test_cart_selected_color_image.py", "UI - Cart Selected Color Image", "Cart shows correct image based on color")],
    "UI-9": [("tests/ui/test_remove_from_cart.py", "UI - Remove Cart", "User can remove item from cart (variant aware)")],
    "UI-10": [("tests/ui/test_same_variant_quantity.py", "UI - Same Variant Quantity", "Same variant increases quantity")],
    "UI-11": [("tests/ui/test_different_variant_separate_line.py", "UI - Different Variant Separate Line", "Different variants shown separately")],
    "UI-12": [("tests/ui/test_remove_specific_variant.py", "UI - Remove Specific Variant", "Removes only selected variant")],
    "UI-13": [("tests/ui/test_checkout_cart_clear.py", "UI - Checkout", "Checkout clears cart")],
    "UI-14": [("tests/ui/test_orders.py", "UI - Orders", "Orders page displays data")],
    "UI-15": [("tests/ui/test_empty_orders.py", "UI - Empty Orders", "Empty orders handled correctly")],
    "UI-16": [("tests/ui/test_cancel_order.py", "UI - Cancel Order", "Order can be cancelled")],
    "UI-17": [("tests/ui/test_dashboard.py", "UI - Dashboard", "Dashboard loads correctly")],
    "UI-18": [("tests/ui/test_dashboard_update_after_cancel.py", "UI - Dashboard Update", "Dashboard updates after cancel")],

    # ================= API TESTS =================
    "API-1": [("tests/api/test_products_api.py", "API - Products", "Fetch all products successfully")],
    "API-2": [("tests/api/test_products_api_variants.py", "API - Product Variants", "Validate color-image mapping")],
    "API-3": [("tests/api/test_cart_api.py", "API - Cart", "Cart API returns correct data")],
    "API-4": [("tests/api/test_orders_api.py", "API - Orders", "Orders API returns data")],
    "API-5": [("tests/api/test_dashboard_summary_api.py", "API - Dashboard", "Dashboard summary metrics correct")],
    "API-6": [("tests/api/test_cart_api_empty_nonempty.py", "API - Cart State", "Handles empty/non-empty cart")],
    "API-7": [("tests/api/test_orders_api_empty_nonempty.py", "API - Orders State", "Handles empty/non-empty orders")],
    "API-8": [("tests/api/test_dashboard_api_after_checkout.py", "API - After Checkout", "Dashboard updates after checkout")],
    "API-9": [("tests/api/test_dashboard_api_after_cancel.py", "API - After Cancel", "Dashboard updates after cancel")],
}


def run_test(file_path, label, description):
    print(f"\n🧪 Running: {label}")
    print(f"📌 What it checks: {description}\n")

    start_time = time.time()
    result = subprocess.run([sys.executable, file_path])
    end_time = time.time()

    duration = round(end_time - start_time, 2)

    if result.returncode == 0:
        print(f"✅ PASSED: {label}")
        print(f"✔ {description}")
        return {
            "name": label,
            "status": "PASS",
            "description": description,
            "time": duration,
            "screenshot": ""
        }
    else:
        print(f"❌ FAILED: {label}")
        print(f"✖ {description}")
        return {
            "name": label,
            "status": "FAIL",
            "description": description,
            "time": duration,
            "screenshot": ""
        }


def print_menu():
    print("\n===== TEST RUNNER MENU =====")

    print("\n--- UI TESTS ---")
    for key, tests in TEST_GROUPS.items():
        if key.startswith("UI-"):
            label = tests[0][1]
            print(f"{key:<6} - {label}")

    print("\n--- API TESTS ---")
    for key, tests in TEST_GROUPS.items():
        if key.startswith("API-"):
            label = tests[0][1]
            print(f"{key:<6} - {label}")

    print("\n--- RUN GROUPS ---")
    print("ALL-UI - Run All UI Tests")
    print("ALL-API - Run All API Tests")
    print("ALL    - Run Complete Suite")


def run_group(prefix):
    results = []
    for key, tests in TEST_GROUPS.items():
        if key.startswith(prefix):
            for file_path, label, description in tests:
                results.append(run_test(file_path, label, description))
    return results


def run_all():
    results = []
    for tests in TEST_GROUPS.values():
        for file_path, label, description in tests:
            results.append(run_test(file_path, label, description))
    return results


def main():
    print_menu()

    choice = input("\nEnter your choice: ").strip().upper()

    if choice == "ALL-UI":
        results = run_group("UI")
    elif choice == "ALL-API":
        results = run_group("API")
    elif choice == "ALL":
        results = run_all()
    elif choice in TEST_GROUPS:
        tests = TEST_GROUPS[choice]
        results = []
        for file_path, label, description in tests:
            results.append(run_test(file_path, label, description))
    else:
        print("❌ Invalid choice")
        return

    print("\n========================")
    passed = all(r["status"] == "PASS" for r in results)

    if passed:
        print("🎉 ALL SELECTED TESTS PASSED")
    else:
        print("⚠️ SOME TESTS FAILED")
    print("========================")

    print("\n===== TEST SUMMARY =====")
    for r in results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"{icon} {r['name']} → {r['description']}")

    generate_reports(results)


if __name__ == "__main__":
    main()