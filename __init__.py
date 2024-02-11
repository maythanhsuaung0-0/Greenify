from flask import Flask, render_template, request, redirect, url_for, json, jsonify, session, send_file, \
    send_from_directory
from Forms import CreateUserForm, StaffLoginForm, LoginForm
import shelve, User, SellerProduct, application
from sellerproductForm import CreateProductForm
from applicationForm import ApplicationForm
from application import ApplicationFormFormat as AppFormFormat
# for accessing and storing image
import random
import os
import secrets
import shutil
import User_login
from werkzeug.utils import secure_filename
from datetime import date, timedelta
from urllib.parse import quote
# for sending mail
import string
import csv
from send_email import *
import uuid
from crud_functions import *
from seller_order import SellerOrder
from searchForm import Search
from updateUser import update
from chat import get_response

app = Flask(__name__, static_url_path='/static')
user_logged_in = False
seller_logged_in = False
staff_logged_in = False
app.secret_key = 'my_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# supporting document upload folder
UPLOAD_RELATIVE_PATH = 'documents/uploads'
UPLOAD_DIRECTORY = os.path.join(app.root_path, 'static', UPLOAD_RELATIVE_PATH)
app.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY

UPLOAD_FOLDER = 'C:/Users/Jia Ying/Downloads/Greenify/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_IMG_FOLDER = os.path.join(app.root_path, 'static', 'uploads/product_image')
app.config['UPLOAD_IMG_FOLDER'] = UPLOAD_IMG_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg'}


# Error Handling
@app.errorhandler(404)
def error_404(e):
    return render_template('error_msg.html')


@app.errorhandler(403)
def error_403(e):
    return render_template('error_msg.html')


