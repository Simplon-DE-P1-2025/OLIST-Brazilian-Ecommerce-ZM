import marimo

__generated_with = "0.19.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import sqlalchemy
    import sys
    import os
    import matplotlib.pyplot as plt

    # --- 1. CONFIGURATION ---
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "notebooks":
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
    else:
        project_root = current_dir

    src_path = os.path.join(project_root, "src")
    sql_path = os.path.join(project_root, "sql")
    db_path = os.path.join(project_root, "olist.db")

    if src_path not in sys.path:
        sys.path.append(src_path)

    # --- 2. IMPORTS & UTILS ---
    try:
        from analysis_utils import execute_and_time, get_query_plan
    except ImportError:
        def execute_and_time(q, e): return pd.DataFrame(), 0
        def get_query_plan(q, e): print("Module non chargé")

    def load_query(filename):
        """Lit un fichier SQL sans conflit."""
        full_path = os.path.join(sql_path, filename)
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    return db_path, execute_and_time, load_query, mo, pd, plt, sqlalchemy


@app.cell
def _(db_path, sqlalchemy):
    # Connexion BDD
    engine = sqlalchemy.create_engine(f"sqlite:///{db_path}")
    return (engine,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Analyse 3 : Granularité Temporelle (Jour / Mois / Année)
    """)
    return


@app.cell
def _(engine, execute_and_time, load_query, mo, pd, plt):
    # --- ANALYSE 3 ---
    # Variables suffixées avec _3 pour éviter les conflits
    query_3 = load_query("3_sales_daily.sql")
    df_daily_3, duration_3 = execute_and_time(query_3, engine)

    # Préparation
    df_daily_3["sale_date"] = pd.to_datetime(df_daily_3["sale_date"])
    df_daily_3.set_index("sale_date", inplace=True)

    df_monthly_3 = df_daily_3["daily_revenue"].resample("ME").sum()
    df_yearly_3 = df_daily_3["daily_revenue"].resample("YE").sum()

    # Visualisation
    fig_3, axes_3 = plt.subplots(3, 1, figsize=(10, 12))

    df_daily_3["daily_revenue"].plot(ax=axes_3[0], title="CA Quotidien", color='skyblue', lw=0.5)
    axes_3[0].set_ylabel("Revenu")

    df_monthly_3.plot(kind='line', ax=axes_3[1], title="CA Mensuel", marker='o', color='orange')
    axes_3[1].set_ylabel("Revenu")

    df_yearly_3.plot(kind='bar', ax=axes_3[2], title="CA Annuel", color='green')
    axes_3[2].set_ylabel("Revenu")

    plt.tight_layout()

    mo.vstack([
        mo.md(f"**Temps d'exécution :** `{duration_3:.4f} sec`"),
        fig_3
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Analyse 1 : CA Mensuel & Croissance
    """)
    return


@app.cell
def _(engine, execute_and_time, load_query, mo, plt):
    # --- ANALYSE 1 ---
    # Variables suffixées avec _1
    query_1 = load_query("1_sales_evolution.sql")
    df_sales_1, duration_1 = execute_and_time(query_1, engine)

    fig_1, ax_1 = plt.subplots(figsize=(10, 5))
    if not df_sales_1.empty:
        df_sales_1.set_index("sales_month")["monthly_revenue"].plot(kind='bar', ax=ax_1, title="CA Mensuel")
        plt.tight_layout()

    mo.vstack([
        mo.md(f"**Temps d'exécution :** `{duration_1:.4f} sec`"),
        df_sales_1.head(),
        fig_1
    ])
    return (duration_1,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Analyse 2 : Top 10 Produits
    """)
    return


@app.cell
def _(engine, execute_and_time, load_query, mo):
    # --- ANALYSE 2 ---
    # Variables suffixées avec _2
    query_2 = load_query("2_top_products.sql")
    df_top_2, duration_2 = execute_and_time(query_2, engine)

    mo.vstack([
        mo.md(f"**Temps d'exécution :** `{duration_2:.4f} sec`"),
        df_top_2
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Benchmark : Optimisé vs Non-Optimisé
    """)
    return


