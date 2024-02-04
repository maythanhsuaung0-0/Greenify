from flask import Flask, render_template, request, redirect, url_for, json, jsonify, session, send_file, send_from_directory
from Forms import CreateUserForm, StaffLoginForm, LoginForm
import shelve, User, SellerProduct, application
from sellerproductForm import CreateProductForm
from applicationForm import ApplicationForm
from application import ApplicationFormFormat as AppFormFormat
# for accessing and storing image
import os
# from set_image import create_image_set
import secrets
import shutil
import User_login
from werkzeug.utils import secure_filename
from datetime import date
from urllib.parse import quote
# for sending mail
import string
from send_email import send_mail
import uuid
from crud_functions import *
from seller_order import SellerOrder
from searchForm import Search
from updateUser import update
from chat import get_response

app = Flask(__name__, static_url_path='/static')
user_logged_in = False
seller_logged_in = False
app.secret_key = 'my_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_DIRECTORY'] = "C:/Users/mayth/PycharmProjects/Greenify/static/documents/uploads"
UPLOAD_FOLDER = 'C:/Users/Jia Ying/Downloads/Greenify/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_IMG_FOLDER = 'C:/Users/Rachel/PycharmProjects/Greenify/static/product_image'
# UPLOAD_IMG_FOLDER = url_for('static', filename='/product_image/')
app.config['UPLOAD_IMG_FOLDER'] = UPLOAD_IMG_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Helper function to get initial reviews
def get_initial_reviews(seller_id, product_id):
    reviews_db = shelve.open('reviews.db', 'r')
    ratings_reviews_dict = reviews_db.get('Reviews', {})

    # Get the seller's dictionary
    seller_reviews = ratings_reviews_dict.get(seller_id, {})

    # Get the list of reviews for the product
    return seller_reviews.get(product_id, [])


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
            return approved_sellers[seller_id].get_seller_name()


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
    try:
        user = session['user_id']
        user_id_hash = session['user_id_hash']
        return render_template("customer/homepage.html", user=user_id_hash, saved_cart_qty=cart_qty(user),
                               form=search_form)
    except:
        return render_template("customer/homepage.html", user=None, form=search_form)


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
                # Get the existing dictionary of ratings and reviews or create a new one
                ratings_reviews_dict = reviews_db.get('Reviews', {})

                # Get the seller ID and product ID from the sent data
                seller_id = int(sent_data.get('seller_id', ''))  # Convert to int
                product_id = int(sent_data.get('product_id', ''))  # Convert to int

                # Ensure the seller ID is in the dictionary
                if seller_id not in ratings_reviews_dict:
                    ratings_reviews_dict[seller_id] = {}

                # Get the seller's dictionary
                seller_reviews = ratings_reviews_dict[seller_id]

                # Ensure the product ID is in the seller's dictionary
                if product_id not in seller_reviews:
                    seller_reviews[product_id] = []

                # Get the list of reviews for the product
                product_reviews = seller_reviews[product_id]

                # Get the new feedback
                new_feedback = {
                    'rating': sent_data.get('ratings', 0),
                    'review': sent_data.get('reviews', '')
                }

                # Add the new feedback to the list under the product ID
                product_reviews.append(new_feedback)

                # Store the updated dictionary back to the database
                reviews_db['Reviews'] = ratings_reviews_dict
                # print("seller_id:", seller_id)
                # print("product_id:", product_id)
                print("ratings_reviews_dict:", ratings_reviews_dict)
                # print("seller_reviews:", seller_reviews)
                # print("product_reviews:", product_reviews)

            except Exception as e:
                print("Error in handling customer feedback:", str(e))
            finally:
                reviews_db.close()
                return json.jsonify({"data": product_reviews, "result": True})

        # New
        # Retrieving r and r
        reviews_db = shelve.open('reviews.db', 'r')
        ratings_reviews_dict = reviews_db.get('Reviews', {})

        # Get the seller ID and product ID
        seller_id = int(seller_id)
        product_id = int(product_id)

        # Get the seller's dictionary
        seller_reviews = ratings_reviews_dict.get(seller_id, {})

        # Get the list of reviews for the product
        product_reviews = seller_reviews.get(product_id, [])
        # test codes 
        # print("seller_id:", seller_id)
        # print("product_id:", product_id)
        # print("ratings_reviews_dict:", ratings_reviews_dict)
        # print("seller_reviews:", seller_reviews)
        # print("product_reviews:", product_reviews)
        # Close the database after retrieving data
        reviews_db.close()

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

    # NEW
    # Handle GET requests
    # if request.method == "GET":
    #     # Initial retrieval of reviews for the product
    #     initial_reviews = get_initial_reviews(seller_id, product_id)
    #     # print(initial_reviews)
    #     return json.jsonify({'data': initial_reviews, 'result': True})


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
        return render_template('error_msg.html', user=session['user_id_hash'], saved_cart_qty=cart_qty(session['user_id']), form=search_form)

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
        return render_template('error_msg.html', user=session['user_id_hash'], saved_cart_qty=cart_qty(session['user_id']), form=search_form)

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

            # Open User Shopping Cart
            user_shopping_cart_db = shelve.open('user_shopping_cart.db')
            users_shopping_cart = user_shopping_cart_db[email]
            user_selected_product = users_shopping_cart["selected_product"]
            amt_paid = users_shopping_cart["payable"]

            # Accessing Info of each individual product bought
            order_history_db = shelve.open('order_history.db')

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

                # Save Qty
                product.set_product_stock(product_qty)
                seller_products[product_id] = product
                seller_product_info['products'] = seller_products
                seller_product_db[str(seller_id)] = seller_product_info
                seller_product_db.close()

                # Creating a Seller Order
                seller_orders = {}
                seller_order_db = shelve.open('seller_order.db')
                try:
                    seller_orders = seller_order_db[str(seller_id)]
                    order = seller_orders[email]
                    order.set_order_products(product_id, bought_qty)

                except KeyError:
                    order = SellerOrder(name, email, address)
                    order.set_order_products(product_id, bought_qty)

                seller_orders[email] = order
                seller_order_db[str(seller_id)] = seller_orders
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

            order_history_id = uuid.uuid4().hex[:8]

            # Saving Datas
            order_history['items'] = user_selected_product
            order_history['shipping_info'] = {'name': name, 'address': address}
            order_history['amt_paid'] = amt_paid

            user_order_history[str(order_history_id)] = order_history
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
    print(payable)

    return render_template("customer/payment.html", user=user_id_hash, user_id=user, user_address=user_info.get_address(), user_name=user_info.get_name(), payable=payable, saved_cart_qty=cart_qty(user), form=search_form)


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
    return render_template('customer/success_payment.html', user=user, saved_cart_qty=cart_qty(user), form=search_form)


