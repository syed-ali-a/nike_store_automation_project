import requests

BASE_URL = "http://127.0.0.1:8000"


def reset_app_state():
    requests.get(f"{BASE_URL}/reset")


def test_dashboard_summary_api():
    reset_app_state()

    response = requests.get(f"{BASE_URL}/api/dashboard-summary")
    assert response.status_code == 200

    data = response.json()
    assert "total_orders" in data
    assert "total_products_purchased" in data
    assert "total_money_spent" in data
    assert "cart_count" in data

    print("Dashboard Summary API test passed")


if __name__ == "__main__":
    test_dashboard_summary_api()