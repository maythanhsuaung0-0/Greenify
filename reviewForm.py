from wtforms import Form, TextAreaField, validators

class CreateReviewsForm(Form):
    review = TextAreaField('My review', [validators.DataRequired()])