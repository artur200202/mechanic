from app.blueprints.service_tickets import service_ticket_bp
from .schemas import service_tickets_schema, services_tickets_schema
from flask import request , jsonify
from marshmallow import ValidationError
from app.models import ServiceTickets , db

@service_ticket_bp.route ('', methods = ['POST'])
def create_service_ticket():
  try:
    data = service_tickets_schema.load(request.json)
  except ValidationError as e:
    return jsonify(e.messages), 400
  
  new_service_ticket = ServiceTickets(**data)
  db.session.add(new_service_ticket)
  db.session.commit()
  return service_tickets_schema.jsonify(new_service_ticket), 201

@service_ticket_bp.route('', methods=['GET']) #Endpoint to get user information
def read_service_tickets():
    service_ticket = db.session.query(ServiceTickets).all()
    return services_tickets_schema.jsonify(service_ticket), 200

@service_ticket_bp.route('<int:service_ticket_id>' , methods =['GET'])
def read_service_ticket(service_ticket_id):
  service_ticket = db.session.get(ServiceTickets, service_ticket_id)
  return service_tickets_schema.jsonify(service_ticket), 200

@service_ticket_bp.route('<int:service_ticket_id>', methods = ['DELETE'])
def delete_service_ticket(service_ticket_id):
  service_ticket = db.session.get(ServiceTickets, service_ticket_id) #which table and which value to query by Select * from Customers where id = customer_id
  db.session.delete(service_ticket)
  db.session.commit()
  return jsonify ({'message' : f"Successfully deleted user {service_ticket_id}"}), 200

@service_ticket_bp.route( '<int:service_ticket_id>', methods = ['PUT'])
def update_service_ticket(service_ticket_id):
  service_ticket = db.session.get(ServiceTickets, service_ticket_id) #getting the customers from the database using the customer id i provided

  if not service_ticket: 
    return jsonify ({"message": "service ticket not found"}), 404 #checks if the id i gave is valid for the customer
  
  try:
    service_ticket_data = service_tickets_schema.load (request.json) # passing the info to schema to validate the data
  except ValidationError as e:
    return jsonify({"message": e.message}), 400
  
  for key, value in service_ticket_data.items(): # looping through customer data and sets it as the new customer info
    setattr(service_ticket, key, value )

  db.session.commit()  #saving it to the database
  return service_tickets_schema.jsonify(service_ticket), 200
