# Package CAI
# https://github.com/Benjamin-Lee/CodonAdaptationIndex/
# https://joss.theoj.org/papers/10.21105/joss.00905

from classe.classe_gene import Gene
from CAI import CAI
class Organisme : 
    def __init__(self,txt_cds):
        with open(txt_cds,"r") as file : 
            self.contenu = file.read()
        self.liste_texte_gene = self.contenu.split(">")
        self.liste_texte_gene.remove("")
        self.liste_gene = []
        self.liste_gene_ribo = []
        self.taux_gc = None
        self.genome_nuc = ""
        self.genome_ribo_nuc = ""
        self.proteome = ""
        self.proteome_ribo = ""
        self.taille_genome_nuc = None
        self.taille_total_ribo_nuc = None
        self.taille_proteome = None
        self.taille_total_ribo_prot = None
        self.teneur_aa_ribos = {}
        self.teneur_aa_uniforme = {}
        self.teneur_aa_ponderee_normalisee = {}
        self._build_organisme()
        self._get_genome_and_ribo()
        self._get_CAI_and_CAI_normalize()
        self._get_taux_gc()
        self._get_uni_teneur_aa()
        self._get_uni_ribo_result()
        self._get_teneur_aa_ponderee_normalisee()

    def _build_organisme(self) : 
        for gene in self.liste_texte_gene : 
            objet_Gene = Gene(str(gene))
            if objet_Gene.is_ribosomal == "Oui" : 
                self.liste_gene_ribo.append(objet_Gene)
                self.liste_gene.append(objet_Gene)
            else : 
                self.liste_gene.append(objet_Gene)

    def _get_genome_and_ribo(self) : 
        for Objet_gene in self.liste_gene : 
            if Objet_gene.is_ribosomal == "Oui" :
                self.genome_ribo_nuc += Objet_gene.sequence_nuc
                self.proteome_ribo += str(Objet_gene.sequence_prot)
                self.genome_nuc += Objet_gene.sequence_nuc
                self.proteome += str(Objet_gene.sequence_prot)
            else : 
                self.genome_nuc += Objet_gene.sequence_nuc
                self.proteome += str(Objet_gene.sequence_prot)
        self.taille_genome_nuc = len(self.genome_nuc)
        self.taille_total_ribo_nuc = len(self.genome_ribo_nuc)
        self.taille_proteome = len(str(self.proteome))
        self.taille_total_ribo_prot = len(str(self.proteome_ribo))


    def _get_taux_gc(self) : 
        purine = 0
        for char in self.genome_nuc : 
            if char == "C" or char == "G" : 
                purine += 1
        self.taux_gc = purine / self.taille_genome_nuc
        
    def __repr__(self):
        repr=""
        for gene in self.liste_gene:
            repr+=gene.__repr__()
        return repr

    def __iter__(self) : 
        return iter(self.liste_gene)
    
    def formatage(self,out_file) : 
        with open(out_file,"w") as out : 
            for gene in self.liste_gene : 
                if gene.nom != "Inconnu" : 
                    out.write(f'>{gene.nom}\n')
                    out.write(f'{gene.sequence_nuc}\n')

    def _get_CAI_and_CAI_normalize(self) : 
        refer = []
        # création de la table de référence
        for gene in self.liste_gene : 
            if gene.is_ribosomal == "Oui" :
                seq=gene.sequence_nuc.replace('N', '')
                if len(seq) % 3 == 1: 
                    seq = seq[:-1]
                elif len(seq) % 3 == 2:
                    seq = seq[:-2]
                if len(seq)!=0:   
                    refer.append(seq)

        # calcul du CAI
        for gene in self.liste_gene :
            seq=gene.sequence_nuc.replace('N', '')
            if len(seq) % 3 == 1: 
                seq = seq[:-1]
            elif len(seq) % 3 == 2:
                seq = seq[:-2]
            if len(seq)!=0:
                gene.CAI = CAI(seq,reference=refer)

        # normalisation CAI
        CAI_total=0
        for gene in self.liste_gene :
            if gene.CAI!=None:
                CAI_total += gene.CAI
        for gene in self.liste_gene :
            if gene.CAI!=None and CAI_total!=0: 
                gene.CAI_normalize = gene.CAI / CAI_total

    #def get_proportion_AA(self) : 
        #for gene in self.liste_gene :
            #for AA in gene.dico_AA : 
                #gene.proportion_AA[AA] = gene.dico_AA[AA]/gene.taille_sequence_prot

    def _get_uni_teneur_aa(self) :
        """
        calcule et stocke les occurences des acides aminés pour un taux d'expression uniforme de tous les gènes
        """
        dico_total_AA={}
        self.teneur_aa_uniforme={}
        for gene in self.liste_gene : 
            for AA,compte in gene.dico_AA.items() :
                if AA not in dico_total_AA : 
                    dico_total_AA[AA] = compte
                else : 
                    dico_total_AA[AA] += compte
        for AA in dico_total_AA: 
            self.teneur_aa_uniforme[AA] = dico_total_AA[AA]/self.taille_proteome

    
    def _get_uni_ribo_result(self) : 
        """
        calcule et stocke les occurences des acides aminés pour un taux d'expression uniforme des gènes ribosomiques exclusivement
        """
        dico_total_AA_ribo={}
        self.teneur_aa_ribos={}
        for gene in self.liste_gene_ribo : 
            for AA,compte in gene.dico_AA.items() :
                if AA not in dico_total_AA_ribo : 
                    dico_total_AA_ribo[AA] = compte
                else : 
                    dico_total_AA_ribo[AA] += compte
        for AA in dico_total_AA_ribo : 
            self.teneur_aa_ribos[AA] = dico_total_AA_ribo[AA]/self.taille_total_ribo_prot
    
    def _get_teneur_aa_ponderee_normalisee(self) :
        dico_aa_CAI={}
        total_compte_aa_normalise=0
        self.teneur_aa_ponderee_normalisee={}

        for gene in self.liste_gene : 
            for AA,compte_aa in gene.dico_AA.items() :
                if AA not in dico_aa_CAI :
                    dico_aa_CAI[AA] = compte_aa * gene.CAI_normalize
                else :
                    dico_aa_CAI[AA] += compte_aa * gene.CAI_normalize

        for compte_pondere_aa in dico_aa_CAI.values() : 
            total_compte_aa_normalise += compte_pondere_aa

        for AA in dico_aa_CAI : 
            self.teneur_aa_ponderee_normalisee[AA] = dico_aa_CAI[AA] / total_compte_aa_normalise

    def compare_teneur_normalisee_avec_ideale(self, output_file):
        """
        Compare les teneurs normalisées pondérées d'acides aminés avec les valeurs idéales
        et écrit les résultats dans un fichier.
        
        :param ideal_aa_content: Dictionnaire des valeurs idéales en mg/g
        :param masse_molaire: Dictionnaire des masses molaires des acides aminés (en g/mol)
        :param output_file: Chemin du fichier de sortie pour la comparaison
        """
        # Vérification ou calcul des teneurs normalisées pondérées
        if not hasattr(self, "teneur_aa_ponderee_normalisee") or not self.teneur_aa_ponderee_normalisee:
            self._get_teneur_aa_ponderee_normalisee()
        
        # Vérification de l'existence des données
        if not self.teneur_aa_ponderee_normalisee:
            raise ValueError("Les teneurs normalisées pondérées des acides aminés ne sont pas disponibles.")
        
        # Calcul du total_proteome
        total_proteome = sum(
            self.teneur_aa_ponderee_normalisee.get(aa, 0) * masse_molaire.get(aa, 0)
            for aa in self.teneur_aa_ponderee_normalisee
        )
        if total_proteome == 0:
            raise ValueError("Le total_proteome calculé est nul, vérifiez les données d'entrée.")

        with open(output_file, "w") as output:
            output.write("Comparaison des teneurs pondérées normalisées avec les valeurs idéales :\n")

            for aa, ideal_value in ideal_aa_content.items():
                # Cas spécial pour F+Y
                if aa == "F+Y":
                    teneur_aa = (
                        (
                            self.teneur_aa_ponderee_normalisee.get('F', 0) * masse_molaire.get('F', 0) +
                            self.teneur_aa_ponderee_normalisee.get('Y', 0) * masse_molaire.get('Y', 0)
                        ) / total_proteome
                    ) * 1000  # Conversion en mg/g
                else:
                    teneur_aa = (
                        self.teneur_aa_ponderee_normalisee.get(aa, 0) * masse_molaire.get(aa, 0) / total_proteome
                    ) * 1000  # Conversion en mg/g
                
                # Comparaison avec la valeur idéale
                if teneur_aa > 0:
                    percentage_of_ideal = (teneur_aa / ideal_value) * 100
                    output.write(f"{aa}: {teneur_aa:.2f} mg/g ({percentage_of_ideal:.2f}% de la teneur idéale)\n")
                else:
                    output.write(f"{aa}: Aucune valeur calculée ou absente pour comparaison\n")

    
    def fetch_gene_expr_reelle(self, exp_results_path):
        """
        exp_results -> gene_name  |  fraction molaire
        extrait la fraction molaire et la stocke dans un nouveau champ gene.expr_reelle
        """
        with open (exp_results_path, 'r') as f:
            lines = f.readlines()
            for l in lines:
                if l!='' and not l.startswith('#') and not l.startswith('>'):
                    #print("l=>", l)
                    
                    tabs= l.strip().split('\t')
                    #print("tabs=>", tabs)
                    gene_exp=tabs[0]
                    expr=tabs[1]

                for gene in self.liste_gene:
                    if gene_exp==gene.nom:
                        gene.expr_reelle=float(expr)

    def get_teneur_aa_reelle (self, exp_results_path):
        """
        extrait les taux d'expression expérimentaux puis  
        comme dans _get_teneur_aa_ponderee_normalisee calcule la teneur réelle en aa
        en utilisant le taux d'expression expérimental à la place du CAI
        """
        # extrait les taux d'expression expérimentaux
        self.fetch_gene_expr_reelle(exp_results_path)

        # calcule la teneur réelle en aa
        dico_aa_tx_expr={}
        total_compte_aa_reel=0
        teneur_aa_relle={}
        for gene in self.liste_gene : 
            for AA,compte_aa in gene.dico_AA.items() :
                if AA not in dico_aa_tx_expr :
                    dico_aa_tx_expr[AA] = compte_aa * gene.expr_reelle
                else :
                    dico_aa_tx_expr[AA] += compte_aa * gene.expr_reelle

        for AA,compte_pondere_aa in dico_aa_tx_expr.items() : 
            total_compte_aa_reel += compte_pondere_aa


        for AA in dico_aa_tx_expr : 
            teneur_aa_relle[AA] = dico_aa_tx_expr[AA] / total_compte_aa_reel

        return teneur_aa_relle
    
    def view_results_aa_predic(self, result_file_output):
        """
        teneur_aa_ponderee_normalisee_modifée=transform(self.teneur_aa_ponderee_normalisee)
        # self.teneur_aa_ponderee_normalisee doit être modifiée pour s'adapter à l'aliment de référence
        results_table = [ 
            teneur_aa_ponderee_normalisee_modifée 
            dico_teneur_aa_aliment_reference
        ]

        results_column = [
            'CAI',  # Teneur pondérée normalisée (indice CAI)
            'idéale'  # Teneur pour l'aliment de référence
        ]

        merged_results = merge_results(results_column, results_table)
        matrix = create_matrix_from_results(results_column, merged_results)
        write_matrix(matrix, result_file_output)
        
        """
        pass

    def view_results_aa_exp(self, exp_results_path, result_file_output):
        """
        Fonction pour traiter les résultats d'expérimentations sur les teneurs en acides aminés
        et générer un fichier de sortie sous forme de matrice avec les résultats fusionnés.

        Paramètres :
        - exp_results_path (str) : Chemin vers le fichier contenant les résultats expérimentaux des teneurs en acides aminés réelles.
        - result_file_output (str) : Chemin vers le fichier de sortie où la matrice des résultats fusionnés sera enregistrée.
        """
        
        # Récupère la teneur en acides aminés réelle à partir du fichier d'expérimentations
        teneur_aa_relle = self.get_teneur_aa_reelle(exp_results_path)

        # Crée une liste `results_table` contenant les différents résultats (ici quatre tableaux de teneur en acides aminés)
        # - self.teneur_aa_uniforme : teneur uniforme
        # - self.teneur_aa_ribos : teneur ribosomique
        # - self.teneur_aa_ponderee_normalisee : teneur pondérée normalisée
        # - teneur_aa_relle : teneur réelle récupérée depuis le fichier d'expérimentation
        results_table = [
            self.teneur_aa_uniforme, 
            self.teneur_aa_ribos, 
            self.teneur_aa_ponderee_normalisee, 
            teneur_aa_relle
        ]

        print("self.teneur_aa_uniforme=>", self.teneur_aa_uniforme)

        # Crée une liste `results_column` contenant les noms correspondant aux résultats dans `results_table`
        # Chaque nom ici sera associé à un des tableaux de la liste `results_table`
        results_column = [
            'uniforme',  # Teneur uniforme
            'ribosomique',  # Teneur ribosomique
            'CAI',  # Teneur pondérée normalisée (indice CAI)
            'experiment'  # Teneur réelle des acides aminés expérimentaux
        ]

        # Fusionne les résultats dans un dictionnaire, en associant chaque nom de résultat (de `results_column`)
        # aux données correspondantes (de `results_table`).
        # La fonction `merge_results` va créer un dictionnaire où chaque acide aminé aura les données pour chaque type de résultat.
        merged_results = merge_results(results_column, results_table)

        # Crée une matrice à partir du dictionnaire `merged_results` en suivant les colonnes spécifiées dans `results_column`.
        # La fonction `create_matrix_from_results` va transformer le dictionnaire fusionné en une matrice (liste de listes).
        # Chaque ligne correspond à un acide aminé, et les colonnes aux résultats pour cet acide aminé.
        matrix = create_matrix_from_results(results_column, merged_results)

        # Écrit la matrice obtenue dans un fichier de sortie, en séparant les colonnes par des tabulations.
        # La fonction `write_matrix` écrit chaque ligne de la matrice dans un fichier texte, avec des tabulations entre les valeurs.
        write_matrix(matrix, result_file_output)