@app.errorhandler(500)
def error_500(e):
    return render_template('error_msg.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Retrieving r and r
def fetch_reviews(seller_id, product_id):
    # Check if the file exists before attempting to open it
    if not os.path.exists('reviews.db'):
        return []

    try:
        reviews_db = shelve.open('reviews.db', 'r')
        ratings_reviews_dict = reviews_db.get('Reviews', {})

        seller_id = int(seller_id)
        product_id = int(product_id)

        # Get the seller's dictionary
        seller_reviews = ratings_reviews_dict.get(seller_id, {})

        # Get the list of reviews for the product
        product_reviews = seller_reviews.get(product_id, [])
        reviews_db.close()
        return product_reviews
    except Exception as e:
        print("Error fetching reviews:", e)
        return []


def delete_folder(item):
    filename = item.get_doc()
    folder_path, _ = os.path.split(filename)
    full_folder_path = os.path.join(app.config["UPLOAD_DIRECTORY"], folder_path)

    if os.path.exists(full_folder_path):
        shutil.rmtree(full_folder_path)
        print(f"folder deleted: {full_folder_path}")


# generate random secure pwd for giving the seller the very first password
def generate_password(length):
    password = (
            secrets.choice(string.ascii_uppercase) +
            secrets.choice(string.ascii_lowercase) +
            secrets.choice(string.digits)
    )
    remaining_length = length - 4
    alphabet = string.ascii_letters + string.digits
    password += ''.join(secrets.choice(alphabet) for _ in range(remaining_length))
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    return ''.join(password_list)


# Returning the qty for the cart icon
def cart_qty(user):
    saved_cart_qty = 0
    shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
    try:
        users_shopping_cart = shopping_cart_db[user]
        saved_cart_qty = users_shopping_cart["cart_qty"]
    except:
        print("Error in loading cart qty db")
    return saved_cart_qty


# Seacrch for Seller id
def seller_id_search(seller_name):
    approved_sellers = {}
    approve_seller_db = shelve.open('approved_sellers.db')
    try:
        approved_sellers = approve_seller_db['Approved_sellers']
    except:
        return False
    for id in approved_sellers:
        if seller_name == approved_sellers[id].get_name():
            seller_id = approved_sellers[id].get_application_id()
            print('seller_id', seller_id)
            return seller_id


def seller_name_search(seller_id):
    seller_id = int(seller_id)
    approved_sellers = {}
    approve_seller_db = shelve.open('approved_sellers.db')
    try:
        approved_sellers = approve_seller_db['Approved_sellers']
    except:
        return False
    for id in approved_sellers:
        if seller_id == id:
            return approved_sellers[seller_id].get_name()


def search_engine(search_query):
    search_query_list = search_query.split()

    seller_product_db = shelve.open('seller-product.db')
    result_list = []
    for seller_id in seller_product_db:
        seller_products = seller_product_db[str(seller_id)]['products']

        # Accessing Indv Product to get the Product Name
        for product_id in seller_products:
            product_name = seller_products[product_id].get_product_name()

            # Loop Through Search Query
            for word in search_query_list:
                result = product_name.lower().find(word)
                if result != -1:
                    print(word)
                    print(product_name)
                    print(result)
                    # Seller Name, Product
                    result_list.append([seller_name_search(seller_id), seller_products[product_id]])
                    break

    search_db = shelve.open('search.db')
    if len(result_list) != 0:
        search_db['result_list'] = result_list
    else:
        search_db['result_list'] = None


def last_url(url):
    logged_in = False
    try:
        logged_in = session['user_logged_in']
    except:
        session['user_logged_in'] = False
        print("User not logged in")

    if not logged_in:
        session['last_url'] = url


# chatbot
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


@app.route("/", methods=['GET', 'POST'])
def home():
    last_url(url_for('home'))
    search_form = Search(request.form)
    if request.method == 'POST' and search_form.validate():
        search_engine(search_form.search_query.data)
        return redirect(url_for('product_search'))
    # Fetch product data
    all_result = []  # Assume this will fetch all products, adjust according to your application logic
    seller_product_db = shelve.open('seller-product.db')

    for seller_id in seller_product_db:
        seller_products = seller_product_db[str(seller_id)]['products']

        # Accessing Individual Product
        for product_id in seller_products:
            all_result.append([seller_name_search(seller_id), seller_products[product_id]])

    seller_product_db.close()

    # Your existing logic to render the template, now including 'all_result' in the context
    try:
        user = session['user_id']
        user_id_hash = session['user_id_hash']
        return render_template("customer/homepage.html", user=user_id_hash, saved_cart_qty=cart_qty(user), form=search_form, all_result=all_result)
    except:
        return render_template("customer/homepage.html", user=None, form=search_form, all_result=all_result)



@app.route("/Product/<seller>/<int:product_id>", methods=['GET', 'POST'])
def product(seller, product_id):
    last_url(url_for('product', seller=seller, product_id=product_id))
    try:
        user = session['user_id']
        user_id_hash = session['user_id_hash']
    except:
        user = None
        user_id_hash = None

    search_form = Search(request.form)

    def cart_qty(user):
        saved_cart_qty = 0
        shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
        try:
            users_shopping_cart = shopping_cart_db[user]
            saved_cart_qty = users_shopping_cart["cart_qty"]
        except:
            print("Error in loading cart qty db")

        return saved_cart_qty

    # Search for Seller Id
    seller_id = seller_id_search(seller)

    if seller_id == False:
        print("Seller_id not found")
        return render_template('error_msg.html')

    # Retrieving Product for html to display
    seller_products = {}
    seller_product_info = {}
    seller_product_db = shelve.open('seller-product.db', 'c')
    try:
        seller_product_info = seller_product_db[str(seller_id)]
        seller_products = seller_product_info['products']
    except:
        print("Product is not found")
        return render_template('error_msg.html')

    product = seller_products[product_id]
    seller_product_db.close()

    product_reviews = []
    # Received AJAX Request
    if request.method == "POST":

        # Search Query
        try:
            if search_form.search_query.id.data != None and search_form.validate():
                search_engine(search_form.search_query.data)
                return redirect(url_for('product_search'))
        except:
            pass

        sent_data = json.loads(request.data)

        # Check Customer Feedback
        if sent_data["request_type"] == "customer_feedback":
            reviews_db = shelve.open('reviews.db', 'c')
            try:
                ratings_reviews_dict = reviews_db.get('Reviews', {})

                # Get the seller ID and product ID from the sent data
                seller_id = int(sent_data.get('seller_id', ''))
                product_id = int(sent_data.get('product_id', ''))

                if seller_id not in ratings_reviews_dict:
                    ratings_reviews_dict[seller_id] = {}

                # Get the seller's dictionary
                seller_reviews = ratings_reviews_dict[seller_id]

                if product_id not in seller_reviews:
                    seller_reviews[product_id] = []

                # Get the list of reviews for the product
                product_reviews = seller_reviews[product_id]

                # Get the new feedback
                new_feedback = {
                    'rating': sent_data.get('ratings', 0),
                    'review': sent_data.get('reviews', ''),
                    'timestamp': date.today()
                }

                product_reviews.append(new_feedback)
                reviews_db['Reviews'] = ratings_reviews_dict
                print("ratings_reviews_dict:", ratings_reviews_dict)

            except Exception as e:
                print("Error in handling customer feedback:", str(e))
            finally:
                reviews_db.close()
                return json.jsonify({"data": product_reviews, "result": True})

        elif sent_data["request_type"] == 'fetch_reviews':
            seller_id = int(sent_data.get('seller_id', ''))
            product_id = int(sent_data.get('product_id', ''))

            if seller_id == '' or product_id == '':
                return jsonify({"error": "Incomplete data for fetching reviews"}), 400

            product_reviews = fetch_reviews(seller_id, product_id)
            return jsonify({"data": product_reviews, "result": True})

        # Check Product Stock
        if sent_data["request_type"] == "product_stock":
            seller_products = {}
            seller_product_info = {}
            seller_product_db = shelve.open('seller-product.db', 'c')
            try:
                seller_product_info = seller_product_db[str(seller_id)]
                seller_products = seller_product_info['products']
            except:
                print("Product is not found")
                return render_template('error_msg.html')

            product = seller_products[product_id]
            product_stock = product.get_product_stock()
            seller_product_db.close()

            return json.jsonify({"stock": product_stock})

        # Add to Cart
        if sent_data["request_type"] == "add_cart":
            product = json.loads(request.data)
            del product["request_type"]

            # Saving Shopping Cart Items
            # Dummy User (User persistent Log In not Developed)
            users_shopping_cart = {}
            user_selected_product = {}
            shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
            try:
                users_shopping_cart = shopping_cart_db[user]
                user_selected_product = users_shopping_cart["selected_product"]
            except KeyError:
                print("KeyError in opening saved cart items")
            except:
                print("Error in retrieving User Shopping Cart Info in user_shopping_cart.db")

            user_selected_products = {}

            # Check Stock
            seller_products = {}
            seller_product_info = {}
            seller_product_db = shelve.open('seller-product.db', 'c')
            try:
                seller_product_info = seller_product_db[str(seller_id)]
                seller_products = seller_product_info['products']
            except:
                print("Product is not found")
                return render_template('error_msg.html')

            seller_saved_product = seller_products[product_id]
            product_stock = seller_saved_product.get_product_stock()

            seller_product_db.close()

            # Check if Product has been added before
            try:
                saved_product = user_selected_product[product["seller"] + str(product["product_id"])]

                saved_product["product_qty"] += product["product_qty"]
                if saved_product["product_qty"] > product_stock:
                    return json.jsonify({"result": False, "reason": "added more than stock"})

                user_selected_product[product["seller"] + str(product["product_id"])] = saved_product
                users_shopping_cart["selected_product"] = user_selected_product
                shopping_cart_db[user] = users_shopping_cart
            # Product not Added
            except:
                if product["product_qty"] > product_stock:
                    return json.jsonify({"result": False, "reason": "added more than stock"})

                product['product_obj'] = seller_saved_product
                user_selected_product[product["seller"] + str(product["product_id"])] = product
                users_shopping_cart["selected_product"] = user_selected_product

            # Update Cart Qty
            saved_cart_qty = 0
            try:
                saved_cart_qty = users_shopping_cart["cart_qty"]
            except:
                print("Failed loading cart qty")

            saved_cart_qty = len(user_selected_product)
            users_shopping_cart["cart_qty"] = saved_cart_qty

            # Saving new info into db
            shopping_cart_db[user] = users_shopping_cart
            shopping_cart_db.close()

            print(users_shopping_cart)
            return json.jsonify({"data": saved_cart_qty, "result": True})

    print(product.get_image())
    return render_template("customer/product.html", product=product, seller=seller, seller_id=seller_id,
                           saved_cart_qty=cart_qty(user), user=user_id_hash, form=search_form,
                           product_reviews=product_reviews)


@app.route('/<user_id_hash>/cart', methods=['GET', 'POST'])
def shopping_cart(user_id_hash):
    def cart_qty(user):
        saved_cart_qty = 0
        shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
        try:
            users_shopping_cart = shopping_cart_db[user]
            saved_cart_qty = users_shopping_cart["cart_qty"]
        except:
            print("Error in loading cart qty db")
        return saved_cart_qty

    search_form = Search(request.form)

    if user_id_hash != session['user_id_hash']:
        return render_template('error_msg.html', user=session['user_id_hash'],
                               saved_cart_qty=cart_qty(session['user_id']), form=search_form)

    user_id_hash = session['user_id_hash']
    user = session['user_id']

    last_url(url_for('shopping_cart', user_id_hash=user))

    users_shopping_cart = {}
    user_selected_product = {}
    shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
    try:
        users_shopping_cart = shopping_cart_db[user]
        user_selected_product = users_shopping_cart["selected_product"]
    except KeyError:
        return render_template("customer/empty_cart.html", user=user_id_hash, saved_cart_qty=cart_qty(user),
                               form=search_form)
    except:
        print("Error in retrieving User Shopping Cart Info in user_shopping_cart.db")

    display_shopping_cart = []

    if len(user_selected_product) != 0:
        for product_selected_name in user_selected_product:
            product_selected = user_selected_product[product_selected_name]

            # Getting the Product Object
            seller_product = {}
            seller_product_db = shelve.open("seller-product.db")

            seller_product_info = seller_product_db[str(product_selected["seller_id"])]
            seller_product = seller_product_info['products']
            product = seller_product[product_selected["product_id"]]

            # Getting Product Qty
            product_qty = product_selected["product_qty"]

            # Getting Seller
            seller_name = product_selected["seller"]

            # Making a dictionary of each product (product, product_qty, seller_name)
            product_dict = {
                "product": product,
                "product_qty": product_qty,
                "seller_name": seller_name
            }
            display_shopping_cart.append(product_dict)

        saved_cart_qty = cart_qty(user)
    else:
        return render_template("customer/empty_cart.html")

    # Receive AJAX Request
    if request.method == "POST":

        # Search Query
        try:
            if search_form.search_query.id.data != None and search_form.validate():
                search_engine(search_form.search_query.data)
                return redirect(url_for('product_search'))
        except:
            pass

        sent_data = json.loads(request.data)

        # Request to Update Cart Qty
        if sent_data["request_type"] == "update_cart_qty":

            seller_name = sent_data["seller_name"]
            product_id = sent_data["product_id"]

            # Searching for Seller id
            seller_id = seller_id_search(seller_name)

            # Update Product Qty into db
            shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
            users_shopping_cart = shopping_cart_db[user]
            user_selected_product = users_shopping_cart["selected_product"]
            product_qty = user_selected_product[seller_name + str(product_id)]["product_qty"]

            if sent_data['type'] == "increment":
                product_qty += 1
            elif sent_data['type'] == "decrement":
                product_qty -= 1

            user_selected_product[seller_name + str(product_id)]["product_qty"] = product_qty
            users_shopping_cart["selected_product"] = user_selected_product
            shopping_cart_db[user] = users_shopping_cart
            shopping_cart_db.close()

            return json.jsonify({'result': True})

        # Request to Delete Item
        elif sent_data["request_type"] == "delete_product":
            seller_name = sent_data["seller_name"]
            seller_name = sent_data["seller_name"]
            product_id = sent_data["product_id"]

            # Searching for Seller id
            seller_id = seller_id_search(seller_name)

            # Open Shopping Cart db
            shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
            users_shopping_cart = shopping_cart_db[user]

            # Remove Item from Cart
            user_selected_product = users_shopping_cart["selected_product"]
            del user_selected_product[seller_name + str(product_id)]

            # Update Saved Cart Qty
            saved_cart_qty = users_shopping_cart["cart_qty"]
            saved_cart_qty -= 1
            users_shopping_cart["cart_qty"] = saved_cart_qty

            # Close Shopping Cart db
            shopping_cart_db[user] = users_shopping_cart
            shopping_cart_db.close()

            return json.jsonify({"result": True, "cart_qty": saved_cart_qty})

        elif sent_data["request_type"] == "checkout":
            payable_price = sent_data['payable_price']

            shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")

            users_shopping_cart = shopping_cart_db[user]
            users_shopping_cart["payable"] = payable_price
            shopping_cart_db[user] = users_shopping_cart

            shopping_cart_db.close()

            return json.jsonify({"redirect_link": url_for("payment", user_id_hash=user_id_hash)})

    return render_template("customer/shopping_cart.html", display_shopping_cart=display_shopping_cart,
                           user=user_id_hash, saved_cart_qty=saved_cart_qty, form=search_form)


@app.route('/<user_id_hash>/payment', methods=['GET', 'POST'])
def payment(user_id_hash):
    search_form = Search(request.form)

    if user_id_hash != session['user_id_hash']:
        return render_template('error_msg.html', user=session['user_id_hash'],
                               saved_cart_qty=cart_qty(session['user_id']), form=search_form)

    user_id_hash = session['user_id_hash']
    user = session['user_id']

    # Receive AJAX Request
    if request.method == "POST":

        # Search Query
        try:
            if search_form.search_query.id.data != None and search_form.validate():
                search_engine(search_form.search_query.data)
                return redirect(url_for('product_search'))
        except:
            pass

        sent_data = json.loads(request.data)

        if sent_data['request_type'] == 'payment':
            name = sent_data['name']
            email = sent_data['email']
            address = sent_data['address']
            date_purchased = date.today()
            order_id = uuid.uuid4().hex

            # Open User Shopping Cart
            user_shopping_cart_db = shelve.open('user_shopping_cart.db')
            users_shopping_cart = user_shopping_cart_db[email]
            user_selected_product = users_shopping_cart["selected_product"]
            amt_paid = users_shopping_cart["payable"]

            # Accessing Info of each individual product bought
            order_history_db = shelve.open('order_history.db')

            # Creating a Seller Order List
            seller_order_dict = {}

            for itemName in user_selected_product:
                seller_product_db = shelve.open('seller-product.db')

                item = user_selected_product[itemName]
                seller_id = item["seller_id"]
                product_id = item["product_id"]
                bought_qty = item["product_qty"]

                # Retrieving Qty
                seller_product_info = seller_product_db[str(seller_id)]
                seller_products = seller_product_info['products']
                product = seller_products[product_id]
                product_qty = product.get_product_stock()
                product_qty -= bought_qty

                # Retrieve Unit Amount
                product_unit_price = product.get_product_price()

                # Save Qty
                product.set_product_stock(product_qty)
                seller_products[product_id] = product
                seller_product_info['products'] = seller_products
                seller_product_db[str(seller_id)] = seller_product_info
                seller_product_db.close()

                # Creating Seller Order
                # Getting Order Stored or Create if Not Found
                if seller_id in seller_order_dict.keys():
                    order = seller_order_dict[seller_id]
                else:
                    order = SellerOrder(name, email, address, date_purchased.strftime('%Y-%m-%d'), order_id)

                # Calculating Total Price for both Product and Order
                total_price = 0.0
                product_price = product_unit_price * bought_qty
                total_price += float(product_price)

                # Saving Data into order
                order.set_order_products(product_id, bought_qty, product_price)
                order.set_total(total_price)
                print("my order total",order.get_total())
                # Saving Everything to seller_order_dict
                seller_id = item['seller_id']
                seller_order_dict[seller_id] = order

            # Updating New Orders to db
            seller_order_db = shelve.open('seller_order.db')

            for seller_id in seller_order_dict:
                try:
                    seller_order_list = seller_order_db[str(seller_id)]
                    seller_order_list.append({order_id: seller_order_dict[seller_id]})
                    seller_order_db[str(seller_id)] = seller_order_list
                except:
                    seller_order_list = []
                    seller_order_list.append({order_id: seller_order_dict[seller_id]})
                    seller_order_db[str(seller_id)] = seller_order_list

            seller_order_db.close()

            # Create Order History
            order_history = {}
            user_order_history = {}
            order_history_db = shelve.open('order_history.db')

            # Retrieve Order History
            try:
                user_order_history = order_history_db[email]
            except:
                print("No Record Found")

            # Saving Datas into Order History
            order_history['items'] = user_selected_product
            order_history['shipping_info'] = {'name': name, 'address': address}
            order_history['amt_paid'] = amt_paid
            order_history['date'] = date_purchased.strftime("%d %B, %Y")

            user_order_history[str(order_id)] = order_history
            order_history_db[email] = user_order_history
            order_history_db.close()

            # Deleting Items from User Shopping Cart
            del user_shopping_cart_db[email]
            user_shopping_cart_db.close()

            return json.jsonify({'result': True, 'redirect_link': url_for('success_payment')})

    user_db = shelve.open('user.db')
    user_dict = user_db['Users']
    user_info = user_dict[user]
    user_db.close()

    shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
    users_shopping_cart = shopping_cart_db[user]
    payable = users_shopping_cart['payable']

    return render_template("customer/payment.html", user=user_id_hash, user_id=user,
                           user_address=user_info.get_address(), user_name=user_info.get_name(), payable=payable,
                           saved_cart_qty=cart_qty(user), form=search_form)


@app.route('/product_search', methods=['GET', 'POST'])
def product_search():
    try:
        user = session['user_id']
        user_id_hash = session['user_id_hash']
    except:
        user = None
        user_id_hash = None
    last_url(url_for('product_search'))

    search_form = Search(request.form)
    if request.method == 'POST' and search_form.validate():
        search_engine(search_form.search_query.data)
        return redirect(url_for('product_search'))

    search_db = shelve.open('search.db')
    result_list = search_db['result_list']

    return render_template('customer/search_result.html', user=user_id_hash, saved_cart_qty=cart_qty(user),
                           result_list=result_list, form=search_form)


@app.route('/Product', methods=['GET', 'POST'])
def product_all():
    try:
        user = session['user_id']
        user_id_hash = session['user_id_hash']
    except:
        user = None
        user_id_hash = None
    last_url(url_for('product_search'))

    search_form = Search(request.form)
    if request.method == 'POST' and search_form.validate():
        search_engine(search_form.search_query.data)
        return redirect(url_for('product_search'))

    # Adding All Saved Products From All Seller Into A List
    all_result = []
    seller_product_db = shelve.open('seller-product.db')

    for seller_id in seller_product_db:
        seller_products = seller_product_db[str(seller_id)]['products']

        # Accessing Indv Product
        for product_id in seller_products:
            all_result.append([seller_name_search(seller_id), seller_products[product_id]])

    return render_template('customer/product_all.html', user=user_id_hash, saved_cart_qty=cart_qty(user),
                           form=search_form, all_result=all_result)


@app.route('/success')
def success_payment():
    try:
        user = session['user_id']
        user_id_hash = session['user_id_hash']
    except:
        user = None
        user_id_hash = None

    search_form = Search(request.form)
    global result_list
    if request.method == 'POST' and search_form.validate():
        result_list = search_engine(search_form.search_query.data)
        return redirect(url_for('product_search'))
    return render_template('customer/success_payment.html', user=user_id_hash, saved_cart_qty=cart_qty(user),
                           form=search_form)


@app.route('/<user_id_hash>/order_history', methods=['GET', 'POST'])
def order_history(user_id_hash):
    search_form = Search(request.form)

    if user_id_hash != session['user_id_hash']:
        return render_template('error_msg.html', user=session['user_id_hash'],
                               saved_cart_qty=cart_qty(session['user_id']), form=search_form)
    user = session['user_id']
    user_id_hash = session['user_id_hash']

    last_url(url_for('product_search'))

    search_form = Search(request.form)
    if request.method == 'POST' and search_form.validate():
        search_engine(search_form.search_query.data)
        return redirect(url_for('product_search'))

    order_history_db = shelve.open('order_history.db')

    try:
        all_orders = order_history_db[user]
        all_orders = dict(reversed(all_orders.items()))
    except:
        return render_template('customer/empty_order_history.html', user=user_id_hash, saved_cart_qty=cart_qty(user),
                               form=search_form)

    return render_template('customer/order_history.html', user=user_id_hash, saved_cart_qty=cart_qty(user),
                           form=search_form, all_orders=all_orders)


@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    error = None
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        if create_user_form.email.data in users_dict:
            error = 'An account has already been created with this email. Please Login.'
        elif len(str(create_user_form.contact_number.data)) != 8:
            error = 'Phone number must be 8 digits.'
        elif len(str(create_user_form.postal_code.data)) != 6:
            error = 'Postal code must be 6 digits.'
        elif create_user_form.password.data != create_user_form.confirm_password.data:
            error = 'Passwords must match.'
        else:
            user = User.User(create_user_form.email.data, create_user_form.password.data, create_user_form.name.data,
                             create_user_form.contact_number.data, create_user_form.postal_code.data,
                             create_user_form.address.data)
            users_dict[user.get_email()] = user
            db['Users'] = users_dict
            return redirect(url_for('login'))

        db.close()
    return render_template('customer/createUser.html', form=create_user_form, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        user = User_login.UserLogin(login_form.email.data, login_form.password.data)
        email = login_form.email.data
        password = login_form.password.data
        db = shelve.open('user.db', 'r')
        try:
            if 'Users' in db:
                users_dict = db["Users"]
                user_id = get_key(email, users_dict)
                if user_id is not None:
                    stored_password = users_dict[user_id].get_password()
                    if password == stored_password:
                        user_id_hash = uuid.uuid4().hex
                        session['user_id_hash'] = user_id_hash
                        session['user_id'] = user.get_email()
                        session['user_logged_in'] = True
                        session['user_email'] = email
                        return redirect(session.get('last_url', '/'))
                    else:
                        error = 'Email or Password is incorrect, please try again.'
                else:
                    error = 'Email or Password is incorrect, please try again.'
            else:
                error = 'Email or Password is incorrect, please try again.'
        except Exception as e:
            print(f"Error: {e}")
        finally:
            db.close()
    return render_template('customer/login.html', form=login_form, error=error)


def get_key(email, users_dict):
    for key, value in users_dict.items():
        if value.get_email() == email:
            return key


@app.route("/check_login")
def check_login():
    return user_logged_in


@app.route('/<user_id_hash>/user/logout')
def user_logout(user_id_hash):
    user = session['user_id']
    user_id_hash = session['user_id_hash']
    if session.get('user_logged_in'):
        session.pop('user_logged_in', None)
        session.pop('user_id', None)
        session.pop('user_id_hash', None)
    print(f"User login status = {session.get('user_logged_in')}")
    return "You have successfully logged out from your account."


@app.route('/staff/logout')
def staff_logout():
    if session.get('staff_logged_in'):
        session.pop('staff_logged_in', None)
    print(f"Staff login status = {session.get('staff_logged_in')}")
    return "You have successfully logged out from the account."


@app.route('/seller/<seller_id_hash>/logout')
def seller_logout(seller_id_hash):
    seller_id = session['seller_id']
    seller_id_hash = session['seller_id_hash']
    if session.get('seller_logged_in'):
        session.pop('seller_logged_in', None)
    print(f"Seller login status = {session.get('seller_logged_in')}")
    return "You have successfully logged out from your account."


@app.route('/<user_id_hash>/profile', methods=['GET', 'POST'])
def profile(user_id_hash):
    search_form = Search(request.form)

    if user_id_hash != session['user_id_hash']:
        return render_template('error_msg.html', user=session['user_id_hash'],
                               saved_cart_qty=cart_qty(session['user_id']), form=search_form)

    user = session['user_id']
    user_id_hash = session['user_id_hash']

    last_url(url_for('product_search'))

    if request.method == 'POST' and search_form.validate():
        search_engine(search_form.search_query.data)
        return redirect(url_for('product_search'))

    user_data = shelve.open('user.db')
    users_dict = user_data.get('Users', {})
    user_obj = users_dict[user]
    user_data.close()

    if session.get('user_logged_in'):
        return render_template('customer/profile.html', user=user_id_hash, saved_cart_qty=cart_qty(user),
                               form=search_form, user_data=user_obj)
    else:
        return redirect(url_for('login'))


@app.route('/<user_id_hash>/updateUser', methods=['GET', 'POST'])
def update_user(user_id_hash):
    global user_obj
    search_form = Search(request.form)

    if user_id_hash != session['user_id_hash']:
        return render_template('error_msg.html', user=session['user_id_hash'],
                               saved_cart_qty=cart_qty(session['user_id']), form=search_form, user_id_hash=user_id_hash)

    user_id_hash = session['user_id_hash']
    user = session['user_id']
    error = None

    if request.method == 'POST':
        email = request.form.get('email-input')
        password = request.form.get('password-input')
        confirm_password = request.form.get('confirm_password-input')
        name = request.form.get('name-input')
        contact_number = request.form.get('contact_number-input')
        postal_code = request.form.get('postal_code-input')
        address = request.form.get('address-input')
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user_obj = users_dict[user]

        if len(str(password)) < 8 or len(str(confirm_password)) < 8:
            error = 'Passwords must have at least 8 characters.'
        elif len(str(contact_number)) != 8:
            error = 'Phone number must be 8 digits.'
        elif len(str(postal_code)) != 6:
            error = 'Postal code must be 6 digits.'
        elif password != confirm_password:
            error = 'Passwords must match.'
        else:
            user_obj.set_email(email)
            user_obj.set_password(password)
            user_obj.set_name(name)
            user_obj.set_contact_number(contact_number)
            user_obj.set_postal_code(postal_code)
            user_obj.set_address(address)
            error = "Update Successful."

            session['user_id'] = email
            print(session['user_id'])

        db['Users'] = users_dict
        db.close()

    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']

        user = session['user_id']
        user_obj = users_dict[user]

        if user:
            email = user_obj.get_email()
            password = user_obj.get_password()
            name = user_obj.get_name()
            contact_number = user_obj.get_contact_number()
            postal_code = user_obj.get_postal_code()
            address = user_obj.get_address()

        db.close()

    if session.get('user_logged_in'):
        return render_template('customer/updateUser.html', error=error, db=user_obj, user=user_id_hash)
    else:
        return redirect(url_for('login'))


@app.route('/<user_id_hash>/deleteUser', methods=['POST'])
def delete_user(user_id_hash):
    user = session['user_id']
    user_id_hash = session['user_id_hash']
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(user)
    user_logout(user_id_hash)

    db['Users'] = users_dict
    db.close()

    return "Your account has successfully been deleted."


@app.route('/stafflogin', methods=['GET', 'POST'])
def staff_login():
    error = None
    staff_login_form = StaffLoginForm(request.form)
    if request.method == 'POST' and staff_login_form.validate():
        if staff_login_form.admin_email.data == 'admin@gmail.com' and staff_login_form.admin_password.data == 'admin_password':
            session['staff_logged_in'] = True
            print(f"Staff login status = {session.get('staff_logged_in')}")
            return redirect(url_for('retrieveApplicationForms'))
        else:
            error = 'Email or Password is incorrect, please try again.'
    return render_template('staff/staff_login.html', form=staff_login_form, error=error)


@app.route('/seller/login', methods=['GET', 'POST'])
def seller_login():
    global seller_password
    error = None
    try:
        if session['seller_logged_in'] == True and session['seller_id_hash']:
            seller_id_hash = session['seller_id_hash']
            return redirect(url_for('seller_dashboard', seller_id_hash=seller_id_hash))
    except:
        pass
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        approved_sellers = {}
        user = User_login.UserLogin(login_form.email.data, login_form.password.data)
        sellers = []
        seller_password = []
        seller_email = []
        sellers_list = retrieve_db('approved_sellers.db', 'Approved_sellers')
        seller_data = {}
        for i in sellers_list:
            seller_data['id'] = i.get_application_id()
            seller_data['email'] = i.get_email()
            seller_data['pw'] = i.get_password()
            sellers.append(seller_data)
            print("seller_id->",seller_data['id'])
        for j in sellers_list:
            seller_email.append(j.get_email())
        print(seller_email)
        for i in sellers:
            print(i)
            if login_form.email.data == i["email"] and login_form.password.data == i["pw"]:
                seller_id = i['id']
                seller_id_hash = uuid.uuid4().hex
                session['seller_id_hash'] = seller_id_hash
                session['seller_id'] = seller_id
                session['seller_logged_in'] = True
                print(f"Seller login status = {session.get('seller_logged_in')}")
                if session.get('seller_logged_in'):
                    return redirect(url_for('seller_dashboard', seller_id_hash=seller_id_hash))
            else:
                error = 'Email or Password is incorrect, please try again.'
    return render_template('seller/seller_login.html', form=login_form, seller_logged_in=seller_logged_in, error=error)


@app.route('/seller/<seller_id_hash>/createProduct', methods=['GET', 'POST'])
def create_product(seller_id_hash):
    if seller_id_hash != session['seller_id_hash']:
        print('route error')
        return render_template('error_msg.html')

    seller_id_hash = session['seller_id_hash']
    approved_sellers = {}
    approved_db = shelve.open('approved_sellers.db', 'r')
    approved_sellers = approved_db['Approved_sellers']
    seller_id = session['seller_id']
    if seller_id not in approved_sellers:
        return "seller not found"
    approved_db.close()

    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        seller_products = {}
        # used to store 'id' and 'products' as key
        seller_product_info = {}
        seller_product_db = shelve.open('seller-product.db', 'c')

        try:
            seller_product_info = seller_product_db[str(seller_id)]
            seller_products = seller_product_info['products']
            # creates 'products' as key

        except:
            print("Error in retrieving products from seller-product.db.")

        # Getting a new Product Id
        try:
            seller_product_id = seller_product_info["id"]
        except KeyError:
            seller_product_id = 1
        #

        create_product = SellerProduct.SellerProduct(create_product_form.product_name.data,
                                                     create_product_form.product_price.data,
                                                     create_product_form.product_stock.data,
                                                     create_product_form.description.data)

        # Image handling
        if 'image' in request.files and request.files['image'].filename != '':
            image = request.files['image']
            if image and allowed_file(image.filename):
                # Save the uploaded image
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename)
                image.save(image_path)
                print(f"Image saved at: {image_path}")

                create_product.set_image(filename)
        else:
            print("not working")

        # Assigning product with id
        create_product.set_product_id(seller_product_id)
        seller_product_id += 1
        #

        # create dict with product id as key and create_product as value; dict name is seller_products
        seller_products[create_product.get_product_id()] = create_product
        # store seller_products(dict) in seller_product_db, with seller_id as key and seller_products as value
        seller_product_info["products"] = seller_products
        seller_product_info["id"] = seller_product_id
        seller_product_db[str(seller_id)] = seller_product_info
        seller_product_db.close()

        return redirect(url_for('retrieve_product', seller_id_hash=seller_id_hash))
    if session.get('seller_logged_in'):
        print(seller_logged_in)
        return render_template('seller/createProduct.html', seller=seller_id_hash, seller_id=seller_id,
                               form=create_product_form)
    else:
        return redirect(url_for('seller_login'))


@app.route('/display_image/<filename>')
def display_image(filename):
    image_path = os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename)
    print(f"Displaying image from: {image_path}")
    return send_from_directory(app.config['UPLOAD_IMG_FOLDER'], filename)


