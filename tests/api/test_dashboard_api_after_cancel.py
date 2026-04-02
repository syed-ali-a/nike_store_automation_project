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


def cancel_first_order():
    response = requests.get(f"{BASE_URL}/api/orders")
    assert response.status_code == 200
    orders = response.json()
    assert len(orders) > 0

    first_order_id = orders[0]["order_id"]

    cancel_response = requests.post(
        f"{BASE_URL}/cancel-order/{first_order_id}",
        allow_redirects=False
    )
    assert cancel_response.status_code in [302, 303]


def test_dashboard_api_after_cancel():
    reset_app_state()

    add_product_to_cart()
    checkout_cart()

    # After checkout
    response = requests.get(f"{BASE_URL}/api/dashboard-summary")
    assert response.status_code == 200
    after_checkout = response.json()

    assert after_checkout["total_orders"] == 1
    assert after_checkout["total_products_purchased"] == 1
    assert after_checkout["total_money_spent"] == 12995
    assert after_checkout["cart_count"] == 0

    # Cancel order
    cancel_first_order()

    # After cancel
    response = requests.get(f"{BASE_URL}/api/dashboard-summary")
    assert response.status_code == 200
    after_cancel = response.json()

    assert after_cancel["total_orders"] == 0
    assert after_cancel["total_products_purchased"] == 0
    assert after_cancel["total_money_spent"] == 0
    assert after_cancel["cart_count"] == 0

    print("Dashboard API After Cancel test passed")


if __name__ == "__main__":
    test_dashboard_api_after_cancel()