def merge_results(results_column, results_table):
    """
    Crée un dictionnaire à partir de deux listes : 
    `results_column` contient les noms des résultats (clés),
    `results_table` contient les dictionnaires de données (valeurs).
    Les dictionnaires contenus dans results_table auront la forme ci-dessous:
    {'M': 0.2, 'R': 0.3, 'S': 0.2, 'N': 0.1, '*': 0.2}

    Dictionnaire final qui regroupera les résultats fusionnés.
    Le dictionnaire final contient un résultat par acide aminé, exemple:
    'M': {'uniforme': 0.2, 'ribosomique': 0.2, 'CAI': 0.2, 'experiment': 0.2}
    """ 
    results = {}
    # Vérifie que les deux listes ont la même longueur, sinon lève une erreur.
    if len(results_column) != len(results_table):
        raise ValueError("Les listes results_column et results_table doivent avoir la même longueur.")

    # Associe chaque élément de `results_column` à un élément correspondant de `results_table` via zip.
    for key, value in zip(results_column, results_table):
        results[key] = value

    # Nouveau dictionnaire pour fusionner les données par acide aminé.
    result_merged = {}

    # Parcourt chaque résultat dans le dictionnaire `results`.
    for result_name in results:
        # Récupère le dictionnaire associé au nom du résultat (ex. uniforme, ribosomique, etc.).
        result_table = results[result_name]

        # Parcourt chaque acide aminé et ses données associées.
        for aa in result_table:
            if aa not in result_merged:
                # Si l'acide aminé n'est pas encore dans `result_merged`,
                # on initialise un dictionnaire avec le résultat actuel.
                result_merged[aa] = {result_name: result_table[aa]}
            else:
                # Si l'acide aminé est déjà présent, on récupère son dictionnaire...
                aa_dico = result_merged[aa]
                # puis on le complète avec le nouveau résultat
                aa_dico[result_name] = result_table[aa]

    return result_merged


