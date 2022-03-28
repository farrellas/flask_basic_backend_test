from tkinter import E
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

#global variables
system_types = ["Forced Air Split", "Hydronic", "Mini Split", "VRF", "Steam", "Packaged System"]
equipment_types = {"Heating": [], "Cooling": [], "Air Handling": []}
fuel_types = ["Natural Gas", "Propane", "Fuel Oil", "Dual Fuel", "Electric"]
refrigerant_types = ["410A", "22", "Other"]

class NewSystemForm(FlaskForm):
    name = StringField('System Name', validators=[DataRequired()])
    area_served = StringField('Area Served', validators=[DataRequired()])
    system_type = SelectField('System Type', validators=[DataRequired()], choices=system_types)
    heating = BooleanField('Heating')
    cooling = BooleanField('Cooling')
    notes = StringField('Notes: ', widget=TextArea())
    submit = SubmitField()

class UpdateSystemForm(FlaskForm):
    name = StringField('System Name', validators=[DataRequired()])
    area_served = StringField('Area Served', validators=[DataRequired()])
    system_type = SelectField('System Type', validators=[DataRequired()], choices=system_types)
    heating = BooleanField('Heating')
    cooling = BooleanField('Cooling')
    notes = StringField('Notes: ', widget=TextArea())
    submit = SubmitField()

class NewHeatingEquipmentForm(FlaskForm):
    brand = StringField('Brand Name', validators=[DataRequired()])
    model_no = StringField('Model Number', validators=[DataRequired()])
    serial_no = StringField('Serial Number', validators=[DataRequired()])
    year = StringField('Year Installed', validators=[DataRequired()])
    equipment_type = SelectField('Equipment Type', validators=[DataRequired()], choices=equipment_types["Heating"])
    fuel_type = SelectField('Fuel Type', validators=[DataRequired()], choices=fuel_types)
    notes = StringField('Notes:', widget=TextArea())
    submit = SubmitField()

class UpdateHeatingEquipmentForm(FlaskForm):
    brand = StringField('Brand Name', validators=[DataRequired()])
    model_no = StringField('Model Number', validators=[DataRequired()])
    serial_no = StringField('Serial Number', validators=[DataRequired()])
    year = StringField('Year Installed', validators=[DataRequired()])
    equipment_type = SelectField('Equipment Type', validators=[DataRequired()], choices=equipment_types["Heating"])
    fuel_type = SelectField('Fuel Type', validators=[DataRequired()], choices=fuel_types)
    notes = StringField('Notes:', widget=TextArea())
    submit = SubmitField()

class NewCoolingEquipmentForm(FlaskForm):
    brand = StringField('Brand Name', validators=[DataRequired()])
    model_no = StringField('Model Number', validators=[DataRequired()])
    serial_no = StringField('Serial Number', validators=[DataRequired()])
    year = StringField('Year Installed', validators=[DataRequired()])
    equipment_type = SelectField('Equipment Type', validators=[DataRequired()], choices=equipment_types["Cooling"])
    refrigerant_type = SelectField('Fuel Type', validators=[DataRequired()], choices=refrigerant_types)
    notes = StringField('Notes:', widget=TextArea())
    submit = SubmitField()

class UpdateCoolingEquipmentForm(FlaskForm):
    brand = StringField('Brand Name', validators=[DataRequired()])
    model_no = StringField('Model Number', validators=[DataRequired()])
    serial_no = StringField('Serial Number', validators=[DataRequired()])
    year = StringField('Year Installed', validators=[DataRequired()])
    equipment_type = SelectField('Equipment Type', validators=[DataRequired()], choices=equipment_types["Cooling"])
    refrigerant_type = SelectField('Fuel Type', validators=[DataRequired()], choices=refrigerant_types)
    notes = StringField('Notes:', widget=TextArea())
    submit = SubmitField()

class NewAirHandlingEquipmentForm(FlaskForm):
    brand = StringField('Brand Name', validators=[DataRequired()])
    model_no = StringField('Model Number', validators=[DataRequired()])
    serial_no = StringField('Serial Number', validators=[DataRequired()])
    year = StringField('Year Installed', validators=[DataRequired()])
    equipment_type = SelectField('Equipment Type', validators=[DataRequired()], choices=equipment_types["Air Handling"])
    notes = StringField('Notes:', widget=TextArea())
    submit = SubmitField()

class UpdateAirHandlingEquipmentForm(FlaskForm):
    brand = StringField('Brand Name', validators=[DataRequired()])
    model_no = StringField('Model Number', validators=[DataRequired()])
    serial_no = StringField('Serial Number', validators=[DataRequired()])
    year = StringField('Year Installed', validators=[DataRequired()])
    equipment_type = SelectField('Equipment Type', validators=[DataRequired()], choices=equipment_types["Air Handling"])
    notes = StringField('Notes:', widget=TextArea())
    submit = SubmitField()