from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from pathlib import Path
Base = declarative_base()

# Definimos las tablas
class Film(Base):
    __tablename__ = 'film'
    film_id = Column(Integer, primary_key=True)
    title = Column(String)
    actors = relationship("FilmActor", back_populates="film")

class FilmActor(Base):
    __tablename__ = 'film_actor'
    film_id = Column(Integer, ForeignKey('film.film_id'), primary_key=True)
    actor_id = Column(Integer, primary_key=True)
    film = relationship("Film", back_populates="actors")


db_path = Path(__file__).parent.parent / "sakilasqlite" / "data.sqlite"
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)
session = Session()

result = (session.query(Film.title, func.count(FilmActor.actor_id).label('num_actores'))
           .join(FilmActor)
           .group_by(Film.film_id)
           .having(func.count(FilmActor.actor_id) > 3)
           .order_by(func.count(FilmActor.actor_id).desc())
           .all())

for title, num_actores in result:
    print(f"{title} - {num_actores} actores")

session.close()