@app.route('/<user_id_hash>/order_history', methods=['GET', 'POST'])
def order_history(user_id_hash):

    search_form = Search(request.form)

    if user_id_hash != session['user_id_hash']:
        return render_template('error_msg.html', user=session['user_id_hash'], saved_cart_qty=cart_qty(session['user_id']), form=search_form)
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
    except:

        return render_template('customer/empty_order_history.html', user=user_id_hash, saved_cart_qty=cart_qty(user),
                               form=search_form)

    for order_id in all_orders:
        for items in all_orders[order_id]['items']:
            print(all_orders[order_id]['items'][items])

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
    global user_id, user
    error = None
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        users_dict = {}
        user = User_login.UserLogin(login_form.email.data, login_form.password.data)
        db = shelve.open('user.db', 'r')
        passwords = []
        for user_id, user_instance in db['Users'].items():
            passwords.append(user_instance.get_password())
        try:
            if 'Users' in db:
                users_dict = db["Users"]
                if login_form.email.data in users_dict and login_form.password.data in passwords:
                    key = get_key(login_form.password.data, db['Users'])
                    if key == user.get_email():
                        user_id_hash = uuid.uuid4().hex
                        session['user_id_hash'] = user_id_hash
                        session['user_id'] = user_id
                        session['user_logged_in'] = True
                        print(session['user_id'])
                        print(f"User login status = {session.get('user_logged_in')}")
                        return redirect(session['last_url'])
                error = 'Email or Password is incorrect, please try again.'
            else:
                return render_template('customer/createUser.html')
        except:
            print("Error in opening user.db")
    return render_template('customer/login.html', form=login_form, user_logged_in=user_logged_in, error=error)


def get_key(val, users_dict):
    for key, value in users_dict.items():
        if val == value.get_password():
            return key


