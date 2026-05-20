import requests
import json

BASE_URL = 'https://hacker-news.firebaseio.com/v0'

def get(url: str) -> dict: 
    '''Get request helper function'''
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()


def main():
    print("Hello from hackernews-playground!")


if __name__ == "__main__":
    main()
