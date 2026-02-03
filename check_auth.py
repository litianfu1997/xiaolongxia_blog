import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "moltbook_sk_xC97Hg-kWQ-YSVmTewoxgqNa8vQAi7Te"

# Check if API key is valid by getting agent info
print("Checking API key validity...")

try:
    url = "https://www.moltbook.com/api/v1/agents/me"
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {API_KEY}'
    })
    with urllib.request.urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("✓ API Key is valid!")
        print(json.dumps(data, indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    print(f"✗ HTTP Error {e.code}: {e.reason}")
    try:
        error_body = e.read().decode('utf-8')
        print(f"Error details: {error_body}")
    except:
        pass
except Exception as e:
    print(f"✗ Error: {e}")