@app.route("/check_login")
def check_login():
    return user_logged_in


@app.route('/user/logout')
def user_logout():
    if session.get('user_logged_in'):
        session.pop('user_logged_in', None)
        session.pop('user_id', None)
        session.pop('user_id_hash', None)
    print(f"User login status = {session.get('user_logged_in')}")
    return "You have successfully logged out from your account."


@app.route('/seller/logout')
def seller_logout():
    if session.get('seller_logged_in'):
        session.pop('seller_logged_in', None)
    print(f"Seller login status = {session.get('seller_logged_in')}")


@app.route('/<user_id_hash>/profile', methods=['GET', 'POST'])
def profile(user_id_hash):
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

    user_data = shelve.open('user.db')
    users_dict = user_data.get('Users', {})

    user_obj = users_dict.get(user)
    user_data.close()
    return render_template('customer/profile.html', user=user_id_hash, saved_cart_qty=cart_qty(user),
                           form=search_form, user_data=user_obj)


@app.route('/<user_id_hash>/updateUser', methods=['GET', 'POST'])
def update_user(user_id_hash):
    search_form = Search(request.form)

    if user_id_hash != session['user_id_hash']:
        return render_template('error_msg.html', user=session['user_id_hash'], saved_cart_qty=cart_qty(session['user_id']), form=search_form, user_id_hash=user_id_hash)

    user_id_hash = session['user_id_hash']
    user = session['user_id']
    error = None
    update_user_form = CreateUserForm(request.form)

    if request.method == 'POST':
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user_obj = users_dict.get(user)

        if update_user_form.validate():
            if len(str(update_user_form.contact_number.data)) != 8:
                error = 'Phone number must be 8 digits.'
            elif len(str(update_user_form.postal_code.data)) != 6:
                error = 'Postal code must be 6 digits.'
            elif update_user_form.password.data != update_user_form.confirm_password.data:
                error = 'Passwords must match.'
            else:
                user_obj.set_email(update_user_form.email.data)
                user_obj.set_password(update_user_form.password.data)
                user_obj.set_name(update_user_form.name.data)
                user_obj.set_contact_number(update_user_form.contact_number.data)
                user_obj.set_postal_code(update_user_form.postal_code.data)
                user_obj.set_address(update_user_form.address.data)
                users_dict[user] = user_obj
                error = "Update Successful."
        else:
            error = "Update Unsuccessful."

        db['Users'] = users_dict
        db.close()

    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']

        user_obj = users_dict.get(user)
        if user:
            update_user_form.email.data = user_obj.get_email()
            update_user_form.password.data = user_obj.get_password()
            update_user_form.name.data = user_obj.get_name()
            update_user_form.contact_number.data = user_obj.get_contact_number()
            update_user_form.postal_code.data = user_obj.get_postal_code()
            update_user_form.address.data = user_obj.get_address()

        db.close()

    if session.get('user_logged_in'):
        return render_template('customer/updateUser.html', form=update_user_form, error=error, db=user_obj, user_id_hash=user_id_hash)
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

    db['Users'] = users_dict
    db.close()

    return "Your account has successfully been deleted."


@app.route('/stafflogin', methods=['GET', 'POST'])
def staff_login():
    error = None
    staff_login_form = StaffLoginForm(request.form)
    if request.method == 'POST' and staff_login_form.validate():
        if staff_login_form.admin_email.data == 'admin@gmail.com' and staff_login_form.admin_password.data == 'admin_password':
            return redirect(url_for('retrieveApplicationForms'))
        else:
            error = 'Email or Password is incorrect, please try again.'
    return render_template('staff/staff_login.html', form=staff_login_form, error=error)


@app.route('/seller/login', methods=['GET', 'POST'])
def seller_login():
    global seller_password
    error = None
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
        print(sellers)
        for j in sellers_list:
            seller_email.append(j.get_email())
        print(seller_email)
        for i in sellers:
            print(i)
            if login_form.email.data == i["email"] and login_form.password.data == i["pw"]:
                seller_id = i['id']
                session['seller_logged_in'] = True
                print(f"Seller login status = {session.get('seller_logged_in')}")
                if session.get('seller_logged_in'):
                    return redirect(url_for('seller_dashboard', seller_id=seller_id))
            else:
                error = 'Email or Password is incorrect, please try again.'
    return render_template('seller/seller_login.html', form=login_form, seller_logged_in=seller_logged_in, error=error)


