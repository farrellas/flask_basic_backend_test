from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

#global variables
states=["Select State","Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware",
"District Of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa""Kansas","Kentucky",
"Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
"Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota",
"Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas",
"Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

class NewCompanyForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_password = StringField('Company Password', validators=[DataRequired()])
    street_address_1 = StringField('Address Line 1', validators=[DataRequired()])
    street_address_2 = StringField('Address Line 2')
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()], choices=states)
    zip_code =StringField('Zip Code', validators=[DataRequired()])
    logo_url = StringField('Logo URL')
    submit = SubmitField()

class UpdateCompanyForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    company_password = StringField('Company Password', validators=[DataRequired()])
    street_address_1 = StringField('Address Line 1', validators=[DataRequired()])
    street_address_2 = StringField('Address Line 2')
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()], choices=states)
    zip_code =StringField('Zip Code', validators=[DataRequired()])
    logo_url = StringField('Logo URL')
    submit = SubmitField()
