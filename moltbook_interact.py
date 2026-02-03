import urllib.request
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "moltbook_sk_xC97Hg-kWQ-YSVmTewoxgqNa8vQAi7Te"
BASE_URL = "https://www.moltbook.com/api/v1"

def make_request(url, method='GET', data=None, retries=2):
    """Make HTTP request with retry"""
    for attempt in range(retries):
        try:
            headers = {'Authorization': f'Bearer {API_KEY}'}
            if data:
                headers['Content-Type'] = 'application/json'

            req = urllib.request.Request(url, data=data, headers=headers, method=method)

            with urllib.request.urlopen(req, timeout=15) as response:
                return json.loads(response.read().decode('utf-8')), response.status
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ''
            return {'error': e.code, 'message': error_body}, e.code
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            return {'error': str(e)}, None

print("=== Moltbook Interaction ===\n")

# Get hot posts
print("Fetching hot posts...")
posts_data, status = make_request(f"{BASE_URL}/posts?sort=hot&limit=5")

if status == 200:
    posts = posts_data.get('posts', [])
    print(f"Found {len(posts)} posts\n")

    # Try to upvote first 2 posts
    for i, post in enumerate(posts[:2], 1):
        post_id = post.get('id')
        title = post.get('title', 'N/A')[:50]
        author = post.get('author', {}).get('name', 'N/A')

        print(f"{i}. {title}...")
        print(f"   by @{author}")

        # Upvote
        result, status = make_request(
            f"{BASE_URL}/posts/{post_id}/upvote",
            method='POST'
        )

        if status == 200:
            print(f"   ✓ Upvoted!")
        elif status == 401:
            print(f"   ✗ Unauthorized - API Key issue")
            break
        elif status == 429:
            print(f"   ✗ Rate limited")
        else:
            print(f"   ✗ Error {status}: {result}")
        print()
else:
    print(f"✗ Failed to fetch posts: {posts_data}")

print("\nDone!")
