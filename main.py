from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float
from database import Base, engine, get_db

# --- DÉFINITION DU MODÈLE ---
# Doit correspondre à la structure vue dans phpMyAdmin
class Compte(Base):
    __tablename__ = "comptes"
    id = Column(Integer, primary_key=True, index=True)
    nom_titulaire = Column(String(100))
    type_compte = Column(String(20), default="courant")
    solde = Column(Float, default=0.0)

# --- INITIALISATION ---
app = FastAPI(title="Mon API Bancaire Pro")

# CRITICAL : On crée les tables APRES avoir défini la classe Compte
Base.metadata.create_all(bind=engine)

# --- ROUTES DE L'API ---

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de ma banque ! Allez sur /docs pour tester."}

# 1. Créer un compte
@app.post("/comptes/")
def creer_compte(nom: str, solde_initial: float = 0.0, db: Session = Depends(get_db)):
    nouveau_compte = Compte(nom_titulaire=nom, solde=solde_initial)
    db.add(nouveau_compte)
    db.commit()
    db.refresh(nouveau_compte)
    return nouveau_compte

# 2. Liste de tous les comptes
@app.get("/comptes/")
def liste_comptes(db: Session = Depends(get_db)):
    return db.query(Compte).all()

# 3. Faire un dépôt
@app.put("/comptes/{compte_id}/depot")
def deposer(compte_id: int, montant: float, db: Session = Depends(get_db)):
    compte = db.query(Compte).filter(Compte.id == compte_id).first()
    if not compte:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    compte.solde += montant
    db.commit()
    return {"message": f"Dépôt réussi. Nouveau solde: {compte.solde}"}

# 4. Faire un retrait
@app.put("/comptes/{compte_id}/retrait")
def retirer(compte_id: int, montant: float, db: Session = Depends(get_db)):
    compte = db.query(Compte).filter(Compte.id == compte_id).first()
    if not compte:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    if compte.solde < montant:
        raise HTTPException(status_code=400, detail="Solde insuffisant !")
    compte.solde -= montant
    db.commit()
    return {"message": f"Retrait réussi. Nouveau solde: {compte.solde}"}
