# frequency_analyzer.py

def calculer_frequences(chemin_fichier: str) -> dict:
    """
    Lit un fichier en mode binaire et calcule la fréquence de chaque octet.
    Retourne un dictionnaire {octet: fréquence}.
    """
    frequences = {}
    with open(chemin_fichier, "rb") as fichier:
        octet = fichier.read(1)
        while octet:
            frequences[octet] = frequences.get(octet, 0) + 1
            octet = fichier.read(1)
    return frequences


def construire_file_priorite(frequences: dict) -> list:
    """
    Construit une file de priorité (simulée par une liste triée) à partir du
    dictionnaire de fréquences. Chaque élément est un tuple (fréquence, octet).
    """
    file_priorite = [(freq, octet) for octet, freq in frequences.items()]
    file_priorite.sort(key=lambda element: element[0])
    return file_priorite
