#!/usr/bin/env python3
import json
from pathlib import Path

p = Path("factory/stack.json")
if not p.exists():
    raise SystemExit("factory/stack.json missing")

data = json.loads(p.read_text(encoding="utf-8"))
skills = data.get("skills", [])
required = [
    "brainstorming",
    "concise-planning",
    "app-builder",
    "android-dev",
    "mobile-design",
    "test-driven-development",
    "systematic-debugging",
    "code-reviewer",
    "github-actions-templates",
    "pre-release-review",
    "app-store-optimization",
    "launch-strategy",
]
missing = [x for x in required if x not in skills]
duplicates = sorted({x for x in skills if skills.count(x) > 1})
if missing:
    raise SystemExit("Missing skills: " + ", ".join(missing))
if duplicates:
    raise SystemExit("Duplicate skills: " + ", ".join(duplicates))
print(f"OK: {data['name']} v{data['version']}")
print(f"Skills: {len(skills)}")
print("Stack validation passed.")
