from app.extensions import ma
from app.models import ServiceTickets

class ServiceTicketsSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = ServiceTickets
    include_fk = True
    
service_tickets_schema = ServiceTicketsSchema()
services_tickets_schema = ServiceTicketsSchema(many=True)