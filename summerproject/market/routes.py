#this is routes file
from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, user 
from market.forms import RegisterForm, LoginForm,PurchessItemForm,SellItemForm
from market import db
from flask_login import login_user,logout_user,current_user,login_required#is a decorator that tells flask that this function is a login required function if not logwd in not to go to market page 
# Routes
@app.route('/')
@app.route('/home')
def homepage():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required #this decorator is used to make sure that the user is logged in to access the market page
def marketpage():
    
    purchase_form = PurchessItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #purchasing item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
    #selling item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
           if current_user.can_sell(s_item_object):
               s_item_object.sell(current_user)
               flash(f"Congratulations! You sold {s_item_object.name} back to market !$", category='success')
           else:
               flash(f"Unfortunately, you don't have enough money to sell {s_item_object.name}!", category='danger') 
    
        return redirect(url_for('marketpage'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None).all()
        owned_items = Item.query.filter_by(owner=current_user.id).all()#this line give me all the items that current user owned them
        return render_template('market.html', items=items, purchase_form=purchase_form,owned_items=owned_items,selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])#to handel get and post request and to handel the form 
def registerpage():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = user(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password_hash.data)
        db.session.add(user_to_create)
        db.session.commit()
        #this 2 lines bellow will redirect the new registerd user to market unless he log in again in same time he registerd
        login_user(user_to_create)
        flash(f"Acoount created successfully! you are now logged in as {user_to_create.username} ",category='success')
        return redirect(url_for('marketpage'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)
@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = user.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            from flask_login import login_user
            login_user(attempted_user)
            flash(f'Successfully logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('marketpage'))
        else:
            flash('Username and password are not match please try again', category='danger')
    return render_template('login.html',form=form)
   
@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logged out', category='success')
    return redirect(url_for('homepage'))

