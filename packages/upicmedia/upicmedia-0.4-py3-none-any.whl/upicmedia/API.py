import requests
import os

def get_datasets(auth_token: str):
    """
    Function to get a list of available datasets from the Upic Media API.
    
    Parameters:
        auth_token (str): The authentication token to access the API.
        
    Returns:
        list: A list of datasets if the request is successful.
    """
    url = "https://upic.media/api/classes/index"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        datasets = response.json()  # Assuming the response is in JSON format
        return datasets
    except requests.exceptions.RequestException as e:
        print(f"Error fetching datasets: {e}")
        return []


def download_dataset(slug: str, save_path: str):
    url = f"https://upic.media/api/classes/files?slug={slug}"
    
    headers = {
        "authority": "http://upic.media",
        "Accept": "application/json",
        "accept-language": "fr-FR",
        "content-type": "application/json",
        "origin": "http://upic.media",
        "referer": "http://upic.media",
        "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Authorization": "Bearer e62e6196c7cd4270debcba99d94c23a0bb2defa64b4469f6cbd60c2cd6461104265777d13b3922ae3d147d2b29a7b5f8445fa27fe03ce2e756e348cdd4eacd9c",
        "X-Requested-With": "XMLHttpRequest"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully to {save_path}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


import requests

def download_dataset(slug: str, save_path: str, auth_token: str):
    """
    Function to download a dataset from Upic Media API.
    
    Parameters:
        slug (str): The slug (identifier) of the dataset to download.
        save_path (str): The path where the dataset should be saved.
        auth_token (str): The authentication token to access the API.
        
    Returns:
        bool: True if the dataset was successfully downloaded, False otherwise.
    """
    url = f"https://upic.media/api/classes/files?slug={slug}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        # Send GET request to download the dataset
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Assuming the response contains the URL to the actual dataset file
        dataset_url = response.json().get("url")  # Assuming the 'url' key contains the dataset URL
        
        if not dataset_url:
            print(f"Error: Dataset URL not found for slug '{slug}'")
            return False
        
        # Download the actual file
        dataset_response = requests.get(dataset_url)
        dataset_response.raise_for_status()  # Raise an error for bad responses
        
        # Save the file
        with open(save_path, 'wb') as f:
            f.write(dataset_response.content)
        
        print(f"Dataset '{slug}' successfully downloaded to {save_path}")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading dataset: {e}")
        return False
