from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, URL, Optional, NumberRange

species = ['dog', 'cat', 'porcupine']

class AddPetForm(FlaskForm):
    """Form to add a new pet"""

    name = StringField('Pet Name', validators=[InputRequired(message="Pet Name can't be blank")])
    species = SelectField('Species', choices = [(s,s) for s in species], validators=[InputRequired(message="Species field can't be blank")])
    photo_url = StringField('Photo', validators=[Optional(), URL(message="Not a valid URL address")])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=30, message='The age must be between 0 and 30') ])
    notes = StringField('Notes/Comments')

class EditPetForm(FlaskForm):
    """Form to edit existing pet"""
    
    photo_url = StringField('Photo', validators=[Optional(), URL(message="Not a valid URL address")])
    notes = StringField('Notes/Comments')
    available = BooleanField('Available')


