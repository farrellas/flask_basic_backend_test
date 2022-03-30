from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required

# models
from app.models import Customer, System, db

# forms
from .forms import NewCustomerForm, UpdateCustomerForm

# blueprint
customer = Blueprint('customer', __name__, template_folder='customer_templates')

#global variables
states=["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware",
"District Of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa""Kansas","Kentucky",
"Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
"Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota",
"Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas",
"Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

@customer.route('/customer-list')
@login_required
def customerList():
    if current_user.company_id:
        customers = Customer.query.filter_by(company_id=current_user.company_id).all()
    else:
        customers = Customer.query.filter_by(user_id=current_user.id).all()
    return render_template('customer_list.html', customers=customers)

@customer.route('/customer/<int:customer_id>')
@login_required
def customerInfo(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    systems = System.query.filter_by(customer_id=customer_id).all()[::-1]
    if customer is None:
        return redirect(url_for('home'))
    return render_template('customer_info.html', customer=customer, systems=systems)
    

@customer.route('/customer/create', methods=["GET","POST"])
@login_required
def createCustomer():
    form = NewCustomerForm()
    if request.method == "POST":
        if form.validate():
            name = form.name.data
            street_address_1 = form.street_address_1.data
            street_address_2 = form.street_address_2.data
            city = form.city.data
            state = form.state.data
            zip_code = form.zip_code.data
            email = form.email.data

            customer = Customer(name, street_address_1, street_address_2, city, state, zip_code, email, user_id=current_user.id)
            if current_user.company_id:
                customer.company_id = current_user.company_id

            db.session.add(customer)
            db.session.commit()

            flash(f'You have successfully created a new customer, {name}.', 'success')
            return redirect(url_for('customer.customerList'))
    return render_template('create_customer.html', form=form, states=states)

@customer.route('/customer/update/<int:customer_id>', methods=["GET","POST"])
@login_required
def updateCustomer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    if customer is None:
        return redirect(url_for('home'))
    if (current_user.company_id != customer.company_id) and (current_user.id != customer.user_id):
        flash('You do not have permission to edit this information.', 'danger')
        return redirect(url_for('home'))

    form = UpdateCustomerForm()

    if request.method == "POST":
        if form.validate():
            name = form.name.data
            street_address_1 = form.street_address_1.data
            street_address_2 = form.street_address_2.data
            city = form.city.data
            state = form.state.data
            zip_code = form.zip_code.data
            email = form.email.data

            customer.name = name
            customer.street_address_1 = street_address_1
            customer.street_address_2 = street_address_2
            customer.city = city
            customer.state = state
            customer.zip_code = zip_code
            customer.email = email
            
            if current_user.company_id:
                customer.company_id = current_user.company_id

            db.session.commit()

            flash(f'You have successfully updated customer: {name}.', 'success')
            return redirect(url_for('customer.customerInfo', customer_id=customer_id))
    return render_template('update_customer.html', form=form, states=states, customer=customer, customer_id=customer_id)


@customer.route('/customer/delete/<int:customer_id>', methods=["POST"])
@login_required
def deleteCustomer(customer_id):
    customer = Customer.query.filter_by(id=customer_id).first()
    if customer is None:
        flash(f'That customer does not exist.', 'danger')
        return redirect(url_for('customer.customerList'))
    if (customer.user_id != current_user.id) and (customer.company_id != current_user.company_id):
        flash(f'You do not have permission to delete this customer.', 'danger')
        return redirect(url_for('customer.customerList'))

    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('customer.customerList'))


@customer.route('/api/customer-list')
def apiCustomerList():
    customers = Customer.query.all()
    return {
        'customers': [c.to_dict() for c in customers],
        'total_results': len(customers)
    }