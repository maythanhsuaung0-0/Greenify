from flask import Flask, render_template, request, redirect, url_for, json
from Forms import CreateUserForm, StaffLoginForm
import shelve, User, SellerProduct, application
from sellerproductForm import CreateProductForm
from applicationForm import ApplicationForm
from application import ApplicationFormFormat as AppFormFormat
# for accessing and storing image
import os
from set_image import create_image_set
import secrets
import shutil
from werkzeug.utils import secure_filename
from datetime import date
from urllib.parse import quote
# for sending mail
import string
from send_email import send_mail

app = Flask(__name__, static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_DIRECTORY'] = "C:/Users/mayth/PycharmProjects/Greenify/static/images/uploads"

def extracting(my_db, db_key, id):  #function for deleting and taking out the deleted value
    form_dict = {}
    db = shelve.open(my_db, 'w')
    form_dict = db[db_key]
    item = form_dict.pop(id)
    db[db_key] = form_dict
    db.close()
    return item


def delete_folder(item):
    filename = item.get_doc()
    folder_path, _ = os.path.split(filename)
    full_folder_path = os.path.join(app.config["UPLOAD_DIRECTORY"], folder_path)

    if os.path.exists(full_folder_path):
        shutil.rmtree(full_folder_path)
        print(f"folder deleted: {full_folder_path}")


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


@app.route("/")
def home():
    saved_cart_qty = cart_qty("hi@gmail.com")
    return render_template("customer/homepage.html")


@app.route("/Product/<seller>/<int:product_id>", methods=['GET', 'POST'])
def product(seller, product_id):
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
    approved_sellers = {}
    approve_seller_db = shelve.open('approved_sellers.db')
    try:
        approved_sellers = approve_seller_db['Approved_sellers']
    except:
        return render_template('customer/error_msg.html', msg="Sorry, Page Could Not Be Found")
    seller_found = False
    for id in approved_sellers:
        if seller == approved_sellers[id].get_name():
            seller_id = approved_sellers[id].get_id()
            seller_found = True
    if seller_found == False:
        return render_template('customer/error_msg.html', msg="Sorry, Page Could Not Be Found")

    # Retrieving Product for html to display
    seller_products = {}
    seller_product_db = shelve.open('seller-product.db', 'c')
    try:
        seller_products = seller_product_db[str(seller_id)]

    except:
        return render_template('customer/error_msg.html', msg="Sorry, Page Could Not Be Found")

    product = seller_products[product_id]
    seller_product_db.close()

    # Received AJAX Request for Add To Cart
    if request.method == "POST":
        product = json.loads(request.data)
        del product["cart_item_qty"]

        send_data = json.loads(request.data)

        # Saving Shopping Cart Items
        # Dummy User (User persistent Log In not Developed)
        users_shopping_cart = {}
        user_selected_product = {}
        shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
        try:
            users_shopping_cart = shopping_cart_db["hi@gmail.com"]
            user_selected_product = users_shopping_cart["selected_product"]
        except KeyError:
            print("KeyError in opening saved cart items")
        except:
            print("Error in retrieving User Shopping Cart Info in user_shopping_cart.db")

        user_selected_products = {}

        # Check if Product has been added before
        try:
            saved_product = user_selected_product[product["seller"] + str(product["product_id"])]
            saved_product["product_qty"] += product["product_qty"]
            user_selected_product[product["seller"] + str(product["product_id"])] = saved_product
            users_shopping_cart["selected_product"] = user_selected_product
            shopping_cart_db["hi@gmail.com"] = users_shopping_cart
        except:
            user_selected_product[product["seller"] + str(product["product_id"])] = product
            users_shopping_cart["selected_product"] = user_selected_product

        # Update Cart Qty
        cart_qty = send_data["cart_item_qty"]
        cart_qty = int(cart_qty)
        print(cart_qty)
        saved_cart_qty = 0
        try:
            saved_cart_qty = users_shopping_cart["cart_qty"]
        except:
            print("Failed loading cart qty")

        saved_cart_qty = cart_qty
        users_shopping_cart["cart_qty"] = saved_cart_qty

        # Saving new info into db
        shopping_cart_db["hi@gmail.com"] = users_shopping_cart
        shopping_cart_db.close()

        return json.jsonify({"data": cart_qty, "result": True})

    return render_template("customer/test_product.html", product=product, seller=seller, seller_id=seller_id,
                           saved_cart_qty=cart_qty("hi@gmail.com"))


@app.route('/<user>/cart', methods=['GET', 'POST'])
def shopping_cart(user):
    users_shopping_cart = {}
    user_selected_product = {}
    shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
    try:
        users_shopping_cart = shopping_cart_db[user]
        user_selected_product = users_shopping_cart["selected_product"]
    except KeyError:
        return render_template("customer/error_msg.html", msg="This user shopping cart is empty")
    except:
        print("Error in retrieving User Shopping Cart Info in user_shopping_cart.db")

    display_shopping_cart = []
    # print("ll")
    # print(user_selected_product)
    for product_selected_name in user_selected_product:
        product_selected = user_selected_product[product_selected_name]

        # Getting the Product Object
        seller_product = {}
        seller_product_db = shelve.open("seller-product.db")
        # print('ho')
        # print(product_selected)
        seller_product = seller_product_db[str(product_selected["seller_id"])]
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

    # Receive AJAX Request to Update Cart Qty
    if request.method == "POST":
        sent_data = json.loads(request.data)
        updated_cart_qty = sent_data["cart_qty"]
        updated_product_qty = sent_data["product_qty"]
        seller_name = sent_data["seller_name"]
        product_id = sent_data["product_id"]

        # Update Cart Icon Qty into db
        saved_cart_qty = 0
        shopping_cart_db = shelve.open("user_shopping_cart.db", flag="c")
        try:
            users_shopping_cart = shopping_cart_db[user]
            saved_cart_qty = users_shopping_cart["cart_qty"]
        except:
            print("Error in loading cart qty db")

        saved_cart_qty = updated_cart_qty
        users_shopping_cart["cart_qty"] = saved_cart_qty
        shopping_cart_db[user] = users_shopping_cart
        shopping_cart_db.close()

        # Searching for Seller id
        approved_sellers = {}
        approve_seller_db = shelve.open('approved_sellers.db')
        approved_sellers = approve_seller_db['Approved_sellers']
        for id in approved_sellers:
            if seller_name == approved_sellers[id].get_name():
                seller_id = approved_sellers[id].get_id()

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

    return render_template("customer/shopping_cart.html", display_shopping_cart=display_shopping_cart, user=user,
                           saved_cart_qty=cart_qty(user))


@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        if create_user_form.email.data in users_dict:
            return 'An account has already been created with this email. Please Login'

        user = User.User(create_user_form.email.data, create_user_form.password.data)
        users_dict[user.get_email()] = user
        db['Users'] = users_dict

        db.close()

        return redirect(url_for('login'))
    return render_template('createUser.html', form=create_user_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # error = None
    # if request.method == 'POST':
    #     user_file = open('user.db', 'r')
    #     contents = user_file.read()
    #     if request.form['Email'] or request.form['Password'] in contents:
    #         return redirect(url_for('home'))
    #     else:
    #         error = 'Invalid Credentials. Please try again.'
    # return render_template('login.html', error=error)
    login_form = CreateUserForm(request.form)
    if request.method == 'POST' and login_form.validate():
        users_dict = {}
        user = User.User(login_form.email.data, login_form.password.data)
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
                        return redirect(url_for('home'))
                    else:
                        return render_template('login_failed.html')
                else:
                    return render_template('login_failed.html')
            else:
                return render_template('createUser.html')
        except:
            print("Error in opening user.db")
    return render_template('login.html', form=login_form)


def get_key(val,users_dict):
    for key, value in users_dict.items():
        if val == value.get_password():
            return key


@app.route('/retrieveUsers')
def retrieve_users():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('retrieveUsers.html', count=len(users_list), users_list=users_list)


@app.route('/updateUser/<string:email>/', methods=['GET', 'POST'])
def update_user(email):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(email)
        user.set_email(update_user_form.email.data)
        user.set_password(update_user_form.password.data)

        db['Users'] = users_dict
        db.close()

        return redirect(url_for('retrieve_users'))
    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(email)
        update_user_form.email.data = user.get_email()
        update_user_form.password.data = user.get_password()

        return render_template('updateUser.html', form=update_user_form)


@app.route('/deleteUser/<string:email>', methods=['POST'])
def delete_user(email):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(email)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('retrieve_users'))


@app.route('/stafflogin', methods=['GET', 'POST'])
def staff_login():
    stafflogin_form = StaffLoginForm(request.form)
    if request.method == 'POST' and stafflogin_form.validate():
        return redirect(url_for('retrieveApplicationForms'))
    return render_template('staff/staff_login.html', form=stafflogin_form)


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
        seller_product_db = shelve.open('seller-product.db', 'c')

        try:
            seller_products = seller_product_db[str(seller_id)]

        except:
            print("Error in retrieving products from seller-product.db.")
        create_product = SellerProduct.SellerProduct(create_product_form.product_name.data,
                                                     create_product_form.product_price.data,
                                                     create_product_form.product_stock.data,
                                                     create_product_form.image.data,
                                                     create_product_form.description.data)

        # create dict with product id as key and create_product as value; dict name is seller_products
        seller_products[create_product.get_product_id()] = create_product
        # store seller_products(dict) in seller_product_db, with seller_id as key and seller_products as value
        seller_product_db[str(seller_id)] = seller_products
        seller_product_db.close()

        return redirect(url_for('retrieve_product', seller_id=seller_id))
    return render_template('seller/createProduct.html', form=create_product_form)


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
    seller_products = seller_product_db[str(seller_id)]
    seller_product_db.close()

    product_list = []
    for product_id in seller_products:
        products = seller_products.get(product_id)
        product_list.append(products)

    return render_template('seller/retrieveProducts.html', count=len(product_list), product_list=product_list)


@app.route('/seller/<int:seller_id>/updateProduct/<int:product_id>/', methods=['GET', 'POST'])
def update_product(seller_id, product_id):
    update_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and update_product_form.validate():

        seller_product_db = shelve.open('seller-product.db', 'w')
        seller_products = seller_product_db[str(seller_id)]
        sellerProduct = seller_products.get(product_id)
        sellerProduct.set_product_name(update_product_form.product_name.data)
        sellerProduct.set_product_price(update_product_form.product_price.data)
        sellerProduct.set_product_stock(update_product_form.product_stock.data)
        sellerProduct.set_description(update_product_form.description.data)
        seller_product_db[str(seller_id)] = seller_products
        seller_product_db.close()

        return redirect(url_for('retrieve_product', seller_id=seller_id, product_id=product_id))

    else:
        seller_product_db = shelve.open('seller-product.db', 'r')
        seller_products = seller_product_db[str(seller_id)]
        seller_product_db.close()
        sellerProduct = seller_products.get(product_id)
        update_product_form.product_name.data = sellerProduct.get_product_name()
        update_product_form.product_price.data = sellerProduct.get_product_price()
        update_product_form.product_stock.data = sellerProduct.get_product_stock()
        update_product_form.description.data = sellerProduct.get_description()

        return render_template('/seller/updateProduct.html', form=update_product_form, seller_id=seller_id, product_id=product_id)


@app.route('/seller/<int:seller_id>/deleteProduct/<int:product_id>/', methods=['POST'])
def delete_product(seller_id, product_id):
    seller_product_db = shelve.open('seller-product.db', 'w')
    seller_products = seller_product_db[str(seller_id)]
    seller_products.pop(product_id)
    seller_product_db[str(seller_id)] = seller_products
    seller_product_db.close()
    return redirect(url_for('retrieve_product', seller_id=seller_id))


@app.route('/respond')
def respond():
    return render_template('sellers_application/respondPage.html')


@app.route("/register", methods=['GET', 'POST'])
def register(): #create
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

        appForm = AppFormFormat(last_id,registration_form.business_name.data, registration_form.seller_email.data,
                                registration_form.business_desc.data)
        application_form[appForm.get_application_id()] = appForm
        today = date.today()
        appForm.set_date(today)
        # saving image
        support_docs = request.files.get('support_document')
        if support_docs:
            filename = secure_filename(support_docs.filename)
            img_id = secrets.token_hex(16)
            # Create
            os.makedirs(os.path.join(app.config["UPLOAD_DIRECTORY"], img_id))
            support_docs.save(os.path.join(app.config["UPLOAD_DIRECTORY"], img_id, filename))
            image_dir = os.path.join(app.config["UPLOAD_DIRECTORY"], img_id)
            create_image_set(image_dir, filename)
            message = f"{img_id}/{filename.split('.')[0]}.webp"
            appForm.set_doc(message)
            print(message)

        db['Application'] = application_form
        # testing
        application_form = db['Application']
        appForm = application_form[appForm.get_application_id()]
        print(appForm.get_name(), appForm.get_email(), "was stored in user.db successfully with user_id ==",
              appForm.get_application_id())
        print("last id--",last_id)
        if application_form.keys():
            last_id = max(application_form.keys())
        db['Id'] = last_id
        db.close()
        return redirect(url_for('respond'))
    return render_template('sellers_application/registration.html', form=registration_form)


@app.route('/display_image/<filename>/<filepath>')
def display_image(filename,filepath):
    image_url = url_for('static',filename='images/uploads/'+ filename+ '/'+ filepath)
    return render_template('display_image.html', image_url = image_url)

@app.route('/staff/retrieveApplicationForms') #read
def retrieveApplicationForms():
    app_dict = {}
    db = shelve.open('application.db', 'r')
    app_dict = db['Application']
    db.close()

    app_list = []
    for key in app_dict:
        forms = app_dict.get(key)
        app_list.append(forms)
    return render_template('staff/retrieveAppForms.html', count=len(app_list), app_list=app_list)



@app.route('/staff/approveForm/<int:seller_id>', methods = ['POST']) # for approving forms
def approve_form(seller_id): # create
    # take the approved application
    approved = extracting('application.db', 'Application', seller_id)
    print("This user is approved", approved.get_application_id())
    # store in the approved_sellers
    approved_sellers = {}
    approved_db = shelve.open('approved_sellers.db', 'c')
    try:
        approved_sellers = approved_db['Approved_sellers']
    except:
        print("Error in retrieving sellers from application.db")

    passwords = []
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(10))
        if password not in passwords:
            break
    send_mail(approved.get_email(),True,approved.get_name(),password)
    approved.set_password(password)
    # storing approved seller
    approved_sellers[approved.get_application_id()] = approved
    approved_db['Approved_sellers'] = approved_sellers
    for key,seller in approved_db['Approved_sellers'].items():
        passwords.append(seller.get_password())
    approved_db.close()
    print(passwords)
    return redirect(url_for('retrieveApplicationForms'))