@app.route('/seller/<seller_id_hash>/retrieveProducts')
def retrieve_product(seller_id_hash):
    if seller_id_hash != session['seller_id_hash']:
        print('route error')
        return render_template('error_msg.html')

    seller_id_hash = session['seller_id_hash']
    seller_id = session['seller_id']
    approved_sellers = {}
    approved_db = shelve.open('approved_sellers.db', 'r')
    approved_sellers = approved_db['Approved_sellers']
    if seller_id not in approved_sellers:
        return "seller not found"
    approved_db.close()

    seller_products = {}
    seller_product_db = shelve.open('seller-product.db', 'r')

    try:
        print(seller_id)
        seller_products = seller_product_db[str(seller_id)]['products']
    except KeyError:
        print("Error in retrieving products from seller-product.db.")

    seller_product_db.close()

    product_list = []
    for product_id, product in seller_products.items():
        product_list.append(product)

    if session.get('seller_logged_in'):
        return render_template('seller/retrieveProducts.html', seller=seller_id_hash, seller_id=seller_id,
                               count=len(product_list),
                               product_list=product_list)
    else:
        return redirect(url_for('seller_login'))


@app.route('/seller/<seller_id>/updateProduct/<int:product_id>/', methods=['GET', 'POST'])
def update_product(seller_id, product_id):
    if 'seller_id' not in session:
        return "Error: Seller ID not found in session"
    seller_id_hash = session['seller_id_hash']
    seller_id = session['seller_id']

    update_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and update_product_form.validate():

        seller_product_db = shelve.open('seller-product.db', 'c')
        seller_products = seller_product_db[str(seller_id)]

        # check if product exists in seller_products
        if product_id in seller_products['products']:
            sellerProduct = seller_products['products'][product_id]
            sellerProduct.set_product_name(update_product_form.product_name.data)
            sellerProduct.set_product_price(update_product_form.product_price.data)
            sellerProduct.set_product_stock(update_product_form.product_stock.data)
            sellerProduct.set_description(update_product_form.description.data)

            # Handle image update
            if 'image' in request.files and request.files['image'].filename != '':
                image = request.files['image']
                if image and allowed_file(image.filename):
                    # Delete previous image if it exists
                    if sellerProduct.get_image():
                        previous_image_path = os.path.join(app.config['UPLOAD_IMG_FOLDER'], sellerProduct.get_image())
                        if os.path.exists(previous_image_path):
                            os.remove(previous_image_path)
                            print(f"Previous image deleted at: {previous_image_path}")

                    # Save the uploaded image
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename)
                    image.save(image_path)
                    print(f"New image saved at: {image_path}")

                    sellerProduct.set_image(filename)

            seller_product_db[str(seller_id)] = seller_products
            seller_product_db.close()

            return redirect(url_for('retrieve_product', seller_id_hash=seller_id_hash))

    else:
        seller_product_db = shelve.open('seller-product.db', 'r')
        seller_products = seller_product_db[str(seller_id)]
        seller_product_db.close()

        if product_id in seller_products['products']:
            sellerProduct = seller_products['products'][product_id]
            update_product_form.product_name.data = sellerProduct.get_product_name()
            update_product_form.product_price.data = sellerProduct.get_product_price()
            update_product_form.product_stock.data = sellerProduct.get_product_stock()
            update_product_form.description.data = sellerProduct.get_description()
            if session.get('seller_logged_in'):
                return render_template('/seller/updateProduct.html', form=update_product_form, seller=seller_id_hash,
                                       seller_id=seller_id,
                                       product_id=product_id)
            else:
                return redirect(url_for('seller_login'))

    return "Product not found"


