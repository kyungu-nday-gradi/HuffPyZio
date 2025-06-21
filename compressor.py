# compressor.py

import os
import json
from module01 import calculer_frequences
from module02 import construire_arbre_huffman, generer_codes

def compresser_fichier(fichier_source: str, fichier_destination: str):
    """
    Compresse le fichier source en utilisant l'algorithme de Huffman.
    Le fichier compressé contient :
      - Un header sérialisé (table des fréquences) permettant de reconstruire l'arbre.
      - La taille du padding appliqué.
      - Les données compressées.
    Affiche également le taux de compression.
    """
    # Étape 1 : Calcul des fréquences
    frequences = calculer_frequences(fichier_source)
    
    # Étape 2 : Construction de l'arbre et génération des codes Huffman
    arbre_huffman = construire_arbre_huffman(frequences)
    codes = generer_codes(arbre_huffman)
    
    # Étape 3 : Réécriture du fichier source en remplaçant les octets par leurs codes
    chaine_bits = ""
    with open(fichier_source, "rb") as source:
        octet = source.read(1)
        while octet:
            chaine_bits += codes[octet]
            octet = source.read(1)
    
    # Gestion du padding : on complète avec des 0 pour que la longueur soit un multiple de 8
    nombre_padding = (8 - len(chaine_bits) % 8) % 8
    chaine_bits += "0" * nombre_padding

    # Transformation de la chaîne binaire en bytes
    donnees_compressees = bytearray()
    for i in range(0, len(chaine_bits), 8):
        segment = chaine_bits[i:i+8]
        donnees_compressees.append(int(segment, 2))
    
    # Sérialisation de la table de fréquences en JSON
    # Pour JSON, on convertit les clés (bytes) en leur représentation entière
    frequences_serialisables = {str(octet[0]): freq for octet, freq in frequences.items()}
    header_str = json.dumps(frequences_serialisables)
    header_bytes = header_str.encode("utf-8")
    longueur_header = len(header_bytes)

    # Écriture dans le fichier destination en mode binaire
    with open(fichier_destination, "wb") as destination:
        # Écriture de la longueur du header (4 octets, big endian)
        destination.write(longueur_header.to_bytes(4, byteorder="big"))
        # Écriture du header (la table des fréquences)
        destination.write(header_bytes)
        # Écriture du padding (1 octet)
        destination.write(nombre_padding.to_bytes(1, byteorder="big"))
        # Écriture des données compressées
        destination.write(donnees_compressees)
    
    # Calcul et affichage du taux de compression
    taille_source = os.path.getsize(fichier_source)
    taille_compressee = os.path.getsize(fichier_destination)
    taux_compression = 100 * (1 - taille_compressee / taille_source)
    print(f"Taux de compression : {taux_compression:.2f}%")
