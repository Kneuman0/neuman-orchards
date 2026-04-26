from __future__ import annotations

import shutil
from pathlib import Path


ORCHESTRATOR_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ORCHESTRATOR_ROOT.parent
KB_ROOT = Path(r"G:\My Drive\Home Docs\Garden\knowledgebase")
DOMAIN_CARDS_DIR = ORCHESTRATOR_ROOT / "references" / "domain-experts"
SPECIALIST_MAP_PATH = ORCHESTRATOR_ROOT / "references" / "specialist-skill-map.md"

SPECIALISTS = [
    {
        "folder": "01_core_microfarm_permaculture",
        "skill_name": "ecoag-microfarm-systems",
        "display_name": "EcoAg Microfarm Systems",
        "short_description": "Microfarm and Bec Hellouin reasoning",
        "focus": "whole-farm ecological microfarm design, labor realism, permaculture market-garden logic, and the Bec Hellouin / Morel literature",
        "when_to_use": [
            "the question is about overall system design, viability, labor, or ecological intensification",
            "the answer needs the end-to-end microfarm lifecycle context before narrower techniques are evaluated",
        ],
        "anchor_files": [
            str(KB_ROOT / "Bec_Hellouin_summary.md"),
        ],
    },
    {
        "folder": "02_intensive_vegetable_systems",
        "skill_name": "ecoag-intensive-vegetables",
        "display_name": "EcoAg Intensive Vegetables",
        "short_description": "Intensive vegetable bed planning",
        "focus": "dense annual vegetable production, succession, bed turnover, cover-crop transitions, and annual-bed throughput",
        "when_to_use": [
            "the question is about annual beds, succession, spacing, turnover, or intensive vegetable planning",
            "the answer depends on crop-sequence logic, occupancy, or harvest-flow management",
        ],
        "anchor_files": [],
    },
    {
        "folder": "03_biochar",
        "skill_name": "ecoag-biochar",
        "display_name": "EcoAg Biochar",
        "short_description": "Biochar strategy and tradeoffs",
        "focus": "biochar production and use, especially where it intersects with composting, nutrient retention, disease suppression, and crop response",
        "when_to_use": [
            "the question is about biochar, charcoal amendments, carbon stabilization, or co-composted char",
            "the answer depends on water, nutrient-retention, or soil-structure effects from char",
        ],
        "anchor_files": [],
    },
    {
        "folder": "04_bokashi_em",
        "skill_name": "ecoag-bokashi-fermentation",
        "display_name": "EcoAg Bokashi Fermentation",
        "short_description": "Bokashi and EM-style systems",
        "focus": "bokashi fermentation, EM-style management, LAB fermentation, and fermentation-based nutrient cycling",
        "when_to_use": [
            "the question is about bokashi, EM, LAB, or fermented organic inputs",
            "the answer depends on fermentation-based handling rather than composting alone",
        ],
        "anchor_files": [],
    },
    {
        "folder": "05_compost_soil_fertility",
        "skill_name": "ecoag-compost-fertility",
        "display_name": "EcoAg Compost Fertility",
        "short_description": "Compost and soil fertility",
        "focus": "compost process control, decomposition, organic-matter building, and baseline soil fertility",
        "when_to_use": [
            "the question is about composting, decomposition, organic matter, or fertility foundations",
            "the answer depends on compost maturity, heat, feedstock balance, or long-term soil building",
        ],
        "anchor_files": [],
    },
    {
        "folder": "06_compost_tea_soil_biology",
        "skill_name": "ecoag-soil-biology",
        "display_name": "EcoAg Soil Biology",
        "short_description": "Soil biology and compost tea",
        "focus": "compost teas, microbial inoculants, rhizosphere biology, and biologically mediated fertility or disease suppression",
        "when_to_use": [
            "the question is about compost tea, inoculants, drenches, or soil-food-web style biological management",
            "the answer depends on rhizosphere or inoculant mechanisms rather than bulk fertility alone",
        ],
        "anchor_files": [],
    },
    {
        "folder": "07_fungi_mycorrhiza_biostimulants",
        "skill_name": "ecoag-fungal-ecology",
        "display_name": "EcoAg Fungal Ecology",
        "short_description": "Fungi, mycorrhizae, biostimulants",
        "focus": "fungal ecology, mycorrhizae, rhizosphere interactions, and biostimulant effects on plant vigor and defense",
        "when_to_use": [
            "the question is about fungi, mycorrhizae, rhizosphere symbiosis, or biostimulants",
            "the answer depends on symbiosis, defense priming, or biological mediation",
        ],
        "anchor_files": [],
    },
    {
        "folder": "08_forest_gardens_agroforestry",
        "skill_name": "ecoag-forest-gardens",
        "display_name": "EcoAg Forest Gardens",
        "short_description": "Forest gardens and agroforestry",
        "focus": "forest gardens, food forests, perennial polycultures, multistrata design, and agroforestry structure",
        "when_to_use": [
            "the question is about perennial layers, food forests, agroforestry, or long-horizon edible structure",
            "the answer depends on layers, perennial succession, or habitat multifunctionality",
        ],
        "anchor_files": [],
    },
    {
        "folder": "09_mid_atlantic_priority",
        "skill_name": "ecoag-mid-atlantic",
        "display_name": "EcoAg Mid-Atlantic",
        "short_description": "Mid-Atlantic ecological adaptation",
        "focus": "Mid-Atlantic timing, transferability, season length, humidity, disease pressure, and regional feasibility",
        "when_to_use": [
            "the question is about climate fit, timing, transferability, or regional realism",
            "a recommendation may work in theory but needs Mid-Atlantic adaptation testing",
        ],
        "anchor_files": [],
    },
    {
        "folder": "10_companion_planting_intercropping",
        "skill_name": "ecoag-companion-cropping",
        "display_name": "EcoAg Companion Cropping",
        "short_description": "Companion planting and intercrops",
        "focus": "companion planting, intercropping, trap crops, relay logic, and spatial crop associations",
        "when_to_use": [
            "the question is about plant combinations, trap crops, row adjacency, or interplanting",
            "the answer depends on spatial mixture effects rather than single-crop management",
        ],
        "anchor_files": [],
    },
    {
        "folder": "11_wild_plants_foraged_integration",
        "skill_name": "ecoag-wild-integration",
        "display_name": "EcoAg Wild Integration",
        "short_description": "Wild edible plant integration",
        "focus": "edible wild plants, managed foraged-plant inclusion, wild-to-garden transfer, and edible green infrastructure",
        "when_to_use": [
            "the question is about edible weeds, foraged plants, or integrating wild species into gardens",
            "the answer depends on tolerated wildness, domestication gradients, or wild-to-managed transfer",
        ],
        "anchor_files": [],
    },
    {
        "folder": "12_beneficial_insects_pest_indicators",
        "skill_name": "ecoag-pest-ecology",
        "display_name": "EcoAg Pest Ecology",
        "short_description": "Beneficial insects and pest ecology",
        "focus": "beneficial insects, ecological pest management, habitat manipulation, and pest pressure as a system signal",
        "when_to_use": [
            "the question is about pests, beneficial insects, insectary plants, or what outbreaks indicate",
            "the answer depends on plant stress, nutrient balance, habitat structure, or predator support",
        ],
        "anchor_files": [],
    },
]


