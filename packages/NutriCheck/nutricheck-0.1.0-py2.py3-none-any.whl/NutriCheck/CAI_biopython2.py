import argparse
from CAI import CAI

def run_CAI(fichier_in, fichier_out):
    """
    Calcule le CAI (Codon Adaptation Index) pour chaque séquence du fichier FASTA d'entrée.
    
    Cette fonction lit un fichier FASTA et calcule le CAI pour chaque séquence en la comparant 
    avec une séquence de référence construite à partir des séquences du fichier FASTA. Les résultats
    sont ensuite enregistrés dans un fichier de sortie au format souhaité.
    
    Paramètres:
    fichier_in (str): Chemin vers le fichier d'entrée contenant les séquences FASTA.
    fichier_out (str): Chemin vers le fichier de sortie où les résultats du CAI seront enregistrés.
    """
    
    with open(fichier_in, "r") as entree:
        refer = []
        index_binaire = ""
        for ligne in entree:
            if 'rps' in ligne :
                index_binaire += "1" 
            elif 'rpl' in ligne : 
                index_binaire += "1"
            else : 
                index_binaire += "0"
            if index_binaire.endswith("10") : 
                if len(ligne.strip()) % 3 == 1: 
                    refer.append(f'{ligne.strip()[:-1]}')
                elif len(ligne.strip()) % 3 == 2:
                    refer.append(f'{ligne.strip()[:-2]}')
                else: 
                    refer.append(f'{ligne.strip()}')
            elif index_binaire.endswith("11") :
                if len(ligne.strip()) % 3 == 1: 
                    refer.append(f'{ligne.strip()[:-1]}')
                elif len(ligne.strip()) % 3 == 2:
                    refer.append(f'{ligne.strip()[:-2]}')
                else: 
                    refer.append(f'{ligne.strip()}')

        with open(fichier_out, "w") as out:
            entree.seek(0)
            for ligne in entree:
                if ligne.startswith(">"):
                    gene = ""
                    gene += ligne.strip()
                    out.write(f'>{gene}\t')
                else: 
                    seq = ""
                    seq += f'{ligne.strip()}'
                    if len(seq) % 3 == 1: 
                        seq = seq[:-1]
                    elif len(seq) % 3 == 2:
                        seq = seq[:-2]
                    else: pass
                    CAI_result = CAI(seq, reference=refer)
                    out.write(f'{CAI_result}\n')


if __name__ == "__main__":
    """
    Fonction principale qui gère les arguments de ligne de commande et exécute la fonction `run_CAI`.
    
    Cette fonction utilise argparse pour accepter les arguments de ligne de commande suivants :
    - --input : Chemin vers le fichier d'entrée (fichier FASTA).
    - --output : Chemin vers le fichier de sortie où les résultats seront enregistrés.
    
    Elle appelle ensuite la fonction `run_CAI` pour effectuer le calcul du CAI et enregistrer les résultats.
    """
    
    # Configuration des arguments en ligne de commande
    parser = argparse.ArgumentParser(description="Calcule le CAI pour chaque séquence d'un fichier FASTA.")
    parser.add_argument("--input", type=str, required=True, help="Fichier d'entrée contenant les séquences FASTA.")
    parser.add_argument("--output", type=str, required=True, help="Fichier de sortie pour enregistrer les résultats du CAI.")
    
    # Analyse des arguments
    args = parser.parse_args()
    input_file = args.input
    output_file = args.output

    # Exécution de la fonction CAI
    run_CAI(input_file, output_file)

    print(f"Le calcul du CAI a été effectué et enregistré dans {output_file}.")
