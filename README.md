# HackerNews Playground 

Created At: 5/20/2026
> [!info] I just found HackerNews has an API and this is an exploratory repo.

## State So-Far

### 1. Counting comments 

`count_comments()` function counts the number of comments within a story. It takes in a list of story ids, and walks the thread for each of the story. This uses BFS traversal, each loop calling the `/item/<id>.json` endpoint.


### 2. Deepest Reply Chain

`deepest_reply_chain()` function walks comment threads under a story and derive the full thread leading to the comment that resides in the deepest layer. Recursion approach with comparison each recursion. Function takes in one story_id as integer. 


### 3. Longest Comment (DFS / BFS)

`longest_comment()` gets the depth of the longest comment thread - similar to (2) but this returns the count of comments to get there. BFS/DFS are both implemented (just for fun lol). Function takes in 1 story_id as usual.


## Setup 

Clone the repo then run...

```bash
uv sync
source .venv/bin/activate
```

## Running it

```bash 
uv run main.py
```
