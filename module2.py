import heapq

def construire_un_arbre_de_huffman(frequences):
    """"construit l'arbre de huffman à partir du dict de fréquences. retourne la racine de l'arbre."""

    heap = [[freq, bits] for bits, freq in frequences.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        #extraire les deux noeuds avec les freqences les plus faibles

        gauche = heapq.heappop(heap)
        droite = heapq.heappop(heap)
        #fusionner les deux noeuds: [samme de fréquences, [gauche, droite]]
        fusionner = [gauche[0] + droite[0], [gauche, droite]]
        heapq.heappush(heap, fusionner)

    #retourne la racine de l'arbre de huffman
    return heap[0] if heap else None

def generer_les_codes_de_huffman(arbre):
    codes = {}

    def generer_les_codes_de_facon_recursive(node, code_actuel):
        if isinstance(node[1], bits):
            #feuille: associer le code au caractère
            codes[node[1]] = code_actuel
            return
        #noeud interne: parcours récursif
        gauche = node[1][0]
        droite = node[1][1]
        generer_les_codes_de_facon_recursive(gauche, code_actuel + "0")
        generer_les_codes_de_facon_recursive(droite, code_actuel + "1")
    if arbre:
        generer_les_codes_de_facon_recursive(arbre, "")
    return codes
