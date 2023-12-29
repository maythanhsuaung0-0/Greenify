import secrets
import shutil
from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm, LoginForm, StaffLoginForm
import shelve, User, SellerProduct
from sellerproductForm import CreateProductForm
from applicationForm import ApplicationForm
from application import ApplicationFormFormat as AppFormFormat
import os
from set_image import create_image_set
from werkzeug.utils import secure_filename
from urllib.parse import quote

app = Flask(__name__, static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_DIRECTORY'] = "C:/Users/mayth/PycharmProjects/Greenify/static/images/uploads"

def deleting(my_db,db_key,id):  #function for deleting and rejecting
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


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/Product/seller/<int:id>")
def product(id):
    seller_product = {}
    db = shelve.open('seller-product.db', 'r')
    seller_product = db['SellerProducts']
    db.close()

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
    # error = None
    # if request.method == 'POST':
    #     user_file = open('user.db.bak', 'r')
    #     contents = user_file.read()
    #     if request.form['Email'] or request.form['Password'] in contents:
    #         return redirect(url_for('home'))
    #     else:
    #         error = 'Invalid Credentials. Please try again.'
    # return render_template('login.html', error=error)
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'r')
        user_values = User.User(login_form.Email.data, login_form.Password.data)
        try:
            if 'Users' in db:
                users_dict = db["Users"]
                if users_dict == user_values:
                    return redirect(url_for('home'))
            else:
                return render_template('createUser.html')
        except:
            print("Error in opening user.db")
    return render_template('login.html', form=login_form)


@app.route('/stafflogin', methods=['GET', 'POST'])
def staff_login():
    stafflogin_form = StaffLoginForm(request.form)
    if request.method == 'POST' and stafflogin_form.validate():
            return redirect(url_for('retrieveApplicationForms'))
    return render_template('staff/staff_login.html', form=stafflogin_form)


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

        sellers_db = shelve.open('SellerDetails.db', 'c')
        sellers_dict = {}
        try:
            sellers_dict = sellers_db['SellerDetails']
        except:
            print("Error in storing Seller Products and Seller ID together in sellers_db.")

        sellers_dict[seller_id] = sellerproduct.get_product_id()
        sellers_db['SellerDetails'] = sellers_dict
        sellers_db.close()

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

    # sellers_dict = {}
    # sellers_db = shelve.open('SellerDetails.db', 'r')
    # sellers_dict = sellers_db['SellerDetails']
    # sellers_db.close()

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

        # saving image
        support_docs = request.files.get('support_document')
        print(support_docs)
        appForm = AppFormFormat(registration_form.business_name.data, registration_form.seller_email.data,
                                registration_form.business_desc.data)
        application_form[appForm.get_application_id()] = appForm

        if support_docs:
            filename = secure_filename(support_docs.filename)
            img_id = secrets.token_hex(16)
            # Create
            os.makedirs(os.path.join(app.config["UPLOAD_DIRECTORY"],img_id))
            support_docs.save(os.path.join(app.config["UPLOAD_DIRECTORY"],img_id,filename))
            image_dir = os.path.join(app.config["UPLOAD_DIRECTORY"],img_id)
            create_image_set(image_dir,filename)
            message = f"{img_id}/{filename.split('.')[0]}.webp"
            appForm.set_doc(message)
            print(message)

        db['Application'] = application_form
        # testing
        application_form = db['Application']
        appForm = application_form[appForm.get_application_id()]
        print(appForm.get_name(), appForm.get_email(), "was stored in user.db successfully with user_id ==",
              appForm.get_application_id())

        db.close()
        return redirect(url_for('respond'))
    return render_template('sellers_application/registration.html', form=registration_form)


@app.route('/display_image/<filename>/<filepath>')
# http://127.0.0.1:5000/static/images/uploads/52a7f27d655036e2a5bb150df85f9ba2/hotel_logo.webp
def display_image(filename,filepath):
    print(filename,filepath)
    image_url = url_for('static',filename='images/uploads/'+ filename+ '/'+ filepath)
    return render_template('display_image.html', image_url = image_url)

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



@app.route('/staff/approveForm/<int:id>', methods = ['POST']) # for approving forms
def approve_form(id):
    # take the approved application
    approved = deleting('application.db', 'Application', id)
    print("This user is approved", approved.get_application_id())
    # store in the approved_sellers
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

@app.route('/staff/rejectForm/<int:id>', methods =['POST']) #for rejecting forms
def reject_form(id):
    rejected = deleting('application.db', 'Application', id)
    delete_folder(rejected)
    return redirect(url_for('retrieveApplicationForms'))


@app.route('/staff/retrieveUpdateForms')
def retrieveUpdateForms():
    return render_template('staff/retrieveUpdateForms.html')


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

@app.route('/staff/deleteForm/<int:id>', methods = ['POST'])
def delete_form(id):
    deleted_item = deleting('approved_sellers.db','Approved_sellers',id)
    delete_folder(deleted_item)
    return redirect(url_for('retrieveSellers'))

# @app.route('/staff/dashboard')
# def dashboard():
#     return render_template('staff/dashboard')


if __name__ == "__main__":
    app.run(debug=True)
