from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    customer = db.relationship('Customer', backref='user', lazy=True)

    def __init__(self, username, email, password, first_name, last_name):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False, unique=True)
    street_address_1 = db.Column(db.String(100), nullable=False)
    street_address_2 = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    logo_url = db.Column(db.String(300))
    company_password = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='company', lazy=True)
    customer = db.relationship('Customer', backref='company', lazy=True)

    def __init__(self, company_name, street_address_1, street_address_2, city, state, zip_code, company_password=company_name):
        self.company_name = company_name
        self.street_address_1 = street_address_1
        self.street_address_2 = street_address_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.company_password = company_password

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    street_address_1 = db.Column(db.String(100), nullable=False)
    street_address_2 = db.Column(db.String(100))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    system = db.relationship('System', backref='owner', lazy=True)

    def __init__(self, name, street_address_1, street_address_2, city, state, zip_code, email, user_id):
        self.name = name
        self.street_address_1 = street_address_1
        self.street_address_2 = street_address_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.email = email
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "street_address_1": self.street_address_1,
            "street_address_2": self.street_address_2,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "email": self.email
        }

class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area_served = db.Column(db.String(100), nullable=False)
    system_type = db.Column(db.String(100), nullable=False)
    heating = db.Column(db.Boolean, default=True, nullable=False)
    cooling = db.Column(db.Boolean, default=True, nullable=False)
    notes = db.Column(db.String(1000), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    heating_equipment = db.relationship('HeatingEquipment', backref='system', lazy=True)
    air_handling_equipment = db.relationship('AirHandlingEquipment', backref='system', lazy=True)
    cooling_equipment = db.relationship('CoolingEquipment', backref='system', lazy=True)
    maintenance_log = db.relationship('MaintenanceLog', backref='system', lazy=True)
    repair_log = db.relationship('RepairLog', backref='system', lazy=True)

    def __init__(self, name, area_served, system_type, heating, cooling, notes, customer_id):
        self.name = name
        self.area_served = area_served
        self.system_type = system_type
        self.heating = heating
        self.cooling = cooling
        self.notes = notes
        self.customer_id = customer_id
    
class HeatingEquipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model_no = db.Column(db.String(100), nullable=False)
    serial_no = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    equipment_type = db.Column(db.String(100), nullable=False)
    fuel_type = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(1000), nullable=True)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)

    def __init__(self, brand, model_no, serial_no, year, equipment_type, fuel_type, notes, system_id):
        self.brand = brand
        self.model_no = model_no
        self.serial_no = serial_no
        self.year = year
        self.equipment_type = equipment_type
        self.fuel_type = fuel_type
        self.notes = notes
        self.system_id = system_id

class AirHandlingEquipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model_no = db.Column(db.String(100), nullable=False)
    serial_no = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    equipment_type = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.String(1000), nullable=True)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)

    def __init__(self, brand, model_no, serial_no, year, equipment_type, notes, system_id):
        self.brand = brand
        self.model_no = model_no
        self.serial_no = serial_no
        self.year = year
        self.equipment_type = equipment_type
        self.notes = notes
        self.system_id = system_id

class CoolingEquipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    model_no = db.Column(db.String(100), nullable=False)
    serial_no = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(10), nullable=False)
    equipment_type = db.Column(db.String(100), nullable=False)
    refrigerant_type = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.String(1000), nullable=True)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)

    def __init__(self, brand, model_no, serial_no, year, equipment_type, refrigerant_type, notes, system_id):
        self.brand = brand
        self.model_no = model_no
        self.serial_no = serial_no
        self.year = year
        self.equipment_type = equipment_type
        self.refrigerant_type = refrigerant_type
        self.notes = notes
        self.system_id = system_id

class MaintenanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)
    work_performed = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, system_id, work_performed):
        self.system_id = system_id
        self.work_performed = work_performed

class RepairLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_id = db.Column(db.Integer, db.ForeignKey('system.id'), nullable=False)
    work_performed = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, system_id, work_performed):
        self.system_id = system_id
        self.work_performed = work_performed