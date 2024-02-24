from flask import Flask, request, render_template, redirect, flash, session
#from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SECRET_KEY'] = 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
app.config['SQLALCHEMY_ECHO'] = True
#debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().__enter__()

@app.route('/')
def home_page():
    """Page listing all pets"""
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet_form():
    """Displaying adding pet form"""
    form = AddPetForm()

    if form.validate_on_submit():
        pet_dict={}
        pet_dict['name'] = form.name.data
        pet_dict['species'] = form.species.data
        if photo_url := form.photo_url.data:
            pet_dict['photo_url'] = photo_url
        pet_dict['age'] = form.age.data
        pet_dict['notes'] = form.notes.data
        new_pet = Pet(**pet_dict)
        db.session.add(new_pet)
        db.session.commit()
        flash(f'{new_pet.name} has been added!')
        return redirect('/')
    else:    
        return render_template('add_pet.html', form=form)

@app.route('/<int:id>', methods=['GET', 'POST'])
def pet_details(id):
    """Page showing pet details"""
    pet = Pet.query.get(id)
    form = EditPetForm(obj=pet)
    
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash(f'{pet.name} has been updated!')
        return redirect (f'/{pet.id}')
    else:
        return render_template('pet_details.html', pet=pet, form=form)