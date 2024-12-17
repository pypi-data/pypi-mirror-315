from Bio.Seq import Seq
class Gene : 
    def __init__(self,gene_txt):
        self.gene_txt = gene_txt
        self.nom = None
        self.sequence_nuc = ""
        self.sequence_prot = None
        self.taille_sequence_prot = None
        self.is_ribosomal = None
        self.CAI = None
        self.CAI_normalize = None
        self.dico_AA_CAI = None
        self.locus_tag = None
        self.dico_AA = {}
        self.expr_reelle=None
        self.parse()
        #self.get_CAI()
        #self.get_teneur()
        #self.get_taux_GC()

    def parse(self) :
        ribosomal_genes = [
    'rpiA', 'rpiB', 'rpiR',
    'rplA', 'rplB', 'rplC', 'rplD', 'rplE', 'rplF', 'rplI', 'rplJ', 'rplK',
    'rplL', 'rplM', 'rplN', 'rplO', 'rplP', 'rplQ', 'rplR', 'rplS', 'rplT',
    'rplU', 'rplV', 'rplW', 'rplX', 'rplY',
    'rpmA', 'rpmB', 'rpmC', 'rpmD', 'rpmE', 'rpmF', 'rpmG', 'rpmH', 'rpmI', 'rpmJ',
    'rpoA', 'rpoB', 'rpoC', 'rpoD', 'rpoE', 'rpoH', 'rpoN', 'rpoS', 'rpoZ',
    'rpsA', 'rpsB', 'rpsC', 'rpsD', 'rpsE', 'rpsF', 'rpsG', 'rpsH', 'rpsI', 
    'rpsJ', 'rpsK', 'rpsL', 'rpsM', 'rpsN', 'rpsO', 'rpsP', 'rpsQ', 'rpsR', 
    'rpsS', 'rpsT', 'rpsU'
]
        text_split = self.gene_txt.split("\n")
        for index,elem in enumerate(text_split) : 
            if index == 0 : 
                parts = elem.split()
                if len(parts) > 1 and "[gene=" in parts[1]:
                    self.nom = elem.split()[1][6:-1]
                    self.locus_tag = elem.split()[2][11:-1]
                    if self.nom in ribosomal_genes : 
                        self.is_ribosomal = "Oui"
                    else : 
                        self.is_ribosomal = "Non"
                else : 
                    self.nom = "Inconnu"
                    self.locus_tag = elem.split()[1][11:-1] if len(parts) > 1 else "Inconnu"
                    self.is_ribosomal = "Inconnu"
            else :
                self.sequence_nuc += str(elem)
        
        # on fait disparaître les nucléotides inconnus! 
        self.sequence_nuc=self.sequence_nuc.replace('N','')

        dna = Seq(self.sequence_nuc)
        self.sequence_prot = dna.translate()
        self.taille_sequence_prot = len(self.sequence_prot)
        for AA in self.sequence_prot : 
            if AA not in self.dico_AA : 
                self.dico_AA[AA] = 1
            else : 
                self.dico_AA[AA] += 1
    def __repr__(self):
        # Méthode aditionelle pour tester nos méthode et notre parsage
        resultat = f"""nom: {self.nom}\nlocus tag : {self.locus_tag}\nsequence_nuc: {self.sequence_nuc}\nsequence_prot : {self.sequence_prot}\n
        Taille sequence prot : {self.taille_sequence_prot}\ndico_AA : {self.dico_AA}\nEst-ce-que c'est un gène ribosomal: {self.is_ribosomal}\nCAI : 
        {self.CAI}\nCAI normalisé : {self.CAI_normalize}\n taux_expr_reel : {self.expr_reelle}\n"""
        return resultat


    

    #def get_CAI(self) : 
        
    #def get_teneur(self) :

    #def get_taux_GC(self) : 
            
        #print(ligne_split)