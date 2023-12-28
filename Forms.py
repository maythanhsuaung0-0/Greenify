from wtforms import Form, StringField, EmailField, validators


class CreateUserForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = StringField('Password', [validators.DataRequired(), validators.length(min=8, max=30), validators.regexp(regex="[a-zA-Z0-9]")])



