# main_cli.py

import argparse
import module03
import module04
def main():
    """
    Interface en ligne de commande pour exécuter la compression ou la décompression.
    """
    parser = argparse.ArgumentParser(
        description="HuAPyZip: Outil de compression/décompression de fichiers utilisant l'algorithme de Huffman."
    )
    parser.add_argument("action", choices=["compresser", "decompresser"],
                        help="Action à effectuer : 'compresser' ou 'decompresser'")
    parser.add_argument("fichier_source", type=str, help="Chemin du fichier source")
    parser.add_argument("fichier_destination", type=str, help="Chemin du fichier de destination")
    args = parser.parse_args()

    if args.action == "compresser":
        module03.compresser_fichier(args.fichier_source, args.fichier_destination)
    elif args.action == "decompresser":
        module04.decompresser_fichier(args.fichier_source, args.fichier_destination)

if __name__ == "__main__":
    main()
