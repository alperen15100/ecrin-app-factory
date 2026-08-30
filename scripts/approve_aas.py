import json, re, sys
from pathlib import Path

src = Path(sys.argv[1]).read_text(errors='replace')
out = Path(sys.argv[2])

digest = None
try:
    data = json.loads(src)
    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in {"approvalDigest", "approval_digest", "digest"} and isinstance(v, str) and v:
                    return v
                found = walk(v)
                if found:
                    return found
        elif isinstance(x, list):
            for v in x:
                found = walk(v)
                if found:
                    return found
        return None
    digest = walk(data)
except Exception:
    pass

if not digest:
    m = re.search(r'(?:approvalDigest|approval[_ -]?digest)\s*[=:]\s*["\']?([A-Za-z0-9._:+/=-]{12,})', src, re.I)
    if m:
        digest = m.group(1)

if not digest:
    print(src)
    raise SystemExit("Could not parse AAS approval digest")

out.write_text(digest)
print("AAS approval digest captured")
