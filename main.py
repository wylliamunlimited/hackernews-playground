import requests
from datetime import datetime
import time
from collections import defaultdict, deque

BASE_URL = 'https://hacker-news.firebaseio.com/v0'


def get(url: str, params=None, retry_attempt: int = 3) -> dict: 
    '''Get request helper function'''
    for i in range(retry_attempt):
        try:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e: 
            if i == retry_attempt - 1:
                raise
            time.sleep(2 ** i)
            


def fetch_item(id: str, pretty: bool = False) -> dict: 
    '''Fetching item through /item/<id>.json

    Returns:
        dict - details of the fetched item
    '''

    params = {}
    if pretty:
        params['print'] = 'pretty'
    
    resp = get(BASE_URL + f'/item/{id}.json')
    return resp


def fetch_maxitem(pretty: bool = False) -> int: 
    '''Fetching Maximum Item through /maxitem.json endpoint

    Returns:
        int - ID of the max item
    '''

    params = {}
    if pretty: 
        params['print'] = 'pretty'
    
    resp = get(BASE_URL + '/maxitem.json', params=params)
    return resp


def fetch_top_stories(pretty: bool = False) -> list: 
    '''Fetching the top 500 stories through /topstories endpoint 

    Returns: 
        list(int) - List of IDs
    '''

    params = {}
    if pretty: 
        params['print'] = 'pretty'
    
    resp = get(BASE_URL + '/topstories.json', params=params)
    return resp


def count_comments(story_ids: list[int]) -> dict:
    '''Traverse function - walking each node and their corresponding kids
    '''
    counter = defaultdict(int)

    for id in story_ids:
        print(f"Walking story {id}...")
        q = deque([id])
        counter[id] = -1

        while q:
            item_id = q.pop()
            counter[id] += 1
            data = fetch_item(id=item_id) # API Call
            for kid in data.get('kids', []):
                q.append(kid)
        
    return counter


def deepest_reply_chain(item_id: int):
    '''Traverse function - getting the longest comment thread
    '''
    
    item_data = fetch_item(item_id)
    if not item_data:
        return []
    
    kids = item_data.get('kids', [])
    if not kids:
        return [item_id]

    best_child_chain = max(
        (deepest_reply_chain(kid) for kid in kids),
        key=len
    )

    return [item_id] + best_child_chain
    

def longest_comment(story_id: int): 
    '''Traverse function - getting the longest comment thread
    '''

    comments = fetch_item(id=story_id).get('kids', [])
    q = deque((kid, 1) for kid in comments)
    max_depth = 0

    while q: 
        item_id, depth = q.popleft()
        max_depth = max(depth, max_depth)

        data = fetch_item(item_id)

        if data:
            for kid in data.get('kids', []):
                q.append((kid, depth + 1))
    return max_depth

def longest_comment_dfs(story_id: int):

    comments = fetch_item(id=story_id).get('kids', [])

    stack = [(c, 1) for c in comments]
    max_depth = 0
    
    while stack: 
        item_id, depth = stack.pop()

        max_depth = max(depth, max_depth)

        item_data = fetch_item(item_id)

        if item_data:
            for kid in item_data.get('kids', []):
                stack.append((kid, depth + 1))
    return max_depth

    

def main():
    
    # Fetch Max Item
    # print(f"Fetching HackerNews Current ({datetime.now().isoformat()}) Max Item...")
    # maxitem_id = fetch_maxitem()
    # print(f"Max Item ID: {maxitem_id}")

    print(f"Fetching top stories ({datetime.now().isoformat()})...")
    ids = fetch_top_stories()
    print(f"IDs fetched: {ids[:5]}")
    print()
    item_data = fetch_item(ids[4])
    
    # Fetch Details
    # for id in ids[:5]: 
    #     print(f"Fetching the details for {id}...")
    #     data = fetch_item(id)
    #     print(f"data: {json.dumps(data, indent=4)}")
    #     print()

    print(f"Fetching the deepest comment depth for {ids[4]} - {item_data.get('title')}...")
    depth, depth_dfs = longest_comment(ids[4]), longest_comment_dfs(story_id=ids[4])
    print(f"For Story {ids[4]} - Deepest Comment at depth = {depth} [BFS] vs {depth_dfs} [DFS]")

    print(f"Finding the deepest child thread for {ids[4]}...")
    deepest_chain = deepest_reply_chain(ids[4])
    print(f"Chain: {deepest_chain}")

    # Count Comments
    counter = count_comments(ids[:10])
    print()
    for k, v in counter.items():
        print(f"Item {k} ==> {v} comments")
    print()


if __name__ == "__main__":
    main()
