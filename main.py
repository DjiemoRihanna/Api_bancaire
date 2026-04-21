from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import Base, engine, get_db, Compte, Transaction

# Interface ultra-épurée
app = FastAPI(
    title="Système Bancaire",
    description=" ",
    version=" "
)

# Création automatique des tables
Base.metadata.create_all(bind=engine)

# --- ACCUEIL ---
@app.get("/")
def root():
    return {
        "Statut": "Opérationnel",
        "Auteur": "Grace - L3 Cybersécurité"
    }

# --- GESTION DES COMPTES ---
@app.post("/comptes/", tags=["Gestion des Comptes"])
def creer_compte(nom: str, solde_initial: float = 0.0, db: Session = Depends(get_db)):
    if solde_initial < 0:
        raise HTTPException(status_code=400, detail="Le solde ne peut pas être négatif")
    nouveau = Compte(nom_titulaire=nom, solde=solde_initial)
    db.add(nouveau)
    db.commit()
    db.refresh(nouveau)
    return nouveau

@app.delete("/comptes/{compte_id}", tags=["Gestion des Comptes"])
def supprimer_compte(compte_id: int, db: Session = Depends(get_db)):
    compte = db.query(Compte).filter(Compte.id == compte_id).first()
    if not compte:
        raise HTTPException(status_code=404, detail="Compte introuvable")
    db.delete(compte)
    db.commit()
    return {"message": "Compte supprimé avec succès"}

# --- TRANSACTIONS ---
@app.put("/comptes/{compte_id}/retrait", tags=["Transactions"])
def retirer(compte_id: int, montant: float = Query(..., gt=0), db: Session = Depends(get_db)):
    compte = db.query(Compte).filter(Compte.id == compte_id).first()
    if not compte:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    if compte.solde < montant:
        raise HTTPException(status_code=400, detail="Solde insuffisant")
    
    compte.solde -= montant
    db.add(Transaction(type_operation="Retrait", montant=montant, compte_id=compte_id))
    db.commit()
    return {"message": "Retrait réussi", "nouveau_solde": compte.solde}

@app.post("/transfert", tags=["Transactions"])
def transfert(expediteur_id: int, destinataire_id: int, montant: float = Query(..., gt=0), db: Session = Depends(get_db)):
    exp = db.query(Compte).filter(Compte.id == expediteur_id).first()
    dest = db.query(Compte).filter(Compte.id == destinataire_id).first()
    
    if not exp or not dest:
        raise HTTPException(status_code=404, detail="Compte introuvable")
    if exp.solde < montant:
        raise HTTPException(status_code=400, detail="Solde insuffisant")
    
    exp.solde -= montant
    dest.solde += montant
    db.add(Transaction(type_operation=f"Transfert vers ID {destinataire_id}", montant=montant, compte_id=expediteur_id))
    db.add(Transaction(type_operation=f"Reçu de ID {expediteur_id}", montant=montant, compte_id=destinataire_id))
    db.commit()
    return {"message": "Transfert effectué avec succès"}

# --- CONSULTATION ---
@app.get("/comptes/", tags=["Consultation"])
def liste_comptes(db: Session = Depends(get_db)):
    """Affiche la liste de tous les comptes enregistrés"""
    return db.query(Compte).all()

@app.get("/comptes/{compte_id}/historique", tags=["Consultation"])
def voir_historique(compte_id: int, db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.compte_id == compte_id).all()
