## SQLAlchemy ORM tutorial Follow-up

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import select, update, delete, func, desc, cast
from datetime import datetime as dt, timedelta

engine = create_engine("sqlite+pysqlite:///data.sqlite", echo=True, future=True)

Session = sessionmaker(bind=engine)
session = Session()

# operación 1: muestra el nombre del cliente y el número de películas que ha alquilado

# definición de clases

Base = declarative_base()

class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String)
    last_update = Column(DateTime)
    films = relationship("FilmCategory", back_populates = "category")


class FilmCategory(Base):
    __tablename__ = "film_category"
    film_id = Column(Integer, ForeignKey("film.film_id"), primary_key = True)
    category_id = Column(Integer, ForeignKey("category.category_id"), primary_key= True)
    last_update = Column(DateTime)

    category = relationship("Category", back_populates = "films")
    film = relationship("Film", back_populates = "film_categories")


class Film(Base):
    __tablename__ = "film"
    film_id = Column(Integer, primary_key = True, autoincrement = True)
    rental_rate = Column(Float)
    film_categories = relationship("FilmCategory", back_populates = "film")


# calculamos el precio medio de alquiler

query1 = (
    select(func.avg(Film.rental_rate))
)

mean = session.scalar(query1)
print(f"\nMedia: {mean}")

# insercción de la nueva categoría

premium_cat = Category(name = "Premium", last_update = dt.now())

session.add(premium_cat)
session.flush()

# películas cuyo precio es mayor que la media

query2 = (
    select(Film.film_id).where(cast(Film.rental_rate, Float) > 2.98)
)

pelis_premium = session.scalars(query2).all()

for id in pelis_premium:
    print(f"{id}") 

print(f"\nCategoría Premium: {premium_cat.category_id}")

for film in pelis_premium:
    peli_premium = FilmCategory(film_id = film, category_id = premium_cat.category_id, last_update = dt.now())
    session.add(peli_premium)

session.commit()

# comprobación

query3 = select(FilmCategory, Film.rental_rate).join(Film)

result = session.execute(query3).all()

for fc, rental_rate in result:
    print(f"{fc.film_id} - {fc.category_id} - {rental_rate} - {fc.last_update}") 