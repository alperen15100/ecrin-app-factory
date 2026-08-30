import os
from pathlib import Path

request = os.environ["APP_REQUEST"].strip()
app_name = os.environ["APP_NAME"].strip()
package_name = os.environ["PACKAGE_NAME"].strip()

brief = f'''# Ecrin App Factory — Agentic Build

You are the primary coding agent. Build a real, installable, production-minded Android application from the user's request.

USER REQUEST:
{request}

APP NAME: {app_name}
PACKAGE: {package_name}
BRAND: Ecrin Labs

## Mandatory AAS Core process

AAS Core is configured as a local MCP server in this Codex session.
Before editing the app, inspect this repository and use the AAS Core tools to search and read the complete local AAS catalog.

Enumerate the primary capability areas of this requested product. At minimum evaluate:
- architecture/runtime
- Android language/framework choices
- domain behavior
- data/storage
- external integrations
- testing/quality
- security/privacy
- UI/UX/accessibility
- deployment/operations
- maintenance workflow
- product positioning, competitor/research needs, monetization, ASO/launch when applicable

For each applicable capability, perform focused AAS searches and inspect multiple plausible skills when available. Do not stop at a tiny generic shortlist. Select a non-redundant stack that covers the real product.
Use compose_stack and inspect_stack. Persist the final exact selection as `aas-stack.json` in the repository root. If the AAS tools support evidence export in this session, also persist `aas-selection-evidence.json`.

## Product work

Do not use the old hard-coded recipe generator as the solution. The user's natural-language request is the source of truth.

Before coding, perform a lightweight current competitor/product analysis. Web search is enabled for this Codex run; use it when useful. Cite the competitor names/sources you actually checked in `factory-output/PRODUCT_REPORT.md`. If search is unexpectedly unavailable, explicitly state that limitation and do not fabricate current competitors or statistics.

Create `factory-output/PRODUCT_REPORT.md` containing:
- target user
- core problem
- key competitors or competitor archetypes
- differentiation
- monetization recommendation
- final app name recommendation
- UI direction
- Play Store/ASO positioning

Then design and implement the Android app. Requirements:
- Native Kotlin + Jetpack Compose unless a selected skill gives a compelling reason otherwise.
- Package name must be exactly `{package_name}`.
- App display name should be `{app_name}` unless your product analysis recommends a clearly better user-facing name; if changed, document it.
- Mobile-first polished UI, not a demo screen.
- Implement the requested core functionality for real; no fake buttons or placeholder success messages.
- Prefer offline/local processing and zero-cost open-source libraries where practical.
- Minimal Android permissions.
- No embedded secrets.
- Handle errors and empty states.
- Add appropriate tests.
- Make the project buildable on GitHub Actions with Java 17.
- Generate both debug APK and release AAB with `assembleDebug` and `bundleRelease` without requiring a private signing key. Release may use unsigned/default build output; do not block the build on signing.

Inspect existing working files before replacing them. Preserve useful working pieces, but you may replace the old generated sample app if needed.

## Validation and recovery

Run available tests/build commands yourself when possible. Fix compile errors you encounter. Do not stop after merely writing code.

Also create:
- `factory-output/BUILD_SUMMARY.md` — what was built, architecture, selected AAS skills, important limitations, manual test checklist.
- `factory-output/APP_REQUEST.txt` — exact user request.

If AAS Core exposes a supported immutable planning command/tool usable from the session, create `aas-plan.json`; otherwise document why it was not produced rather than inventing it.

Finish only when the repository contains a coherent Android project ready for the workflow's Gradle build step.
'''

Path("factory-output").mkdir(exist_ok=True)
Path("factory-output/AGENT_BRIEF.md").write_text(brief)
Path("factory-output/APP_REQUEST.txt").write_text(request + "\n")
print("Agent brief written")
