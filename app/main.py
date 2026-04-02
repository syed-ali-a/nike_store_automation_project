from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


# -----------------------------
# MOCK DATA
# -----------------------------

customer = {
    "username": "nikeuser",
    "password": "1234",
    "name": "Syed Ali",
    "email": "nikeuser@example.com"
}

products = [
    {
        "id": 1,
        "name": "Nike Air Max 270",
        "category": "Shoes",
        "price": 12995,
        "rating": 4.7,
        "stock": "In Stock",
        "image": "/static/images/products/airmax270_white.webp",
        "default_color": "White",
        "images_by_color": {
            "Black": "/static/images/products/airmax270_black.jpeg",
            "White": "/static/images/products/airmax270_white.webp",
            "Red": "/static/images/products/airmax270_red.webp"
        },
        "sizes": ["7", "8", "9", "10"],
        "colors": ["Black", "White", "Red"],
        "material": "Mesh & Synthetic"
    },
    {
        "id": 2,
        "name": "Nike Revolution 7",
        "category": "Running Shoes",
        "price": 4995,
        "rating": 4.4,
        "stock": "In Stock",
        "image": "/static/images/products/revolution7_blue.jpg",
        "default_color": "Blue",
        "images_by_color": {
            "Black": "/static/images/products/revolution7_black.jpg",
            "Blue": "/static/images/products/revolution7_blue.jpg"
        },
        "sizes": ["6", "7", "8", "9"],
        "colors": ["Blue", "Black"],
        "material": "Lightweight Knit"
    },
    {
        "id": 3,
        "name": "Nike Pegasus 41",
        "category": "Running Shoes",
        "price": 11995,
        "rating": 4.6,
        "stock": "In Stock",
        "image": "/static/images/products/pegasus41_blue.avif",
        "default_color": "Blue",
        "images_by_color": {
            "Black": "/static/images/products/pegasus41_black.avif",
            "Blue": "/static/images/products/pegasus41_blue.avif",
            "White": "/static/images/products/pegasus41_white.avif"
        },
        "sizes": ["7", "8", "9", "10", "11"],
        "colors": ["Black", "Blue", "White"],
        "material": "Engineered Mesh"
    },
    {
        "id": 4,
        "name": "Nike Dunk Low",
        "category": "Lifestyle Shoes",
        "price": 8695,
        "rating": 4.8,
        "stock": "In Stock",
        "image": "/static/images/products/dunklow_orange.webp",
        "default_color": "Orange",
        "images_by_color": {
            "Black": "/static/images/products/dunklow_black.webp",
            "Orange": "/static/images/products/dunklow_orange.webp",
            "White": "/static/images/products/dunklow_white.avif"
        },
        "sizes": ["7", "8", "9", "10"],
        "colors": ["Black", "Orange", "White"],
        "material": "Leather"
    },
    {
        "id": 5,
        "name": "Nike Air Force 1",
        "category": "Lifestyle Shoes",
        "price": 8995,
        "rating": 4.9,
        "stock": "In Stock",
        "image": "/static/images/products/airforce1_white.jpg",
        "default_color": "White",
        "images_by_color": {
            "White": "/static/images/products/airforce1_white.jpg",
            "Black": "/static/images/products/airforce1_black.jpg"
        },
        "sizes": ["7", "8", "9", "10", "11"],
        "colors": ["White", "Black"],
        "material": "Premium Leather"
    },
    {
        "id": 6,
        "name": "Nike Sportswear Hoodie",
        "category": "Apparel",
        "price": 3495,
        "rating": 4.5,
        "stock": "In Stock",
        "image": "/static/images/products/hoodie_white.webp",
        "default_color": "White",
        "images_by_color": {
            "Black": "/static/images/products/hoodie_black.webp",
            "White": "/static/images/products/hoodie_white.webp"
        },
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Black", "White"],
        "material": "Cotton Fleece"
    },
    {
        "id": 7,
        "name": "Nike Running T-Shirt",
        "category": "Apparel",
        "price": 1995,
        "rating": 4.3,
        "stock": "In Stock",
        "image": "/static/images/products/tshirt_blue.jpg",
        "default_color": "Blue",
        "images_by_color": {
            "Black": "/static/images/products/tshirt_black.webp",
            "Blue": "/static/images/products/tshirt_blue.jpg",
            "White": "/static/images/products/tshirt_white.webp"
        },
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Black", "Blue", "White"],
        "material": "Dri-FIT Polyester"
    },
    {
        "id": 8,
        "name": "Nike Running Shorts",
        "category": "Apparel",
        "price": 2495,
        "rating": 4.4,
        "stock": "In Stock",
        "image": "/static/images/products/shorts_black.jpg",
        "default_color": "Black",
        "images_by_color": {
            "Black": "/static/images/products/shorts_black.jpg",
            "Blue": "/static/images/products/shorts_blue.webp"
        },
        "sizes": ["S", "M", "L", "XL"],
        "colors": ["Black", "Blue"],
        "material": "Polyester Blend"
    },
    {
        "id": 9,
        "name": "Nike Brasilia Backpack",
        "category": "Accessories",
        "price": 2495,
        "rating": 4.3,
        "stock": "In Stock",
        "image": "/static/images/products/backpack_grey.jpg",
        "default_color": "Grey",
        "images_by_color": {
            "Black": "/static/images/products/backpack_black.jpg",
            "Grey": "/static/images/products/backpack_grey.jpg",
            "Red": "/static/images/products/backpack_red.jpg"
        },
        "sizes": ["Standard"],
        "colors": ["Black", "Grey", "Red"],
        "material": "Polyester"
    },
    {
        "id": 10,
        "name": "Nike Gym Duffel Bag",
        "category": "Accessories",
        "price": 3295,
        "rating": 4.5,
        "stock": "In Stock",
        "image": "/static/images/products/duffelbag_green.jpg",
        "default_color": "Green",
        "images_by_color": {
            "Black": "/static/images/products/duffelbag_black.webp",
            "Green": "/static/images/products/duffelbag_green.jpg",
            "Red": "/static/images/products/duffelbag_red.jpg"
        },
        "sizes": ["Standard"],
        "colors": ["Black", "Green", "Red"],
        "material": "Durable Polyester"
    },
    {
        "id": 11,
        "name": "Nike Cap",
        "category": "Accessories",
        "price": 1295,
        "rating": 4.2,
        "stock": "In Stock",
        "image": "/static/images/products/cap_grey.avif",
        "default_color": "Grey",
        "images_by_color": {
            "Grey": "/static/images/products/cap_grey.avif",
            "White": "/static/images/products/cap_white.avif"
        },
        "sizes": ["Standard"],
        "colors": ["Grey", "White"],
        "material": "Cotton Twill"
    },
    {
        "id": 12,
        "name": "Nike Socks Pack",
        "category": "Accessories",
        "price": 995,
        "rating": 4.1,
        "stock": "In Stock",
        "image": "/static/images/products/socks_black.jpg",
        "default_color": "Black",
        "images_by_color": {
            "Black": "/static/images/products/socks_black.jpg",
            "Green": "/static/images/products/socks_green.webp",
            "White": "/static/images/products/socks_white.webp"
        },
        "sizes": ["M", "L"],
        "colors": ["Black", "Green", "White"],
        "material": "Cotton Blend"
    }
]

