import os
import subprocess
from Bio import SeqIO
import pandas as pd
import sys
import argparse
import re

"""""
MISE EN FORME !!!!!
"""""

def main_format(fichier_fasta: str):
    """
    Fonction principale pour générer un fichier FASTA formaté contenant uniquement
    les séquences de gènes codants.

    Args:
        fichier_fasta (str): Chemin du fichier FASTA d'entrée.
    """
    # Vérifier si les fichiers existent
    if not os.path.isfile(fichier_fasta):
        print(f"Erreur : Le fichier FASTA '{fichier_fasta}' n'existe pas.")
        return

"""""
LECTURE FICHIERS !!!!!
"""""

def load_fasta(fasta_path):
    """
    Charge le fichier FASTA et retourne un dictionnaire contenant les séquences.
    """
    sequences = {}
    try:
        for record in SeqIO.parse(fasta_path, "fasta"):
            sequences[record.id] = str(record.seq)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier FASTA : {e}")
    return sequences


"""""
GENOMAD !!!!!
"""""

def run_genomad(output_fasta, output_dir="genomad_output"):
    """
    Exécute geNomad sur le fichier FASTA dans l'environnement conda "genomad" et stocke les résultats dans le répertoire de sortie spécifié.
    """
    try:
# Crée le répertoire de sortie s'il n'existe pas
        os.makedirs(output_dir, exist_ok=True)
       
        # Commande pour activer l'environnement Conda et lancer geNomad
        command = f"genomad end-to-end --cleanup {output_fasta} {output_dir} genomad_db"
        
        # Exécute la commande dans un shell
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True, executable="/bin/bash")

        # Traite les résultats
        output_lines = result.stdout.splitlines()
        print(f"GeNomad a terminé l'analyse. Les résultats sont enregistrés dans : {output_dir}")
        return output_lines
    
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de geNomad : {e.stderr}")
        return []
    

def check_comestibility_from_summary(output_dir):
    """
    Analyse les fichiers de résultats de geNomad pour déterminer si l'organisme est potentiellement comestible, en recherchant le répertoire de résumé qui se termine par 'summary'.

    Args:
        output_dir (str): Chemin du répertoire contenant les fichiers de sortie de geNomad.
    """
    # Rechercher le répertoire qui se termine par "summary"
    summary_dir = None
    for dir_name in os.listdir(output_dir):
        full_path = os.path.join(output_dir, dir_name)
        if os.path.isdir(full_path) and dir_name.endswith("summary"):
            summary_dir = full_path
            break

    # Si aucun répertoire ne termine par "summary" n'est trouvé
    if not summary_dir:
        return "Aucun répertoire se terminant par 'summary' n'a été trouvé. Impossible de déterminer la comestibilité."

    # Localiser les fichiers *plasmid_summary.tsv et *virus_summary.tsv dans le répertoire "summary"
    plasmid_file = None
    for file_name in os.listdir(summary_dir):
        if file_name.endswith("_plasmid_summary.tsv"):
            plasmid_file = os.path.join(summary_dir, file_name)


    # Vérifier si les fichiers requis existent
    if not plasmid_file:
        return "Fichiers de résumé manquants. Impossible de déterminer la comestibilité."

    # Charger les fichiers et vérifier s'ils contiennent des données (autres que les en-têtes)
    plasmid_data = pd.read_csv(plasmid_file, sep='\t')

    # Vérifier si les fichiers contiennent des données (autres que les en-têtes)
    if not plasmid_data.empty:
        print("GeNomad : L'organisme pourrait contenir des éléments génétiques mobiles (viral ou bactérien) et est donc considéré comme non comestible sans analyses complémentaires.")
#        sys.exit(1)  # Arrêter le programme avec un code de sortie non nul

    # Si les deux fichiers sont vides, l'organisme est potentiellement comestible
    if plasmid_data.empty:
        print("GeNomad : potentiellement comestible")


