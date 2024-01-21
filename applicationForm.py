from wtforms import Form, StringField, EmailField, TextAreaField, FileField, validators


class ApplicationForm(Form):
    name = StringField('Fullname',[validators.DataRequired()])
    business_name = StringField('Business Name', [validators.DataRequired(), validators.length(max=20)])
    business_desc = TextAreaField("Business Description", [validators.DataRequired()])
    seller_email = EmailField("Email Address", [validators.DataRequired(), validators.Email()])
    support_document = FileField('Upload Supporting Document (* pdf file only *)', [validators.optional()],render_kw={'accept': '.pdf'})
    profile_pic = FileField('Upload Profile Picture (* image files only *)', [validators.optional()], render_kw={'accept': '.jpg, .jpeg, .png'})
