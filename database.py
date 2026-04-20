import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. On récupère l'URL de Render, sinon on utilise ton MySQL local par défaut
# Note : 'ma_banque' doit correspondre au nom de ta base dans phpMyAdmin
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root@localhost/ma_banque")

# 2. Correction automatique du préfixe pour PostgreSQL (Spécificité Render/SQLAlchemy)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Création du moteur de base de données
engine = create_engine(DATABASE_URL)

# 4. Configuration de la session et de la base déclarative
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 5. Dépendance pour obtenir la session de base de données dans les routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
