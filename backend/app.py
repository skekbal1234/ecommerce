from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

PRODUCTS = [
    {
        "id": 1,
        "name": "Classic Leather Tote Bag",
        "category": "Bag",
        "price": 139.99,
        "description": "Smooth leather tote with roomy interior and durable straps.",
        "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80",
        "stock": 12
    },
    {
        "id": 2,
        "name": "Vintage Leather Belt",
        "category": "Belt",
        "price": 49.99,
        "description": "Full grain leather belt with antique brass buckle.",
        "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=800&q=80",
        "stock": 25
    },
    {
        "id": 3,
        "name": "Leather Travel Pouch",
        "category": "Accessory",
        "price": 69.99,
        "description": "Compact leather pouch for chargers, keys, and essentials.",
        "image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&q=80",
        "stock": 18
    },
    {
        "id": 4,
        "name": "Leather Messenger Bag",
        "category": "Bag",
        "price": 189.99,
        "description": "Structured leather messenger bag with adjustable shoulder strap.",
        "image": "https://images.unsplash.com/photo-1560347876-aeef00ee58a1?auto=format&fit=crop&w=800&q=80",
        "stock": 9
    },
    {
        "id": 5,
        "name": "Leather Card Wallet",
        "category": "Accessory",
        "price": 34.99,
        "description": "Slim leather wallet designed for cards and a few bills.",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80",
        "stock": 40
    }
]

@app.route("/product", methods=["GET"])
def get_products():
    return jsonify(PRODUCTS)

@app.route("/product/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((item for item in PRODUCTS if item["id"] == product_id), None)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product)

@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.get_json() or {}
    cart_items = data.get("cart", [])
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    total = 0.0
    for item in cart_items:
        product = next((p for p in PRODUCTS if p["id"] == item.get("id")), None)
        if not product:
            return jsonify({"message": f"Product {item.get('id')} not found"}), 404
        total += product["price"] * item.get("quantity", 1)

    return jsonify({
        "message": "Checkout successful",
        "total": round(total, 2),
        "currency": "USD"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
