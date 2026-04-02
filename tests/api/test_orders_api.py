import requests

BASE_URL = "http://127.0.0.1:8000"


def reset_app_state():
    requests.get(f"{BASE_URL}/reset")


def test_orders_api():
    reset_app_state()

    response = requests.get(f"{BASE_URL}/api/orders")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        first_order = data[0]
        assert "order_id" in first_order
        assert "product_name" in first_order
        assert "category" in first_order
        assert "amount" in first_order
        assert "quantity" in first_order
        assert "status" in first_order

    print("Orders API test passed")


if __name__ == "__main__":
    test_orders_api()