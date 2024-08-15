import os
from huggingface_hub import HfApi, snapshot_download, login
import requests

# Replace these with your Hugging Face username, access token, and the directory you want to use for the backup
HF_USERNAME = '{YOUR_HF_USERNAME}'
HF_ACCESS_TOKEN = '{YOUR_HF_ACCESS_TOKEN}'
BACKUP_DIR = '{YOUR_BACKUP_DIR}'

# Log in to Hugging Face using the access token
login(token=HF_ACCESS_TOKEN)

# Initialize the Hugging Face API
api = HfApi()

# Ensure backup directory exists
os.makedirs(BACKUP_DIR, exist_ok=True)

# Function to download models
def download_models(username, backup_dir):
    models = api.list_models(author=username, token=HF_ACCESS_TOKEN)
    for model in models:
        model_name = model.modelId
        model_dir = os.path.join(backup_dir, 'models', model_name)
        if os.path.exists(model_dir):
            print(f"Model {model_name} already exists, skipping...")
        else:
            print(f"Downloading model: {model_name}...")
            snapshot_download(repo_id=model_name, local_dir=model_dir, token=HF_ACCESS_TOKEN)

# Function to download spaces
def download_spaces(username, backup_dir):
    spaces = api.list_spaces(author=username, token=HF_ACCESS_TOKEN)
    for space in spaces:
        space_name = space.id
        space_dir = os.path.join(backup_dir, 'spaces', space_name)
        if os.path.exists(space_dir):
            print(f"Space {space_name} already exists, skipping...")
        else:
            print(f"Downloading space: {space_name}...")
            space_url = f"https://huggingface.co/spaces/{space_name}/resolve/main"
            os.makedirs(space_dir, exist_ok=True)
            # Assuming the space is a repository of files
            download_space_files(space_url, space_dir)

# Helper function to download files from a space
def download_space_files(url, local_dir):
    main_zip_path = os.path.join(local_dir, 'main.zip')
    if os.path.exists(main_zip_path):
        print(f"File {main_zip_path} already exists, skipping...")
    else:
        response = requests.get(url)
        if response.status_code == 200:
            with open(main_zip_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Failed to download space from {url}: {response.status_code}")

if __name__ == "__main__":
    download_models(HF_USERNAME, BACKUP_DIR)
    download_spaces(HF_USERNAME, BACKUP_DIR)
