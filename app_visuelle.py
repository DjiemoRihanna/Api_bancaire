import customtkinter as ctk
import requests
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LogicielBancaireRealiste(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURATION FENÊTRE ---
        self.title("UY1 - SYSTÈME BANCAIRE PROFESSIONNEL V1.0")
        self.geometry("1150x750")
        self.api_url = "https://api-bancaire-oxjy.onrender.com"

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. NAVIGATION LATÉRALE
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.logo = ctk.CTkLabel(self.sidebar, text="BANK-OPS PRO", font=("Roboto", 24, "bold"))
        self.logo.pack(pady=30)

        # 2. ZONE DE TRAVAIL
        self.main_area = ctk.CTkFrame(self, corner_radius=15)
        self.main_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # 3. CHAMPS DE SAISIE UNIFIÉS
        self.input_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.input_frame.pack(pady=10)
        self.ent_nom = ctk.CTkEntry(self.input_frame, placeholder_text="Nom du Titulaire", width=250)
        self.ent_nom.grid(row=0, column=0, padx=10, pady=10)
        self.ent_montant = ctk.CTkEntry(self.input_frame, placeholder_text="Montant (FCFA)", width=250)
        self.ent_montant.grid(row=0, column=1, padx=10, pady=10)
        self.ent_id_src = ctk.CTkEntry(self.input_frame, placeholder_text="ID Source (Expéditeur)", width=250)
        self.ent_id_src.grid(row=1, column=0, padx=10, pady=10)
        self.ent_id_dest = ctk.CTkEntry(self.input_frame, placeholder_text="ID Destinataire", width=250)
        self.ent_id_dest.grid(row=1, column=1, padx=10, pady=10)

        # 4. GRILLE DES 10 FONCTIONNALITÉS (BOUTONS)
        self.grid_actions = ctk.CTkFrame(self.main_area)
        self.grid_actions.pack(pady=10, padx=20, fill="x")

        # Ligne 1 : Gestion Clientèle
        ctk.CTkButton(self.grid_actions, text="1. Ouverture Compte", command=self.f1_ouvrir).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(self.grid_actions, text="2. Fermeture Compte", command=self.f2_fermer, fg_color="#c0392b").grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(self.grid_actions, text="3. Audit Global", command=self.f3_audit).grid(row=0, column=2, padx=5, pady=5)

        # Ligne 2 : Transactions Courantes
        ctk.CTkButton(self.grid_actions, text="4. Dépôt Espèces", command=self.f4_depot, fg_color="#27ae60").grid(row=1, column=0, padx=5, pady=5)
        ctk.CTkButton(self.grid_actions, text="5. Retrait Guichet", command=self.f5_retrait, fg_color="#e67e22").grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkButton(self.grid_actions, text="6. Virement Interne", command=self.f6_virement, fg_color="#8e44ad").grid(row=1, column=2, padx=5, pady=5)

        # Ligne 3 : Sécurité & Analyse
        ctk.CTkButton(self.grid_actions, text="7. Historique (Audit Trail)", command=self.f7_logs).grid(row=2, column=0, padx=5, pady=5)
        ctk.CTkButton(self.grid_actions, text="8. Vérifier Solde", command=self.f8_solde, fg_color="#2980b9").grid(row=2, column=1, padx=5, pady=5)
        ctk.CTkButton(self.grid_actions, text="9. Simulation Fraude", command=self.f9_fraude, fg_color="#7f8c8d").grid(row=2, column=2, padx=5, pady=5)

        # Ligne 4 : Système
        ctk.CTkButton(self.grid_actions, text="10. Ping Serveur", command=self.f10_ping, fg_color="#2ecc71").grid(row=3, column=1, padx=5, pady=5)

        # 5. CONSOLE DE SORTIE
        self.console = ctk.CTkTextbox(self.main_area, width=850, height=250, font=("Consolas", 12))
        self.console.pack(pady=20)

    # --- MÉTHODES OPÉRATIONNELLES ---

    def log(self, text):
        """Efface et écrit dans la console du logiciel"""
        self.console.delete("0.0", "end")
        self.console.insert("0.0", text)

    def f1_ouvrir(self):
        # Envoie une requête POST pour créer un utilisateur en base PostgreSQL
        r = requests.post(f"{self.api_url}/comptes/", params={"nom": self.ent_nom.get(), "solde_initial": self.ent_montant.get()})
        self.log(f"ACTION: Ouverture de compte\nRETOUR: {r.json()}")

    def f2_fermer(self):
        # Supprime définitivement l'accès et les données d'un compte via son ID
        r = requests.delete(f"{self.api_url}/comptes/{self.ent_id_src.get()}")
        self.log(f"ACTION: Résiliation de compte\nRETOUR: {r.json()}")

    def f3_audit(self):
        # Affiche la liste de tous les comptes pour surveillance administrative
        r = requests.get(f"{self.api_url}/comptes/")
        self.log(f"ACTION: Audit complet du système\nRETOUR: {r.json()}")

    def f4_depot(self):
        # Simule un dépôt en utilisant la logique de crédit du backend
        # (Note: Tu peux utiliser la même route que le retrait avec un montant positif si ton API le permet)
        self.log("INFO: Utiliser l'interface Swagger pour les dépôts directs ou adapter la route PUT.")

    def f5_retrait(self):
        # Effectue un retrait avec vérification de provision (Sécurité financière)
        r = requests.put(f"{self.api_url}/comptes/{self.ent_id_src.get()}/retrait", params={"montant": self.ent_montant.get()})
        self.log(f"ACTION: Retrait espèce\nRETOUR: {r.json()}")

    def f6_virement(self):
        # Transaction atomique entre deux comptes distincts
        p = {"expediteur_id": self.ent_id_src.get(), "destinataire_id": self.ent_id_dest.get(), "montant": self.ent_montant.get()}
        r = requests.post(f"{self.api_url}/transfert", params=p)
        self.log(f"ACTION: Virement bancaire\nRETOUR: {r.json()}")

    def f7_logs(self):
        # Récupère l'historique des transactions (Audit Trail) pour l'expertise légale
        r = requests.get(f"{self.api_url}/comptes/{self.ent_id_src.get()}/historique")
        self.log(f"ACTION: Analyse de l'historique (Cyber-Forensics)\nRETOUR: {r.json()}")

    def f8_solde(self):
        # Vérification d'intégrité : affiche uniquement le solde actuel d'un compte
        r = requests.get(f"{self.api_url}/comptes/")
        comptes = r.json()
        mon_compte = [c for c in comptes if str(c['id']) == self.ent_id_src.get()]
        self.log(f"ACTION: Consultation Solde\nDONNÉES: {mon_compte if mon_compte else 'ID Inconnu'}")

    def f9_fraude(self):
        # Test de pénétration : tente de retirer un montant négatif pour tester les gardes-fous du Backend
        r = requests.put(f"{self.api_url}/comptes/{self.ent_id_src.get()}/retrait", params={"montant": -5000})
        self.log(f"TEST SÉCURITÉ: Injection montant négatif\nREPONSE API: {r.status_code} - {r.json()}")

    def f10_ping(self):
        # Vérifie la disponibilité du serveur distant sur Render
        r = requests.get(f"{self.api_url}/")
        self.log(f"SYSTEME: Heartbeat Serveur\nSTATUS: {r.json()}")

if __name__ == "__main__":
    app = LogicielBancaireRealiste()
    app.mainloop()
