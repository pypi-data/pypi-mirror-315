import argparse
from Bio import SeqIO

def purine_percentage(fasta_file):
    """
    Calcule le pourcentage de bases purines (A et G) dans un fichier FASTA donné.

    Parameters:
        fasta_file (str): Chemin vers le fichier FASTA contenant les séquences annotées.

    Returns:
        float: Pourcentage de bases purines dans l'ensemble des séquences du fichier.
    """
    # Initialiser les compteurs pour les bases purines et le total de bases
    purine_count = 0
    total_bases = 0

    # Parcourir chaque séquence dans le fichier FASTA
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence = str(record.seq)  # Récupérer la séquence en tant que chaîne de caractères
        purine_count += sum(1 for base in sequence if base in "AG")
        total_bases += len(sequence)

    # Calculer le pourcentage de bases purines
    percentage = (purine_count / total_bases) * 100 if total_bases > 0 else 0
    return percentage

if __name__ == "__main__":
    """
    Script principal pour calculer le pourcentage de bases purines
    dans les séquences annotées d'un fichier FASTA.
    """
    # Configuration des arguments en ligne de commande
    parser = argparse.ArgumentParser(
        description="Calcule le pourcentage de bases purines (A et G) dans un fichier FASTA annoté."
    )
    parser.add_argument(
        "--input", type=str, required=True,
        help="Fichier d'entrée contenant les séquences annotées au format FASTA."
    )
    parser.add_argument(
        "--output", type=str, required=True,
        help="Fichier de sortie pour enregistrer le résultat."
    )
    
    # Analyse des arguments
    args = parser.parse_args()
    input_file = args.input
    output_file = args.output

    # Calculer le pourcentage de purines
    percentage = purine_percentage(input_file)
    
    # Écrire le résultat dans le fichier de sortie
    with open(output_file, "w") as output:
        output.write(f"Pourcentage de purines : {percentage:.2f}%\n")
    
    print(f"Le pourcentage de purines a été calculé et enregistré dans {output_file}.")