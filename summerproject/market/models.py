#this is models.py
from market import db
from market import bcrypt
from flask_login import UserMixin
from market import login_manager

@login_manager.user_loader
def load_user(user_id):
        return user.query.get(int(user_id))

class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(30), nullable=False, unique=True)
    email_address=db.Column(db.String(50), nullable=False, unique=True)
    password_hash=db.Column(db.String(60), nullable=False)
    budget=db.Column(db.Integer, nullable=False, default=10000000)
    items=db.relationship('Item', backref='owned_user', lazy=True)
    #backref is the name of the variable that will be used to access the parent object from the child object.
    #backref make you have referance obj between 2 tables as if yoy want to know who is th owner of the item it will take obj from user table which is owned_user
    #lazy=True means that the items will be loaded from the database when they are accessed for the first time.
    #lazy bt5liny aload all objects lo 5litha false aw el deafult bta3ha momkn ts2t obj mt5dho4
    #sql alchemy will not grab all objects in one shot
    @property
    def prettier_budget(self):
        if len(str(self.budget))>=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"
    
    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')    
    def check_password_correction(self, attempted_password):#attempted_password is the password fill in the form of login page and i want to verify it
        return bcrypt.check_password_hash(self.password_hash, attempted_password)#return true or false if password hash is match that fill in the form
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    def can_sell(self, item_obj):
        return item_obj in self.items #this line check if the item object is in the items list of the current useran give true or false then go to routes to see the logic
# Define your SQLAlchemy model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False)  # Corrected column name
    owner = db.Column(db.Integer, db.ForeignKey('user.id')) 
    #make it give information about user that have specifc item ex ig iphon owner is ahmed then go to talble user and give information about ahmed
    #so user id is the primary key of user table and owner is foreign key in item table
    def __repr__(self):
        return f'Item(name={self.name}, price={self.price}, barcode={self.barcode})'
    
    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
    def sell(self, user):
        self.owner = None # i want to sell the item so i want to change the owner of the item to none
        user.budget += self.price
        db.session.commit()
#this is models and when all data i added to it must to be add to all users not one user only when i try to purchase item with specific user i found that it disapeare from other user withput buing it why?