@app.route('/seller/<int:seller_id>/deleteProduct/<int:product_id>/', methods=['POST'])
def delete_product(seller_id, product_id):
    try:
        # Retrieve seller_id from session
        if 'seller_id' not in session:
            return "Error: Seller ID not found in session"
        seller_id_hash = session['seller_id_hash']

        seller_product_db = shelve.open('seller-product.db', 'c')
        seller_products = seller_product_db.get(str(seller_id), {'products': {}})

        # Get the product and its image filename
        deleted_product = seller_products['products'][product_id]
        deleted_image_filename = deleted_product.get_image()

        # Delete the product from the dictionary
        del seller_products['products'][product_id]
        seller_product_db[str(seller_id)] = seller_products
        seller_product_db.close()

        # Delete the associated image file
        if deleted_image_filename:
            deleted_image_path = os.path.join(app.config['UPLOAD_IMG_FOLDER'], deleted_image_filename)
            if os.path.exists(deleted_image_path):
                os.remove(deleted_image_path)
                print(f"Deleted image file at: {deleted_image_path}")
        if session.get('seller_logged_in'):
            return redirect(url_for('retrieve_product', seller_id_hash=seller_id_hash))
        else:
            return redirect(url_for('seller_login'))
    except Exception as e:
        print("Error:", str(e))
        return "Error in deleting product from seller-product db"


