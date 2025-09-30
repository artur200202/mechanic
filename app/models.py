from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, String, Table, Column, Integer

class Base(DeclarativeBase):
  pass

db= SQLAlchemy(model_class=Base)

ticket_mechanics= db.Table(
  'ticket_mechanics',
    Base.metadata,
    db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

class Customers(Base):
  __tablename__= 'customers'

  id: Mapped[int]= mapped_column(primary_key=True)
  first_name: Mapped[str] = mapped_column(String(120), nullable=False)
  last_name: Mapped [str] = mapped_column (String(130), nullable=False)
  email: Mapped [str] = mapped_column (String(200), unique= True, nullable=False)
  phone: Mapped [str] = mapped_column (String(25), nullable=False)
  address: Mapped [str] = mapped_column (String (122), nullable=False)
  password: Mapped [str] = mapped_column (String (130), nullable= False)

  service_tickets: Mapped[list['ServiceTickets']] = relationship('ServiceTickets', back_populates= 'customer')

  def __repr__(self):
    return super().__repr__()
class ServiceTickets (Base):
  __tablename__= 'service_tickets'

  id: Mapped[int]= mapped_column(primary_key= True)
  service_desc: Mapped [str] = mapped_column (String(140), nullable=False)
  price: Mapped [int] = mapped_column (Integer, nullable=False)
  vin: Mapped [str] = mapped_column (String(150), unique= True)
  service_date: Mapped [date] = mapped_column (Date, nullable= False)
  customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'), nullable= False )
  
  customer : Mapped['Customers'] = relationship ('Customers', back_populates= 'service_tickets')
  mechanics: Mapped [list['Mechanics']] = relationship ('Mechanics' ,secondary='ticket_mechanics', back_populates='service_tickets' )

class Mechanics (Base) :
  __tablename__ = 'mechanics'

  id: Mapped [int] = mapped_column(primary_key=True)
  first_name: Mapped[str] = mapped_column(String(120), nullable=False)
  last_name: Mapped [str] = mapped_column (String(130), nullable=False)
  email: Mapped [str] = mapped_column (String(200), unique= True, nullable=False)
  password: Mapped [str] = mapped_column (String(200), unique = True, nullable=False)
  salary: Mapped [int]= mapped_column (Integer)
  address: Mapped [str] = mapped_column (String(260), nullable= False)

  service_tickets: Mapped[list['ServiceTickets']] = relationship('ServiceTickets', secondary = 'ticket_mechanics' , back_populates= 'mechanics')