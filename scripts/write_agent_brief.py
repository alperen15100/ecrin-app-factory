import os
from pathlib import Path

req = os.environ["APP_REQUEST"].strip()
name = os.environ["APP_NAME"].strip()
pkg = os.environ["PACKAGE_NAME"].strip()

Path("factory-output").mkdir(exist_ok=True)
Path("factory-output/AGENT_BRIEF.md").write_text(f"""# Ecrin App Factory — Agentic Build

Build request:
{req}

Required app name: {name}
Required Android package: {pkg}

You are the autonomous product + Android engineering agent.

Use the configured local AAS Core MCP. Inspect this repository and the request. Search and read the complete AAS catalog across all capabilities relevant to the product. Compare multiple candidate skills where appropriate. You—not AAS—must choose the exact skill IDs. Use AAS compose_stack to validate your exact selection, and persist a valid `aas-stack.json` in the repository root. If supported, also persist selection evidence and a plan.

Before implementation cover: product/market and competitor research when web search can support it, naming/positioning, UX/UI/accessibility, Android architecture, data/storage, integrations, privacy/security, monetization, testing/quality, performance, Play Store policy/readiness, ASO, release/maintenance.

Then IMPLEMENT the requested app. Do not make a fake demo or recipe placeholder. Create a buildable native Android project, preferably Kotlin + Jetpack Compose unless the product requires otherwise. Use the exact package `{pkg}` and visible app name `{name}`. Prefer offline/local and zero-cost open-source components where practical. Minimize permissions and never hardcode secrets.

You may modify/create repository files required for the generated app. Preserve unrelated factory workflows/scripts. Run appropriate checks you can run in the workspace. The workflow after you will build APK and AAB, so leave a valid Gradle project at repository root with an `app` module and preferably a Gradle wrapper.

At the end summarize what you built and any unavoidable limitations.
""", encoding="utf-8")
