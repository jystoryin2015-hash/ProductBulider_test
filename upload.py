import base64
import json
import os
import urllib.request

OWNER = "jystoryin2015-hash"
REPO = "ProductBulider_test"
FILES = ["hello.py", "help.py", "index.html", "contact.html", "contact/index.html", "upload.py"]
TOKEN = os.environ.get("GITHUB_TOKEN")

if not TOKEN:
    raise SystemExit("GITHUB_TOKEN 환경 변수가 필요합니다.")

def upload(file_path):
    with open(file_path, "rb") as f:
        content = base64.b64encode(f.read()).decode('utf-8')
    
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{file_path}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "CodexUpload",
    }
    
    # Get SHA
    sha = None
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as res:
            sha = json.loads(res.read().decode())["sha"]
    except:
        pass

    payload = {"message": f"Upload {file_path}", "content": content}
    if sha: payload["sha"] = sha

    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={**headers, "Content-Type": "application/json"}, method="PUT")
    with urllib.request.urlopen(req) as res:
        print(f"Uploaded {file_path}")

for f in FILES:
    try:
        upload(f)
    except Exception as e:
        print(f"Failed {f}: {e}")
