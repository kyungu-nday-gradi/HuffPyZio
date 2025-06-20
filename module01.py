"""
 cet outil lit un fichier en mode binaire , calcule la frequence de chaque
octet, et construit une file de priorite sous forme de liste triee de noeuds pour 
l'arbre de huffman 
"""
class noeud : 
    """
    represente un noeud dans l'arbre de huffman .
    """
    def init(self,caractere=None,frequence=0):
        self.caractere=caractere
        self.frequence=frequence
        self.gauche=None
        self.droite=None
    def lt(self,autre):
        # permet de comparer deux noeuds selon leur frequence
        return self.frequence< autre.frequence 
    def repr(self):
        return f"noeud(caractere={self.caractere},frequence={self.frequence})"
def analyser_frequence(chemin_fichire):
    """
    lit le fichier donne en mode binaire et calcule la frequences  de chaque actet.
    """
    frequences={}
    try:
        with open(chemin_fichire,'rb') as fichier:
            donnees=fichier.read()
            for octet in donnees : 
                frequences[octet]=frequences.get(octet,0)+1
    except Exception as erreur : 
        print(f"erreur lors de la lecture du fichier:{erreur}")
    return frequences
def creer_file_priorite(dictionnaire_freaiences):
    """
    construit une file de priorite a partir du dictionnaire de frequences .
    chaque entree est transformee en une instance de noeud , et la liste est triee par oedre croissant de frequences 
    """
    file_priorite=[]
    for octet , frequence in dictionnaire_freaiences.items():
        noeud=noeud(caractere=octet,frequence=frequence)
        file_priorite.append(noeud)
        #tri de la liste pour simuler une file de priorite (min-heap)
        file_priorite.sort(key=lambda noeud : noeud.frequence)
        return file_priorite
if __name__=='__main__':
    import sys
    if len(sys.argv)<2:
        print("utilisation:python frequency_analyzer.py<chemin_dufichier>")
        sys.exit(1)
    chemin=sys.argv[1]
    print(f"analyse du fichier : {chemin}")
    # analyse des frequences dans le fichier 
    frequences=analyser_frequence(chemin)
    if not frequences:
        print("aucune donnee analysee. verifiez le chemin  ou le contenue du fichier.")
        sys.exit(1)
    print("\nfrequences des octeta (en hexadecimal):")
    for octet ,nombre in sorted(frequences.items(),key=lambda item : item[1]):
        print(f"octet (hex:{octet:02x}) : {nombre} occurrence(s)")
    # construction de la file de priorite
    file_priorite =creer_file_priorite(frequences)
    print("\nfile de priorite des noeuds (triee par frequences):")
    for noeud in file_priorite:
        print(f"noeud:octet(hex:{noeud.caractere:02x}) - frequence : {noeud.frequence}")

        
