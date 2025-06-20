import heapq

def build_huffman_tree(frequencies):
    """"construit l'arbre de huffman à partir du dict de fréquences. retourne la racine de l'arbre."""

    heap = [[freq, byte] for byte, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        #extraire les deux noeuds avec les freqences les plus faibles

        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        #fusionner les deux noeuds: [samme de fréquences, [gauche, droite]]
        merged = [left[0] + right[0], [left, right]]
        heapq.heappush(heap, merged)

    #retourne la racine de l'arbre de huffman
    return heap[0] if heap else None

def generate_huffman_codes(tree):
    codes = {}

    def generate_codes_rec(node, current_code):
        if isinstance(node[1], bytes):
            #feuille: associer le code au caractère
            codes[node[1]] = current_code
            return
        #noeud interne: parcours récursif
        left = node[1][0]
        right = node[1][1]
        generate_codes_rec(left, current_code + "0")
        generate_codes_rec(right, current_code + "1")
    if tree:
        generate_codes_rec(tree, "")
    return codes