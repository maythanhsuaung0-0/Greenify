from wtforms import Form, EmailField, validators, PasswordField, StringField, TelField


class CreateUserForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.length(min=8, max=30)])
    name = StringField('Name', [validators.DataRequired()])
    contact_number = TelField('Phone Number', [validators.DataRequired(), validators.length(min=8)])
    postal_code = StringField('Postal Code', [validators.DataRequired(), validators.length(min=6)])
    address = StringField('Address', [validators.DataRequired()])


class StaffLoginForm(Form):
    admin_email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    admin_password = PasswordField('Password', [validators.DataRequired(), validators.length(min=8, max=30)])


class LoginForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.length(min=8, max=30)])