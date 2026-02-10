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
def _(mo, pd, raw_data_path):
    # Chargement de la table des commandes
    df_orders = pd.read_csv(f"{raw_data_path}/olist_orders_dataset.csv")

    # Conversion des dates (très important pour ce dataset !)
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']
    for col in date_cols:
        df_orders[col] = pd.to_datetime(df_orders[col])

    # Affichage des infos clés
    mo.vstack([
        mo.md("### Aperçu des Commandes"),
        df_orders.head(),
        mo.md("### Infos et Types"),
        df_orders.dtypes,
        mo.md(f"### Valeurs manquantes : \n {df_orders.isnull().sum()}")
    ])
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


if __name__ == "__main__":
    app.run()
