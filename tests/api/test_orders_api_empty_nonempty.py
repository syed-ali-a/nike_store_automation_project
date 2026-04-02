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


def test_orders_api_empty_nonempty():
    reset_app_state()

    # Empty orders check
    response = requests.get(f"{BASE_URL}/api/orders")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

    # Add item and checkout
    add_product_to_cart()
    checkout_cart()

    # Non-empty orders check
    response = requests.get(f"{BASE_URL}/api/orders")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    first_order = data[0]
    assert first_order["product_name"] == "Nike Air Max 270"
    assert first_order["status"] == "Placed"

    print("Orders API Empty/Non-Empty test passed")


if __name__ == "__main__":
    test_orders_api_empty_nonempty()