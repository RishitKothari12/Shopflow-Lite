from flask import Flask, render_template, redirect, session
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session

# Supabase config
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# Homepage
@app.route('/')
def home():
    return render_template('index.html')


# Product listing
@app.route('/products')
def show_products():
    response = supabase.table("products").select("*").execute()
    products = response.data or []   # ✅ safety fix
    return render_template('products.html', products=products)


# Add to cart
@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]

    pid = str(product_id)

    if pid in cart:
        cart[pid] += 1
    else:
        cart[pid] = 1

    session["cart"] = cart
    session.modified = True

    return redirect('/cart')


# Decrease quantity
@app.route('/decrease/<int:product_id>')
def decrease(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        cart[pid] -= 1
        if cart[pid] <= 0:
            del cart[pid]

    session["cart"] = cart
    session.modified = True

    return redirect('/cart')


# Remove item completely
@app.route('/remove/<int:product_id>')
def remove(product_id):
    cart = session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    session["cart"] = cart
    session.modified = True

    return redirect('/cart')


# View cart
@app.route('/cart')
def view_cart():
    cart = session.get("cart", {})

    items = []
    total = 0

    for pid, qty in cart.items():
        response = supabase.table("products").select("*").eq("id", int(pid)).execute()

        if response.data:   # ✅ safety check
            product = response.data[0]

            product["quantity"] = qty
            product["subtotal"] = qty * product["price"]

            items.append(product)
            total += product["subtotal"]

    return render_template('cart.html', items=items, total=total)


# Health check
@app.route('/health')
def health():
    return {"status": "running"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)