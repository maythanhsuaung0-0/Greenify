from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserForm, CreateProductForm
import shelve, User, SellerProduct

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
        sellerProduct = {}
        db = shelve.open('seller-product.db', 'c')

        try:
            sellerProduct = db['SellerProducts']

        except:
            print("Error in retrieving Seller Products from seller-product.db.")
        sellerproduct = SellerProduct.SellerProduct(create_product_form.product_name.data, create_product_form.product_price.data, create_product_form.product_stock.data, create_product_form.description.data)
        sellerProduct[sellerproduct.get_product_id()] = sellerproduct
        db['SellerProducts'] = sellerProduct

        db.close()

        # return redirect()
    return render_template('createProduct.html', form=create_product_form)


if __name__ == "__main__":
    app.run()