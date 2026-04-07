## SQLAlchemy ORM tutorial Follow-up

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import select, update, delete, func, desc

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
    customer = relationship("Customer", back_populates = "rentals")

# definición de consulta

query = (
    select(Customer.first_name, Customer.last_name, func.count(Rental.rental_id).label("num_rentals"))
    .join(Rental)
    .group_by("customer_id")
    )

result = session.execute(query).all()

for first, last, num_rentals in result:
    print(f"{first} {last} - {num_rentals} películas alquiladas")
