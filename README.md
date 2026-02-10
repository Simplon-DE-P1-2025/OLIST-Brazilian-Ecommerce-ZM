# OLIST Brazilian Ecommerce - Analyse de Données

Analyse complète des données de l'e-commerce brésilien OLIST. Ce projet vise à explorer, nettoyer et analyser les données de commandes, clients, produits et avis du plus grand marketplace d'e-commerce au Brésil.

## 📊 Aperçu du Projet

Ce projet utilise un dataset public de Kaggle contenant les données d'OLIST, le plus grand departement store du Brésil. Il comprend :

- **100 000+ commandes** réparties entre 2016 et 2018
- **32 000+ produits** de différentes catégories
- **9 fichiers CSV** avec informations détaillées

### Objectifs

- ✅ Extraire et nettoyer les données
- ✅ Analyser les tendances de vente
- ✅ Étudier le comportement des clients
- ✅ Évaluer la satisfaction des clients
- ✅ Créer des visualisations informatives

## 🚀 Installation & Configuration

### Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Git
- Un compte Kaggle

### 1. Cloner le Repository

```bash
git clone https://github.com/Simplon-DE-P1-2025/OLIST-Brazilian-Ecommerce-ZM.git
cd OLIST-Brazilian-Ecommerce-ZM
```

### 2. Créer et Activer l'Environnement Virtuel

**Sur Windows (PowerShell) :**
```powershell
python -m venv .venv
.\.venv\Scripts\activate.ps1
```

**Sur macOS/Linux :**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les Credentials Kaggle

**Option 1 : Via le fichier `.env`** (Recommandé)

1. Allez sur [https://www.kaggle.com/settings/account](https://www.kaggle.com/settings/account)
2. Cliquez sur **"Create New API Token"**
3. Un fichier `kaggle.json` sera téléchargé
4. Ouvrez `.env.example` et copiez-le comme `.env`
5. Complétez avec vos credentials :

```env
KAGGLE_USERNAME=votre_username
KAGGLE_KEY=votre_api_key
```

⚠️ **Important** : Ne commitez jamais le fichier `.env` (il est ignoré par `.gitignore`)

**Option 2 : Via kaggle.json**

Placez le fichier `kaggle.json` à :
- **Windows** : `C:\Users\<username>\.kaggle\kaggle.json`
- **macOS/Linux** : `~/.kaggle/kaggle.json`

## 📥 Télécharger et Extraire les Données

Exécutez le script d'extraction :

```bash
python src/extract.py
```

**Résultat attendu :**
- Les données sont téléchargées et stockées dans `data/raw/`
- 9 fichiers CSV extraits automatiquement

### Fichiers Téléchargés

| Fichier | Taille | Description |
|---------|--------|-------------|
| `olist_customers_dataset.csv` | 8.62 MB | Informations clients |
| `olist_orders_dataset.csv` | 16.84 MB | Données des commandes |
| `olist_order_items_dataset.csv` | 14.72 MB | Articles des commandes |
| `olist_order_payments_dataset.csv` | 5.51 MB | Méthodes de paiement |
| `olist_order_reviews_dataset.csv` | 13.78 MB | Avis clients |
| `olist_products_dataset.csv` | 2.27 MB | Informations produits |
| `olist_geolocation_dataset.csv` | 58.44 MB | Données géographiques |
| `olist_sellers_dataset.csv` | 0.17 MB | Informations vendeurs |
| `product_category_name_translation.csv` | 0.00 MB | Traduction des catégories |

## 📁 Structure du Projet

```
OLIST-Brazilian-Ecommerce-ZM/
├── src/
│   ├── extract.py              # Script de téléchargement des données
│   ├── transform.py            # (À venir) Nettoyage et transformation
│   ├── analyze.py              # (À venir) Analyses principales
│   └── visualize.py            # (À venir) Créer les visualisations
├── data/
│   ├── raw/                    # Données brutes téléchargées
│   └── processed/              # Données nettoyées et transformées
├── notebooks/                  # Jupyter Notebooks pour exploration
├── requirements.txt            # Dépendances Python
├── .env.example               # Exemple de configuration
├── .gitignore                 # Fichiers ignorés par Git
└── README.md                  # Ce fichier
```

## 🔧 Scripts Disponibles

### `src/extract.py`
Télécharge les données du dataset OLIST depuis Kaggle et les extrait dans `data/raw/`.

```bash
python src/extract.py
```

**Fonctionnalités :**
- ✅ Authentification automatique via `.env`
- ✅ Téléchargement du dataset complet
- ✅ Extraction des fichiers ZIP
- ✅ Vérification et affichage des fichiers téléchargés
- ✅ Messages d'erreur informatifs

## 📦 Dépendances

| Paquet | Version | Description |
|--------|---------|-------------|
| `kaggle` | - | API Kaggle pour télécharger les données |
| `pandas` | - | Manipulation et analyse de données |
| `marimo` | - | Notebooks interactifs |
| `sqlalchemy` | - | ORM pour base de données |
| `matplotlib` | - | Visualisation de données |
| `python-dotenv` | - | Gestion des variables d'environnement |

Voir `requirements.txt` pour la liste complète.

## 🐛 Dépannage

### "ModuleNotFoundError: No module named 'kaggle'"
```bash
pip install kaggle
```

### "You must authenticate before you can call the Kaggle API"
- Vérifiez que le fichier `.env` existe et contient les bonnes credentials
- Assurez-vous que `KAGGLE_USERNAME` et `KAGGLE_KEY` sont correctement définis

### "Permission denied" sur `.venv\Scripts\activate.ps1` (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🎯 Prochaines Étapes

- [ ] Créer un script de transformation des données (`src/transform.py`)
- [ ] Développer les analyses principales (`src/analyze.py`)
- [ ] Créer des visualisations (`src/visualize.py`)
- [ ] Ajouter des notebooks Jupyter
- [ ] Documenter les insights clés

## 📊 Data Description (À venir)

Prochainement : Description détaillée de chaque dataset et ses colonnes.

## 👥 Auteurs

- **Projet** : OLIST Brazilian Ecommerce Analysis
- **Équipe** : Simplon DE P1 2025

## 📄 License

Ce projet est sous License MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🔗 Ressources

- [Dataset Kaggle OLIST](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [Documentation Kaggle API](https://github.com/Kaggle/kaggle-cli)
- [Pandas Documentation](https://pandas.pydata.org/)

---

**Dernière mise à jour** : 10 février 2026