@app.route('/seller/<int:seller_id>/createProduct', methods=['GET', 'POST'])
def create_product(seller_id):
    approved_sellers = {}
    approved_db = shelve.open('approved_sellers.db', 'r')
    approved_sellers = approved_db['Approved_sellers']
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

        # New
        if 'image' in request.files and request.files['image'].filename != '':
            image = request.files['image']
            if image and allowed_file(image.filename):
                # Save the uploaded image
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename)
                image.save(image_path)
                print(f"Image saved at: {image_path}")

                # Call the create_image_set function
                # create_image_set(app.config['UPLOAD_IMG_FOLDER'], filename)

                # Set the image field in your SellerProduct instance
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
        # New
        seller_product_info["products"] = seller_products
        seller_product_info["id"] = seller_product_id
        seller_product_db[str(seller_id)] = seller_product_info
        #
        seller_product_db.close()

        return redirect(url_for('retrieve_product', seller_id=seller_id))
    return render_template('seller/createProduct.html', form=create_product_form)


@app.route('/display_image/<filename>')
def display_image(filename):
    image_path = os.path.join(app.config['UPLOAD_IMG_FOLDER'], filename)
    print(f"Displaying image from: {image_path}")
    return send_from_directory(app.config['UPLOAD_IMG_FOLDER'], filename)


@app.route('/seller/<int:seller_id>/retrieveProducts')
def retrieve_product(seller_id):
    approved_sellers = {}
    approved_db = shelve.open('approved_sellers.db', 'r')
    approved_sellers = approved_db['Approved_sellers']
    if seller_id not in approved_sellers:
        return "seller not found"
    approved_db.close()

    seller_products = {}
    seller_product_db = shelve.open('seller-product.db', 'r')

    try:
        seller_products = seller_product_db[str(seller_id)]['products']
    except KeyError:
        print("Error in retrieving products from seller-product.db.")

    seller_product_db.close()

    product_list = []
    for product_id, product in seller_products.items():
        product_list.append(product)

    return render_template('seller/retrieveProducts.html', seller_id=seller_id, count=len(product_list),
                           product_list=product_list)


@app.route('/seller/<int:seller_id>/updateProduct/<int:product_id>/', methods=['GET', 'POST'])
def update_product(seller_id, product_id):
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

                    # Call the create_image_set function if needed (not sure yet)
                    # create_image_set(app.config['UPLOAD_IMG_FOLDER'], filename)

                    # Set the image field in your SellerProduct instance
                    sellerProduct.set_image(filename)

            seller_product_db[str(seller_id)] = seller_products
            seller_product_db.close()

            return redirect(url_for('retrieve_product', seller_id=seller_id))

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

            return render_template('/seller/updateProduct.html', form=update_product_form, seller_id=seller_id,
                                   product_id=product_id)
    return "Product not found"


@app.route('/seller/<int:seller_id>/deleteProduct/<int:product_id>/', methods=['POST'])
def delete_product(seller_id, product_id):
    try:
        seller_product_db = shelve.open('seller-product.db', 'c')
        seller_products = seller_product_db[str(seller_id)]

        # Get the product and its image filename
        deleted_product = seller_products['products'][product_id]
        deleted_image_filename = deleted_product.get_image()

        # Delete the product from the dictionary
        seller_products['products'].pop(product_id)
        seller_product_db[str(seller_id)] = seller_products
        seller_product_db.close()

        # Delete the associated image file
        if deleted_image_filename:
            deleted_image_path = os.path.join(app.config['UPLOAD_IMG_FOLDER'], deleted_image_filename)
            if os.path.exists(deleted_image_path):
                os.remove(deleted_image_path)
                print(f"Deleted image file at: {deleted_image_path}")

        return redirect(url_for('retrieve_product', seller_id=seller_id))
    except:
        return "Error in deleting product from seller-product db"


@app.route('/seller/<int:seller_id>/orders')
def orders(seller_id):
    return render_template('seller/orders.html')


@app.route('/seller/<int:seller_id>/dashboard')
def seller_dashboard(seller_id):
    return render_template('seller/dashboard.html')


