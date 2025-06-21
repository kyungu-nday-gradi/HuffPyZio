Huffman Coding – Compression et Décompression
Ce projet implémente l’algorithme de Huffman en Python pour compresser et décompresser des fichiers. L’objectif est de réduire la taille des fichiers texte en utilisant une approche de codage par fréquence de caractères, tout en facilitant leur récupération à l’identique lors de la décompression.
Introduction
L’algorithme de Huffman constitue une méthode efficace de compression sans perte. En attribuant des codes courts aux caractères fréquents et des codes plus longs aux caractères rares, l’algorithme parvient à réduire la taille globale des données. Ce projet permet non seulement de comprendre le fonctionnement de la méthode de compression, mais aussi d’en expérimenter la mise en œuvre en Python.
Fonctionnalités
•	Compression : Analyse d’un fichier texte pour construire un dictionnaire de fréquences et générer un arbre de Huffman qui permet de créer un code binaire optimisé.
•	Décompression : Restauration exacte du fichier d’origine à partir du fichier compressé.
•	Interface en ligne de commande : Exécution simple via le terminal pour compresser ou décompresser un fichier.
•	Gestion des erreurs : Vérification des arguments d’entrée et prise en charge des exceptions pour garantir une expérience utilisateur robuste.
Algorithme
	Analyse de Fréquence : Lecture du fichier pour compter l’occurrence de chaque caractère.
	Construction de l’Arbre : Création d’un arbre binaire où chaque nœud représente la somme des fréquences des caractères qui le composent.
	Génération des Codes : Parcours de l’arbre pour attribuer à chaque caractère un code binaire unique ; les codes les plus courts correspondent aux caractères les plus fréquents.
	Compression : Encodage du fichier original en remplaçant chaque caractère par son code binaire.
	Décompression : Décodage du fichier compressé en parcourant l’arbre de Huffman pour retrouver les caractères originaux.
MEMBRES 	
KYANDA MUTALE LAUREA	Frequency_analyzer.py
KYELE KIZAMBA SARAH	Compressor.py
KYOMBE KAPINI EUNICE	Decompressor.py
KYUNGU MAKENDE OTHNIEL	Main_cli.py
KYUNGU NDAY GRADI	Huffman_tree.py


# HuffPyZio
