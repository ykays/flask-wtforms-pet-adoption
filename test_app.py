from unittest import TestCase

from app import app
from models import db, Pet
from forms import AddPetForm, EditPetForm

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_test'
app.config['SQLALCHEMY_ECHO'] = False


app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED']=False 

db.drop_all()
db.create_all()

class PetViewTestCases(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""
        Pet.query.delete()

        pet = Pet(name='Jack', species='dog',photo_url='/static/dog.jpg' , age=1, notes='little dog')

        db.session.add(pet)
        db.session.commit()
        self.pet_id = pet.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    def test_home(self):
        """Testing home page with all pets"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jack', html)
            self.assertIn('is available', html)
    
    def test_add_new_pet(self):
        """Testing adding new pet"""
        with app.test_client() as client:
            d = {'name': 'Lua', 'species': 'cat', 'age': 2, 'notes': 'loves treats!'}
            resp = client.post('/add', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Lua', html)
            self.assertIn('is available', html)
    
    def test_pet_details(self):
        """Testing details page"""
        with app.test_client() as client:
            resp = client.get(f'/{self.pet_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Name: Jack', html)
            self.assertIn('is available', html)
            self.assertIn('Species: dog', html)
            self.assertIn('Age: 1', html)
            self.assertIn('Notes/Comments: little dog', html)
    
    def test_editing_pet_details(self):
        """Testing edit form"""
        with app.test_client() as client:
            d = {'notes': 'little dog, loves running'}
            resp = client.post(f'/{self.pet_id}', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Name: Jack', html)
            self.assertIn('Species: dog', html)
            self.assertIn('Notes/Comments: little dog, loves running', html)