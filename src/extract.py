import os
import sys
import zipfile
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables depuis le fichier .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def download_data(dataset_name, download_path="data/raw"):
    """
    Télécharge et dézippe le dataset Kaggle.
    """
    # Vérifier que les credentials sont présentes
    kaggle_username = os.environ.get('KAGGLE_USERNAME')
    kaggle_key = os.environ.get('KAGGLE_KEY')
    
    print(f"📋 Credentials détectées :")
    print(f"   - Username: {kaggle_username}")
    print(f"   - Key: {kaggle_key[:20]}..." if kaggle_key else "   - Key: Non défini")
    
    if not kaggle_username or not kaggle_key:
        print("❌ Erreur : Les variables d'environnement KAGGLE_USERNAME et KAGGLE_KEY ne sont pas définies.")
        print("\nVoici comment configurer :")
        print("1. Allez sur https://www.kaggle.com/settings/account")
        print("2. Cliquez sur 'Create New API Token'")
        print("3. Vous obtiendrez : username et api_key")
        print("4. Mettez à jour le fichier .env à la racine du projet :")
        print("   - KAGGLE_USERNAME=votre_username")
        print("   - KAGGLE_KEY=votre_api_key")
        return
    
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        # Authentification avec les credentials chargées
        # Les variables d'environnement doivent être définies avant d'appeler KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            print(f"📁 Dossier créé : {download_path}")

        print(f"⬇️  Téléchargement de {dataset_name}...")
        
        # Téléchargement
        api.dataset_download_files(dataset_name, path=download_path, unzip=True)
        
        print("✅ Téléchargement et extraction terminés !")
        
        # Lister les fichiers pour vérifier
        files = os.listdir(download_path)
        print("📦 Fichiers récupérés :")
        for f in files:
            if os.path.isfile(os.path.join(download_path, f)):
                file_size = os.path.getsize(os.path.join(download_path, f)) / (1024 * 1024)  # Taille en MB
                print(f"   - {f} ({file_size:.2f} MB)")
            else:
                print(f"   - {f}/ (dossier)")
                
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement : {str(e)}")
        print(f"\n⚠️  Vérifiez :")
        print(f"   1. Que votre clé API est valide et active")
        print(f"   2. Que vous avez accepté les conditions du dataset sur Kaggle")
        print(f"   3. Que la clé n'a pas expiré")

if __name__ == "__main__":
    # Nom du dataset Olist sur Kaggle
    DATASET = "olistbr/brazilian-ecommerce"
    download_data(DATASET)
