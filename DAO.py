from sqlalchemy import *
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from mapping import *

class DAO():
    #Criação da sessão com o banco de dados
    def getSession():
        engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/moviesDB")
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    
    #Método para inserir no banco
    def insert(session, obj):
        session.add(obj)
        

# DAO's para selects (por id)

class DAOGenres:
    def select(session, id):
        genre = session.query(Genre).filter(Genre.id == id).first()
        return genre
    
    
class DAOMovies:
    def select(session, id):
        movie = session.query(Movie).filter(Movie.id == id).first()
        return movie

   
class DAOCompanies:
    def select(session, id):
        company = session.query(Company).filter(Company.id == id).first()
        return company


class DAOReviews:
    def select(session, id):
        review = session.query(Review).filter(Review.id == id).first()
        return review
    

class DAOCast:
    def select(session, id):
        cast = session.query(Tcast).filter(Tcast.id == id).first()
        return cast


class DAOCrew:
    def select(session, id):
        crew = session.query(Crew).filter(Crew.id == id).first()
        return crew
    

class DAOPeople:
    def select(session, id):
        person = session.query(Person).filter(Person.id == id).first()
        return person