def main_genomad(fasta_file):
    """
    Fonction principale pour charger les fichiers,cd ..
     extraire les gènes,
    créer un fichier FASTA formaté et exécuter geNomad sur ce fichier.

    Args:
        fasta_file (str): Chemin du fichier FASTA d'entrée.
    """
    # Lancer geNomad sur le fichier FASTA formaté
    run_genomad(fasta_file)

    #Vérifier la comestibilité
    check_comestibility_from_summary("genomad_output")


"""
AMR FINDER + !!!!
"""

def run_amrfinder(fichier_fasta: str, output_file="output_amrfinder.txt"):
    """
    Exécute amrfinder dans un "environnement Conda spécifié" sur le fichier FASTA et stocke les résultats dans le fichier de sortie spécifié.
    """
    try:
        command = f"amrfinder -n {fichier_fasta} -o {output_file} --plus"
        # Exécute la commande dans un shell
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True, executable="/bin/bash")
        
        if result.returncode != 0:
            print(f"Erreur lors de l'exécution de AmrFinder : {result.stderr}")
            return []
        
        # Traite les résultats
        output_lines = result.stdout.splitlines()
        print(f"AmrFinder a terminé l'analyse. Les résultats sont enregistrés dans : {output_file}")
        return output_lines
    
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de AmrFinder : {e.stderr}")
        return []


def check_amrfinder_output(output_file):
    """
    Vérifie le fichier de sortie d'AMRFinder pour détecter la présence de gènes de virulence/toxiques.
    """
    try:
        with open(output_file, 'r') as file:
            lines = file.readlines()

# Si le fichier contient plus d'une ligne, cela signifie qu'il y a au moins un résultat
            if len(lines) > 1:
                print("AmrFinder : Gènes de virulence/toxiques détectés.")
#                sys.exit()  # Arrête l'exécution du programme

            else:
                print("AmrFinder : Aucun gène toxique détecté.")

    except FileNotFoundError:
        print(f"Erreur : le fichier {output_file} est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")


def main_amrfinder(fasta_file):
    """
    Fonction principale pour exécuter AMRFinder et vérifier les résultats.
    """
    output_file = str  # Définir le nom du fichier de sortie d'AMRFinder
    
    # Exécuter AMRFinder
    run_amrfinder(fasta_file, output_file)

    # Vérifier les résultats d'AMRFinder
    check_amrfinder_output(output_file)


"""
VIRSORTER 2!!!!
"""

def run_virsorter(fichier_fasta: str, output_dir):
    """
    Exécute virsorter dans un "environnement Conda spécifié" sur le fichier FASTA et stocke les résultats dans le fichier de sortie spécifié.
    """
    # Crée le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    try:
        command = f"virsorter run -i {fichier_fasta} -w {output_dir} --min-length 2500 -j 8"
        # Exécute la commande dans un shell
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True, executable="/bin/bash")
        
        if result.returncode != 0:
            print(f"Erreur lors de l'exécution de Virsorter : {result.stderr}")
            return []
        
        # Traite les résultats
        output_lines = result.stdout.splitlines()
        print(f"Virsoter a terminé l'analyse. Les résultats sont enregistrés dans : {output_dir}")
        return output_lines
    
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de Virsorter : {e.stderr}")
        return []