def create_matrix_from_results(columns, matrix_to_write):
    """
    Fonction pour créer une matrice de résultats à partir d'un dictionnaire d'acides aminés et de leurs teneurs.
    
    Paramètres :
    - columns (list) : Liste contenant les noms des colonnes (types de résultats, ex: 'uniforme', 'ribosomique', etc.)
    - matrix_to_write (dict) : Dictionnaire où les clés sont des acides aminés (par exemple, 'A', 'G', etc.) 
                              et les valeurs sont des dictionnaires contenant les résultats associés à ces acides aminés. 
    
    Retourne :
    - (list) : Une matrice sous forme de liste de listes, où chaque ligne contient un acide aminé 
              suivi de ses résultats pour chaque type de données (les colonnes).
    """

    # Initialisation de la matrice comme une liste vide
    matrix = []

    # Création du header, qui contient une première cellule vide suivie des noms des colonnes
    # La première cellule vide est incluse pour représenter la colonne d'acides aminés
    header = [""] + columns

    # Ajoute le header à la matrice
    matrix.append(header)

    # Parcourt chaque acide aminé dans le dictionnaire 'matrix_to_write'
    for aa in matrix_to_write:
        # Crée une nouvelle ligne pour chaque acide aminé
        line_aa = [aa]
        
        # Récupère le dictionnaire des résultats pour cet acide aminé
        aa_dico = matrix_to_write[aa]

        # Parcourt chaque nom de résultat dans 'columns' et récupère la valeur correspondante
        # Si le résultat existe pour cet acide aminé, on l'ajoute à la ligne
        # Sinon, on ajoute un 0 si le résultat n'est pas présent
        for result_name in columns:
            if result_name in aa_dico:
                result_aa = aa_dico[result_name]
                line_aa.append(str(result_aa))  # Ajoute le résultat sous forme de chaîne de caractères
            else:
                line_aa.append(str(0))  # Si le résultat est manquant, ajoute 0

        # Ajoute la ligne complète à la matrice
        matrix.append(line_aa)

    # Retourne la matrice complète
    return matrix


