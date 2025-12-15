from app import create_app
from app.models import Customers, db
import unittest
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils import encode_token
class TestCustomers(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer= Customers(email='tester@gmail.com', firstName='greg', lastName='jef', phone='210-222-2222', address='123 fun st', password=generate_password_hash('123') )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1, 'customer')
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {
            "firstName": "david",
            "lastName": 'jeff',
            "email" : "test@email.com",
            "phone": "220-222-2222",
            "address" : "123 fun st.",
            "password" : '12334'
        }
        response = self.client.post('/customers', json=customer_payload)
        print(response)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['email'], 'test_customer')
        self.assertTrue(check_password_hash(response.json['password'], '12334'))
    
    def test_invalid_create(self):
        customer_payload = {
            "lastName": 'jeff',
            "email" : "test@email.com",
            "phone": "220-222-2222",
            "address" : "123 fun st.",
            "password" : '12334'
        }
        response = self.client.post('/customers', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('firstName', response.json)
    
    def test_get_customers(self):
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['email'], 'tester')

   
    def test_login(self):
      login_creds = {
        "email": "tester@gmail.com",
        "password": '123'
      }

      response = self.client.post('/customers/login', json =login_creds)
      self.assertEqual(response.status_code, 200)
      self.assertIn('auth_token', response.json)
  
    def test_delete(self):
      headers = {'authorization': "bearer " + self.token}

      response = self.client.delete('/customers', headers.headers)
      self.assertEqual(response.status_code, 201)
      self.assertEqual(response.json['message'], 'succesfully deleted user 1')
    