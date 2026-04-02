from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, aliased
from pathlib import Path

Base = declarative_base()

class Film(Base):
    __tablename__ = 'film'
    film_id = Column(Integer, primary_key=True)
    title = Column(String)
    inventory = relationship("Inventory", back_populates="film")
    actors = relationship("FilmActor", back_populates="film")

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

inv = aliased(Inventory)
r = aliased(Rental)

pelis_sin_alquiler = (
    session.query(Film)
    .outerjoin(inv, Film.film_id == inv.film_id)
    .outerjoin(r, inv.inventory_id == r.inventory_id)
    .filter(r.rental_id == None)
    .all()
)

print("\nPelículas nunca alquiladas:")
for film in pelis_sin_alquiler:
    print(film.title)


session.close()