import heapq
from module1 import noeud

def construire_un_arbre_de_huffman (frequences):
    """"construit l'arbre de huffman à partir du dict de fréquences. retourne la racine de l'arbre."""

    tas = [noeud(c, f) for c, f in frequences.items]

    while len(tas) > 1:
        #extraire les deux noeuds avec les freqences les plus faibles

        gauche = heapq.heappop(tas)
        droite = heapq.heappop(tas)
        #fusionner les deux noeuds: [samme de fréquences, [gauche, droite]]
        fusion = noeud = noeud[gauche[0] + droite[0], [gauche, droite]]
        heapq.heappush(tas, fusion)
    return tas[0]

    #retourne la racine de l'arbre de huffman
    return heap[0] if heap else None

def generer_les_codes_de_huffman(noeud, prefixe="", codes={}):
    if noeud is None:
           return
    #if noeud.caractere is not None:
     #   codes [noeud.caractere] = prefixe
    if noeud[1][0] is not None:
         codes[noeud[1][0]] = prefixe
         return
    generer_les_codes_de_huffman(noeud[1][1], prefixe + '0', codes)
    generer_les_codes_de_huffman(noeud[1][2], prefixe + '1', codes)
    return codes
