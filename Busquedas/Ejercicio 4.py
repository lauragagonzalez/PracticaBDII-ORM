## SQLAlchemy ORM tutorial Follow-up

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import select, update, delete, func, desc
from datetime import datetime as dt, timedelta

engine = create_engine("sqlite+pysqlite:///data.sqlite", echo=True, future=True)

Session = sessionmaker(bind=engine)
session = Session()

# operación 1: muestra el nombre del cliente y el número de películas que ha alquilado

# definición de clases

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key = True, autoincrement = True)
    first_name = Column(String)
    last_name = Column(String)
    rentals = relationship("Rental", back_populates = "customer")

class Rental(Base):
    __tablename__ = "rental"
    rental_id= Column(Integer, primary_key = True, autoincrement = True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    rental_date = Column(DateTime)
    customer = relationship("Customer", back_populates = "rentals")

# definición de consulta

# calculamos fecha hace 30 días

date_now = dt.now()
t = date_now - timedelta(days=30)

query = (
    select(Customer.first_name, Customer.last_name, Customer.customer_id, func.max(Rental.rental_date).label("last_rental"))
    .join(Rental)
    .group_by(Customer.customer_id, Customer.first_name, Customer.last_name)
    .having(func.max(Rental.rental_date) < t)
    )

result = session.execute(query).all()

for first, last, id, last_rental in result:
    print(f"{first} {last} (customer id: {id}) - último alquiler realizado el {last_rental}")
