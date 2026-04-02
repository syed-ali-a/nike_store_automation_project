import requests

BASE_URL = "http://127.0.0.1:8000"


def reset_app_state():
    requests.get(f"{BASE_URL}/reset")


def add_product_to_cart():
    response = requests.post(
        f"{BASE_URL}/add-to-cart/1",
        data={
            "selected_size": "8",
            "selected_color": "Black"
        },
        allow_redirects=False
    )
    assert response.status_code in [302, 303]


def checkout_cart():
    response = requests.post(f"{BASE_URL}/checkout", allow_redirects=False)
    assert response.status_code in [302, 303]


def test_dashboard_api_after_checkout():
    reset_app_state()

    # Before checkout
    response = requests.get(f"{BASE_URL}/api/dashboard-summary")
    assert response.status_code == 200
    before_data = response.json()

    assert before_data["total_orders"] == 0
    assert before_data["total_products_purchased"] == 0
    assert before_data["total_money_spent"] == 0
    assert before_data["cart_count"] == 0

    # Add product -> cart count should increase
    add_product_to_cart()

    response = requests.get(f"{BASE_URL}/api/dashboard-summary")
    cart_data = response.json()
    assert cart_data["cart_count"] == 1

    # Checkout -> orders and totals should increase, cart count should go 0
    checkout_cart()

    response = requests.get(f"{BASE_URL}/api/dashboard-summary")
    after_data = response.json()

    assert after_data["total_orders"] == 1
    assert after_data["total_products_purchased"] == 1
    assert after_data["total_money_spent"] == 12995
    assert after_data["cart_count"] == 0

    print("Dashboard API After Checkout test passed")


if __name__ == "__main__":
    test_dashboard_api_after_checkout()