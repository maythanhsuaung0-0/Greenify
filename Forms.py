from wtforms import Form, EmailField, validators, PasswordField, StringField, IntegerField

class CreateUserForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('', [validators.DataRequired(), validators.length(min=8, max=30)])
    confirm_password = PasswordField('', [validators.DataRequired(), validators.length(min=8, max=30)])
    name = StringField('Name', [validators.DataRequired()])
    contact_number = IntegerField('Phone Number', [validators.DataRequired(), validators.NumberRange(min=00000000, max=99999999)])
    postal_code = IntegerField('Postal Code', [validators.DataRequired(), validators.NumberRange(min=000000, max=999999)])
    address = StringField('Address', [validators.DataRequired()])


class StaffLoginForm(Form):
    admin_email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    admin_password = PasswordField('Password', [validators.DataRequired(), validators.length(min=8, max=30)])


class LoginForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('', [validators.DataRequired(), validators.length(min=8, max=30)])