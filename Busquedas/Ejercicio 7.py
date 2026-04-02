from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

Base = declarative_base()

class Film(Base):
    __tablename__ = 'film'
    film_id = Column(Integer, primary_key=True)
    title = Column(String)
    inventory = relationship("Inventory", back_populates="film")
    actors = relationship("FilmActor", back_populates="film")
    rental_duration = Column(Integer) 
    rental_rate = Column(Numeric(5, 2, asdecimal=False))

class FilmActor(Base):
    __tablename__ = 'film_actor'
    film_id = Column(Integer, ForeignKey('film.film_id'), primary_key=True)
    actor_id = Column(Integer, primary_key=True)
    film = relationship("Film", back_populates="actors")

class Inventory(Base):
    __tablename__ = 'inventory'
    inventory_id = Column(Integer, primary_key=True)
    film_id = Column(Integer, ForeignKey('film.film_id'))
    film = relationship("Film", back_populates="inventory")
    rentals = relationship("Rental", back_populates="inventory")

class Rental(Base):
    __tablename__ = 'rental'
    rental_id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey('inventory.inventory_id'))
    inventory = relationship("Inventory", back_populates="rentals")



db_path = Path(__file__).parent.parent / "sakilasqlite" / "data.sqlite"
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
session = Session()


avg_length_value = session.query(func.avg(Film.rental_duration)).scalar()
films_to_update = session.query(Film).filter(Film.rental_duration > avg_length_value).all()


print("Antes -> Después de actualización del precio:")
for film in films_to_update:
    old_price = Decimal(str(film.rental_rate))
    new_price = (Decimal(old_price) * Decimal('1.10')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) 
    print(f"{film.title}: {old_price} -> {new_price}")
    film.rental_rate = float(new_price)


#session.commit()
session.close()