import importlib.util
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path("/opt/data/solace-skin-lab")
PROMPT_FILE = ROOT / "prompt_pilot_free_facial_v2.md"
OUT = ROOT / "images" / "pilot-v2-free-facial.png"
REPORT = ROOT / "pilot-v2-report.json"

# The creative profile contains the migrated Codex/ChatGPT OAuth credential.
os.environ["HERMES_HOME"] = "/opt/data/profiles/creative"
os.environ["OPENAI_IMAGE_MODEL"] = "gpt-image-2-high"

text = PROMPT_FILE.read_text(encoding="utf-8")
match = re.search(r"```text\n(.*?)\n```", text, re.S)
if not match:
    raise RuntimeError("No se encontró el bloque de prompt")
prompt = match.group(1).strip()

module_path = "/opt/data/hermes-agent/plugins/image_gen/openai-codex/__init__.py"
spec = importlib.util.spec_from_file_location("openai_codex_image_backend_pilot_v2", module_path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"No se pudo cargar {module_path}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
provider = module.OpenAICodexImageGenProvider()
result = provider.generate(prompt=prompt, aspect_ratio="square")
if not result.get("success"):
    REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    raise RuntimeError(json.dumps(result, ensure_ascii=False))

OUT.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(result["image"], OUT)
report = {
    "success": True,
    "provider": result.get("provider", "openai-codex"),
    "model": result.get("model"),
    "size": result.get("size"),
    "quality": result.get("quality", "high"),
    "image": str(OUT),
    "source_image": result.get("image"),
}
REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
