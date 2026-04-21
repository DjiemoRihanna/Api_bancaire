import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# URL pour Render ou ton MySQL local
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root@localhost/ma_banque")

# Correction pour PostgreSQL sur Render
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle des Comptes
class Compte(Base):
    __tablename__ = "comptes"
    id = Column(Integer, primary_key=True, index=True)
    nom_titulaire = Column(String(100))
    solde = Column(Float, default=0.0)
    transactions = relationship("Transaction", back_populates="proprietaire")

# Modèle des Transactions (Historique)
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    type_operation = Column(String(50))
    montant = Column(Float)
    date_heure = Column(DateTime, default=datetime.utcnow)
    compte_id = Column(Integer, ForeignKey("comptes.id"))
    proprietaire = relationship("Compte", back_populates="transactions")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()