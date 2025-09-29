from flask import request , jsonify
from marshmallow import ValidationError
from app.models import Mechanics , db
from app.blueprints.mechanics import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema

@mechanic_bp.route ('', methods = ['POST'])
def create_mechanic():
  try:
    data = mechanic_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages), 400
  
  new_mechanic = Mechanics(**data)
  db.session.add(new_mechanic)
  db.session.commit()
  return mechanic_schema.jsonify(new_mechanic), 201

@mechanic_bp.route('', methods=['GET']) #Endpoint to get user information
def read_mechanics():
    mechanic = db.session.query(Mechanics).all()
    print(mechanic)
    return mechanics_schema.jsonify(mechanic), 200

@mechanic_bp.route('<int:mechanic_id>' , methods =['GET'])
def read_mechanic(mechanic_id):
  mechanic = db.session.get(Mechanics, mechanic_id)
  return mechanic_schema.jsonify(mechanic), 200

@mechanic_bp.route('<int:mechanic_id>', methods = ['DELETE'])
def delete_mechanic(mechanic_id):
  mechanic = db.session.get(Mechanics, mechanic_id) #which table and which value to query by Select * from Customers where id = customer_id
  db.session.delete(mechanic)
  db.session.commit()
  return jsonify ({'message' : f"Successfully deleted user {mechanic_id}"}), 200

@mechanic_bp.route( '<int:mechanic_id>', methods = ['PUT'])
def update_mechanic(mechanic_id):
  mechanic = db.session.get(Mechanics, mechanic_id) #getting the customers from the database using the customer id i provided

  if not mechanic: 
    return jsonify ({"message": "mechanic not found"}), 404 #checks if the id i gave is valid for the customer
  
  try:
    mechanic_data = mechanic_schema.load (request.json) # passing the info to schema to validate the data
  except ValidationError as e:
    return jsonify({"message": e.message}), 400
  
  for key, value in mechanic_data.items(): # looping through customer data and sets it as the new customer info
    setattr(mechanic, key, value )

  db.session.commit()  #saving it to the database
  return mechanic_schema.jsonify(mechanic), 200
