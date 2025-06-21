import tkinter as tk
from tkinter import filedialog, messagebox
from module03 import compresser_fichier  # Assurez-vous d’ouvrir en mode binaire dans la fonction
from module04 import decompresser_fichier  # Idem pour la décompression

def selectionner_fichier_entree(type_fichier, operation):
    """
    Ouvre une boîte de dialogue pour sélectionner le fichier source selon le type choisi.
    Les filtres s'adaptent à la nature du fichier :
      - Textuel : fichiers .txt, .md, .csv, ...
      - Image   : fichiers .png, .jpg, .jpeg, .bmp, ...
      - Binaire : tous les fichiers
    Pour la décompression, on privilégie l'extension .hz.
    """
    if operation == "compresser":
        titre = "Sélectionnez le fichier à compresser"
        if type_fichier == "textuel":
            filtres = [("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        elif type_fichier == "image":
            filtres = [("Fichiers image", "*.png *.jpg *.jpeg *.bmp"), ("Tous les fichiers", "*.*")]
        elif type_fichier == "binaire":
            filtres = [("Fichiers binaires", "*.*")]
        else:
            filtres = [("Tous les fichiers", "*.*")]
    else:
        titre = "Sélectionnez le fichier compressé (.hz)"
        filtres = [("Fichiers compressés", "*.hz"), ("Tous les fichiers", "*.*")]
    
    chemin = filedialog.askopenfilename(title=titre, filetypes=filtres)
    return chemin

def selectionner_fichier_sortie(operation):
    """
    Ouvre une boîte de dialogue pour spécifier le chemin du fichier de sortie.
    Pour la compression, on suggère l'extension .hz.
    """
    if operation == "compresser":
        titre = "Enregistrez le fichier compressé"
        ext_defaut = ".hz"
    else:
        titre = "Enregistrez le fichier décompressé"
        ext_defaut = ""
    
    chemin = filedialog.asksaveasfilename(title=titre, defaultextension=ext_defaut)
    return chemin

def compresser_action(type_fichier):
    # Sélection du fichier source en fonction du type choisi par l'utilisateur
    fichier_source = selectionner_fichier_entree(type_fichier, "compresser")
    if not fichier_source:
        messagebox.showwarning("Avertissement", "Aucun fichier sélectionné pour la compression.")
        return
    # Sélection du fichier destination
    fichier_destination = selectionner_fichier_sortie("compresser")
    if not fichier_destination:
        messagebox.showwarning("Avertissement", "Aucun fichier de destination sélectionné.")
        return
    try:
        # L'appel à la fonction de compression doit gérer la lecture ("rb") et l'écriture ("wb")
        compresser_fichier(fichier_source, fichier_destination)
        messagebox.showinfo("Succès", f"Compression réussie !\nFichier compressé (mode binaire): {fichier_destination}")
    except Exception as erreur:
        messagebox.showerror("Erreur", f"Erreur lors de la compression : {erreur}")

def decompresser_action():
    # Pour la décompression, on privilégie l'extension .hz
    fichier_source = filedialog.askopenfilename(
        title="Sélectionnez le fichier compressé (.hz)",
        filetypes=[("Fichiers compressés", "*.hz"), ("Tous les fichiers", "*.*")]
    )
    if not fichier_source:
        messagebox.showwarning("Avertissement", "Aucun fichier sélectionné pour la décompression.")
        return
    fichier_destination = selectionner_fichier_sortie("decompresser")
    if not fichier_destination:
        messagebox.showwarning("Avertissement", "Aucun fichier de destination sélectionné.")
        return
    try:
        decompresser_fichier(fichier_source, fichier_destination)
        messagebox.showinfo("Succès", f"Décompression réussie !\nFichier décompressé: {fichier_destination}")
    except Exception as erreur:
        messagebox.showerror("Erreur", f"Erreur lors de la décompression : {erreur}")

def lancer_interface_graphique():
    # Création de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("HuAPyZip - Compression/Décompression")
    fenetre.geometry("500x300")

    # Titre de la fenêtre
    label_titre = tk.Label(
        fenetre, 
        text="HuAPyZip - Outil de compression/décompression Huffman", 
        font=("Helvetica", 14)
    )
    label_titre.pack(pady=10)

    # Frame pour choisir l'action (compression ou décompression)
    frame_action = tk.Frame(fenetre)
    frame_action.pack(pady=10)

    bouton_compresser = tk.Button(
        frame_action, text="Compresser", width=15,
        command=lambda: compresser_action(var_type.get())
    )
    bouton_compresser.grid(row=0, column=0, padx=10)

    bouton_decompresser = tk.Button(
        frame_action, text="Décompresser", width=15,
        command=decompresser_action
    )
    bouton_decompresser.grid(row=0, column=1, padx=10)

    # Frame pour le choix du type de fichier (utilisé uniquement pour la compression)
    frame_type = tk.LabelFrame(fenetre, text="Type de fichier (pour la compression)", padx=10, pady=10)
    frame_type.pack(pady=20)

    global var_type
    var_type = tk.StringVar(value="textuel")
    tk.Radiobutton(frame_type, text="Textuel", variable=var_type, value="textuel").pack(anchor="w")
    tk.Radiobutton(frame_type, text="Image", variable=var_type, value="image").pack(anchor="w")
    tk.Radiobutton(frame_type, text="Binaire", variable=var_type, value="binaire").pack(anchor="w")

    fenetre.mainloop()

if __name__ == "__main__":
    lancer_interface_graphique()
