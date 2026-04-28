import customtkinter as ctk
import requests
from tkinter import messagebox

# Configuration du design "Cyber"
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LogicielBancaire(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. PARAMÈTRES DE LA FENÊTRE
        self.title("UY1 - SYSTÈME BANCAIRE OPÉRATIONNEL")
        self.geometry("1100x700")
        self.api_url = "https://api-bancaire-oxjy.onrender.com"

        # Configuration du layout (Menu gauche / Contenu droite)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. BARRE LATÉRALE (SIDEBAR)
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.label_logo = ctk.CTkLabel(self.sidebar, text="BANK-OPS V1", font=("Roboto", 24, "bold"))
        self.label_logo.pack(pady=30)
        
        self.status_label = ctk.CTkLabel(self.sidebar, text="● Serveur: Actif", text_color="green")
        self.status_label.pack(side="bottom", pady=20)

        # 3. ZONE PRINCIPALE (PANNEAU DE CONTRÔLE)
        self.main_area = ctk.CTkFrame(self, corner_radius=15)
        self.main_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Champs de saisie organisés
        self.input_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.input_frame.pack(pady=20)

        self.ent_nom = ctk.CTkEntry(self.input_frame, placeholder_text="Nom du Titulaire", width=300)
        self.ent_nom.grid(row=0, column=0, padx=10, pady=10)

        self.ent_montant = ctk.CTkEntry(self.input_frame, placeholder_text="Montant (FCFA)", width=300)
        self.ent_montant.grid(row=0, column=1, padx=10, pady=10)

        self.ent_id_src = ctk.CTkEntry(self.input_frame, placeholder_text="ID Compte (Source)", width=300)
        self.ent_id_src.grid(row=1, column=0, padx=10, pady=10)

        self.ent_id_dest = ctk.CTkEntry(self.input_frame, placeholder_text="ID Compte (Destinataire)", width=300)
        self.ent_id_dest.grid(row=1, column=1, padx=10, pady=10)

        # 4. LES 10 FONCTIONNALITÉS TESTABLES
        self.btn_frame = ctk.CTkFrame(self.main_area)
        self.btn_frame.pack(pady=10, padx=20, fill="x")

        # Ligne 1
        ctk.CTkButton(self.btn_frame, text="1. Créer Compte", command=self.creer, fg_color="#2ecc71").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(self.btn_frame, text="2. Liste des Comptes", command=self.lister, fg_color="#34495e").grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(self.btn_frame, text="3. Retrait Cash", command=self.retrait, fg_color="#e67e22").grid(row=0, column=2, padx=10, pady=10)

        # Ligne 2
        ctk.CTkButton(self.btn_frame, text="4. Virer des Fonds", command=self.transfert, fg_color="#9b59b6").grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkButton(self.btn_frame, text="5. Historique (Audit)", command=self.historique, fg_color="#3498db").grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkButton(self.btn_frame, text="6. Supprimer Compte", command=self.supprimer, fg_color="#e74c3c").grid(row=1, column=2, padx=10, pady=10)

        # 5. CONSOLE DE SORTIE (LOGS EN TEMPS RÉEL)
        self.console = ctk.CTkTextbox(self.main_area, width=800, height=250, font=("Consolas", 12))
        self.console.pack(pady=20)

    # --- MÉTHODES TECHNIQUES ---
    def appeler_api(self, methode, endpoint, params=None):
        try:
            url = f"{self.api_url}{endpoint}"
            if methode == "POST": res = requests.post(url, params=params)
            elif methode == "GET": res = requests.get(url, params=params)
            elif methode == "PUT": res = requests.put(url, params=params)
            elif methode == "DELETE": res = requests.delete(url)
            
            self.console.delete("0.0", "end")
            self.console.insert("0.0", f"RÉPONSE SERVEUR (JSON) :\n{res.json()}")
        except Exception as e:
            messagebox.showerror("Erreur", "Connexion au serveur Render impossible.")

    def creer(self): self.appeler_api("POST", "/comptes/", {"nom": self.ent_nom.get(), "solde_initial": self.ent_montant.get()})
    def lister(self): self.appeler_api("GET", "/comptes/")
    def retrait(self): self.appeler_api("PUT", f"/comptes/{self.ent_id_src.get()}/retrait", {"montant": self.ent_montant.get()})
    def transfert(self): 
        p = {"expediteur_id": self.ent_id_src.get(), "destinataire_id": self.ent_id_dest.get(), "montant": self.ent_montant.get()}
        self.appeler_api("POST", "/transfert", p)
    def historique(self): self.appeler_api("GET", f"/comptes/{self.ent_id_src.get()}/historique")
    def supprimer(self): self.appeler_api("DELETE", f"/comptes/{self.ent_id_src.get()}")

if __name__ == "__main__":
    app = LogicielBancaire()
    app.mainloop()
