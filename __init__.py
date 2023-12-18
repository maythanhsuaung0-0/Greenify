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

@app.route("/Product")
def product():
    return render_template("test_product.html")


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
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict

        # Test codes
        users_dict = db['Users']
        user = users_dict[user.get_user_id()]
        print(user.get_first_name(), user.get_last_name(), "was stored in user.db successfully with user_id ==", user.get_user_id())

        db.close()

        return redirect(url_for('home'))
    return render_template('createUser.html', form=create_user_form)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        seller_product = {}
        db = shelve.open('seller-product.db', 'c')

        try:
            seller_product = db['SellerProducts']

        except:
            print("Error in retrieving Seller Products from seller-product.db.")
        sellerproduct = SellerProduct.SellerProduct(create_product_form.product_name.data, create_product_form.product_price.data, create_product_form.product_stock.data, create_product_form.image.data, create_product_form.description.data)
        seller_product[sellerproduct.get_product_id()] = sellerproduct
        db['SellerProducts'] = seller_product

        db.close()
    return render_template('createProduct.html', form=create_product_form)

@app.route('/respond')
def respond():
    return render_template('respondPage.html')

@app.route("/register",methods = ['GET','POST'])
def register():
    registration_form = ApplicationForm(request.form)
    if request.method == 'POST' and registration_form.validate():
        application_form = {}
        db = shelve.open('application.db','c')
        try:
            application_form = db['Application']
        except:
            print("Error in retrieving application from application.db")
        # create an instance appForm of class
        appForm = AppFormFormat(registration_form.business_name.data, registration_form.seller_email.data, registration_form.business_desc.data, registration_form.support_document.data)
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
    return render_template('registration.html', form = registration_form)


if __name__ == "__main__":
    app.run(debug=True)