@app.route('/seller/<seller_id_hash>/orders',methods = ['POST','GET'])
def orders(seller_id_hash):
    print(seller_id_hash)
    seller_id = str(session['seller_id'])

    if session.get('seller_logged_in'):
        if seller_id_hash != session['seller_id_hash']:
            print('route error')
            return render_template('error_msg.html')
        seller_id_hash = session['seller_id_hash']
        print('sellerid:::', seller_id)
        orders_db = shelve.open('seller_order.db', 'r')
        seller_orders = {}
        try:
            seller_orders = orders_db[seller_id]
        except:
            print("The seller has no order yet")
        sent_out_orders = []
        to_send_orders = []
        seller_products = retrieve_db('seller-product.db', seller_id)
        print(seller_products)
        total_orders = []
        for order in seller_orders:
            for order_id in order:
                if order[order_id].get_sent_out():
                    sent_out_orders.append(order[order_id])
                else:
                    to_send_orders.append(order[order_id])
            total_orders.append(order)
        orders_db.close()
        current_order = []
        if request.method == 'POST':
            data = json.loads(request.data)
            updated_orders = {}
            _orders_ = shelve.open('seller_order.db', 'w')
            try:
                updated_orders = _orders_[seller_id]
            except:
                print("The seller has no order yet")
            if data["request_type"] == 'order_sent':
                print('received', data["id"])
                for order in updated_orders:
                    if data["id"] in order:
                        order[data["id"]].set_sent_out(True)
                        current_order.append(order[data["id"]])
                _orders_[seller_id] = updated_orders
                _orders_.close()
                if len(current_order) == 1:
                    send_notification(current_order[0].get_email(),current_order[0].get_order_id())
        return render_template('seller/orders.html', seller=seller_id_hash, sent_out=sent_out_orders,
                               to_send=to_send_orders, products=seller_products, orders=total_orders)
    else:
        return redirect(url_for('seller_login'))


