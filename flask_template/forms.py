from wtforms import Form, StringField, SelectField, DateField, validators

class Test(Form):
    string = StringField('First Name', [validators.Length(min=0, max=25), validators.DataRequired()])