def write_matrix(matrix, result_file_output):
    # Ouvre le fichier en mode écriture.
    with open(result_file_output, 'w') as f:
        # Parcourt chaque ligne de la matrice.
        for result in matrix:
            # Joint les éléments de la ligne avec des tabulations et ajoute un saut de ligne à la fin.
            line = '\t'.join(result) + '\n'

            # Écrit la ligne dans le fichier.
            f.write(line)
                
# Valeurs idéales en mg/g de protéine pour chaque acide aminé essentiel
ideal_aa_content = {
    "H": 15,   # Histidine
    "I": 30,   # Isoleucine
    "L": 59,   # Leucine
    "K": 45,   # Lysine
    "M": 16,   # Méthionine
    "C": 6,    # Cystéine
    "F+Y": 30, # Phénylalanine + Tyrosine
    "T": 23,   # Thréonine
    "W": 6,    # Tryptophane
    "V": 39    # Valine
}

# Masse molaire moyenne des acides aminés (en g/mol)
masse_molaire = {
    "A": 89.09, "R": 174.20, "N": 132.12, "D": 133.10, "C": 121.15, "E": 147.13,
    "Q": 146.15, "G": 75.07, "H": 155.16, "I": 131.17, "L": 131.17, "K": 146.19,
    "M": 149.21, "F": 165.19, "P": 115.13, "S": 105.09, "T": 119.12, "W": 204.23,
    "Y": 181.19, "V": 117.15
}