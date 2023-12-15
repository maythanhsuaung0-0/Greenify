from wtforms import Form, StringField, validators
from wtforms.validators import DataRequired


class CreateUserForm(Form):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = StringField(label='Password',
                           validators=[DataRequired(),
                                       validators.Length(min=8, max=30),
                                       validators.Regexp(regex="[a-zA-Z0-9]")])
