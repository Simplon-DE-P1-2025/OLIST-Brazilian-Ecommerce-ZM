import time
import pandas as pd
import sqlalchemy

def execute_and_time(query, engine):
    """
    Exécute une requête SQL, mesure le temps et retourne le DataFrame.
    """
    start_time = time.time()
    
    try:
        df = pd.read_sql(query, con=engine)
        duration = time.time() - start_time
        print(f"⏱️ Temps d'exécution : {duration:.4f} secondes")
        print(f"📊 Lignes récupérées : {len(df)}")
        return df, duration
    except Exception as e:
        print(f"❌ Erreur SQL : {e}")
        return None, 0

def get_query_plan(query, engine):
    """
    Affiche le plan d'exécution (EXPLAIN QUERY PLAN) pour vérifier l'usage des index.
    """
    with engine.connect() as conn:
        result = conn.execute(sqlalchemy.text(f"EXPLAIN QUERY PLAN {query}"))
        print("\n--- 🔍 Plan d'Exécution ---")
        for row in result:
            print(row)
        print("---------------------------\n")