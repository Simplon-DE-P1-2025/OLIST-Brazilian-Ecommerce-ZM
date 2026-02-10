# 🛍️ OLIST Brazilian Ecommerce - Analyse de Données

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)
[![Marimo](https://img.shields.io/badge/Marimo-Interactive-purple.svg)](https://marimo.io/)

Projet d'analyse complète des données de l'e-commerce brésilien **OLIST**, incluant l'extraction, la transformation (ETL), le chargement en base de données SQLite, et l'exploration interactive des données via des notebooks **Marimo**.

## 📊 Aperçu du Projet

Ce projet exploite un dataset public de Kaggle contenant les données d'**OLIST**, le plus grand marketplace d'e-commerce du Brésil. Le dataset comprend :

- **100 000+ commandes** effectuées entre 2016 et 2018
- **32 000+ produits** répartis dans 73 catégories
- **9 fichiers CSV** interconnectés (commandes, clients, produits, avis, paiements, etc.)
- **1 million+ d'enregistrements géographiques** pour l'analyse spatiale

### 🎯 Objectifs du Projet

- ✅ **Extraction automatisée** des données depuis Kaggle via API
- ✅ **Transformation et nettoyage** des données (ETL complet)
- ✅ **Modélisation relationnelle** et chargement en base SQLite
- ✅ **Exploration interactive** avec notebooks Marimo
- ✅ **Indexation optimisée** pour des requêtes SQL performantes
- ✅ **Traduction des catégories** (portugais → anglais)
- ✅ **Dédoublonnage géographique** et standardisation des données


## 🚀 Installation & Configuration

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git
- Un compte Kaggle (pour télécharger les données)

---

### 1️⃣ Cloner le Repository

```bash
git clone https://github.com/Simplon-DE-P1-2025/OLIST-Brazilian-Ecommerce-ZM.git
cd OLIST-Brazilian-Ecommerce-ZM
```

---

### 2️⃣ Créer et Activer l'Environnement Virtuel

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

---

### 3️⃣ Installer les Dépendances

```bash
pip install -r requirements.txt
```

**Dépendances installées :**
- `kaggle` : API pour télécharger les données
- `pandas` : Manipulation et transformation de données
- `marimo` : Notebooks interactifs (alternative à Jupyter)
- `sqlalchemy` : ORM pour la base de données SQLite
- `matplotlib` : Visualisation de données
- `python-dotenv` : Gestion des variables d'environnement

---

### 4️⃣ Configurer les Credentials Kaggle

#### **Option 1 : Via le fichier `.env`** (Recommandé)

1. Allez sur [https://www.kaggle.com/settings/account](https://www.kaggle.com/settings/account)
2. Cliquez sur **"Create New API Token"**
3. Récupérer le token.
4. Créez un fichier `.env` à la racine du projet :

```env
KAGGLE_USERNAME=votre_username
KAGGLE_KEY=votre_api_key
```

⚠️ **Important** : Ne commitez jamais le fichier `.env` (déjà dans `.gitignore`)

---

## 📥 Télécharger et Extraire les Données

Une fois les credentials configurées, exécutez le script d'extraction :

```bash
python src/extract.py
```

**Ce que fait ce script :**
- ✅ Authentification automatique avec l'API Kaggle
- ✅ Téléchargement du dataset complet (`olistbr/brazilian-ecommerce`)
- ✅ Extraction automatique des fichiers ZIP
- ✅ Stockage dans `data/raw/`
- ✅ Affichage du récapitulatif des fichiers et tailles

**Résultat attendu :**

```
📋 Credentials détectées :
   - Username: votre_username
   - Key: abcdef1234567890...
⬇️  Téléchargement de olistbr/brazilian-ecommerce...
✅ Téléchargement et extraction terminés !
📦 Fichiers récupérés :
   - olist_customers_dataset.csv (8.62 MB)
   - olist_orders_dataset.csv (16.84 MB)
   - olist_order_items_dataset.csv (14.72 MB)
   ...
```

### 📂 Fichiers Téléchargés

| Fichier | Taille | Lignes | Description |
|---------|--------|--------|-------------|
| `olist_customers_dataset.csv` | 8.62 MB | 99,441 | Informations clients (ID, localisation) |
| `olist_orders_dataset.csv` | 16.84 MB | 99,441 | Commandes (dates, statuts) |
| `olist_order_items_dataset.csv` | 14.72 MB | 112,650 | Articles commandés (prix unitaire) |
| `olist_order_payments_dataset.csv` | 5.51 MB | 103,886 | Méthodes de paiement |
| `olist_order_reviews_dataset.csv` | 13.78 MB | 99,224 | Avis clients (notes, commentaires) |
| `olist_products_dataset.csv` | 2.27 MB | 32,951 | Produits (catégories, dimensions) |
| `olist_geolocation_dataset.csv` | 58.44 MB | 1,000,163 | Coordonnées GPS par code postal |
| `olist_sellers_dataset.csv` | 0.17 MB | 3,095 | Vendeurs (localisation) |
| `product_category_name_translation.csv` | 0.00 MB | 71 | Traduction portugais → anglais |

---

## 🔄 Transformation ETL et Chargement en Base de Données

Le notebook Marimo `notebooks/explore.py` contient tout le pipeline ETL pour transformer et charger les données dans une base SQLite.

### Lancer le Notebook Interactif

```bash
marimo edit notebooks/explore.py
```

Le notebook s'ouvrira dans votre navigateur avec une interface interactive.

### 📋 Étapes du Pipeline ETL

#### **1. Traduction des Catégories Produits**
- Fusion avec `product_category_name_translation.csv`
- Conversion du portugais vers l'anglais
- Remplissage des valeurs manquantes par `"unknown"`

#### **2. Nettoyage des Données Produits**
- Remplissage des valeurs numériques manquantes (poids, dimensions) par `0`
- Standardisation des types de données

#### **3. Conversion des Dates (Commandes)**
- Conversion de 5 colonnes de dates de `object` vers `datetime64[ns]` :
  - `order_purchase_timestamp`
  - `order_approved_at`
  - `order_delivered_carrier_date`
  - `order_delivered_customer_date`
  - `order_estimated_delivery_date`

#### **4. Nettoyage des Avis Clients**
- Remplacement des valeurs `NaN` par des chaînes vides
- Nettoyage des caractères spéciaux dans les commentaires
- Remplacement des guillemets doubles par des simples
- Suppression des retours à la ligne

#### **5. Dédoublonnage Géographique**
- **Problème initial** : 1 million+ de lignes avec duplicatas de codes postaux
- **Solution** : Groupement par `geolocation_zip_code_prefix` + moyenne des coordonnées
- **Résultat** : Réduction à ~19,000 codes postaux uniques (**-98% de lignes**)

#### **6. Création de la Base SQLite**
- Création du fichier `olist.db` à la racine
- Insertion de 8 tables :
  - `orders` (table de faits centrale)
  - `order_items` (table de liaison)
  - `products`
  - `customers`
  - `sellers`
  - `order_payments`
  - `order_reviews`
  - `geolocation`

#### **7. Indexation pour Performances**
- Création de 10 index sur les clés primaires et étrangères
- Optimisation des jointures SQL futures

---

## 📁 Structure du Projet

```
OLIST-Brazilian-Ecommerce-ZM/
│
├── 📂 src/
│   └── extract.py              # Script d'extraction depuis Kaggle
│
├── 📂 data/
│   └── raw/                    # Données brutes téléchargées (9 CSV)
│
├── 📂 notebooks/
│   ├── explore.py              # Notebook Marimo interactif (ETL complet)
│   └── __marimo__/
│       └── session/
│           └── explore.py.json # État de session Marimo
│
├── 📄 requirements.txt         # Dépendances Python
├── 📄 .env                     # Variables d'environnement (Kaggle API)
├── 📄 .gitignore              # Fichiers ignorés par Git
├── 📄 LICENSE                 # Licence MIT
├── 📄 README.md               # Ce fichier
└── 🗄️ olist.db               # Base de données SQLite (générée après ETL)
```

---

## 🔧 Utilisation du Projet

### Workflow Complet

#### **Étape 1 : Extraction**
```bash
python src/extract.py
```
↳ Télécharge les données dans `data/raw/`

#### **Étape 2 : Exploration et ETL**
```bash
marimo edit notebooks/explore.py
```
↳ Lance le notebook interactif dans le navigateur

**Dans le notebook :**
1. Exécutez les cellules séquentiellement (⏯️ bouton play)
2. Visualisez l'aperçu des données
3. Lancez les transformations ETL
4. Vérifiez les rapports de validation
5. Créez la base de données `olist.db`

#### **Étape 3 : Requêtes SQL (Exemple)**
```bash
sqlite3 olist.db
```

```sql
-- Top 5 des catégories les plus vendues
SELECT 
    p.product_category_name_english,
    COUNT(DISTINCT oi.order_id) as nb_commandes,
    SUM(oi.price) as revenue_total
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name_english
ORDER BY revenue_total DESC
LIMIT 5;
```

---

## 🗂️ Schéma Relationnel de la Base de Données

```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│  customers  │◄────────┤    orders    │────────►│ order_items  │
└─────────────┘         └──────────────┘         └──────────────┘
                               │                         │
                               │                         │
                               ▼                         ▼
                        ┌──────────────┐         ┌──────────────┐
                        │order_payments│         │   products   │
                        └──────────────┘         └──────────────┘
                               │                         
                               │                         
                               ▼                         ▼
                        ┌──────────────┐         ┌──────────────┐
                        │order_reviews │         │   sellers    │
                        └──────────────┘         └──────────────┘
                        
                        ┌──────────────┐
                        │ geolocation  │ (Table de référence)
                        └──────────────┘
```

**Clés Primaires :**
- `orders.order_id`
- `customers.customer_id`
- `products.product_id`
- `sellers.seller_id`
- `geolocation.geolocation_zip_code_prefix`

**Clés Étrangères (order_items) :**
- `order_id` → `orders.order_id`
- `product_id` → `products.product_id`
- `seller_id` → `sellers.seller_id`

---

## 📊 Insights Clés Identifiés

### 1. **Granularité des Données**
- La table `order_items` contient **plusieurs lignes par commande** (1 ligne = 1 article)
- Pour obtenir le montant total d'une commande : agrégation requise (`SUM(price)`)

### 2. **Méthodes de Paiement**
- **Dominance** : Carte de crédit (`credit_card`) et Boleto (paiement brésilien)
- Les autres méthodes sont marginales (<5%)

### 3. **Traduction Obligatoire**
- Les catégories produits sont en **portugais** (ex : `cama_mesa_banho`)
- Utilisation du fichier de traduction pour analyses en anglais

### 4. **Qualité des Données**
- **Dates manquantes** : Certaines commandes n'ont pas de date de livraison (commandes annulées)
- **Commentaires vides** : ~50% des avis n'ont pas de texte (seulement une note)

### 5. **Optimisation Géographique**
- Réduction de **1 million → 19,000 lignes** après dédoublonnage
- Gain de **98%** en volumétrie

---



## 📦 Dépendances

| Paquet | Description |
|--------|-------------|
| `kaggle` | API Kaggle pour télécharger les données |
| `pandas` | Manipulation et analyse de données |
| `marimo` | Notebooks interactifs (alternative à Jupyter) |
| `sqlalchemy` | ORM pour base de données SQLite |
| `matplotlib` | Visualisation de données |
| `python-dotenv` | Gestion des variables d'environnement |

Voir `requirements.txt` pour la liste complète.

---


## 👤 Auteur

**Zoubir MABED**

📧 **Email :** [mabedzoubir05@gmail.com](mailto:mabedzoubir05@gmail.com)

🎓 **Formation :** Data Engineering - Simplon (Promotion 2026)
