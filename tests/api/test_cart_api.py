import requests

BASE_URL = "http://127.0.0.1:8000"


def reset_app_state():
    requests.get(f"{BASE_URL}/reset")


def test_cart_api():
    reset_app_state()

    response = requests.get(f"{BASE_URL}/api/cart")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        first_item = data[0]
        assert "product_id" in first_item
        assert "name" in first_item
        assert "price" in first_item
        assert "quantity" in first_item

    print("Cart API test passed")


if __name__ == "__main__":
    test_cart_api()