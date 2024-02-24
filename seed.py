from models import db, Pet
from app import app

#Create all tables
db.drop_all()
db.create_all()


# Add new pets

buddy = Pet(name='Buddy', species='dog',photo_url='/static/dog.jpg' , age=1, notes='cute little dog')
hannah = Pet(name='Hannah', species='cat',photo_url='/static/cat.jpg' , age=2, notes='moody')
hillary = Pet(name='Hillary', species='porcupine',photo_url='/static/porcupine.jpg' , age=1, available=False)


# Add new objects to the session
db.session.add(buddy)
db.session.add(hannah)
db.session.add(hillary)


# Commit changes
db.session.commit()