cart_items = []
orders = []


# -----------------------------
# HELPERS
# -----------------------------

def get_dashboard_summary():
    active_orders = [order for order in orders if order["status"] != "Cancelled"]

    total_orders = len(active_orders)
    total_products_purchased = sum(order["quantity"] for order in active_orders)
    total_money_spent = sum(order["amount"] * order["quantity"] for order in active_orders)
    cart_count = sum(item["quantity"] for item in cart_items)

    return {
        "total_orders": total_orders,
        "total_products_purchased": total_products_purchased,
        "total_money_spent": total_money_spent,
        "cart_count": cart_count
    }


def get_next_order_id():
    if not orders:
        return "NK1001"

    last_number = max(int(order["order_id"].replace("NK", "")) for order in orders)
    return f"NK{last_number + 1}"


def get_analytics_data():
    active_orders = [order for order in orders if order["status"] != "Cancelled"]

    category_count = {}
    total_spent_over_time = []
    cumulative = 0
    product_count = {}

    for order in active_orders:
        category = order["category"]
        category_count[category] = category_count.get(category, 0) + order["quantity"]

        product_name = order["product_name"]
        product_count[product_name] = product_count.get(product_name, 0) + order["quantity"]

        cumulative += order["amount"] * order["quantity"]
        total_spent_over_time.append(cumulative)

    most_ordered = max(category_count, key=category_count.get) if category_count else None
    most_product = max(product_count, key=product_count.get) if product_count else None

    total_spent = sum(order["amount"] * order["quantity"] for order in active_orders)
    rewards = total_spent // 100

    avg_order_value = (
        total_spent / len(active_orders)
        if active_orders else 0
    )

    return {
        "category_count": category_count,
        "most_ordered": most_ordered,
        "spending_trend": total_spent_over_time,
        "rewards": rewards,
        "most_product": most_product,
        "avg_order_value": round(avg_order_value, 2)
    }


