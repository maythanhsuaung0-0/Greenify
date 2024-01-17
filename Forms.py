from wtforms import Form, EmailField, validators, PasswordField


class CreateUserForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.length(min=8, max=30)])


class StaffLoginForm(Form):
    admin_email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    admin_password = PasswordField('Password', [validators.DataRequired(), validators.length(min=8, max=30)])


class SellerLoginForm(Form):
    seller_email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    seller_password = PasswordField('Password', [validators.DataRequired(), validators.length(min=8, max=30)])