# decompressor.py

import json
from module02 import construire_arbre_huffman

def decompresser_fichier(fichier_entree: str, fichier_sortie: str):
    """
    Décompresse un fichier compressé en reconstruisant l'arbre de Huffman à partir
    du header, puis en décodant le flux binaire pour reconstituer le fichier original.
    """
    with open(fichier_entree, "rb") as entree:
        # Lecture de la longueur du header (4 octets)
        longueur_header_bytes = entree.read(4)
        longueur_header = int.from_bytes(longueur_header_bytes, byteorder="big")
        
        # Lecture et désérialisation du header (table des fréquences)
        header_bytes = entree.read(longueur_header)
        frequences_serialisables = json.loads(header_bytes.decode("utf-8"))
        frequences = {bytes([int(cle)]): valeur for cle, valeur in frequences_serialisables.items()}

        # Lecture du padding (1 octet)
        nombre_padding = int.from_bytes(entree.read(1), byteorder="big")
        # Lecture des données compressées
        donnees_compressees = entree.read()

    # Reconstruction de l'arbre de Huffman à partir des fréquences
    arbre_huffman = construire_arbre_huffman(frequences)

    # Conversion des octets compressés en chaîne binaire
    chaine_bits = ""
    for octet in donnees_compressees:
        bits = bin(octet)[2:].rjust(8, "0")
        chaine_bits += bits

    # Suppression du padding
    if nombre_padding > 0:
        chaine_bits = chaine_bits[:-nombre_padding]

    # Décompression : parcourir l'arbre pour retrouver les octets originaux
    noeud_courant = arbre_huffman
    donnees_decompressees = bytearray()
    for bit in chaine_bits:
        if bit == "0":
            noeud_courant = noeud_courant.gauche
        else:
            noeud_courant = noeud_courant.droite
        
        # Si une feuille est atteinte, on récupère le symbole
        if noeud_courant.gauche is None and noeud_courant.droite is None:
            donnees_decompressees += noeud_courant.symbole
            noeud_courant = arbre_huffman

    # Écriture des données décompressées dans le fichier de sortie
    with open(fichier_sortie, "wb") as sortie:
        sortie.write(donnees_decompressees)
    
    print("Décompression terminée.")
