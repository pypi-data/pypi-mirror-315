import tools_toxico
import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Pipeline d'analyse génomique")
    parser.add_argument("fasta_file", type=str, help="Chemin vers le fichier FASTA")
    parser.add_argument("output_dir", type=str, help="chemin vers le répertoire de sortie")
    parser.add_argument("--nom_logiciel", "-l",type=str, nargs='*', help="nom du logiciel de recherche de toxicité (genomad / amrfinder / vs2)")
    args = parser.parse_args()

# nargs signifie que l'argument peut accepter zéro ou plusieurs valeurs. Si l'option --nom_logiciel est omise, nargs='*' permet que l'argument soit simplement absent sans provoquer d'erreur.

    if not os.path.isfile(args.fasta_file):
        print(f"Erreur : Le fichier FASTA '{args.fasta_file}' n'existe pas.")
        sys.exit(1)

    logiciels = args.nom_logiciel if args.nom_logiciel else ["genomad", "amrfinder", "vs2", "checkv"]

    for logiciel in logiciels:
        if logiciel == "genomad":
            tools_toxico.main_genomad(args.fasta_file,args.output_dir)
        if logiciel == "amrfinder":
            tools_toxico.main_amrfinder(args.fasta_file)
        if logiciel == "vs2":
            tools_toxico.main_virsorter(args.fasta_file,args.output_dir)
        if logiciel == "checkv":
            tools_toxico.main_checkv(args.fasta_file,args.output_dir)

if __name__ == "__main__":
    main()