from wtforms import Form, StringField, FileField, TextAreaField, IntegerField, FloatField, validators
from wtforms.validators import DataRequired
from wtforms.fields import EmailField


class CreateUserForm(Form):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = StringField(label='Password',
                           validators=[DataRequired(),
                                       validators.Length(min=8, max=30),
                                       validators.Regexp(regex="[a-zA-Z0-9]")])


class CreateProductForm(Form):
    product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_price = FloatField('Price', validators.DataRequired())
    product_stock = IntegerField('Stock', validators.DataRequired())
    image = FileField('Image File', [validators.regexp('^[^/\\]\.jpg$'), validators.DataRequired()])
    description = TextAreaField('Product Description')
