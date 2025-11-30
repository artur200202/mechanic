from app import create_app
from app.models import db
from werkzeug.security import check_password_hash, generate_password_hash
import unittest
from app.utils.util import encode_token

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customers(email='', username='', password='', role='')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.comit() 
        self.token = encode_token(1, 'customer')
        self.client = self.app.test_cllient()
    def test_create_customer(self):
        customer_payload = {
            
            "firstName": "test_customer",
            "email": "test@email.com",
           	"DOB": "1900-01-01",
            "role": "admin",
            "password": "123",
            "address" : "123 fun st."
        }
        response = self.client.post('/customers/', json=customer_payload)
        print(response.json)
        self.assertEqual(response.status_code, 201)
        self.assertIn(response.json['email'], "response.json")

    def test_invalid_customer(self):
        customer_payload = {
            
            "firstName": "test_customer",
           	"DOB": "1900-01-01",
            "role": "admin",
            "password": "123",
            "address" : "123 fun st."
        }
        response = self.client.post('/customers/', json=customer_payload)
        print(response.json)
        self.assertEqual(response.status_code, 400)
        self.assertIn(response.json['email'], "response.json")

    def test_login(self):
      login_creds = {
        "email": "tester",
        "password": '123'
      }

      response = self.client.post('/customers/login', json =login_creds)
      self.assertEqual(response.status_code, 200)
      self.assertIn('auth_token', response.json)

    def test_get_customers(self):
      response = self.client.get('/customers')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.json [0]['username'], 'tester')
  
    def test_delete(self):
      headers = {'auhotization': "bearer " + self.token}

      response = self.client.delete('/users', headers.headers)
      self.assertEqual(response.status_code, 201)
      self.assertEqual(response.json['message'], 'succesfully deleted user 1')
    