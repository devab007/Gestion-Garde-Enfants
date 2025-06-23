from models import Base, Employe
from sqlalchemy import create_engine
from config import DATABASE_URL
from sqlalchemy.orm import sessionmaker
from datetime import date

engine = create_engine("postgresql://postgres:passer@localhost:5432/garderie_enfants")

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
db_session = SessionLocal()
