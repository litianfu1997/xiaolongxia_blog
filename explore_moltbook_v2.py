import urllib.request
import json
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Get hot posts
url = "https://www.moltbook.com/api/v1/posts?sort=hot&limit=15"

req = urllib.request.Request(url, headers={
    'Authorization': 'Bearer moltbook_sk_xC97Hg-kWQ-YSVmTewoxgqNa8vQAi7Te'
})

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("=== Moltbook Hot Posts ===\n")
        for i, post in enumerate(data.get('posts', [])[:10], 1):
            print(f"{i}. {post.get('title', 'N/A')}")
            print(f"   By: {post.get('author', {}).get('name', 'N/A')}")
            print(f"   Submolt: {post.get('submolt', {}).get('display_name', 'N/A')}")
            if post.get('url'):
                print(f"   Link: {post.get('url')}")
            else:
                content = post.get('content', '')
                if content:
                    preview = content[:150].replace('\n', ' ')
                    print(f"   Preview: {preview}...")
            print(f"   Votes: {post.get('upvotes', 0)} | Comments: {post.get('comment_count', 0)}")
            print()
except Exception as e:
    print(f"Error: {e}")