@app.route('/respond')
def respond():
    return render_template('sellers_application/respondPage.html')


@app.route('/errorPage')
def error():
    return render_template('staff/errorPage.html')


@app.route("/register", methods=['GET', 'POST'])
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
        print(appForm.get_date())
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
            # storing approved seller
            approved_sellers[approved.get_application_id()] = approved
            approved_db['Approved_sellers'] = approved_sellers
            for key, seller in approved_db['Approved_sellers'].items():
                passwords.append(seller.get_password())
            approved_db.close()

            send_mail(approved.get_email(), True, approved.get_seller_name(), password)
        if data_to_modify['request_type'] == 'filter':
            if data_to_modify['filter_by'] == 'certificate':
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
    return render_template('staff/retrieveUpdateForms.html', count=len(waiting_list), waiting_list=waiting_list)


@app.route('/staff/retrieveSellers', methods=['POST', 'GET'])
def retrieveSellers():  # read
    sellers_list = retrieve_db('approved_sellers.db', 'Approved_sellers')
    print("sellers", sellers_list)
    if request.method == 'POST':
        data_to_modify = json.loads(request.data)
        # for removing
        if data_to_modify['request_type'] == 'delete':
            print(data_to_modify['id'], "deleted")
            deleted_item = extracting('approved_sellers.db', 'Approved_sellers', data_to_modify['id'])
            if deleted_item.get_doc():
                delete_folder(deleted_item)
    return render_template('staff/retrieveSellers.html', count=len(sellers_list), sellers=sellers_list)


@app.route('/staff/dashboard')
def dashboard():
    sellers = retrieve_db('approved_sellers.db', 'Approved_sellers')
    users = retrieve_db('user.db', 'Users')
    return render_template('staff/dashboard.html', sellers_count=len(sellers), users_count=len(users))


@app.route('/seller/<int:seller_id>/profile', methods=['GET', 'POST'])
def update_seller(seller_id):
    filename = session.get('filename', '/images/placeholder.jpg')
    update_seller_form = ApplicationForm(request.form)
    if request.method == 'POST' and update_seller_form.validate():
        updated_sellers = {}
        db = shelve.open('updated_sellers.db', 'c')
        approved_sellers = {}
        approved_db = shelve.open('approved_sellers.db', 'r')
        approved_sellers = approved_db['Approved_sellers']

        seller = approved_sellers.get(seller_id)

        if 'image' in request.files:
            uploaded_file = request.files['image']
            if uploaded_file.filename != '':
                filename = secure_filename(uploaded_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                uploaded_file.save(filepath)
                print(f"Image saved at: {filepath}")
                session['filename'] = filename  # Update the session data

        seller.set_seller_name(update_seller_form.business_name.data)
        seller.set_email(update_seller_form.seller_email.data)
        seller.set_name(update_seller_form.business_name.data)
        seller.set_desc(update_seller_form.business_desc.data)
        seller.set_doc(update_seller_form.support_document.data)
        seller.set_profile_image(update_seller_form.profile_pic.data)

        # for adding data
        updated_sellers[seller.get_application_id()] = seller
        db['Updated_sellers'] = updated_sellers
        db.close()

        return 'Your info will be sent to our staff for review :)'
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
        # update_seller_form.profile_pic.data = seller.get_profile_image()

        return render_template('/seller/updateSeller.html', form=update_seller_form, seller_id=seller_id)


@app.route('/deleteSeller/<int:seller_id>', methods=['POST'])
def delete_seller(seller_id):
    approved_sellers = {}
    approved_db = shelve.open('approved_sellers.db', 'w')
    approved_sellers = approved_db['Approved_sellers']

    approved_sellers.pop(seller_id)

    approved_db['Approved_sellers'] = approved_sellers
    approved_db.close()

    return "Your account has successfully been deleted."


# game1
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


@app.route('/')
def dummy_index():
    message = 'To test the game1 route, append /game1 at the end of the URL string'
    return message


@app.route('/game1')
def game1():
    user_id = session.get('user_id', 'Unknown Player')
    if session.get('logged_in'):
        return render_template('/games/game1.html', user_id=user_id)
    else:
        return redirect(url_for('login'))


# @app.route('/about_us')
# def about_us():
#     return render_template('/customer/about_us.html')

if __name__ == "__main__":
    app.run(debug=True)
