import requests

BASE_URL = "http://127.0.0.1:8000"


def reset_app_state():
    requests.get(f"{BASE_URL}/reset")


def test_products_api():
    reset_app_state()

    response = requests.get(f"{BASE_URL}/api/products")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    first_product = data[0]
    assert "id" in first_product
    assert "name" in first_product
    assert "price" in first_product
    assert "category" in first_product

    print("Products API test passed")


if __name__ == "__main__":
    test_products_api()