import requests
from datetime import datetime
import json

BASE_URL = 'https://hacker-news.firebaseio.com/v0'

def get(url: str, params: dict = {}) -> dict: 
    '''Get request helper function'''
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()


def fetch_maxitem(pretty: bool = False) -> int: 
    '''Fetching Maximum Item through /maxitem.json endpoint

    Returns:
        int - ID of the max item
    '''

    try: 
        params = {}
        if pretty: 
            params['print'] = 'pretty'
        
        resp = get(BASE_URL + '/maxitem.json', params=params)
        return resp
    except requests.exceptions.RequestException as request_error: 
        print(f"Request encountered errors: {request_error}")
    except Exception as error:
        print(f"Unknown error encountered: {error}")


def main():
    
    print(f"Fetching HackerNews Current ({datetime.now().isoformat()}) Max Item...")
    print(f"Max Item ID: {fetch_maxitem()}")


if __name__ == "__main__":
    main()
