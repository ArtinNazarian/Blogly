from unittest import TestCase
from app import app
from flask import session
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True


db.drop_all()
db.create_all()

class UserRouteTest(TestCase):

    def setUp(self):
        User.query.delete()

        user= User(first_name='Sergio', last_name='Ramos', img_url='https://b.fssta.com/uploads/application/soccer/headshots/884.vresize.350.350.medium.61.png')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user
    
    def tearDown(self):
        db.session.rollback()

    
    def test_users_page(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code,200)
            self.assertIn('<h1>Users</h1>', html)

    def test_user_info(self):
        with app.test_client() as client:
            res = client.get(f'users/{self.user_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3>Sergio Ramos</h3>',html)
            self.assertIn(self.user.img_url, html)

    def test_add_user(self):
        with app.test_client() as client:
            data = {'first_name': 'John', 'last_name':'Adams', 'img_url':'www.img.com'}
            res = client.post("/users/new", data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.user.full_name, html)

    def test_delete_user(self):
        with app.test_client() as client:
            data = {'first_name': 'Sergio', 'last_name':'Ramos', 'img_url':'https://b.fssta.com/uploads/application/soccer/headshots/884.vresize.350.350.medium.61.png'}
            res=client.post(f'/users/{self.user_id}/delete', data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            user = User.query.get(self.user_id)
            self.assertNotIn('Sergio Ramos',html)






  