@app.route('/seller/<seller_id_hash>/dashboard')
def seller_dashboard(seller_id_hash):

    if session.get('seller_logged_in'):
        if seller_id_hash != session['seller_id_hash']:
            print('route error')
            return render_template('error_msg.html')
        seller_id_hash = session['seller_id_hash']
        seller_id = session['seller_id']
        sellers_list = retrieve_db('approved_sellers.db', 'Approved_sellers')
        product_list = retrieve_db('seller-product.db',str(seller_id))
        print("sellers", sellers_list)
        seller_name = ''
        for i in sellers_list:
            if i.get_application_id() == seller_id:
                seller_name += i.get_name()


        try:
            with shelve.open('seller_order.db'):
                orders_db = shelve.open('seller_order.db', 'r')  # Just open and close to check if it exists
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                return False

        print("sellerid--", str(seller_id))
        seller_orders = {}
        try:
            seller_orders = orders_db[str(seller_id)]
        except:
            print("Error retrieving db")
        customers = 0
        sold_out = 0
        earning = 0.0
        operation_weeks = []
        products_record = []
        revenue_in_days = []
        today = date.today()
        for i in range(0, 7):
            operation_weeks.append(str(today - timedelta(days=i)))
        for order in seller_orders:
            revenue_per_day = {}
            for key,val in order.items():
                if val.get_date() in operation_weeks:
                    commission = val.get_total() * 0.10
                    earn_amt = val.get_total() - commission
                    earning += earn_amt
                    revenue_per_day["date"] = val.get_date()
                    revenue_per_day["revenue"] = val.get_total() - commission
                    print('total',val.get_total())
                    for i in val.get_order_products():
                        products_dict = {}
                        sold_out += int(i['quantity'])
                        print( i['product_id'],i['quantity'],i['product_price'])
                        products_dict['product_id'] = i['product_id']
                        products_dict['quantity'] = int(i['quantity'])
                        products_dict['revenue'] = int(i['product_price'])
                        products_record.append(products_dict)
                else:
                    print("no data within last week")
            revenue_in_days.append(revenue_per_day)
        products_main_record = []
        for i in products_record:
            if len(products_main_record) > 0:
                for j in products_main_record:
                    if j['product_id'] == i['product_id']:
                        j['quantity'] += i['quantity']
                        j['revenue'] += i['revenue']
                    else:
                        products_main_record.append(i)
                    break
            else:
                products_main_record.append(i)

        revenue_in_week = []
        for i in revenue_in_days:
            if len(revenue_in_week) > 0:
                for j in revenue_in_week:
                    if i['date'] == j['date']:
                        j['revenue'] += i['revenue']
                    else:
                        revenue_in_week.append(i)
                    break
            else:
                revenue_in_week.append(i)

        # getting the best selling item
        max_sold_out = max(entry['quantity'] for entry in products_record)
        max_sold_out_entries = [entry for entry in products_record if entry['quantity'] == max_sold_out]
        max_revenue = max(max_sold_out_entries, key=lambda x: x['revenue'])
        if len(max_sold_out_entries) == 1:
            max_sold_out_product_id = max_sold_out_entries[0]['product_id']
        else:
            max_revenue_entry = max_revenue
            max_sold_out_product_id = max_revenue_entry['product_id']
        best_selling_item = product_list[0].get(max_sold_out_product_id)
        print('best',max_sold_out,max_revenue)
        earning = '$' + str(earning)
        revenue_in_week_json = json.dumps(revenue_in_week)

        stock_left = 0
        for key,val in product_list[0].items():
            stock_left += val.get_product_stock()
        original_stock = sold_out + stock_left
        stock = [original_stock,sold_out]
        stock_json = json.dumps(stock)
        return render_template('seller/dashboard.html', seller=seller_id_hash, seller_name=seller_name,
                               customers=customers,
                               sold_out=sold_out, earning=earning, best_item = best_selling_item, revenue_in_week=revenue_in_week_json,
                               best_item_sold = max_sold_out, best_item_revenue = max_revenue, stock = stock_json)
    else:
        return redirect(url_for('seller_login'))

# operation_weeks = []
#         today = date.today()
#         for i in range(0, 7):
#             operation_weeks.append(str(today - timedelta(days=i)))
#         commission = 0.0
#         max_sold_out = 0
#         revenue_in_days = []
#         sellers_record = []
#         for i in orders:
#             sellers = {}
#             sold_out_quantity = 0
#             sellers_revenue = 0.0
#             for j in orders[i]:
#                 commission_for_time = {}
#                 for key,val in j.items():
#                     rate = val.get_total() * 0.10
#                     commission += rate
#                     if val.get_date() in operation_weeks:
#                         rate_in_week = val.get_total() * 0.10
#                         commission_for_time["date"] = val.get_date()
#                         commission_for_time["revenue"] = rate_in_week
#                         sellers_revenue += val.get_total()
#                         for p in val.get_order_products():
#                             print(' product', p)
#                             sold_out_quantity += int(p['quantity'])
#                             sellers['seller_id'] = i
#                             sellers['sold_out'] = sold_out_quantity
#                         sellers['revenue'] = sellers_revenue
#                     else:
#                         print("no data within last week")
#                 revenue_in_days.append(commission_for_time)


@app.route('/respond')
def respond():
    return render_template('sellers_application/respondPage.html')


@app.route('/errorPage')
def error():
    return render_template('staff/errorPage.html')


@app.route('/readApplicationsFromFile')
def readApplicationsFromFile():
    application_form = {}
    with shelve.open('application.db', 'c') as db:
        try:
            application_form = db['Application']
        except:
            print("Error in retrieving application from application.db")
        # store id
        try:
            prev_id = db['Id']
        except KeyError:
            if application_form.keys():
                prev_id = max(application_form.keys())
            else:
                prev_id = 0
        db['Id'] = prev_id
        with open('static/documents/applications.txt', 'r') as applicationFile:
            for i in applicationFile:
                seller = i.split(',')
                formatted_seller = []
                for j in seller:
                    withoutPunctuation = j.replace("\"", "")
                    formatted = withoutPunctuation.replace("\n", '')
                    formatted_seller.append(formatted)
                appForm = AppFormFormat(prev_id, formatted_seller[0], formatted_seller[1],
                                        formatted_seller[2],
                                        formatted_seller[3])
                appForm.set_date(formatted_seller[4])
                application_form[appForm.get_application_id()] = appForm
                db['Application'] = application_form
                # testing
                application_form = db['Application']
                appForm = application_form[appForm.get_application_id()]
                print(appForm.get_name(), appForm.get_email(),
                      "was stored in application.db successfully with user_id ==",
                      appForm.get_application_id())
                print("last id--", prev_id)
                if application_form.keys():
                    prev_id = max(application_form.keys())
                db['Id'] = prev_id
    return redirect(url_for('retrieveApplicationForms'))


