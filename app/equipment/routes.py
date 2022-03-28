from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

# models
from app.models import HeatingEquipment, CoolingEquipment, AirHandlingEquipment, MaintenanceLog, RepairLog, System, Customer, db

# forms
from .forms import NewSystemForm, UpdateSystemForm

# blueprint
equipment = Blueprint('equipment', __name__, template_folder='equipment_templates')

@equipment.route('/systems/<int:system_id>', methods=["GET","POST"])
@login_required
def systemInfo(system_id):
    system = System.query.filter_by(id=system_id).first()
    heat = HeatingEquipment.query.filter_by(id=system_id).all()
    cool = CoolingEquipment.query.filter_by(id=system_id).all()
    air_handler = AirHandlingEquipment.query.filter_by(id=system_id).all()
    maintenance_logs = MaintenanceLog.query.filter_by(id=system_id).all()[::-1]
    repair_logs = RepairLog.query.filter_by(id=system_id).all()[::-1]
    if system is None:
        redirect(url_for('home'))
    return render_template('system_info.html', system=system, heat=heat, cool=cool, air_handler=air_handler, maintenance_logs=maintenance_logs, repair_logs=repair_logs)

@equipment.route('/systems/create/<int:customer_id>', methods=["GET","POST"])
@login_required
def createSystem(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    if current_user.company_id != customer.company_id and current_user.id != customer.user_id:
        flash("You do not have permission to edit this customer's equipment.", 'success')
        return redirect(url_for('home'))
    
    form = NewSystemForm()
    if request.method == "POST":
        if form.validate():
            name = form.name.data
            area_served = form.area_served.data
            system_type = form.system_type.data
            heating = form.heating.data
            cooling = form.cooling.data
            notes = form.notes.data

            system = System(name, area_served, system_type, heating, cooling, notes, customer.id)

            db.session.add(system)
            db.session.commit()

            flash(f'You have successfully created a new System for {customer.name}', 'success')
            return redirect(url_for('customer.customerInfo', customer_id=customer.id))
    return render_template('create_system.html', form=form, customer=customer)

@equipment.route('/systems/update/<int:system_id>', methods=["GET","POST"])
@login_required
def updateSystem(system_id):
    system = System.query.filter_by(id=system_id).first()
    customer = Customer.query.filter_by(id=system.customer_id).first()
    if current_user.company_id != customer.company_id and current_user.id != customer.user_id:
        flash("You do not have permission to edit this customer's equipment.", 'success')
        return redirect(url_for('home'))
    
    form = UpdateSystemForm()
    if request.method == "POST":
        if form.validate():
            name = form.name.data
            area_served = form.area_served.data
            system_type = form.system_type.data
            heating = form.heating.data
            cooling = form.cooling.data
            notes = form.notes.data

            system.name = name
            system.area_served = area_served
            system.system_type = system_type
            system.heating = heating
            system.cooling = cooling
            system.notes = notes

            db.session.commit()

            flash(f'You have successfully updated system: {name}.', 'success')
            return redirect(url_for('equipment.systemInfo', system_id=system.id))
    return render_template('update_system.html', form=form, customer=customer, system=system)