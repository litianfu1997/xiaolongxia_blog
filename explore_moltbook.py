import urllib.request
import json

# Get hot posts
url = "https://www.moltbook.com/api/v1/posts?sort=hot&limit=10"

req = urllib.request.Request(url, headers={
    'Authorization': 'Bearer moltbook_sk_xC97Hg-kWQ-YSVmTewoxgqNa8vQAi7Te'
})

try:
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("=== Moltbook 热门帖子 ===\n")
        for post in data.get('posts', [])[:5]:
            print(f"标题: {post.get('title', 'N/A')}")
            print(f"作者: {post.get('author', {}).get('name', 'N/A')}")
            print(f"社区: {post.get('submolt', {}).get('display_name', 'N/A')}")
            print(f"内容预览: {post.get('content', 'N/A')[:200]}...")
            print(f"点赞: {post.get('upvotes', 0)} | 评论: {post.get('comment_count', 0)}")
            print("-" * 80)
except Exception as e:
    print(f"Error: {e}")
