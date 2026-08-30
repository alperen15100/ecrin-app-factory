import json, re, sys
src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
digest = None
try:
    obj = json.loads(text)
    for key in ("approvalDigest", "approval_digest", "digest"):
        if isinstance(obj, dict) and obj.get(key):
            digest = str(obj[key])
            break
except Exception:
    pass
if not digest:
    m = re.search(r'(?i)"?approval(?:_|-)?digest"?\s*[:=]\s*"([^"]+)"', text)
    if m:
        digest = m.group(1)
if not digest:
    print(text)
    raise SystemExit("Could not find AAS approval digest")
open(dst, "w", encoding="utf-8").write(digest)
print("AAS approval digest captured")
