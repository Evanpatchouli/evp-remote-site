"""Capture the November draft. Run before detection or when comparing revisions."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parent
SKILL = SITE.parent / "evp-remote/.agents/skills/lieflat-less-ai-tone"
SNAP = HERE / "snapshot"
manifest = {}


def save(name, source, lines, mapping, exclusions):
    target = SNAP / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    manifest[name] = dict(source=source.relative_to(SITE).as_posix(),
                          source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                          snapshot_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                          lines=mapping, excluded=exclusions)


for path in [*sorted((SITE / "docs/guide").glob("*.md")), SITE / "docs/copyright.md"]:
    lines, mapping, excluded = [], {}, []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if re.fullmatch(r"!\[[^]]*]\([^)]*\)|<ClientDownload\s*/>", line.strip()):
            excluded.append(dict(line=n, source=line))
            line = ""
        else:
            line = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", line)
            line = line.replace("**", "").replace(chr(96), "")
        lines.append(line)
        if line:
            mapping[n] = n
    save(path.name, path, lines, mapping, excluded)

# Source-anchored transcription of Chinese template blocks and alternate UI states.
templates = {
    "Home": [
        ("- ", "FIELD GUIDE / 使用手册"), ("## ", "你想连接哪台电脑？"),
        ("### ", "亲友的电脑"), ("", "让对方创建邀请码。默认需要本人同意，才会共享桌面。"),
        ("### ", "自己的电脑"), ("", "两台电脑配对一次。允许远控后，下次从设备列表连接。")],
    "OrbitHero": [
        ("", "用邀请码帮亲友操作电脑，或从设备列表连回自己的 Windows 桌面。"),
        ("- ", "使用指南"), ("- ", "WINDOWS x64 / 非商业使用"), ("- ", "向下探索 ↓"),
        ("- ", "▷ 播放动效"), ("- ", "Ⅱ 暂停动效"), ("- ", "静态视图")],
    "ClientDownload": [("- ", "下载 Windows 客户端"), ("- ", "下载地址尚未配置")]
}
for component, blocks in templates.items():
    path = SITE / f"docs/.vitepress/theme/{component}.vue"
    visible = [re.sub(r"<[^>]*>", "", line) for line in path.read_text(encoding="utf-8").splitlines()]
    lines, mapping = [], {}
    for prefix, label in blocks:
        matches = [i for i, line in enumerate(visible, 1) if label in line]
        assert len(matches) == 1, (component, label, matches)
        mapping[len(lines) + 1] = matches[0]
        lines.extend([prefix + label, ""])
    save(component + ".md", path, lines, mapping,
         ["脚本、模板标记、属性、装饰图形、纯英文品牌与编号；下载组件按定义去重。"])

(HERE / "sources.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
for name, flag in [("before.json", "--json"), ("candidates.json", "--candidates")]:
    result = subprocess.run([sys.executable, "-X", "utf8", SKILL / "scripts/detect.py", SNAP, flag],
                            capture_output=True, check=True)
    (HERE / name).write_bytes(result.stdout)
