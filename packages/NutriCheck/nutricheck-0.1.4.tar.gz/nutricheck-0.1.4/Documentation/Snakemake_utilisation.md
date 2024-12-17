# Pipeline Snakemake : Analyse de toxicité, CAI et pourcentage de purines

Ce pipeline utilise **Snakemake** pour automatiser l'analyse de fichiers FASTA et GTF. Il effectue trois types d'analyses :
- Analyse de toxicité des séquences.
- Calcul de l'indice d'adaptation des codons (**CAI**).
- Calcul du pourcentage de purines (A et G) dans des régions spécifiées par un fichier GTF.

---

## Prérequis

### **1. Installation de Snakemake**
Assurez-vous que Snakemake est installé. Vous pouvez utiliser conda ou pip :
```bash
conda install -c bioconda snakemake
```
ou
```bash
pip install snakemake
```

### **2. Scripts nécessaires**
Assurez-vous que les trois scripts suivants sont présents dans le même dossier que le fichier `Snakefile` :
- `script_toxico.py`
- `run_CAI.py` (le script pour calculer le CAI)
- `purine_percentage.py` (le script pour le pourcentage de purines)

### **3. Données d'entrée**
Placez vos fichiers dans un dossier nommé `data/` :
- Fichier FASTA : `data/sequences.fasta`
- Fichier GTF : `data/regions.gtf`

Vérifiez que ces fichiers sont correctement formatés.

---

## Utilisation

### **1. Vérifier le plan d'exécution**
Avant de lancer le pipeline, vérifiez ce que Snakemake prévoit d'exécuter avec la commande suivante :
```bash
snakemake -n
```
L'option `-n` affiche les étapes qui seront exécutées sans réellement les lancer.

---

### **2. Lancer le pipeline**
Pour exécuter le pipeline, utilisez simplement :
```bash
snakemake
```

#### Exécution parallèle
Pour exécuter le pipeline en parallèle, spécifiez le nombre de cœurs à utiliser :
```bash
snakemake --cores N
```
Remplacez `N` par le nombre de cœurs disponibles.

---

#### Avec environnement conda
Pour exécuter le pipeline dans un environnement conda
```bash
snakemake --use-conda
```



## Résultats

Les résultats sont générés dans le dossier `results/` :
- `results/toxico_results.txt` : Résultats de l'analyse de toxicité.
- `results/cai_results.txt` : Indice d'adaptation de codons pour chaque séquence.
- `results/purine_percentage.txt` : Pourcentage de purines dans les régions spécifiées.

---

## Exemple d'exécution

Imaginons un scénario où vos fichiers d'entrée se trouvent dans `data/` :
- `data/sequences.fasta`
- `data/regions.gtf`

Pour exécuter le pipeline avec 4 cœurs, utilisez :
```bash
snakemake --cores 4
```
Après l'exécution, consultez le dossier `results/` pour trouver les fichiers de sortie.

---

## Dépannage

### **1. Fichiers manquants ou noms incorrects**
- Assurez-vous que les chemins des fichiers définis dans le Snakefile correspondent aux fichiers réels dans votre répertoire.

### **2. Erreurs dans les scripts Python**
- Testez les scripts individuellement en ligne de commande pour valider leur bon fonctionnement.

### **3. Exécuter une règle spécifique**
Pour exécuter uniquement une règle spécifique, utilisez :
```bash
snakemake results/toxico_results.txt
```

---

## Ajustements possibles

### **Analyser de nouveaux fichiers**
Pour analyser de nouveaux fichiers FASTA ou GTF :
1. Remplacez les fichiers dans le dossier `data/`.
2. Relancez le pipeline.

### **Ajouter une étape supplémentaire**
Pour ajouter une nouvelle étape, il suffit d'éditer le `Snakefile` et d'y inclure une nouvelle règle.

---

En suivant ces instructions, vous pourrez utiliser et ajuster ce pipeline Snakemake efficacement. Bonne analyse !
