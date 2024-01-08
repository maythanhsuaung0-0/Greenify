from wtforms import Form, StringField, EmailField, validators, PasswordField


class CreateUserForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.length(min=8, max=30), validators.regexp(regex="[a-zA-Z0-9]")])


class StaffLoginForm(Form):
    admin_email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    admin_password = StringField('Password', [validators.DataRequired(), validators.length(min=8, max=30)])


