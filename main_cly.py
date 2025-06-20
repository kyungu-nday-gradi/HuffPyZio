import argparse
import os
import heapq
import json
class Noeud:
    def __init__(self, caractere=None, frequence=0, gauche=None, droite=None):
        self.caractere = caractere
        self.frequence = frequence
        self.gauche = gauche
        self.droite = droite

    def __lt__(self, autre):
        return self.frequence < autre.frequence

def construire_arbre(frequences):
    tas = [Noeud(c, f) for c, f in frequences.items()]
    heapq.heapify(tas)

    while len(tas) > 1:
        g = heapq.heappop(tas)
        d = heapq.heappop(tas)
        nouveau = Noeud(frequence=g.frequence + d.frequence, gauche=g, droite=d)
        heapq.heappush(tas, nouveau)

    return tas[0]

def construire_codes(noeud, prefixe='', code={}):
    if noeud is None:
        return
    if noeud.caractere is not None:
        code[noeud.caractere] = prefixe
    construire_codes(noeud.gauche, prefixe + '0', code)
    construire_codes(noeud.droite, prefixe + '1', code)
    return code

def compresser(fichier_source, fichier_destination):
    try:
        with open(fichier_source, 'r', encoding='utf-8') as f:
            texte = f.read()

        # Fréquences des caractères
        freqs = {}
        for c in texte:
            freqs[c] = freqs.get(c, 0) + 1

        # Construction arbre + codes
        arbre = construire_arbre(freqs)
        codes = construire_codes(arbre)

        donnees_binaires = ''.join(codes[c] for c in texte)

        # Ajout de padding à 8 bits
        pad_len = 8 - len(donnees_binaires) % 8
        donnees_binaires += '0' * pad_len

        donnees_bytes = bytearray()
        for i in range(0, len(donnees_binaires), 8):
            octet = donnees_binaires[i:i+8]
            donnees_bytes.append(int(octet, 2))

        with open(fichier_destination, 'wb') as f:
            f.write(bytes([pad_len]))  # stocker le padding
            f.write(json.dumps(codes).encode() + b'\n')
            f.write(donnees_bytes)

        taux = 100 * (1 - len(donnees_bytes) / len(texte.encode()))
        print(f"Taux de compression : {taux:.2f}%")

    except FileNotFoundError:
        print(f"Erreur : fichier '{fichier_source}' introuvable.")
    except Exception as e:
        print(f"Erreur de compression : {e}")

def decompresser(fichier_source, fichier_destination):
    try:
        with open(fichier_source, 'rb') as f:
            pad_len = int.from_bytes(f.read(1), 'big')
            ligne = b''
            while not ligne.endswith(b'\n'):
                ligne += f.read(1)
            codes = json.loads(ligne.decode())
            donnees = f.read()

        # Inverser les codes pour décodage
        inv_codes = {v: k for k, v in codes.items()}

        bits = ''.join(f'{byte:08b}' for byte in donnees)
        bits = bits[:-pad_len]  # retirer le padding

        current = ''
        texte = ''
        for bit in bits:
            current += bit
            if current in inv_codes:
                texte += inv_codes[current]
                current = ''

        with open(fichier_destination, 'w', encoding='utf-8') as f:
            f.write(texte)

        print("Décompression terminée.")

    except FileNotFoundError:
        print(f"Erreur : fichier '{fichier_source}' introuvable.")
    except Exception as e:
        print(f"Erreur de décompression : {e}")

def main():
    parser = argparse.ArgumentParser(description="Compression Huffman CLI")
    parser.add_argument("action", choices=["compresser", "decompresser"])
    parser.add_argument("source")
    parser.add_argument("destination")
    args = parser.parse_args()

    if args.action == "compresser":
        compresser(args.source, args.destination)
    elif args.action == "decompresser":
        decompresser(args.source, args.destination)

if __name__ == "__main__":
    main()


