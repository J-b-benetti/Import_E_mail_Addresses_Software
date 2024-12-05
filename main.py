import csv
import chardet
import tkinter as tk
from tkinter import filedialog, ttk

def detect_encodage(chemin_fichier):
    with open(chemin_fichier, 'rb') as fichier:
        result = chardet.detect(fichier.read(10000))
    return result['encoding']

def read_csv_file(chemin_fichier):
    try:
        encodage = detect_encodage(chemin_fichier)
        with open(chemin_fichier, mode='r', encoding=encodage) as fichier:
            reader = csv.DictReader(fichier)
            emails = []
            for row in reader:
                email_principal = row.get('Adresse e-mail principale', '').strip()
                email_secondaire = row.get('Adresse e-mail secondaire', '').strip()
                prenom = row.get('Prénom', '').strip()
                nom = row.get('Nom de famille', '').strip()
                ville = row.get('Ville', '').strip()
                tel_personnel = row.get('Tél. personnel', '').strip()
                profession = row.get('Profession', '').strip()

                if email_principal or email_secondaire:
                    emails.append({
                        "Prénom": prenom or "Non spécifié",
                        "Nom": nom or "Non spécifié",
                        "E-mail principal": email_principal or "Non spécifié",
                        "E-mail secondaire": email_secondaire or "Non spécifié",
                        "Ville": ville or "Non spécifié",
                        "Tél. personnel": tel_personnel or "Non spécifié",
                        "Profession": profession or "Non spécifié",
                    })
            return emails
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return []

def display_csv_data():
    # Ouvrir une boîte de dialogue pour sélectionner le fichier
    chemin_fichier = filedialog.askopenfilename(
        title="Sélectionnez un fichier CSV",
        filetypes=[("Fichiers CSV", "*.csv")]
    )
    
    if not chemin_fichier:
        return  # Si aucun fichier n'est sélectionné

    # Lire les données du fichier CSV
    donnees = read_csv_file(chemin_fichier)
    
    # Effacer les données actuelles du tableau
    for item in tableau.get_children():
        tableau.delete(item)
    
    # Ajouter les nouvelles données au tableau
    for ligne in donnees:
        tableau.insert("", "end", values=(ligne["Prénom"], ligne["Nom"], ligne["E-mail principal"], ligne["E-mail secondaire"], ligne["Ville"], ligne["Tél. personnel"], ligne["Profession"]))

# Interface graphique
fenetre = tk.Tk()
fenetre.title("Affichage des adresses e-mail")

# Bouton pour charger un fichier CSV
bouton_charger = tk.Button(fenetre, text="Charger un fichier CSV", bg="#b36b66", height=2, relief="groove", justify="center", border=2, command=display_csv_data)
bouton_charger.pack(pady=10)

# Tableau pour afficher les données
colonnes = ("Prénom", "Nom", "E-mail principal", "E-mail secondaire", "Ville", "Tél. personnel", "Profession")
tableau = ttk.Treeview(fenetre, columns=colonnes, show="headings")

# Configurer les en-têtes
for col in colonnes:
    tableau.heading(col, text=col)
    tableau.column(col, width=150)

tableau.pack(expand=True, fill="both")

# Lancer l'interface graphique
fenetre.mainloop()