# -----------------------------
# PAGE ROUTES
# -----------------------------

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None}
    )


@app.post("/login", response_class=HTMLResponse)
def validate_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if username == customer["username"] and password == customer["password"]:
        return RedirectResponse(url="/products", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": "Invalid username or password"}
    )


@app.get("/products", response_class=HTMLResponse)
def products_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={
            "products": products,
            "customer": customer
        }
    )


@app.get("/product/{product_id}", response_class=HTMLResponse)
def product_details_page(request: Request, product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)

    if product is None:
        return HTMLResponse("<h1>Product not found</h1>", status_code=404)

    return templates.TemplateResponse(
        request=request,
        name="product_details.html",
        context={
            "product": product,
            "customer": customer
        }
    )


@app.post("/add-to-cart/{product_id}")
def add_to_cart(
    product_id: int,
    selected_size: str = Form(default="Standard"),
    selected_color: str = Form(default="Default")
):
    product = next((p for p in products if p["id"] == product_id), None)

    if product is not None:
        existing_item = next(
            (
                item for item in cart_items
                if item["product_id"] == product_id
                and item.get("selected_size") == selected_size
                and item.get("selected_color") == selected_color
            ),
            None
        )

        if existing_item:
            existing_item["quantity"] += 1
        else:
            selected_image = product.get("images_by_color", {}).get(
                selected_color,
                product["image"]
            )

            cart_items.append({
                "product_id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": 1,
                "selected_size": selected_size,
                "selected_color": selected_color,
                "image": selected_image
            })

    return RedirectResponse(url="/cart", status_code=303)


@app.get("/cart", response_class=HTMLResponse)
def cart_page(request: Request):
    total_amount = sum(item["price"] * item["quantity"] for item in cart_items)

    return templates.TemplateResponse(
        request=request,
        name="cart.html",
        context={
            "cart_items": cart_items,
            "total_amount": total_amount,
            "customer": customer
        }
    )


@app.post("/remove-from-cart/{product_id}")
def remove_from_cart(
    product_id: int,
    selected_size: str = Form(default=None),
    selected_color: str = Form(default=None)
):
    global cart_items

    cart_items = [
        item for item in cart_items
        if not (
            item["product_id"] == product_id
            and item.get("selected_size") == selected_size
            and item.get("selected_color") == selected_color
        )
    ]

    return RedirectResponse(url="/cart", status_code=303)


@app.post("/checkout")
def checkout():
    global cart_items, orders

    for item in cart_items:
        matched_product = next((p for p in products if p["id"] == item["product_id"]), None)
        category = matched_product["category"] if matched_product else "Unknown"

        orders.append({
            "order_id": get_next_order_id(),
            "product_name": item["name"],
            "category": category,
            "amount": item["price"],
            "quantity": item["quantity"],
            "status": "Placed"
        })

    cart_items = []

    return RedirectResponse(url="/dashboard", status_code=303)


@app.post("/cancel-order/{order_id}")
def cancel_order(order_id: str):
    for order in orders:
        if order["order_id"] == order_id:
            if order["status"] in ["Placed", "Pending", "Processing"]:
                order["status"] = "Cancelled"
            break

    return RedirectResponse(url="/dashboard", status_code=303)


@app.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="orders.html",
        context={
            "orders": orders,
            "customer": customer
        }
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    summary = get_dashboard_summary()
    analytics = get_analytics_data()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "summary": summary,
            "analytics": analytics,
            "customer": customer
        }
    )


@app.get("/reset")
def reset_app():
    global cart_items, orders
    cart_items = []
    orders = []
    return RedirectResponse(url="/", status_code=303)


# -----------------------------
# API ROUTES
# -----------------------------

@app.get("/api/products")
def get_products_api():
    return JSONResponse(content=products)


@app.get("/api/cart")
def get_cart_api():
    return JSONResponse(content=cart_items)


@app.get("/api/orders")
def get_orders_api():
    return JSONResponse(content=orders)


@app.get("/api/dashboard-summary")
def get_dashboard_summary_api():
    return JSONResponse(content=get_dashboard_summary())