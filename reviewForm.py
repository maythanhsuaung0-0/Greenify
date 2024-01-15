from wtforms import Form, TextAreaField, validators


class CreateReviewsForm(Form):
    review = TextAreaField('My Review:', [validators.DataRequired()], render_kw={'rows': '4', 'style': 'width: 550px;', 'placeholder': 'Enter your review here'})

