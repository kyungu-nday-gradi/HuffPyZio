# huffman_tree.py

class Noeud:
    def __init__(self, frequence, symbole=None, gauche=None, droite=None):
        """
        Un nœud de l'arbre de Huffman.
        - frequence : fréquence cumulée (int)
        - symbole    : l'octet représenté (bytes) (None pour un nœud interne)
        - gauche     : sous-arbre gauche (Noeud)
        - droite     : sous-arbre droit (Noeud)
        """
        self.frequence = frequence
        self.symbole = symbole
        self.gauche = gauche
        self.droite = droite

    def __lt__(self, autre):
        return self.frequence < autre.frequence


def construire_arbre_huffman(frequences: dict) -> Noeud:
    """
    Construit l'arbre de Huffman à partir d'un dictionnaire de fréquences.
    Retourne la racine de l'arbre.
    """
    # Création d'une liste de nœuds pour chaque symbole
    noeuds = [Noeud(freq, symbole) for symbole, freq in frequences.items()]
    while len(noeuds) > 1:
        # Trier les nœuds par ordre croissant de fréquence
        noeuds.sort(key=lambda n: n.frequence)
        # Extraire les deux nœuds ayant la plus faible fréquence
        noeud_gauche = noeuds.pop(0)
        noeud_droite = noeuds.pop(0)
        # Fusionner ces deux nœuds dans un nouveau nœud interne
        noeud_fusion = Noeud(noeud_gauche.frequence + noeud_droite.frequence,
                              symbole=None,
                              gauche=noeud_gauche,
                              droite=noeud_droite)
        noeuds.append(noeud_fusion)
    return noeuds[0] if noeuds else None


def generer_codes(noeud: Noeud, prefixe: str = "", codes: dict = None) -> dict:
    """
    Parcourt récursivement l'arbre pour générer le code binaire de chaque octet.
    Retourne un dictionnaire {octet: code binaire (str)}.
    """
    if codes is None:
        codes = {}
    if noeud is None:
        return codes
    # Cas d'une feuille : associer le code
    if noeud.symbole is not None:
        codes[noeud.symbole] = prefixe or "0"  # Si l'arbre ne contient qu'un nœud
    else:
        generer_codes(noeud.gauche, prefixe + "0", codes)
        generer_codes(noeud.droite, prefixe + "1", codes)
    return codes
