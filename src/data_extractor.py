import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_datasets():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    print("Downloading from Kaggle...")
    api = KaggleApi()
    api.authenticate()
    
    # Download the dataset
    api.dataset_download_files(
        'davidcariboo/player-scores',
        path='data',
        unzip=True
    )
    print("Download complete!")

if __name__ == "__main__":
    download_datasets()    
    
