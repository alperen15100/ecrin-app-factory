#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

def clean(s):
    return " ".join((s or "").strip().split())

def infer_name(request):
    r = request.lower()
    if "pdf" in r and ("image" in r or "photo" in r):
        return "ImagePDF"
    if "compress" in r and ("image" in r or "photo" in r):
        return "CompressX"
    if "compress" in r and "video" in r:
        return "VideoCompress"
    if "ocr" in r or "scan" in r:
        return "ScanLens"
    if "file" in r and "search" in r:
        return "FindAnything"
    return "Ecrin App"

def infer_features(request):
    r = request.lower()
    features = []
    if any(x in r for x in ["offline", "local", "without internet"]):
        features.append("Offline-first processing")
    if "pdf" in r:
        features += ["PDF generation", "PDF preview and share"]
    if any(x in r for x in ["image", "photo", "picture"]):
        features += ["Gallery image picker", "Image preview"]
    if "compress" in r:
        features += ["Compression quality control", "Before/after size comparison"]
    if "ocr" in r or "scan" in r:
        features += ["Document/image scanning", "OCR text extraction"]
    if "search" in r:
        features += ["Fast local search", "Search history"]
    if "video" in r:
        features += ["Video picker", "Video processing progress"]
    if not features:
        features = ["Core app workflow", "Recent items", "Settings"]
    # unique preserve order
    out = []
    for x in features:
        if x not in out:
            out.append(x)
    return out[:10]

def infer_permissions(request):
    r = request.lower()
    perms = []
    if any(x in r for x in ["image", "photo", "video", "pdf", "file", "scan"]):
        perms.append("Use Android Photo Picker / Storage Access Framework; avoid broad storage permission")
    if "camera" in r or "scan" in r:
        perms.append("CAMERA only when user starts scanning")
    if any(x in r for x in ["offline", "local", "without internet"]):
        perms.append("No INTERNET permission unless ads/analytics are enabled")
    return perms or ["No dangerous permissions by default"]

def infer_architecture(request, monetization):
    return {
        "language": "Kotlin",
        "ui": "Jetpack Compose",
        "architecture": "MVVM + Repository",
        "local_storage": "Room/DataStore when persistent data is needed",
        "background_work": "WorkManager for long-running user-visible jobs when needed",
        "dependency_injection": "Hilt only if project complexity justifies it",
        "build": "Gradle + GitHub Actions",
        "release": "APK debug + AAB release",
        "monetization": monetization
    }

def screens_for(request):
    r = request.lower()
    screens = ["Splash", "Home"]
    if any(x in r for x in ["image", "photo", "video", "pdf", "file", "scan"]):
        screens += ["Picker / Import", "Preview"]
    if any(x in r for x in ["compress", "convert", "pdf", "scan", "ocr"]):
        screens += ["Processing", "Result"]
    screens += ["Settings"]
    out=[]
    for s in screens:
        if s not in out:
            out.append(s)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", required=True)
    ap.add_argument("--package", required=True)
    ap.add_argument("--monetization", choices=["ads", "free", "freemium"], default="ads")
    args = ap.parse_args()

    req = clean(args.request)
    pkg = clean(args.package)

    if not re.fullmatch(r"[a-zA-Z_]\w*(\.[a-zA-Z_]\w*){2,}", pkg):
        raise SystemExit("Invalid Android package name: " + pkg)

    name = infer_name(req)
    features = infer_features(req)
    spec = {
        "factory": "Ecrin App Factory V1",
        "brand": "Ecrin Labs",
        "request": req,
        "app_name": name,
        "package_name": pkg,
        "platform": "Android",
        "min_sdk": 26,
        "target_strategy": "Use current stable Play-compatible SDK in build stage",
        "features": features,
        "screens": screens_for(req),
        "permissions_policy": infer_permissions(req),
        "architecture": infer_architecture(req, args.monetization),
        "quality_rules": [
            "Preserve working builds",
            "No secrets in repository",
            "Minimal Android permissions",
            "Offline/local processing preferred where practical",
            "Validate APK/AAB in GitHub Actions before release"
        ],
        "next_stage": "Generate native Android Kotlin/Compose project from this specification"
    }

    out = Path("output")
    out.mkdir(exist_ok=True)
    (out / "app-spec.json").write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")

    feature_lines = "\n".join(f"- {x}" for x in spec["features"])
    screen_lines = "\n".join(f"- {x}" for x in spec["screens"])
    perm_lines = "\n".join(f"- {x}" for x in spec["permissions_policy"])

    plan = f"""# Ecrin App Factory V1 — Build Plan

## Request
{req}

## Product
- App name: **{name}**
- Package: `{pkg}`
- Brand: **Ecrin Labs**
- Platform: Android
- Monetization: {args.monetization}

## Core features
{feature_lines}

## Screens
{screen_lines}

## Permission policy
{perm_lines}

## Technical baseline
- Kotlin
- Jetpack Compose
- MVVM + Repository
- Room/DataStore only when required
- WorkManager for suitable long-running jobs
- GitHub Actions build pipeline
- APK + AAB validation

## Factory execution order
1. Product scope
2. Compose UI shell
3. Core feature implementation
4. Local persistence if required
5. Tests
6. Systematic debugging
7. Code review
8. GitHub Actions APK/AAB build
9. Pre-release review
10. Play Store ASO package

## Next stage
V2 will consume `app-spec.json` and generate the actual Android project scaffold.
"""
    (out / "BUILD_PLAN.md").write_text(plan, encoding="utf-8")

    print(f"Generated plan for: {name}")
    print(f"Package: {pkg}")
    print(f"Features: {len(features)}")
    print("Output: output/app-spec.json")
    print("Output: output/BUILD_PLAN.md")

if __name__ == "__main__":
    main()