@app.route("/register", methods=['GET', 'POST'])
def register():  # create
    global last_id
    registration_form = ApplicationForm(request.form)
    if request.method == 'POST' and registration_form.validate():
        application_form = {}
        db = shelve.open('application.db', 'c')
        try:
            application_form = db['Application']
        except:
            print("Error in retrieving application from application.db")
        # store id
        try:
            last_id = db['Id']
        except KeyError:
            if application_form.keys():
                last_id = max(application_form.keys())
            else:
                last_id = 0
        db['Id'] = last_id
        appForm = AppFormFormat(last_id, registration_form.seller_name.data, registration_form.business_name.data,
                                registration_form.seller_email.data,
                                registration_form.business_desc.data)
        application_form[appForm.get_application_id()] = appForm
        today = date.today()
        appForm.set_date(today)
        if 'support_document' in request.files:
            support_docs = request.files['support_document']
            if support_docs:
                filename = support_docs.filename
                if filename.endswith('.pdf'):
                    pdf_id = secrets.token_hex(16)
                    print('filename', filename)
                    os.makedirs(os.path.join(app.config["UPLOAD_DIRECTORY"], pdf_id))
                    support_docs.save(os.path.join(app.config["UPLOAD_DIRECTORY"], pdf_id, filename))
                    os.path.join(app.config["UPLOAD_DIRECTORY"], pdf_id)
                    message = f"{pdf_id}/{filename.split('.')[0]}.pdf"
                    print('message', message)
                    appForm.set_doc(message)
                else:
                    return redirect(url_for('error'))
        db['Application'] = application_form
        # testing
        application_form = db['Application']
        appForm = application_form[appForm.get_application_id()]
        print(appForm.get_name(), appForm.get_email(), "was stored in application.db successfully with user_id ==",
              appForm.get_application_id())
        print("last id--", last_id)
        if application_form.keys():
            last_id = max(application_form.keys())
        db['Id'] = last_id
        db.close()
        return redirect(url_for('respond'))
    return render_template('sellers_application/registration.html', form=registration_form)


@app.route('/view/<path:pdf>')
def view_pdf(pdf):
    pdf_path = os.path.join(app.config["UPLOAD_DIRECTORY"], pdf)
    return send_from_directory(os.path.dirname(pdf_path), os.path.basename(pdf_path), as_attachment=False)


@app.route('/staff/retrieveApplicationForms', methods=['POST', 'GET'])  # read
def retrieveApplicationForms():
    app_list = retrieve_db('application.db', 'Application')
    if session.get('staff_logged_in'):
        if request.method == 'POST':
            data_to_modify = json.loads(request.data)
            # for rejecting the form
            if data_to_modify['request_type'] == 'reject':
                print(data_to_modify['id'], "rejected")
                rejected = extracting('application.db', 'Application', data_to_modify['id'])
                if rejected.get_doc():
                    delete_folder(rejected)
                send_mail(rejected.get_email(), False, rejected.get_name(), '')
            if data_to_modify['request_type'] == 'approve':
                print(data_to_modify['id'], "approved")
                # take the approved application
                approved = extracting('application.db', 'Application', data_to_modify['id'])
                print("This user is approved", approved.get_application_id())
                # store in the approved_sellers
                approved_sellers = {}
                approved_db = shelve.open('approved_sellers.db', 'c')
                try:
                    approved_sellers = approved_db['Approved_sellers']
                except:
                    print("Error in retrieving sellers from application.db")

                passwords = []
                while True:
                    password = generate_password(14)
                    if password not in passwords:
                        break
                approved.set_password(password)
                approved_date = date.today()
                approved.set_date(approved_date)
                # storing approved seller
                approved_sellers[approved.get_application_id()] = approved
                approved_db['Approved_sellers'] = approved_sellers
                for key, seller in approved_db['Approved_sellers'].items():
                    passwords.append(seller.get_password())
                approved_db.close()
                print("seller mail and pw:",approved.get_email(),approved.get_password())
                send_mail(approved.get_email(), True, approved.get_seller_name(), password)
            if data_to_modify['request_type'] == 'filter':
                print(" got filered")
                if data_to_modify['id'] == '1':
                    certify = []
                    print('filtered')
                    for i in app_list:
                        print(i)
                        if i.get_doc():
                            print('have certificate')
                            certify.append(i)
                            print('certified sellers', i.get_name())
                    print('certified', certify)
                    return render_template('staff/retrieveAppForms.html', count=len(certify), app_list=certify)
        return render_template('staff/retrieveAppForms.html', count=len(app_list), app_list=app_list)
    else:
        return redirect(url_for('staff_login'))


@app.route('/staff/retrieveUpdateForms', methods=['POST', 'GET'])
def retrieveUpdateForms():  # for approving updates
    waiting_list = retrieve_db('updated_sellers.db', 'Updated_sellers')
    print('waiting list', waiting_list)
    if request.method == 'POST':
        data_to_modify = json.loads(request.data)
        # for rejecting the update form
        if data_to_modify['request_type'] == 'reject':
            print(data_to_modify['id'], "rejected")
            deleted_item = extracting('updated_sellers.db', 'Updated_sellers', data_to_modify['id'])
            if deleted_item.get_doc():
                delete_folder(deleted_item)
        # for approving the update
        if data_to_modify['request_type'] == 'approve':
            approved = extracting('updated_sellers.db', 'Updated_sellers', data_to_modify['id'])
            print("This user is approved", approved.get_application_id(), data_to_modify['id'])
            sellers = {}
            sellers_db = shelve.open('approved_sellers.db', 'w')
            sellers = sellers_db['Approved_sellers']
            if data_to_modify['id'] in sellers:
                seller = sellers.get(data_to_modify['id'])
                seller.set_name(approved.get_name())
                seller.set_email(approved.get_email())
                seller.set_password(approved.get_password())
                seller.set_desc(approved.get_desc())
            # seller.set_doc(approved.get_doc())
            sellers_db['Approved_sellers'] = sellers
            sellers_db.close()
    if session.get('staff_logged_in'):
        return render_template('staff/retrieveUpdateForms.html', count=len(waiting_list), waiting_list=waiting_list)
    else:
        return redirect(url_for('staff_login'))


@app.route('/staff/retrieveSellers', methods=['POST', 'GET'])
def retrieveSellers():
    sellers_list = retrieve_db('approved_sellers.db', 'Approved_sellers')
    print("sellers", sellers_list)
    if session.get('staff_logged_in'):
        if request.method == 'POST':
            data_to_modify = json.loads(request.data)
            # for removing
            if data_to_modify['request_type'] == 'delete':
                print(data_to_modify['id'], "deleted")
                deleted_item = extracting('approved_sellers.db', 'Approved_sellers', data_to_modify['id'])
                if deleted_item.get_doc():
                    delete_folder(deleted_item)
            elif data_to_modify['request_type'] == 'filter':
                if data_to_modify['filter_by'] == 'certificate':
                    certify = []
                    print('filtered')
                    for i in sellers_list:
                        print(i)
                        if i.get_doc():
                            print('have certificate')
                            certify.append(i)
                    return redirect(url_for('staff_login'))  # Redirect when filtering by certificate
        else:
            return render_template('staff/retrieveSellers.html', count=len(sellers_list), sellers=sellers_list)
    else:
        return redirect(url_for('staff_login'))  # Redirect if staff not logged in


