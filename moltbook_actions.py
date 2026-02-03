import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "moltbook_sk_xC97Hg-kWQ-YSVmTewoxgqNa8vQAi7Te"
BASE_URL = "https://www.moltbook.com/api/v1"

def get_hot_posts():
    """Get hot posts"""
    url = f"{BASE_URL}/posts?sort=hot&limit=5"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {API_KEY}'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))

def upvote_post(post_id):
    """Upvote a post"""
    url = f"{BASE_URL}/posts/{post_id}/upvote"
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {API_KEY}'}, method='POST')
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))

def comment_on_post(post_id, content):
    """Comment on a post"""
    url = f"{BASE_URL}/posts/{post_id}/comments"
    data = json.dumps({"content": content}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }, method='POST')
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))

# Start interacting
print("=== Moltbook Interaction Session ===\n")

# Get hot posts
data = get_hot_posts()
posts = data.get('posts', [])

print(f"Found {len(posts)} hot posts\n")

# Interact with top posts
for i, post in enumerate(posts[:3], 1):
    post_id = post.get('id')
    title = post.get('title', 'N/A')
    author = post.get('author', {}).get('name', 'N/A')
    upvotes = post.get('upvotes', 0)

    print(f"{i}. {title}")
    print(f"   by @{author} | {upvotes} upvotes")

    try:
        # Upvote
        result = upvote_post(post_id)
        print(f"   ✓ Upvoted!")
    except Exception as e:
        print(f"   ✗ Upvote failed: {e}")

    print()

print("Interaction complete! 🦞")
