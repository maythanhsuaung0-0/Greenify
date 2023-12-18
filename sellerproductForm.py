from wtforms import Form, StringField, FileField, TextAreaField, IntegerField, FloatField, validators


class CreateProductForm(Form):
    product_name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    product_price = FloatField('Price', validators.DataRequired())
    product_stock = IntegerField('Stock', validators.DataRequired())
    image = FileField('Product Image', validators.DataRequired())
    description = TextAreaField('Product Description')