def check_virsorter_output(output_dir, verbose=True):
    """
    Analyse les fichiers de résultats de virsorter pour déterminer si l'organisme est potentiellement comestible.
    
    Args:
        output_dir (str): Chemin du répertoire contenant les fichiers de sortie de geNomad.
        verbose (bool): Si True, affiche les messages détaillés.
    """
    # Rechercher le répertoire se terminant par 'fasta'
    fasta_dir = None
    for dir_name in os.listdir(output_dir):
        full_path = os.path.join(output_dir, dir_name)
        if os.path.isdir(full_path) and dir_name.endswith("iter-o"):
            fasta_dir = full_path
            break

    # Si aucun répertoire 'fasta' n'est trouvé
    if not fasta_dir:
        return "Aucun répertoire se terminant par 'fasta' n'a été trouvé."

    # Rechercher les fichiers *.tsv dans le répertoire 'fasta'
    fichier_tsv = [f for f in os.listdir(fasta_dir) if f == "all.pdg.gff"]

    if not fichier_tsv:
        return "Aucun fichier TSV trouvé. Impossible de déterminer la comestibilité."

    # Vérifier le contenu des fichiers TSV
    comestible = True
    for fichier in fichier_tsv:
        chemin_fichier = os.path.join(fasta_dir, fichier)
        try:
            donnees = pd.read_csv(chemin_fichier, sep='\t')
            if len(donnees) > 0:  # Si le fichier contient des lignes (autres que l'en-tête)
                comestible = False
                if verbose:
                    print(f"Virsorter a terminé l'analyse. Les résultats sont enregistrés dans {output_dir}\nVirsorter : Le fichier {fichier} contient des données donc l'organisme est probablement non comestible.")
        except pd.errors.EmptyDataError:
            if verbose:
                print(f"Fichier vide ou mal formaté : {fichier}")
        except Exception:
            if verbose:
                print(f"Erreur de lecture du fichier {fichier}.")

    if comestible:
        return "Organisme considéré comme non comestible."

    return "Virsorter : L'organisme étudié est potentiellement comestible."



def main_virsorter(fasta_file, output_file):
    """
    Fonction principale pour exécuter AMRFinder et vérifier les résultats.
    """    
    # Exécuter AMRFinder
    run_virsorter(fasta_file, output_file)

    # Vérifier les résultats d'AMRFinder
    check_virsorter_output(output_file)



"""""
CHECK V !!!!!!
"""""

def run_checkv(fasta, output_dir):
    """
    Analyse les fichiers de résultats de Virsorter pour déterminer si l'organisme est potentiellement comestible.
    
    Args:
        output_dir (str): Chemin du répertoire contenant les fichiers de sortie de geNomad.
        fasta (str): chemin du fichier contenant sequence de l'organisme dont on souhaite déterminer sa comestibilité.
    """

        # Crée le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    try:
        command = f"checkv end_to_end {fasta} {output_dir} -t 8 -d checkv-db-v1.5"     #dernière version de la db à mettre à jour si elle évolue

            # Exécute la commande dans un shell
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True, executable="/bin/bash")
            
        if result.returncode != 0:
            print(f"Erreur lors de l'exécution de AmrFinder : {result.stderr}")
            return []
            
            # Traite les résultats
        output_lines = result.stdout.splitlines()
        print(f"AmrFinder a terminé l'analyse. Les résultats sont enregistrés dans : {output_dir}")
        return output_lines
    
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de Virsorter : {e.stderr}")
        return []


def check_checkV(output_dir):
    """
    Vérifie si un organisme est potentiellement comestible en analysant le fichier quality_summary.tsv.
    
    Args:
        output_dir (str): Chemin vers le répertoire contenant les fichiers de sortie de CheckV.
    
    """
    # Cherche le fichier quality_summary.tsv
    summary_file = os.path.join(output_dir, "quality_summary.tsv")

    try:
        with open(summary_file, "r") as file:
            for line in file:
                if line.startswith("contig_id"):
                    continue  # Ignore l'en-tête
                columns = line.strip().split('\t')
                contig_id = columns[0]
                warning = columns[-1].strip()

                if warning != "no viral genes detected":
                    print(f"Checkv : le contig {contig_id} est NON comestible car des gènes viraux ont été détectés.")
                else:
                    print(f"Checkv : le contig {contig_id} est POTENTIELLEMENT comestible car il n'y a aucun gène viral détecté.")
    
    except FileNotFoundError:
        print(f"Fichier {summary_file} introuvable.")
    except IndexError:
        print("Erreur : Format du fichier incorrect.")


def main_checkv(fasta_file, output_file):
    """
    Fonction principale pour exécuter AMRFinder et vérifier les résultats.
    """    
    # Exécuter AMRFinder
    run_checkv(fasta_file, output_file)

    # Vérifier les résultats d'AMRFinder
    check_checkV(output_file)