#!/usr/bin/env python3
"""Scaffold a new local ecological-agriculture domain expert."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
CODEX_SKILLS_ROOT = WORKSPACE_ROOT / ".codex" / "skills"
KB_ROOT = WORKSPACE_ROOT / "knowledgebase"
ORCH_ROOT = CODEX_SKILLS_ROOT / "ecological-agriculture-orchestrator"
DOMAIN_EXPERTS_DIR = ORCH_ROOT / "references" / "domain-experts"
REGISTRY_PATH = ORCH_ROOT / "references" / "domain-expert-registry.md"
SKILL_MAP_PATH = ORCH_ROOT / "references" / "specialist-skill-map.md"
AGENTS_PATH = WORKSPACE_ROOT / "AGENTS.md"

REQUIRED_KEYS = {
    "folder",
    "skill_name",
    "display_name",
    "short_description",
    "expert_name",
    "focus",
    "mission",
    "core_lens",
    "when_to_use",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, help="Path to the domain expert JSON spec.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite generated files if they already exist.")
    parser.add_argument("--update-agents", action="store_true", help="Also update the local AGENTS.md knowledge-center and skill-location lists.")
    parser.add_argument("--dry-run", action="store_true", help="Print the files that would be created or updated without writing them.")
    return parser.parse_args()


def load_spec(path: Path) -> dict:
    spec = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(spec, dict):
        raise ValueError("Spec must be a JSON object.")
    missing = sorted(REQUIRED_KEYS - set(spec))
    if missing:
        raise ValueError(f"Spec is missing required keys: {', '.join(missing)}")
    if not isinstance(spec["when_to_use"], list) or not spec["when_to_use"]:
        raise ValueError("when_to_use must be a non-empty list.")
    for key in REQUIRED_KEYS - {"when_to_use"}:
        if not str(spec[key]).strip():
            raise ValueError(f"{key} must be a non-empty string.")
    spec.setdefault("default_handoffs", [])
    spec.setdefault("discovery_queries", [])
    spec.setdefault("anchor_files", [])
    return spec


def normalize_yaml_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def card_filename(folder: str) -> str:
    return folder.replace("_", "-") + ".md"


def ensure_write(path: Path, content: str, overwrite: bool, dry_run: bool) -> str:
    if path.exists() and not overwrite:
        return f"exists: {path}"
    if dry_run:
        return f"write: {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"write: {path}"


def build_skill_md(spec: dict) -> str:
    folder = spec["folder"]
    skill_name = spec["skill_name"]
    display_name = spec["display_name"]
    lines = [
        "---",
        f"name: {skill_name}",
        f"description: Use this skill when the user needs domain-specific ecological agriculture reasoning from `{KB_ROOT / folder}`, especially for {spec['focus']}.",
        "---",
        "",
        f"# {display_name}",
        "",
        "## Overview",
        "",
        f"This local specialist skill owns reasoning for `{folder}` in the ecological agriculture knowledgebase. It should answer from this domain first, using the local literature in `{KB_ROOT / folder}` and the attached expert brief.",
        "",
        "If this skill is being used by the orchestrator as an isolated sub-agent, do not assume what the other specialists think. Work only from your own domain scope until the orchestrator asks a follow-up question that intentionally shares outside findings.",
        "",
        "## Use This Skill When",
        "",
    ]
    lines.extend(f"- {item}" for item in spec["when_to_use"])
    lines.extend(
        [
            "",
            "## Working Rules",
            "",
            "- Search local sources first: start with `references/taxonomy.md`, then `references/expert-brief.md`, then the mapped files in the primary folder.",
            "- After exhausting local sources, you may search the internet for additional scientific context when the local folder is thin, conflicting, incomplete, or missing a mechanism required by the question.",
            "- When browsing, prefer primary literature, extension publications, and other high-quality technical sources.",
            "- Distinguish clearly between local-source evidence and outside-source context in your answer.",
            f"- Primary folder scope: `{KB_ROOT / folder}`",
            "- Read `references/expert-brief.md` before answering.",
            "- Read `references/taxonomy.md` before answering and use it to route the question to the most relevant local source files.",
            "- Stay inside this domain unless the user explicitly asks for wider synthesis.",
            "- If another domain clearly matters, name it and explain why, but do not synthesize it yourself unless the user directly asks you to broaden scope.",
            "- When used as an isolated specialist, do not assume other experts' answers.",
            "",
            "## Output Contract",
            "",
            "- Give the strongest answer supported by this domain.",
            "- Explain the mechanism, not just the conclusion.",
            "- State important caveats or uncertainty.",
            "- Name the next domains that should be checked if the question is broader than this skill.",
            "- List the specific local files used.",
            "- List any external sources used after the local pass, if any.",
            "",
            "## Resources",
            "",
            "- `references/expert-brief.md`",
            f"  Domain brief for `{folder}`.",
            "- `references/taxonomy.md`",
            f"  Retrieval-oriented map for routing questions inside `{folder}`.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_openai_yaml(spec: dict) -> str:
    prompt = (
        f"Use ${spec['skill_name']} to answer a domain-specific ecological agriculture "
        "question from the local knowledgebase."
    )
    return "\n".join(
        [
            "interface:",
            f"  display_name: {normalize_yaml_string(spec['display_name'])}",
            f"  short_description: {normalize_yaml_string(spec['short_description'])}",
            f"  default_prompt: {normalize_yaml_string(prompt)}",
        ]
    ) + "\n"


def build_expert_brief(spec: dict) -> str:
    lines = [
        f"# Domain Expert: {spec['display_name'].replace('EcoAg ', '')}",
        "",
        f"- Expert name: {spec['expert_name']}",
        f"- Knowledgebase folder: `{KB_ROOT / spec['folder']}`",
        f"- Domain mission: {spec['mission']}",
        "",
        "## Expert Lens",
        "",
        spec["core_lens"],
        "",
        "## Use This Expert When",
        "",
    ]
    lines.extend(f"- {sentence[0].upper() + sentence[1:] if sentence else sentence}" for sentence in spec["when_to_use"])
    lines.extend(["", "## Default Handoffs", ""])
    if spec["default_handoffs"]:
        lines.extend(f"- {item}" for item in spec["default_handoffs"])
    else:
        lines.append("- Add neighboring experts after the first integration pass.")
    lines.extend(
        [
            "",
            "## Indexed Resources",
            "",
            "- Add local PDFs, `.url` shortcuts, and synthesis notes here after paper intake.",
            "",
            "## Specialist Output Contract",
            "",
            "- Answer from this domain first, not from generic gardening intuition.",
            "- Explain the mechanism behind the recommendation.",
            "- State what this domain cannot decide alone.",
            "- Name the neighboring experts that should be consulted next if the question is cross-domain.",
            "- List the specific local files used.",
        ]
    )
    if spec["anchor_files"]:
        lines.extend(["", "## Anchor Files", ""])
        lines.extend(f"- `{item}`" for item in spec["anchor_files"])
    return "\n".join(lines) + "\n"


def build_taxonomy(spec: dict) -> str:
    lines = [
        f"# {spec['display_name'].replace('EcoAg ', '')} Retrieval Taxonomy",
        "",
        f"Purpose: route questions in `{KB_ROOT / spec['folder']}` to the fastest relevant local source and identify what still needs to be downloaded or synthesized.",
        "",
        "## 1. Major Themes",
        "",
        "- Add the major domain themes and subthemes once papers are in the folder.",
        "",
        "## 2. Question Routing Patterns",
        "",
        "- Route concrete question types to exact local files after paper intake.",
        "",
        "## 3. Source Inventory",
        "",
        "- `references/expert-brief.md`",
        f"  Initial domain framing for `{spec['folder']}`.",
        f"- `{KB_ROOT / spec['folder']}`",
        "  Add each downloaded PDF, `.url`, or local synthesis note here with a one-line relevance summary.",
        "",
        "## 4. Search Cues",
        "",
    ]
    if spec["discovery_queries"]:
        lines.extend(f"- `{query}`" for query in spec["discovery_queries"])
    else:
        lines.append("- Add discovery queries after defining the first paper-search pass.")
    lines.extend(
        [
            "",
            "## 5. Unresolved Gaps / Weak Evidence",
            "",
            "- Add the missing mechanisms, missing crops, or weak evidence areas after the first paper set is ingested.",
            "",
            "## 6. Domain Resources",
            "",
            "- Add matrices, process guides, troubleshooting maps, or timelines here when the domain needs structured retrieval beyond the paper set.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_registry_section(spec: dict) -> str:
    return "\n".join(
        [
            f"## {spec['expert_name']}",
            "",
            f"- Folder: `{spec['folder']}`",
            f"- Card: `references/domain-experts/{card_filename(spec['folder'])}`",
            f"- Mission: {spec['mission']}",
            f"- Core lens: {spec['core_lens']}",
            "",
        ]
    )


def build_skill_map_section(spec: dict) -> str:
    skill_folder = CODEX_SKILLS_ROOT / spec["skill_name"]
    return "\n".join(
        [
            f"## {spec['display_name']}",
            "",
            f"- Skill name: `${spec['skill_name']}`",
            f"- Skill file: `{skill_folder / 'SKILL.md'}`",
            f"- Knowledge folder: `{KB_ROOT / spec['folder']}`",
            f"- Expert brief: `{skill_folder / 'references' / 'expert-brief.md'}`",
            "",
        ]
    )


def replace_or_append_section(text: str, heading: str, section: str, insert_before: str | None = None) -> str:
    pattern = re.compile(rf"(?ms)^## {re.escape(heading)}\n.*?(?=^## |\Z)")
    if pattern.search(text):
        return pattern.sub(section.rstrip() + "\n\n", text, count=1)
    if insert_before and insert_before in text:
        return text.replace(insert_before, section.rstrip() + "\n\n" + insert_before, 1)
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n" + section.rstrip() + "\n"


def ensure_phrase(text: str, old: str, new: str) -> str:
    return text.replace(old, new)


def update_agents_md(spec: dict, dry_run: bool) -> str:
    text = AGENTS_PATH.read_text(encoding="utf-8")
    knowledge_line = f"- `{spec['folder']}`: {spec['expert_name']}"
    skill_line = f"- `.codex/skills/{spec['skill_name']}`"
    if knowledge_line not in text:
        marker = "Support data:"
        text = text.replace(marker, knowledge_line + "\n\n" + marker, 1)
    if skill_line not in text:
        marker = "## Norms For This Directory"
        text = text.replace(marker, skill_line + "\n\n" + marker, 1)
    text = text.replace(
        "- The local skill should treat the 12 knowledge centers as expert agents, not just as folders to summarize.",
        "- The local skill should treat the knowledge centers as expert agents, not just as folders to summarize.",
    )
    if dry_run:
        return f"update: {AGENTS_PATH}"
    AGENTS_PATH.write_text(text, encoding="utf-8")
    return f"update: {AGENTS_PATH}"


def main() -> int:
    args = parse_args()
    spec = load_spec(Path(args.spec))

    kb_folder = KB_ROOT / spec["folder"]
    skill_folder = CODEX_SKILLS_ROOT / spec["skill_name"]
    card_path = DOMAIN_EXPERTS_DIR / card_filename(spec["folder"])

    actions = []
    if args.dry_run:
        actions.append(f"mkdir: {kb_folder}")
    else:
        kb_folder.mkdir(parents=True, exist_ok=True)
        actions.append(f"mkdir: {kb_folder}")

    actions.append(
        ensure_write(skill_folder / "SKILL.md", build_skill_md(spec), args.overwrite, args.dry_run)
    )
    actions.append(
        ensure_write(skill_folder / "agents" / "openai.yaml", build_openai_yaml(spec), args.overwrite, args.dry_run)
    )
    actions.append(
        ensure_write(skill_folder / "references" / "expert-brief.md", build_expert_brief(spec), args.overwrite, args.dry_run)
    )
    actions.append(
        ensure_write(skill_folder / "references" / "taxonomy.md", build_taxonomy(spec), args.overwrite, args.dry_run)
    )
    actions.append(
        ensure_write(card_path, build_expert_brief(spec), args.overwrite, args.dry_run)
    )

    registry_text = REGISTRY_PATH.read_text(encoding="utf-8")
    registry_text = ensure_phrase(
        registry_text,
        "These are the 12 specialist agents that the local ecological-agriculture skill should orchestrate across.",
        "These are the specialist agents that the local ecological-agriculture skill should orchestrate across.",
    )
    registry_text = ensure_phrase(
        registry_text,
        "- It is not a thirteenth expert. It supports the 12 experts.",
        "- It is not a standalone expert. It supports the specialist experts.",
    )
    registry_text = replace_or_append_section(
        registry_text,
        spec["expert_name"],
        build_registry_section(spec),
        insert_before="## Support Data",
    )
    actions.append(ensure_write(REGISTRY_PATH, registry_text, True, args.dry_run))

    map_text = SKILL_MAP_PATH.read_text(encoding="utf-8")
    map_text = replace_or_append_section(map_text, spec["display_name"], build_skill_map_section(spec))
    actions.append(ensure_write(SKILL_MAP_PATH, map_text, True, args.dry_run))

    if args.update_agents or spec.get("update_agents"):
        actions.append(update_agents_md(spec, args.dry_run))

    for action in actions:
        print(action)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
