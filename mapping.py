# coding: utf-8
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, ForeignKey, Integer, Numeric, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Company(Base):
    __tablename__ = 'companies'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    homepage = Column(String(100))
    origin_country = Column(String(50))
    headquarters = Column(String(100))


class Genre(Base):
    __tablename__ = 'genres'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Movie(Base):
    __tablename__ = 'movies'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    status = Column(String(50))
    runtime = Column(Integer)
    revenue = Column(BigInteger)
    release_date = Column(Date)
    popularity = Column(Numeric)
    overview = Column(Text)
    original_title = Column(String(100))
    original_language = Column(String(50))
    budget = Column(BigInteger)
    adult = Column(Boolean)
    vote_count = Column(Integer)
    vote_average = Column(Numeric)

    companies = relationship('Company', secondary='public.movies_companies')
    genres = relationship('Genre', secondary='public.movies_genres')


class Person(Base):
    __tablename__ = 'people'
    __table_args__ = (
        CheckConstraint('(gender >= 0) AND (gender <= 3)'),
        {'schema': 'public'}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    gender = Column(Integer, server_default=text("0"))
    popularity = Column(Numeric)



class Crew(Base):
    __tablename__ = 'crew'
    __table_args__ = {'schema': 'public'}

    id = Column(String(50), primary_key=True)
    job = Column(String(100))
    department = Column(String(100))
    personid = Column(ForeignKey('public.people.id', ondelete='CASCADE'), nullable=False)
    movieid = Column(ForeignKey('public.movies.id', ondelete='CASCADE'), nullable=False)

    movie = relationship('Movie')
    person = relationship('Person')


t_movies_companies = Table(
    'movies_companies', metadata,
    Column('movieid', ForeignKey('public.movies.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('companyid', ForeignKey('public.companies.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    schema='public'
)


t_movies_genres = Table(
    'movies_genres', metadata,
    Column('movieid', ForeignKey('public.movies.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('genreid', ForeignKey('public.genres.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    schema='public'
)


class Review(Base):
    __tablename__ = 'reviews'
    __table_args__ = (
        CheckConstraint('(rating >= 0) AND (rating <= 10)'),
        {'schema': 'public'}
    )

    id = Column(String(50), primary_key=True)
    author = Column(String(100))
    content = Column(Text)
    rating = Column(Integer)
    movieid = Column(ForeignKey('public.movies.id', ondelete='CASCADE'), nullable=False)

    movie = relationship('Movie')


class Tcast(Base):
    __tablename__ = 'tcast'
    __table_args__ = {'schema': 'public'}

    id = Column(String(50), primary_key=True)
    character = Column(String(100))
    department = Column(String(100))
    personid = Column(ForeignKey('public.people.id', ondelete='CASCADE'), nullable=False)
    movieid = Column(ForeignKey('public.movies.id', ondelete='CASCADE'), nullable=False)

    movie = relationship('Movie')
    person = relationship('Person')
