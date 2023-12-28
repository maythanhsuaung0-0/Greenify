from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm
import shelve, User, SellerProduct
from sellerproductForm import CreateProductForm
from applicationForm import ApplicationForm
from application import ApplicationFormFormat as AppFormFormat

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def home():
    return render_template("homepage.html")

<<<<<<< HEAD
@app.route("/Product/seller/<int:id>")
def product(id):
    seller_product = {}
    db = shelve.open('seller-product.db', 'r')
    seller_product = db['SellerProducts']
    db.close()
=======

@app.route("/Product")
def product():
    return render_template("test_product.html")
>>>>>>> c6a985243a01cc90a98ad2185507dad01a153081

    product = seller_product[id]

    return render_template("test_product.html", product=product)

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

        user = User.User(create_user_form.email.data, create_user_form.password.data)
        users_dict[user.get_email()] = user
        db['Users'] = users_dict

        db.close()

        return redirect(url_for('login'))
    return render_template('createUser.html', form=create_user_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_file = open('user.db.bak', 'r')
        contents = user_file.read()
        if request.form['Email'] or request.form['Password'] in contents:
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


def staff_login():
    if request.form['Email'] != '@dmin@gmail.com' or request.form['Password'] != 'admin':
        error = 'Please try again.'
    else:
        return redirect(url_for('retrieveApplicationForms'))
    return render_template('login.html', error=error)


# @app.route('/seller')
# def retrieve_seller_id():
#     approved_sellers = {}
#     approved_db = shelve.open('approved_sellers.db', 'r')
#     approved_sellers = approved_db['Approved_sellers']
#     seller_id = []
#     for key in approved_sellers.keys():
#         seller_id.append(key)
#
#     approved_db.close()
#     return seller_id


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
        seller_product = {}
        db = shelve.open('seller-product.db', 'c')

        try:
            seller_product = db['SellerProducts']

        except:
            print("Error in retrieving Seller Products from seller-product.db.")
        sellerproduct = SellerProduct.SellerProduct(create_product_form.product_name.data,
                                                    create_product_form.product_price.data,
                                                    create_product_form.product_stock.data,
                                                    create_product_form.image.data,
                                                    create_product_form.description.data)
        seller_product[sellerproduct.get_product_id()] = sellerproduct
        db['SellerProducts'] = seller_product

        db.close()
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
    seller_product = {}
    db = shelve.open('seller-product.db', 'r')
    seller_product = db['SellerProducts']
    db.close()

    product_list = []
    for key in seller_product:
        products = seller_product.get(key)
        product_list.append(products)

    return render_template('seller/retrieveProducts.html', count=len(product_list), product_list=product_list)


# @app.route('/seller/updateProduct/<int:id>/', methods=['GET', 'POST'])
# def update_product(id):
#     update_product_form = CreateProductForm(request.form)
#     if request.method == 'POST' and update_product_form.validate():
#         db = shelve.open('seller-product.db', 'w')
#         seller_product = db['SellerProducts']
#         sellerProduct = seller_product.get(id)
#         sellerProduct.set_product_name(update_product_form.product_name.data)
#         sellerProduct.set_product_price(update_product_form.product_price.data)
#         sellerProduct.set_product_stock(update_product_form.product_stock.data)
#         sellerProduct.set_description(update_product_form.description.data)
#         db['SellerProducts'] = seller_product
#         db.close()
#
#         return redirect(url_for('retrieve_product'))
#     else:
#         seller_product = {}
#         db = shelve.open('seller-product.db', 'r')
#         seller_product = db['SellerProducts']
#         db.close()
#         sellerProduct = seller_product.get(id)
#         update_product_form.product_name.data = sellerProduct.get_product_name()
#         update_product_form.product_price.data = sellerProduct.get_product_price()
#         update_product_form.product_stock.data = sellerProduct.get_product_stock()
#         update_product_form.description.data = sellerProduct.get_description()
#
#         return render_template('/seller/updateProduct.html', form=update_product_form)


@app.route('/respond')
def respond():
    return render_template('sellers_application/respondPage.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    registration_form = ApplicationForm(request.form)
    if request.method == 'POST' and registration_form.validate():
        application_form = {}
        db = shelve.open('application.db', 'c')
        try:
            application_form = db['Application']
        except:
            print("Error in retrieving application from application.db")
        # create an instance appForm of class
        # ----haven't done storing files-----
        appForm = AppFormFormat(registration_form.business_name.data, registration_form.seller_email.data,
                                registration_form.business_desc.data, registration_form.support_document.data)
        print("appForm", appForm)
        application_form[appForm.get_application_id()] = appForm
        db['Application'] = application_form
        # testing
        application_form = db['Application']
        appForm = application_form[appForm.get_application_id()]
        print(appForm.get_name(), appForm.get_email(), "was stored in user.db successfully with user_id ==",
              appForm.get_application_id())

        db.close()
        return redirect(url_for('respond'))
    return render_template('sellers_application/registration.html', form=registration_form)


@app.route('/staff/retrieveApplicationForms')
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


@app.route('/staff/retrieveUpdateForms')
def retrieveUpdateForms():
    return render_template('staff/retrieveUpdateForms.html')


# for approving forms
@app.route('/staff/approveForm/<int:id>', methods=['POST'])
def approve_form(id):
    app_dict = {}
    db = shelve.open('application.db', 'w')
    app_dict = db['Application']
    approved = app_dict.pop(id)
    db['Application'] = app_dict
    db.close()
    print("This user is approved", approved.get_application_id())
    # storing approved sellers
    approved_sellers = {}
    approved_db = shelve.open('approved_sellers.db', 'c')
    try:
        approved_sellers = approved_db['Approved_sellers']
    except:
        print("Error in retrieving sellers from application.db")
    approved_sellers[approved.get_application_id()] = approved
    approved_db['Approved_sellers'] = approved_sellers
    print("approved seller is ---", approved_sellers)
    approved_db.close()
    return redirect(url_for('retrieveApplicationForms'))


@app.route('/staff/retrieveSellers')
def retrieveSellers():
    approved_sellers = {}
    approved_db = shelve.open('approved_sellers.db', 'r')
    approved_sellers = approved_db['Approved_sellers']
    approved_db.close()

    sellers_list = []
    for key in approved_sellers:
        forms = approved_sellers.get(key)
        sellers_list.append(forms)
    return render_template('staff/retrieveSellers.html', count=len(sellers_list), sellers=sellers_list)


# @app.route('/staff/dashboard')
# def dashboard():
#     return render_template('staff/dashboard')


if __name__ == "__main__":
    app.run(debug=True)