def quote_yaml(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def card_filename(folder: str) -> str:
    return folder.replace("_", "-") + ".md"


def build_skill_md(spec: dict[str, object]) -> str:
    folder = spec["folder"]
    skill_name = spec["skill_name"]
    display_name = spec["display_name"]
    focus = spec["focus"]
    when_to_use = spec["when_to_use"]
    lines = [
        "---",
        f"name: {skill_name}",
        f"description: Use this skill when the user needs domain-specific ecological agriculture reasoning from `{KB_ROOT / folder}`, especially for {focus}.",
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
    for item in when_to_use:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Working Rules",
            "",
            f"- Primary folder scope: `{KB_ROOT / folder}`",
            "- Read `references/expert-brief.md` before answering.",
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
            "",
            "## Resources",
            "",
            "- `references/expert-brief.md`",
            f"  Domain brief for `{folder}`.",
        ]
    )
    anchor_files = spec["anchor_files"]
    if anchor_files:
        lines.extend(["- Anchor files", "  Use these when they are explicitly relevant to this domain."])
        for path in anchor_files:
            lines.append(f"  - `{path}`")
    return "\n".join(lines) + "\n"


def build_openai_yaml(spec: dict[str, object]) -> str:
    default_prompt = (
        f"Use ${spec['skill_name']} to answer a domain-specific ecological "
        "agriculture question from the local knowledgebase."
    )
    return "\n".join(
        [
            "interface:",
            f"  display_name: {quote_yaml(spec['display_name'])}",
            f"  short_description: {quote_yaml(spec['short_description'])}",
            f"  default_prompt: {quote_yaml(default_prompt)}",
        ]
    ) + "\n"


def build_map(specs: list[dict[str, object]]) -> str:
    lines = [
        "# Specialist Skill Map",
        "",
        "Use this map when the orchestrator needs to spawn isolated specialist agents with their own local skills.",
        "",
        "Runtime rule:",
        "",
        "- spawn specialists with `fork_context=false`",
        "- pass only the specialist skill, narrowed question, and minimal scoped files",
        "- do not pass other specialists' outputs on the first pass",
        "",
    ]
    for spec in specs:
        skill_folder = SKILLS_ROOT / spec["skill_name"]
        lines.extend(
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
    return "\n".join(lines) + "\n"


def write_specialist_skill(spec: dict[str, object]) -> None:
    folder = SKILLS_ROOT / spec["skill_name"]
    refs = folder / "references"
    agents = folder / "agents"
    refs.mkdir(parents=True, exist_ok=True)
    agents.mkdir(parents=True, exist_ok=True)

    expert_card = DOMAIN_CARDS_DIR / card_filename(spec["folder"])
    if not expert_card.exists():
        raise FileNotFoundError(expert_card)

    (folder / "SKILL.md").write_text(build_skill_md(spec), encoding="utf-8")
    shutil.copy2(expert_card, refs / "expert-brief.md")
    (agents / "openai.yaml").write_text(build_openai_yaml(spec), encoding="utf-8")


def main() -> None:
    for spec in SPECIALISTS:
        write_specialist_skill(spec)
    SPECIALIST_MAP_PATH.write_text(build_map(SPECIALISTS), encoding="utf-8")


if __name__ == "__main__":
    main()
