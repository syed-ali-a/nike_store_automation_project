import requests

BASE_URL = "http://127.0.0.1:8000"


def reset_app_state():
    requests.get(f"{BASE_URL}/reset")


def add_product_to_cart():
    # product 1 with one size/color
    response = requests.post(
        f"{BASE_URL}/add-to-cart/1",
        data={
            "selected_size": "8",
            "selected_color": "Black"
        },
        allow_redirects=False
    )
    assert response.status_code in [302, 303]


def test_cart_api_empty_nonempty():
    reset_app_state()

    # Empty cart check
    response = requests.get(f"{BASE_URL}/api/cart")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

    # Add one product
    add_product_to_cart()

    # Non-empty cart check
    response = requests.get(f"{BASE_URL}/api/cart")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    first_item = data[0]
    assert first_item["product_id"] == 1
    assert first_item["selected_size"] == "8"
    assert first_item["selected_color"] == "Black"

    print("Cart API Empty/Non-Empty test passed")


if __name__ == "__main__":
    test_cart_api_empty_nonempty()