@app.cell
def _(duration_1, engine, execute_and_time, load_query, mo):
    # --- BENCHMARK ---
    # Variables suffixées avec _bench
    query_bench = load_query("1_sales_evolution_simple.sql")

    with mo.status.spinner("Exécution de la requête non-optimisée..."):
        df_bench, duration_bench = execute_and_time(query_bench, engine)

    # Calcul Gain
    speedup = 0
    if duration_bench > 0 and duration_1 > 0:
        speedup = duration_bench / duration_1
        msg_bench = f"La version optimisée est **{speedup:.1f}x plus rapide**."
    else:
        msg_bench = "Calcul impossible."

    mo.vstack([
        mo.md("### Résultats du Benchmark"),
        mo.md(f"* **Optimisé :** `{duration_1:.4f} s`"),
        mo.md(f"* **Non-Optimisé :** `{duration_bench:.4f} s`"),
        mo.md(msg_bench)
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Analyse 4 : Nouveaux Clients vs Récurrents
    """)
    return


@app.cell
def _(engine, execute_and_time, load_query, mo, plt):
    # --- ANALYSE 4 ---
    # Variables suffixées avec _4
    query_4 = load_query("4_new_vs_returning.sql")
    df_ret_4, duration_4 = execute_and_time(query_4, engine)

    df_pivot_4 = df_ret_4.pivot(index="month", columns="customer_type", values="total_orders").fillna(0)

    fig_4, ax_4 = plt.subplots(figsize=(10, 5))
    df_pivot_4.plot(kind='bar', stacked=True, ax=ax_4, color=['#1f77b4', '#ff7f0e'])

    ax_4.set_title("Nouveaux vs Récurrents")
    plt.tight_layout()

    total_orders = df_ret_4['total_orders'].sum()
    recurring_orders = df_ret_4[df_ret_4['customer_type'] == 'Récurrent']['total_orders'].sum()
    rate_4 = (recurring_orders / total_orders) * 100

    mo.vstack([
        mo.md(f"**Temps :** `{duration_4:.4f} sec` | **Taux Récurrence :** `{rate_4:.2f}%`"),
        fig_4
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Analyse 5 : Panier Moyen (AOV)
    """)
    return


@app.cell
def _(engine, execute_and_time, load_query, mo, plt):
    # --- ANALYSE 5 ---
    # Variables suffixées avec _5
    query_5 = load_query("5_average_basket.sql")
    df_aov_5, duration_5 = execute_and_time(query_5, engine)

    global_aov_5 = df_aov_5["total_revenue"].sum() / df_aov_5["total_orders"].sum()

    fig_5, ax_5 = plt.subplots(figsize=(10, 5))
    df_aov_5.set_index("month")["average_ticket"].plot(kind='line', ax=ax_5, color='purple', marker='o')
    ax_5.axhline(global_aov_5, color='red', linestyle='--')

    ax_5.set_title("Panier Moyen")
    plt.tight_layout()

    mo.vstack([
        mo.md(f"**Temps :** `{duration_5:.4f} sec` | **AOV Global :** `{global_aov_5:.2f} BRL`"),
        fig_5
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Analyse 6 : Taux de Conversion (Approbation)
    """)
    return


@app.cell
def _(engine, execute_and_time, load_query, mo, plt):
    # --- ANALYSE 6 ---
    # Variables suffixées avec _6
    query_6 = load_query("6_conversion_rate.sql")
    df_conv_6, duration_6 = execute_and_time(query_6, engine)

    # Graphique : Comparaison Taux d'approbation vs Taux de livraison
    fig_6, ax_6 = plt.subplots(figsize=(10, 5))

    # On trace les deux courbes
    df_conv_6.set_index("month")["approval_rate"].plot(kind='line', ax=ax_6, color='green', marker='o', label="Taux d'Approbation")
    df_conv_6.set_index("month")["delivery_rate"].plot(kind='line', ax=ax_6, color='blue', linestyle='--', label="Taux de Livraison")

    ax_6.set_title("Entonnoir de Conversion Transactionnel")
    ax_6.set_ylabel("Pourcentage (%)")
    ax_6.set_ylim(80, 105) # On zoom sur le haut du graphique car les taux sont hauts
    ax_6.legend()
    plt.tight_layout()

    # Calcul des moyennes globales
    avg_approval_6 = df_conv_6["approval_rate"].mean()
    avg_delivery_6 = df_conv_6["delivery_rate"].mean()

    mo.vstack([
        mo.md(f"**Temps d'exécution :** `{duration_6:.4f} sec`"),
        mo.md("Ce graphique montre la perte entre la commande client, la validation du paiement et la livraison."),
        mo.md(f"* **Taux moyen d'approbation :** `{avg_approval_6:.2f}%`"),
        mo.md(f"* **Taux moyen de livraison :** `{avg_delivery_6:.2f}%`"),
        fig_6,
        mo.md("### Données"),
        df_conv_6.tail()
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Analyse 7 : Segmentation RFM
    """)
    return


@app.cell
def _(engine, execute_and_time, load_query, mo, pd, plt):
    # --- ANALYSE 7 : RFM SEGMENTATION ---
    # Variables suffixées avec _7

    query_7 = load_query("7_rfm_analysis.sql")
    df_rfm_7, duration_7 = execute_and_time(query_7, engine)

    # --- CALCUL DES SCORES (1 à 5) ---

    # 1. Récence (R) : On utilise qcut pour faire 5 groupes de taille égale
    # Note : labels=[5, 4, 3, 2, 1] car une petite récence est meilleure (donc score 5)
    df_rfm_7['R'] = pd.qcut(df_rfm_7['recency'], q=5, labels=[5, 4, 3, 2, 1])

    # 2. Montant (M) : On utilise qcut
    # Note : labels=[1, 2, 3, 4, 5] car un gros montant est meilleur (donc score 5)
    df_rfm_7['M'] = pd.qcut(df_rfm_7['monetary'], q=5, labels=[1, 2, 3, 4, 5])

    # 3. Fréquence (F) : Cas particulier Olist
    # Comme 97% des gens ont F=1, qcut ne marche pas. On fait un mapping manuel.
    # 1 commande -> Score 1 | 2 commandes -> Score 3 | 3+ commandes -> Score 5
    def get_f_score(x):
        if x == 1: return 1
        if x == 2: return 3
        return 5

    df_rfm_7['F'] = df_rfm_7['frequency'].apply(get_f_score)

    # Création du score concaténé (ex: "515")
    df_rfm_7['RFM_Score'] = df_rfm_7['R'].astype(str) + df_rfm_7['F'].astype(str) + df_rfm_7['M'].astype(str)

    # --- SEGMENTATION ---
    # On se base principalement sur R et F pour définir le segment (Matrice classique)
    # Convertissons R et F en entiers pour la logique
    r_int = df_rfm_7['R'].astype(int)
    f_int = df_rfm_7['F'].astype(int)

    def segment_customer(row):
        r, f = row['R'], row['F']
        # Logique simplifiée basée sur la récence et la fréquence
        if r >= 4 and f >= 4: return 'Champions'
        if r >= 3 and f >= 3: return 'Fidèles'
        if r >= 4 and f == 1: return 'Nouveaux Prometteurs'
        if r == 3 and f == 1: return 'Nouveaux Récents'
        if r == 2: return 'A réactiver'
        if r == 1: return 'Perdus'
        return 'Autres' # Cas intermédiaires

    df_rfm_7['Segment'] = df_rfm_7.apply(lambda row: segment_customer(row), axis=1)

    # --- VISUALISATION ---

    # Comptage par segment
    segment_counts_7 = df_rfm_7['Segment'].value_counts().sort_values()

    fig_7, ax_7 = plt.subplots(figsize=(10, 6))

    # Bar Chart horizontal
    bars = ax_7.barh(segment_counts_7.index, segment_counts_7.values, color='#2ca02c')

    ax_7.set_title("Répartition des Clients par Segment RFM")
    ax_7.set_xlabel("Nombre de Clients")

    # Ajout des étiquettes de valeur
    for m, v in enumerate(segment_counts_7.values):
        ax_7.text(v + 100, m, str(v), va='center')

    plt.tight_layout()

    mo.vstack([
        mo.md(f"**Temps d'exécution :** `{duration_7:.4f} sec`"),
        mo.md("### Distribution des Segments"),
        mo.md("On remarque une masse énorme de clients 'Perdus' ou 'A réactiver', typique d'un business sans stratégie de rétention forte."),
        fig_7,
        mo.md("### Aperçu des données RFM"),
        df_rfm_7[['customer_unique_id', 'recency', 'frequency', 'monetary', 'R', 'F', 'M', 'Segment']].head()
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Analyse 8 : Analyse de Cohortes (Rétention)
    """)
    return


@app.cell
def _(engine, execute_and_time, load_query, mo, pd, plt):
    # --- ANALYSE 8 : COHORTS ---
    # Variables suffixées avec _8

    query_8 = load_query("8_cohort_retention.sql")
    df_cohort_8, duration_8 = execute_and_time(query_8, engine)

    # --- PIVOT TABLE ---
    # On transforme les données pour avoir :
    # Lignes = Mois de Cohorte
    # Colonnes = Mois +X (0, 1, 2...)
    # Valeurs = Taux de rétention
    cohort_pivot_8 = df_cohort_8.pivot_table(
        index="cohort_month", 
        columns="month_number", 
        values="retention_rate"
    )

    # On ne garde que les 12 premiers mois pour la lisibilité
    cohort_pivot_8 = cohort_pivot_8.iloc[:, 0:13]

    # --- VISUALISATION (HEATMAP) ---
    fig_8, ax_8 = plt.subplots(figsize=(12, 8))

    # Création de la heatmap avec Matplotlib (imshow)
    im_8 = ax_8.imshow(cohort_pivot_8, cmap='YlGn', aspect='auto')

    # Configuration des axes
    ax_8.set_xticks(range(len(cohort_pivot_8.columns)))
    ax_8.set_xticklabels(cohort_pivot_8.columns)
    ax_8.set_yticks(range(len(cohort_pivot_8.index)))
    ax_8.set_yticklabels(cohort_pivot_8.index)

    ax_8.set_title("Taux de Rétention par Cohorte (%)")
    ax_8.set_xlabel("Mois après le 1er achat")
    ax_8.set_ylabel("Mois de Cohorte")

    # Ajout de la barre de couleur
    cbar = plt.colorbar(im_8)
    cbar.set_label('Rétention (%)')

    # Ajout des valeurs textuelles dans les cases
    # On boucle sur les données pour afficher le %
    for i in range(len(cohort_pivot_8.index)):
        for j in range(len(cohort_pivot_8.columns)):
            val = cohort_pivot_8.iloc[i, j]
            if pd.notnull(val):
                text_color = "white" if val > 50 else "black"
                ax_8.text(j, i, f"{val:.1f}", ha="center", va="center", color=text_color, fontsize=8)

    plt.tight_layout()

    mo.vstack([
        mo.md(f"**Temps d'exécution :** `{duration_8:.4f} sec`"),
        mo.md("Lecture : La colonne 0 représente 100% (l'achat initial). La colonne 1 montre le % de clients revenus le mois suivant."),
        mo.md("_Observation : La rétention chute drastiquement après le mois 0, ce qui confirme le modèle 'achat unique' d'Olist._"),
        fig_8
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Analyse 9 : LTV (Lifetime Value) par Cohorte
    """)
    return


@app.cell
def _(engine, execute_and_time, load_query, mo, pd, plt):
    # --- ANALYSE 9 : LTV PAR COHORTE ---
    # Variables suffixees avec _9

    query_9 = load_query("9_cohort_ltv.sql")
    df_ltv_9, duration_9 = execute_and_time(query_9, engine)

    # --- PIVOT TABLE ---
    # Lignes = Mois de Cohorte | Colonnes = Mois d'activite | Valeurs = LTV Cumulee
    ltv_pivot_9 = df_ltv_9.pivot_table(
        index="cohort_month", 
        columns="month_number", 
        values="cumulative_ltv_per_customer"
    )

    # On ne garde que les 12 premiers mois (au-dela, les donnees sont eparses)
    ltv_pivot_9 = ltv_pivot_9.iloc[:, 0:13]

    # Remplissage par propagation (forward fill) sur les colonnes.
    # Si une cohorte ne fait aucun achat le mois 2, sa LTV cumulee reste la meme qu'au mois 1.
    ltv_pivot_9 = ltv_pivot_9.ffill(axis=1)

    # --- VISUALISATION (HEATMAP) ---
    fig_9, ax_9 = plt.subplots(figsize=(12, 8))

    # Heatmap avec cmap 'Blues' (plus c'est fonce, plus la LTV est elevee)
    im_9 = ax_9.imshow(ltv_pivot_9, cmap='Blues', aspect='auto')

    ax_9.set_xticks(range(len(ltv_pivot_9.columns)))
    ax_9.set_xticklabels(ltv_pivot_9.columns)
    ax_9.set_yticks(range(len(ltv_pivot_9.index)))
    ax_9.set_yticklabels(ltv_pivot_9.index)

    ax_9.set_title("Evolution de la LTV Cumulee par Cohorte (en BRL)")
    ax_9.set_xlabel("Mois apres le premier achat")
    ax_9.set_ylabel("Mois de Cohorte")

    cbar_9 = plt.colorbar(im_9)
    cbar_9.set_label('LTV Cumulee Moyenne (BRL)')

    # Ajout des valeurs textuelles
    for i_9 in range(len(ltv_pivot_9.index)):
        for j_9 in range(len(ltv_pivot_9.columns)):
            val_9 = ltv_pivot_9.iloc[i_9, j_9]
            if pd.notnull(val_9):
                # On ajuste la couleur du texte selon l'intensite du fond pour la lisibilite
                max_val = ltv_pivot_9.max().max()
                text_color_9 = "white" if val_9 > (max_val * 0.6) else "black"
                ax_9.text(j_9, i_9, f"{val_9:.0f}", ha="center", va="center", color=text_color_9, fontsize=8)

    plt.tight_layout()

    mo.vstack([
        mo.md(f"**Temps d'execution :** `{duration_9:.4f} sec`"),
        mo.md("Lecture : La colonne 0 montre le panier moyen du premier achat. Les colonnes suivantes montrent comment ce chiffre augmente si le client revient."),
        mo.md("_Observation : La LTV augmente tres peu apres le mois 0, ce qui reflete la faible retention (Analyse 8). Olist repose sur l'acquisition continue de nouveaux clients._"),
        fig_9
    ])
    return


if __name__ == "__main__":
    app.run()