@app.route('/staff/rejectForm/<int:seller_id>', methods =['POST']) #for rejecting forms
def reject_form(seller_id): # delete
    rejected = extracting('application.db', 'Application', seller_id)
    if rejected.get_doc():
        delete_folder(rejected)
    send_mail(rejected.get_email(), False, rejected.get_name(), '')
    return redirect(url_for('retrieveApplicationForms'))


@app.route('/staff/retrieveUpdateForms')
def retrieveUpdateForms(): # approving updates
    return render_template('staff/retrieveUpdateForms.html')


@app.route('/staff/retrieveSellers')
def retrieveSellers(): # read
    approved_sellers = {}
    approved_db = shelve.open('approved_sellers.db', 'r')
    approved_sellers = approved_db['Approved_sellers']
    approved_db.close()

    sellers_list = []
    for key in approved_sellers:
        forms = approved_sellers.get(key)
        sellers_list.append(forms)
    return render_template('staff/retrieveSellers.html', count=len(sellers_list), sellers=sellers_list)

@app.route('/staff/deleteForm/<int:id>', methods = ['POST'])
def delete_form(id): # delete
    deleted_item = extracting('approved_sellers.db', 'Approved_sellers', id)
    delete_folder(deleted_item)
    return redirect(url_for('retrieveSellers'))


# @app.route('/staff/dashboard')
# def dashboard():
#     return render_template('staff/dashboard')


if __name__ == "__main__":
    app.run(debug=True)
