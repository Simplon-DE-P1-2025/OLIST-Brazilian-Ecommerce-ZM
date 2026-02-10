import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import os

    return mo, os, pd


@app.cell
def _():
    # On définit le chemin vers les données brutes
    raw_data_path = "data/raw"
    return (raw_data_path,)


@app.cell
def _():
    # # Chargement de la table des commandes
    # df_orders = pd.read_csv(f"{raw_data_path}/olist_orders_dataset.csv")

    # # Conversion des dates (très important pour ce dataset !)
    # date_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    # for col in date_cols:
    #     df_orders[col] = pd.to_datetime(df_orders[col])

    # # Affichage des infos clés
    # mo.vstack([
    #     mo.md("### Aperçu des Commandes"),
    #     df_orders.head(),
    #     mo.md("### Infos et Types"),
    #     df_orders.dtypes,
    #     mo.md(f"### Valeurs manquantes : \n {df_orders.isnull().sum()}")
    # ])
    return


@app.cell
def _(mo, os, pd, raw_data_path):
    # Cellule pour explorer tous les fichiers en boucle

    files = [f for f in os.listdir(raw_data_path) if f.endswith('.csv')]
    display_elements = []

    for file_name in files:
        # Chargement
        df_temp = pd.read_csv(f"{raw_data_path}/{file_name}")

        # Préparation des infos spécifiques
        specific_info = []

        # Si c'est le fichier des commandes, on regarde les statuts
        if "order_status" in df_temp.columns:
            specific_info.append(mo.md("** Distribution des Statuts :**"))
            specific_info.append(df_temp["order_status"].value_counts())

        # Si c'est le fichier des paiements, on regarde les types de paiement
        if "payment_type" in df_temp.columns:
            specific_info.append(mo.md("** Types de Paiement :**"))
            specific_info.append(df_temp["payment_type"].value_counts())

        # Construction de l'affichage pour ce fichier
        element = mo.vstack([
            mo.md(f"## `{file_name}`"),
            mo.md(f"**Volumétrie :** {df_temp.shape[0]} lignes x {df_temp.shape[1]} colonnes"),
            mo.md("**Aperçu des données :**"),
            df_temp.head(3),
            *specific_info, # Ajoute les infos spécifiques si elles existent
            mo.md("---") # Séparateur visuel
        ])

        display_elements.append(element)

    # Affichage final de tous les blocs empilés
    mo.vstack(display_elements)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Notes :

    Voici les points critiques identifiés pour la future étape de nettoyage (ETL) :

    1.  **`olist_order_items_dataset` (Granularité)** :
        * Le prix indiqué est **par article**, pas par commande.
        * *Structure* : Une commande de 3 articles génère **3 lignes** avec le même `order_id`.
        * *Action* : Il faudra faire des agrégations (SUM) pour obtenir le montant total du panier.

    2.  **`olist_order_payments_dataset` (Distribution)** :
        * Les méthodes **`credit_card`** et **`boleto`** sont ultra-dominantes. Les autres méthodes sont marginales.

    3.  **`olist_products_dataset` (Traduction)** :
        * La colonne `product_category_name` est en **portugais** (ex: *cama_mesa_banho*).
        * *Action* : Il est impératif d'utiliser le fichier `product_category_name_translation.csv` pour traduire ces catégories en anglais/français avant l'analyse finale.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    # Stratégie de Nettoyage et Transformation (ETL)

    Avant l'insertion en base de données, nous allons standardiser les datasets. Voici le plan d'action par table :

    ### 1. products (Produits)
    * **Transformation majeure :** Fusion avec `product_category_name_translation` pour avoir les catégories en **Anglais**.
    * **Nettoyage :** Remplissage des valeurs manquantes (NaN) dans les colonnes numériques (poids, dimensions) par 0.
    * **Suppression :** On garde la colonne originale en portugais pour référence, mais la colonne prioritaire devient `product_category_name_english`.

    ### 2. geolocation (Géolocalisation)
    * **Problème :** Ce dataset contient des milliers de duplicatas (plusieurs latitudes/longitudes pour un même code postal).
    * **Stratégie :** Nous allons **grouper par `geolocation_zip_code_prefix`** et prendre la **moyenne** des coordonnées.
    * **Objectif :** Avoir une table unique (Clé Primaire : Zip Code) pour éviter d'exploser la volumétrie lors des jointures.

    ### 3. orders (Commandes)
    * **Typage :** Conversion impérative des 5 colonnes de dates (actuellement `object/string`) vers `datetime64[ns]` pour permettre les calculs de délais.
    * **Nettoyage :** Les commandes non livrées ont des dates de livraison nulles. On les laisse telles quelles (NULL est une information).

    ### 4. order_reviews (Avis)
    * **Nettoyage Textuel :** Les colonnes `comment_title` et `comment_message` contiennent des retours à la ligne qui peuvent casser certains exports. On va les remplacer par des espaces.
    * **Gestion des Nulls :** Remplacer les commentaires vides (NaN) par une chaîne vide `"\"`.

    ### 5. order_payments & order_items
    * **Typage :** Vérification que les ID sont bien des chaînes de caractères et les valeurs numériques correctes.
    """)
    return


@app.cell
def _(mo, pd):
    # --- 1. Chargement des données brutes (Si pas déjà fait) ---
    path = "data/raw"
    df_orders = pd.read_csv(f"{path}/olist_orders_dataset.csv")
    df_products = pd.read_csv(f"{path}/olist_products_dataset.csv")
    df_items = pd.read_csv(f"{path}/olist_order_items_dataset.csv")
    df_customers = pd.read_csv(f"{path}/olist_customers_dataset.csv")
    df_reviews = pd.read_csv(f"{path}/olist_order_reviews_dataset.csv")
    df_payments = pd.read_csv(f"{path}/olist_order_payments_dataset.csv")
    df_sellers = pd.read_csv(f"{path}/olist_sellers_dataset.csv")
    df_geo = pd.read_csv(f"{path}/olist_geolocation_dataset.csv")
    df_translation = pd.read_csv(f"{path}/product_category_name_translation.csv")

    # --- 2. TRANSFORMATION : PRODUCTS (Traduction) ---
    # On joint la traduction
    df_products = df_products.merge(df_translation, on='product_category_name', how='left')
    # On remplit les catégories inconnues par 'unknown'
    df_products['product_category_name_english'] = df_products['product_category_name_english'].fillna('unknown')
    # On remplit les données numériques manquantes par 0 (poids, dimensions) pour éviter les erreurs SQL
    cols_num = ['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']
    df_products[cols_num] = df_products[cols_num].fillna(0)


    # --- 3. TRANSFORMATION : ORDERS (Dates) ---
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_cols:
        df_orders[col] = pd.to_datetime(df_orders[col])


    # --- 4. TRANSFORMATION : REVIEWS (Texte) ---
    # Remplacer les NaN par vide
    df_reviews['review_comment_title'] = df_reviews['review_comment_title'].fillna("")
    df_reviews['review_comment_message'] = df_reviews['review_comment_message'].fillna("")
    # Nettoyer les caractères spéciaux qui cassent le SQL
    df_reviews['review_comment_message'] = df_reviews['review_comment_message'].str.replace('"', "'").str.replace('\n', ' ')


    # --- 5. TRANSFORMATION : GEOLOCATION (Dédoublonnage) ---
    # Etape critique : on groupe par Zip Code et on prend la moyenne des coordonnées
    df_geo_clean = df_geo.groupby("geolocation_zip_code_prefix").agg({
        "geolocation_lat": "mean",
        "geolocation_lng": "mean",
        "geolocation_city": "first", # On garde le premier nom de ville trouvé
        "geolocation_state": "first"
    }).reset_index()


    # Affichage de confirmation pour Marimo
    mo.vstack([
        mo.md("### Transformation terminée"),
        mo.md(f"**Produits :** Catégories traduites ({df_products['product_category_name_english'].nunique()} catégories uniques)."),
        mo.md(f"**Commandes :** Dates converties."),
        mo.md(f"**Géolocalisation :** Réduite de {df_geo.shape[0]} lignes à {df_geo_clean.shape[0]} codes postaux uniques.")
    ])
    return (
        df_customers,
        df_geo,
        df_geo_clean,
        df_items,
        df_orders,
        df_payments,
        df_products,
        df_reviews,
        df_sellers,
    )


@app.cell
def _(df_geo, df_geo_clean, df_orders, df_products, df_reviews, mo):
    # --- CELLULE DE VÉRIFICATION DES DONNÉES ---

    # 1. Vérification de la traduction des produits
    # On affiche côte à côte la catégorie originale et la version anglaise
    check_products = df_products[['product_category_name', 'product_category_name_english']].drop_duplicates().head(5)

    # 2. Vérification du format des dates
    # On vérifie que les colonnes sont bien en 'datetime64[ns]' et non plus 'object'
    check_dates = df_orders[['order_purchase_timestamp', 'order_delivered_customer_date']].dtypes

    # 3. Vérification de la réduction de la Géolocalisation
    lignes_avant = df_geo.shape[0]
    lignes_apres = df_geo_clean.shape[0]
    gain = lignes_avant - lignes_apres

    # 4. Vérification du nettoyage des Avis
    # On vérifie qu'il n'y a plus de valeurs nulles (NaN)
    check_reviews = df_reviews[['review_comment_title', 'review_comment_message']].isnull().sum()

    # Affichage structuré dans Marimo
    mo.vstack([
        mo.md("# Rapport de Validation des Transformations"),

        mo.md("### 1. Traduction (Aperçu)"),
        check_products,

        mo.md("### 2. Typage des Dates"),
        mo.md("Les colonnes doivent indiquer `datetime64[ns]` :"),
        check_dates,

        mo.md("### 3. Optimisation Géographique"),
        mo.md(f"* Lignes initiales : **{lignes_avant:,}**"),
        mo.md(f"* Lignes après dédoublonnage : **{lignes_apres:,}**"),
        mo.md(f"* **Gain : {gain:,} lignes supprimées**"),

        mo.md("### 4. Nettoyage des Nulls (Avis)"),
        mo.md("Nombre de valeurs nulles restantes :"),
        check_reviews
    ])
    return


@app.cell
def _(mo):
    mo.md("""
    # Modélisation et Ingestion en Base de Données (SQLite)

    Nous allons structurer la base de données relationnelle autour de la table de faits centrale : **orders**.

    ### Le Schéma Relationnel
    Voici comment les tables seront connectées :

    1.  **orders (Table de Faits)** : Le cœur du système.
        * *Clé Primaire :* order_id
        * *Clés Étrangères :* customer_id

    2.  **order_items (Table de Liaison)** : Relie une commande à des produits et des vendeurs.
        * *Clés Étrangères :* order_id, product_id, seller_id

    3.  **Tables de Dimension (Le "Qui" et "Quoi")** :
        * **products** : Détails des articles (catégorie, taille).
        * **customers** : Infos clients (localisation).
        * **sellers** : Infos vendeurs.
        * **geolocation** : Table de référence pour les codes postaux (zip_code_prefix).

    4.  **Tables de Détails (Attributs de la commande)** :
        * **order_payments** : Comment la commande a été payée.
        * **order_reviews** : La note et le commentaire laissés par le client.

    ---
    **Objectif Technique :** Créer le fichier `olist.db`, insérer les DataFrames nettoyés, et indexer les colonnes clés pour accélérer les futures requêtes SQL.
    """)
    return


@app.cell
def _(
    df_customers,
    df_geo_clean,
    df_items,
    df_orders,
    df_payments,
    df_products,
    df_reviews,
    df_sellers,
    mo,
):
    import sqlalchemy

    # Configuration du moteur SQL
    db_name = "olist.db"
    # Le fichier sera créé à la racine (ou dans le dossier courant selon l'exécution)
    engine = sqlalchemy.create_engine(f"sqlite:///{db_name}")

    # On prépare un dictionnaire pour itérer proprement
    # Assure-toi que ces variables sont bien disponibles depuis l'étape précédente
    tables_to_insert = {
        "orders": df_orders,
        "order_items": df_items,  # Celui-ci n'avait pas besoin de nettoyage spécifique
        "products": df_products,
        "customers": df_customers, # Idem, brut
        "sellers": df_sellers,     # Idem, brut
        "order_payments": df_payments, # Idem, brut
        "order_reviews": df_reviews,
        "geolocation": df_geo_clean
    }

    status_messages = []

    # Boucle d'insertion
    for table_name, df in tables_to_insert.items():
        try:
            # chunksize : insère par paquets pour ne pas saturer la mémoire
            df.to_sql(name=table_name, con=engine, if_exists="replace", index=False, chunksize=10000)
            status_messages.append(f"Table '{table_name}' générée ({len(df)} lignes).")
        except Exception as e:
            status_messages.append(f"Erreur sur '{table_name}' : {str(e)}")

    mo.vstack([
        mo.md("### Journal d'Ingestion SQL"),
        mo.md("\n".join(f"* {msg}" for msg in status_messages))
    ])
    return engine, sqlalchemy


@app.cell
def _(engine, mo, sqlalchemy):
    # Création des index pour accélérer les requêtes futures
    # On utilise du SQL brut via SQLAlchemy
    with engine.connect() as conn:
        # Liste des index à créer : (Table, Colonne)
        indices = [
            ("orders", "order_id"),
            ("orders", "customer_id"),
            ("order_items", "order_id"),
            ("order_items", "product_id"),
            ("order_items", "seller_id"),
            ("products", "product_id"),
            ("customers", "customer_id"),
            ("customers", "customer_unique_id"),
            ("sellers", "seller_id"),
            ("geolocation", "geolocation_zip_code_prefix")
        ]
    
        index_log = []
        for table, coll in indices:
            try:
                index_name = f"idx_{table}_{coll}"
                # On supprime l'index s'il existe déjà pour éviter les erreurs
                conn.execute(sqlalchemy.text(f"DROP INDEX IF EXISTS {index_name}"))
                # Création de l'index
                conn.execute(sqlalchemy.text(f"CREATE INDEX {index_name} ON {table} ({coll})"))
                index_log.append(f"Index créé : {index_name}")
            except Exception as e:
                index_log.append(f"Erreur index {table}.{coll} : {e}")

    mo.vstack([
        mo.md("### Optimisation (Indexation)"),
        mo.md("Les index permettent d'accélérer les jointures SQL."),
        mo.md(f"_{len(index_log)} index créés avec succès._")
    ])
    return


if __name__ == "__main__":
    app.run()
