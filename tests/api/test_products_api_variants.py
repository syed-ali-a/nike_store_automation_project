import requests


def test_products_api_variants():
    response = requests.get("http://127.0.0.1:8000/api/products")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for product in data:
        # Basic keys
        assert "name" in product
        assert "image" in product
        assert "default_color" in product
        assert "images_by_color" in product

        images_map = product["images_by_color"]
        default_color = product["default_color"]

        # Validate mapping
        assert isinstance(images_map, dict)
        assert default_color in images_map

        # Each color should have image
        for color, img in images_map.items():
            assert img is not None
            assert img != ""

    print("Products API Variant Test Passed")


if __name__ == "__main__":
    test_products_api_variants()