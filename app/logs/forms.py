from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class CreateCustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', widget=TextArea(), validators=[DataRequired()])
    email = StringField('E-mail')
    submit = SubmitField()

class UpdateCustomerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', widget=TextArea(), validators=[DataRequired()])
    email = StringField('E-mail')
    submit = SubmitField()

class CreateLogForm(FlaskForm):
    work_performed = StringField('Work Performed', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField()

class UpdateLogForm(FlaskForm):
    work_performed = StringField('Work Performed', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField()