#!/usr/bin/env python3
import sys

def assembler_chaine_de_bits(fichier_source, codes_huffman):
    """
    Lit le fichier source en mode binaire, remplace chaque octet par son code Huffman,
    et assemble une chaîne de bits (une succession de '0' et de '1').
    """
    chaine_bits = ""
    with open(fichier_source, "rb") as fichier:
        octet = fichier.read(1)
        while octet:
            if octet in codes_huffman:
                code = codes_huffman[octet]
            else:
                # Vous pouvez choisir de gérer l'absence de code différemment (ex. lever une erreur)
                raise ValueError(f"Aucun code Huffman pour l'octet {octet}")
            chaine_bits += code
            octet = fichier.read(1)
    return chaine_bits

def ajouter_padding(chaine_bits):
    """
    Ajoute le padding nécessaire à la chaîne de bits pour que sa longueur soit un multiple de 8.
    Le premier octet de la chaîne finale contient l'information sur la quantité de padding ajoutée.
    """
    # Calcul du nombre de bits à ajouter
    longueur_padding = (8 - len(chaine_bits) % 8) if (len(chaine_bits) % 8) != 0 else 0
    # Stocke cette information sur 8 bits
    info_padding = "{0:08b}".format(longueur_padding)
    # Ajoute le padding à la chaîne principale
    chaine_bits_paddee = chaine_bits + "0" * longueur_padding
    # On préfixe l'information de padding
    return info_padding + chaine_bits_paddee

def chaine_bits_vers_octets(chaine_bits_paddee):
    """
    Convertit la chaîne de bits en une séquence d'octets.
    Chaque groupe de 8 bits est transformé en entier, puis ajouté à une séquence d'octets.
    """
    tableau_octets = bytearray()
    for i in range(0, len(chaine_bits_paddee), 8):
        octet_str = chaine_bits_paddee[i:i+8]
        tableau_octets.append(int(octet_str, 2))
    return bytes(tableau_octets)

def compresser_fichier(fichier_source, fichier_sortie, codes_huffman):
    """
    Module principal de compression :
    - Assemble les codes Huffman en une chaîne de bits.
    - Ajoute le padding si nécessaire.
    - Convertit la chaîne en données binaires et l'écrit dans le fichier de sortie.
    """
    # Assemblage des codes Huffman
    chaine_bits = assembler_chaine_de_bits(fichier_source, codes_huffman)
    
    # Gestion du padding (et ajout de l'info sur le padding)
    chaine_bits_paddee = ajouter_padding(chaine_bits)
    
    # Conversion en données binaires (octets)
    donnees_compressees = chaine_bits_vers_octets(chaine_bits_paddee)
    
    # Écriture dans le fichier de sortie
    with open(fichier_sortie, "wb") as fichier_sortie_obj:
        fichier_sortie_obj.write(donnees_compressees)
    
    print(f"Compression terminée. Fichier compressé : {fichier_sortie}")

if __name__ == "__main__":
    # Exemple de dictionnaire de codes Huffman pour tester (à adapter selon votre algorithme)
    codes_huffman = {
        b'A': '101',
        b'B': '100',
        b'C': '0',
        b'D': '111',
        b'E': '110'
        # Ajoutez ou modifiez les codes pour chaque octet présent dans votre fichier source
    }
    
    if len(sys.argv) != 3:
        print("Usage : python compressor.py fichier_source fichier_sortie")
        sys.exit(1)
        
    fichier_source = sys.argv[1]
    fichier_sortie = sys.argv[2]
    
    compresser_fichier(fichier_source, fichier_sortie, codes_huffman)
