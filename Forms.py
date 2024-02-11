from wtforms import Form, EmailField, validators, PasswordField, StringField, IntegerField


def no_special_characters(Form, field):
    special_characters = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"
    if any(char in special_characters for char in field.data):
        raise validators.ValidationError("Special characters are not allowed.")


class CreateUserForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('', [validators.DataRequired(), validators.length(min=8, max=30)])
    confirm_password = PasswordField('', [validators.DataRequired(), validators.length(min=8, max=30)])
    name = StringField('Name', validators=[validators.DataRequired(), no_special_characters])
    contact_number = IntegerField('Phone Number', [validators.DataRequired(), validators.NumberRange(min=00000000, max=99999999)])
    postal_code = IntegerField('Postal Code', [validators.DataRequired(), validators.NumberRange(min=000000, max=999999)])
    address = StringField('Address', [validators.DataRequired()])


class StaffLoginForm(Form):
    admin_email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    admin_password = PasswordField('', [validators.DataRequired(), validators.length(min=8, max=30)])


class LoginForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('', [validators.DataRequired(), validators.length(min=8, max=30)])