import sys

class NoeudHuffman:
    def __init__(self, octet=None, gauche=None, droite=None):
        self.octet = octet    # Caractère (octet) associé (défini pour les feuilles)
        self.gauche = gauche  # Sous-arbre gauche
        self.droite = droite  # Sous-arbre droit

    def est_feuille(self):
        return self.octet is not None

def sérialiser_arbre(noeud, flux_bits):
    """
    Sérialise l'arbre de Huffman en pré-ordre.
    Pour une feuille, ajoute '1' suivi de l'octet codé sur 8 bits.
    Pour un noeud interne, ajoute '0' puis sérialise ses sous-arbres gauche et droit.
    """
    if noeud is None:
        return
    if noeud.est_feuille():
        flux_bits.append('1')
        flux_bits.append('{:08b}'.format(ord(noeud.octet)))
    else:
        flux_bits.append('0')
        sérialiser_arbre(noeud.gauche, flux_bits)
        sérialiser_arbre(noeud.droite, flux_bits)

def reconstruire_arbre(flux_iter):
    """
    Reconstruit l'arbre de Huffman récursivement à partir d'un itérateur de la chaîne binaire.
    """
    try:
        bit = next(flux_iter)
    except StopIteration:
        return None

    if bit == '1':
        # Lire les 8 bits suivants qui représentent un octet (feuille)
        octet_bits = ''.join(next(flux_iter) for _ in range(8))
        return NoeudHuffman(chr(int(octet_bits, 2)))
    # Si le bit est '0', c'est un noeud interne.
    gauche = reconstruire_arbre(flux_iter)
    droite = reconstruire_arbre(flux_iter)
    return NoeudHuffman(None, gauche, droite)

def lire_entier_depuis_fichier(fichier, taille_octets):
    """
    Lit un entier codé sur 'taille_octets' octets depuis le fichier.
    """
    entier_bytes = fichier.read(taille_octets)
    return int.from_bytes(entier_bytes, 'big')

def lire_infos_sérialisées(chemin_fichier_compresse):
    """
    Lit depuis le fichier compressé :
      - La taille (en nombre de bits) de la sérialisation de l'arbre (sur 2 octets).
      - Les octets contenant la sérialisation de l'arbre, convertis en chaîne binaire.
      - Le reste du fichier qui correspond au flux compressé.
    """
    try:
        with open(chemin_fichier_compresse, 'rb') as f:
            # Lire la taille de la sérialisation de l'arbre sur 2 octets
            taille_bits_arbre = lire_entier_depuis_fichier(f, 2)
            # Calculer le nombre d'octets nécessaires pour contenir ces bits
            nb_octets_arbre = (taille_bits_arbre + 7) // 8
            arbre_bytes = f.read(nb_octets_arbre)
            # Conversion des octets en chaîne binaire complète
            bits_arbre = ''.join('{:08b}'.format(b) for b in arbre_bytes)
            # Garder uniquement les bits nécessaires
            bits_arbre = bits_arbre[:taille_bits_arbre]
            # Lire le reste du fichier (données compressées)
            donnees_comprimees = f.read()
    except IOError as e:
        print(f"Erreur lors de la lecture du fichier compressé: {e}")
        sys.exit(1)

    return bits_arbre, donnees_comprimees

def décompresser_données(donnees_comprimees, racine_arbre):
    """
    Décompresse le flux compressé en parcourant le flux de bits.
    Pour chaque bit, se déplace à gauche (bit '0') ou à droite (bit '1') dans l'arbre.
    Lorsqu'une feuille est atteinte, récupère l'octet et réinitialise le parcours.
    """
    # Conversion des données compressées en une chaîne de bits
    flux_bits = ''.join('{:08b}'.format(b) for b in donnees_comprimees)
    resultat = bytearray()
    noeud_courant = racine_arbre

    for bit in flux_bits:
        noeud_courant = noeud_courant.gauche if bit == '0' else noeud_courant.droite
        if noeud_courant.est_feuille():
            resultat.append(ord(noeud_courant.octet))
            noeud_courant = racine_arbre
    return resultat

def écrire_fichier_décompressé(chemin_sortie, donnees):
    """
    Écrit les données décompressées dans le fichier de sortie en mode binaire.
    """
    with open(chemin_sortie, 'wb') as f:
        f.write(donnees)

if __name__ == "__main__":
    chemin_fichier_compresse = "fichier_compressé.huff"
    chemin_fichier_sortie   = "fichier_décompressé.txt"

    # 1. Lire la sérialisation de l'arbre et le flux compressé depuis le fichier
    bits_arbre, donnees_comprimees = lire_infos_sérialisées(chemin_fichier_compresse)
    print("Sérialisation de l'arbre lue :", bits_arbre)

    # 2. Reconstruire l'arbre de Huffman
    arbre_reconstruit = reconstruire_arbre(iter(bits_arbre))
    print("Arbre de Huffman reconstruit avec succès.")

    # 3. Décompresser les données
    donnees_decompressees = décompresser_données(donnees_comprimees, arbre_reconstruit)
    print("Les données ont été décompressées.")

    # 4. Écrire les données décompressées dans le fichier de sortie
    écrire_fichier_décompressé(chemin_fichier_sortie, donnees_decompressees)
    print("Le fichier décompressé a été écrit :", chemin_fichier_sortie)
