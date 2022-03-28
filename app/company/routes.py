from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required

# models
from app.models import User, Company, db

# forms
from .forms import NewCompanyForm, UpdateCompanyForm

# blueprint
company = Blueprint('company', __name__, template_folder='company_templates')

@company.route('/create-company', methods=["GET","POST"])
@login_required
def createCompany():
    form = NewCompanyForm()
    user = User.query.filter_by(id=current_user.id).first()
    if user.company_id:
        return redirect(url_for('home'))
    
    if request.method == "POST":
        if form.validate():
            company_name = form.company_name.data
            company_password = form.company_password.data
            street_address_1 = form.street_address_1.data
            street_address_2 = form.street_address_2.data
            city = form.city.data
            state = form.state.data
            zip_code = form.zip_code.data
            logo_url = form.logo_url.data
            admin_id = user.id

            # check if company exists
            company = Company.query.filter_by(company_name=company_name).first()
            if company:
                flash('That company name already exists. Please pick another name.', 'danger')
                return redirect(url_for('company.createCompany'))

            company = Company(company_name, street_address_1, street_address_2, city, state, zip_code, company_password=company_password)
            company.logo_url = logo_url
            company.admin_id = admin_id

            db.session.add(company)
            db.session.commit()

            user.company_id = company.id
            db.session.commit()

            flash(f'You have successfully created a new Company, {company_name}. ', 'success')
            return redirect(url_for('company.companyProfile'))

    return render_template('create_company.html', form=form)

@company.route('/company-profile')
@login_required
def companyProfile():
    if not current_user.company_id:
        flash('This account is not affiliated with a company.', 'danger')
        return redirect(url_for('home'))
    company = Company.query.filter_by(id=current_user.company_id).first()
    return render_template('company_profile.html', company=company)


@company.route('/update-company', methods=["GET","POST"])
@login_required
def updateCompany():
    form = UpdateCompanyForm()
    user = User.query.filter_by(id=current_user.id).first()
    company = Company.query.filter_by(id=current_user.company_id).first()

    if company.admin_id != user.id:
        flash('You do not have permission to edit this information.', 'danger')
        return redirect(url_for('auth.showProfile'))

    if request.method == "POST":
        if form.validate():
            company_name = form.company_name.data
            company_password = form.company_password.data
            street_address_1 = form.street_address_1.data
            street_address_2 = form.street_address_2.data
            city = form.city.data
            state = form.state.data
            zip_code = form.zip_code.data
            logo_url = form.logo_url.data

            company.company_name = company_name
            company.company_password = company_password
            company.street_address_1 = street_address_1
            company.street_address_2 = street_address_2
            company.city = city
            company.state = state
            company.zip_code = zip_code
            company.logo_url = logo_url

            db.session.commit()

            flash(f'You have successfully updated {company_name}. ', 'success')
            return redirect(url_for('company.companyProfile'))
    return render_template('update_company_info.html', form=form, company=company)
            