@app.route('/staff/dashboard')
def dashboard():

    if session.get('staff_logged_in'):
        sellers = retrieve_db('approved_sellers.db', 'Approved_sellers')
        users = retrieve_db('user.db', 'Users')
        applications = retrieve_db('application.db', 'Application')
        orders = {}
        orders_db = shelve.open('seller_order.db', 'r')
        seller_list = []
        for i in orders_db:
            seller_list.append(i)
        for j in seller_list:
            try:
                orders[j] = orders_db[j]
            except:
                print("Key does not exists")

        operation_weeks = []
        today = date.today()
        for i in range(0, 7):
            operation_weeks.append(str(today - timedelta(days=i)))

        commission = 0.0
        revenue_in_days = []
        sellers_record = []
        for i in orders:
            sellers = {}
            sold_out_quantity = 0
            sellers_revenue = 0.0
            for j in orders[i]:
                commission_for_time = {}
                for key,val in j.items():
                    rate = val.get_total() * 0.10
                    commission += rate
                    if val.get_date() in operation_weeks:
                        rate_in_days = val.get_total() * 0.10
                        commission_for_time["date"] = val.get_date()
                        commission_for_time["revenue"] = rate_in_days
                        sellers_revenue += val.get_total()
                        for p in val.get_order_products():
                            print(' product', p)
                            sold_out_quantity += int(p['quantity'])
                            sellers['seller_id'] = i
                            sellers['sold_out'] = sold_out_quantity
                        sellers['revenue'] = sellers_revenue
                    else:
                        print("no data within last week")
                revenue_in_days.append(commission_for_time)
            sellers_record.append(sellers)
        print(sellers_record)
        # getting the best seller
        max_sold_out = max(entry['sold_out'] for entry in sellers_record)
        max_sold_out_entries = [entry for entry in sellers_record if entry['sold_out'] == max_sold_out]
        max_revenue = max(max_sold_out_entries, key=lambda x: x['revenue'])
        if len(max_sold_out_entries) == 1:
            max_sold_out_seller_id = max_sold_out_entries[0]['seller_id']
        else:
            max_revenue_entry = max_revenue
            max_sold_out_seller_id = max_revenue_entry['seller_id']
        revenue_in_week = []
        for i in revenue_in_days:
            if len(revenue_in_week) > 0:
                for j in revenue_in_week:
                    if i['date'] == j['date']:
                        j['revenue'] += i['revenue']
                    else:
                        revenue_in_week.append(i)
                    break
            else:
                revenue_in_week.append(i)
        json_revenue_in_week = json.dumps(revenue_in_week)
        greenify_sellers = {}
        try:
            with shelve.open('approved_sellers.db','r') as approved_sellers:
                greenify_sellers = approved_sellers['Approved_sellers']
        except dbm.error:
            return "DB file does not exists"

        best_seller = {}
        for key,val in greenify_sellers.items():
            if int(max_sold_out_seller_id) == key:
                best_seller = val
        print(" best seller",best_seller.get_name(),max_sold_out,max_revenue)

        return render_template('staff/dashboard.html', sellers_count=sellers, users_count=users, commission = f"${commission}", revenue_in_week = json_revenue_in_week, best_seller = best_seller,sold_out= max_sold_out,best_selling_detail = max_revenue)
    else:
        return redirect(url_for('staff_login'))


@app.route('/seller/<seller_id_hash>/updateSeller', methods=['GET', 'POST'])
def update_seller(seller_id_hash):
    if seller_id_hash != session['seller_id_hash']:
        print('route error')
        return render_template('error_msg.html')

    seller_id_hash = session['seller_id_hash']
    seller_id = session['seller_id']

    update_seller_form = ApplicationForm(request.form)
    if request.method == 'POST':
        updated_sellers = {}
        db = shelve.open('updated_sellers.db', 'c')
        approved_sellers = {}
        approved_db = shelve.open('approved_sellers.db', 'r')
        approved_sellers = approved_db['Approved_sellers']

        seller = approved_sellers.get(seller_id)

        seller.set_seller_name(update_seller_form.business_name.data)
        seller.set_name(update_seller_form.business_name.data)
        seller.set_email(update_seller_form.seller_email.data)
        seller.set_desc(update_seller_form.business_desc.data)
        seller.set_doc(update_seller_form.support_document.data)

        # for adding data
        updated_sellers[seller.get_application_id()] = seller
        db['Updated_sellers'] = updated_sellers
        db.close()

        return render_template('/seller/update_successful.html', form=update_seller_form, seller_id_hash=seller_id_hash,
                               seller_id=seller_id)

    else:
        approved_sellers = {}
        approved_db = shelve.open('approved_sellers.db', 'r')
        approved_sellers = approved_db['Approved_sellers']
        approved_db.close()

        seller = approved_sellers.get(seller_id)
        update_seller_form.business_name.data = seller.get_seller_name()
        update_seller_form.seller_email.data = seller.get_email()
        update_seller_form.business_name.data = seller.get_name()
        update_seller_form.business_desc.data = seller.get_desc()
        update_seller_form.support_document.data = seller.get_doc()

        if session.get('seller_logged_in'):
            return render_template('/seller/updateSeller.html', form=update_seller_form, seller_id_hash=seller_id_hash,
                                   seller_id=seller_id)
        else:
            return redirect(url_for('seller_login'))


@app.route('/seller/<seller_id_hash>/deleteSeller', methods=['POST'])
def delete_seller(seller_id_hash):
    if seller_id_hash != session['seller_id_hash']:
        print('route error')
        return render_template('error_msg.html')

    seller_id_hash = session['seller_id_hash']
    seller_id = session['seller_id']
    approved_sellers = {}
    approved_db = shelve.open('approved_sellers.db', 'w')
    approved_sellers = approved_db['Approved_sellers']

    approved_sellers.pop(seller_id)
    seller_logout(seller_id_hash)
    seller_product_db = shelve.open('seller-product.db', writeback=True)
    if str(seller_id) in seller_product_db:
        del seller_product_db[str(seller_id)]
        print(f"Products of seller {seller_id} deleted successfully.")
    else:
        print(f"No products found for seller {seller_id}.")

    approved_db['Approved_sellers'] = approved_sellers
    approved_db.close()
    seller_product_db.close()

    return "Your account has successfully been deleted."

# game1
@app.route('/game1')
def game1():
    if not (session.get('user_logged_in') or session.get('seller_logged_in') or session.get('staff_logged_in')):
        # If no user is logged in, redirect to login page
        return redirect(url_for('login'))
    # Assuming 'user_id' is set for any logged-in user, otherwise, adjust accordingly
    user_id = session.get('user_id', 'Unknown Player')
    return render_template('/games/game1.html', user_id=user_id)


@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    player_name = session.get('user_id', 'Unknown Player')
    new_score = data['score']

    with shelve.open('game_scores.db', writeback=True) as db:
        current_high_score = db.get(player_name, 0)
        if new_score > current_high_score:
            db[player_name] = new_score

    return jsonify({'message': 'Score received'})


@app.route('/view_scores')
def view_scores():
    with shelve.open('game_scores.db') as db:
        scores = dict(db)
    return jsonify(scores)


@app.route('/get_scores')
def get_scores():
    with shelve.open('game_scores.db') as db:
        scores = dict(db)
    return jsonify(scores)


@app.route('/get_score/<player_name>')
def get_score(player_name):
    with shelve.open('game_scores.db') as db:
        score = db.get(player_name, "Player not found")
    return jsonify({player_name: score})


@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.get_json()
    player_name = data['player_name']
    new_score = data['score']
    with shelve.open('game_scores.db', writeback=True) as db:
        db[player_name] = new_score
    return jsonify({'message': 'Score updated successfully!'})


@app.route('/delete_score', methods=['POST'])
def delete_score():
    data = request.get_json()
    player_name = data['player_name']

    with shelve.open('game_scores.db', writeback=True) as db:
        if player_name in db:
            del db[player_name]
            message = "Player score deleted successfully."
        else:
            message = "Player not found."

    return jsonify({'message': message})


@app.route('/delete_score_page')
def delete_score_page():
    return render_template('/staff/game1_delete_player.html')


@app.route('/game2')
def game2():
    if not (session.get('user_logged_in') or session.get('seller_logged_in') or session.get('staff_logged_in')):
        # If no user is logged in, redirect to login page
        return redirect(url_for('login'))
    # Assuming 'user_id' is set for any logged-in user, otherwise, adjust accordingly
    user_id = session.get('user_id', 'Unknown Player')
    return render_template('/games/game2.html', user_id=user_id)

@app.route('/game2/start')
def start_game():
    words = ["reuse", "reduce", "recycle", "sustainability", "environment", "conservation", "green"]
    selected_word = random.choice(words)
    session['game_word'] = selected_word  # Store the selected word in session
    return jsonify({'success': True})


# @app.route('/about_us')
# def about_us():
#     return render_template('/customer/about_us.html')

if __name__ == "__main__":
    app.run(debug=True)
