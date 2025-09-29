from app.blueprints.customers import customer_bp
from .schemas import customer_schema, customers_schema
from flask import request , jsonify
from marshmallow import ValidationError
from app.models import Customers , db
from app.utils.util import encode_token
@customer_bp.route('/login', methods = ['POST'])
def login():
  try:
    credentials = request.json
    username = credentials ['username']
    password = credentials ['password']
  except KeyError:
    return jsonify({'messages:' 'invalid payload, excepting username and password'})
  query = select(Customers).where(Customers.username === username)
  customer = db.session.execute(query).scalar_one_or_none()

  if customer and customer.password == password:
    auth_token = encode_token(customer.id)

  response = {
    "status": "sucess",
    "message": "sucessfully logged in",
    'auth_token': auth_token
  }
  return jsonify(respsn)
@customer_bp.route ('', methods = ['POST'])
def create_customer():
  try:
    data = customer_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages), 400
  
  new_customer = Customers(**data)
  db.session.add(new_customer)
  db.session.commit()
  return customer_schema.jsonify(new_customer), 201

@customer_bp.route('', methods=['GET']) #Endpoint to get user information
def read_customers():
    customer = db.session.query(Customers).all()
    return customers_schema.jsonify(customer), 200

@customer_bp.route('<int:customer_id>' , methods =['GET'])
def read_customer(customer_id):
  customer = db.session.get(Customers, customer_id)
  return customer_schema.jsonify(customer), 200

@customer_bp.route('<int:customer_id>', methods = ['DELETE'])
def delete_customer(customer_id):
  customer= db.session.get(Customers, customer_id) #which table and which value to query by Select * from Customers where id = customer_id
  db.session.delete(customer)
  db.session.commit()
  return jsonify ({'message' : f"Successfully deleted user {customer_id}"}), 200

@customer_bp.route( '<int:customer_id>', methods = ['PUT'])
def update_customer(customer_id):
  customer = db.session.get(Customers, customer_id) #getting the customers from the database using the customer id i provided

  if not customer: 
    return jsonify ({"message": "customer not found"}), 404 #checks if the id i gave is valid for the customer
  
  try:
    customer_data = customer_schema.load (request.json) # passing the info to schema to validate the data
  except ValidationError as e:
    return jsonify({"message": e.message}), 400
  
  for key, value in customer_data.items(): # looping through customer data and sets it as the new customer info
    setattr(customer, key, value )

  db.session.commit()  #saving it to the database
  return customer_schema.jsonify(customer), 200