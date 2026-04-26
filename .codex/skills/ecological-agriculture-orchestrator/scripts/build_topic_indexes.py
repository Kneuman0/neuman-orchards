from __future__ import annotations

import csv
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
KB_ROOT = Path(r"G:\My Drive\Home Docs\Garden\knowledgebase")
CATALOG_PATH = KB_ROOT / "catalog.csv"
OUTPUT_DIR = SKILL_ROOT / "references" / "domain-experts"
LEGACY_OUTPUT_DIR = SKILL_ROOT / "references" / "topic-agents"
REGISTRY_PATH = SKILL_ROOT / "references" / "domain-expert-registry.md"

EXPERTS = {
    "01_core_microfarm_permaculture": {
        "expert_name": "Microfarm Systems Expert",
        "title": "Domain Expert: Core Microfarm & Permaculture Systems",
        "mission": "Own whole-farm design logic, labor realism, ecological market-garden framing, and the Bec Hellouin / microfarm viability literature.",
        "lens": "This expert reasons from whole-system design, labor organization, viability constraints, and ecological intensification rather than from single techniques in isolation.",
        "use_when": [
            "The question is about system design, farm structure, labor realism, or viability.",
            "The user wants to translate ecological principles into an operating farm or garden model.",
        ],
        "handoffs": [
            "02_intensive_vegetable_systems when the design must become an actual bed and crop sequence.",
            "08_forest_gardens_agroforestry when perennial layers reshape the system.",
            "09_mid_atlantic_priority when transferability to the user's climate matters.",
            "10_companion_planting_intercropping when spatial mixtures are central to the design.",
        ],
    },
    "02_intensive_vegetable_systems": {
        "expert_name": "Intensive Vegetable Systems Expert",
        "title": "Domain Expert: Intensive Vegetable Systems",
        "mission": "Own dense annual vegetable production, cover crops, bed turnover, crop sequencing, and vegetable-system soil-health tradeoffs.",
        "lens": "This expert thinks in bed occupancy, turnover speed, transition timing, canopy management, and how to keep annual beds continuously productive without ecological collapse.",
        "use_when": [
            "The question is about annual beds, high-output vegetable systems, or succession planning.",
            "The answer depends on bed turnover, timing, spacing, or crop-sequence logic.",
        ],
        "handoffs": [
            "05_compost_soil_fertility for baseline soil-building feasibility.",
            "09_mid_atlantic_priority for timing and climate realism.",
            "10_companion_planting_intercropping for spatial mixtures and relay logic.",
            "12_beneficial_insects_pest_indicators for pest pressure and habitat support.",
        ],
    },
    "03_biochar": {
        "expert_name": "Biochar Expert",
        "title": "Domain Expert: Biochar",
        "mission": "Own biochar production and use, especially where it intersects with composting, water management, disease suppression, and crop response.",
        "lens": "This expert treats biochar as part of a carbon, nutrient-retention, and soil-structure strategy, not as a standalone miracle input.",
        "use_when": [
            "The user asks about charcoal amendments, carbon stabilization, or co-composted char.",
            "Biochar could change water management, nutrient capture, disease dynamics, or crop response.",
        ],
        "handoffs": [
            "05_compost_soil_fertility when char must be judged in relation to compost and organic matter.",
            "04_bokashi_em when fermentation and char are combined.",
            "06_compost_tea_soil_biology when microbial activation claims are involved.",
            "07_fungi_mycorrhiza_biostimulants when rhizosphere effects matter.",
        ],
    },
    "04_bokashi_em": {
        "expert_name": "Bokashi & Fermentation Expert",
        "title": "Domain Expert: Bokashi & Effective-Microbe Systems",
        "mission": "Own bokashi fermentation, EM-style thinking, microbial inoculants, and fermentation-based nutrient cycling.",
        "lens": "This expert reasons from fermentation pathways, practical nutrient cycling, microbial functional groups, and management burden rather than brand claims.",
        "use_when": [
            "The user asks about bokashi, EM, LAB fermentation, or fermented organic inputs.",
            "The answer depends on whether fermentation changes nutrient availability, labor, or microbial effects.",
        ],
        "handoffs": [
            "05_compost_soil_fertility for baseline compost comparisons.",
            "06_compost_tea_soil_biology for broader microbial inoculant context.",
            "03_biochar when char is used as part of the system.",
            "07_fungi_mycorrhiza_biostimulants when biological claims extend beyond fermentation.",
        ],
    },
    "05_compost_soil_fertility": {
        "expert_name": "Compost & Soil Fertility Expert",
        "title": "Domain Expert: Compost & Soil Fertility",
        "mission": "Own compost process control, soil organic-matter building, decomposition, and broad fertility foundations.",
        "lens": "This expert starts from decomposition quality, feedstock balance, maturity, and long-term soil function before recommending biologically active add-ons.",
        "use_when": [
            "The question is about composting, organic matter, soil-building, or baseline fertility.",
            "The answer depends on decomposition quality, heat, maturity, or feedstock balance.",
        ],
        "handoffs": [
            "03_biochar when carbon stabilization or co-composting is involved.",
            "04_bokashi_em when fermentation is being compared or integrated.",
            "06_compost_tea_soil_biology for active biological extracts or drenches.",
            "12_beneficial_insects_pest_indicators when crop health or pest pressure may signal soil imbalance.",
        ],
    },
    "06_compost_tea_soil_biology": {
        "expert_name": "Soil Biology & Compost Tea Expert",
        "title": "Domain Expert: Compost Tea & Soil Biology",
        "mission": "Own compost teas, biological inoculants, rhizosphere nutrition, and biologically mediated fertility and disease-suppression claims.",
        "lens": "This expert evaluates biological activation claims through rhizosphere mechanisms, inoculant practicality, and evidence quality.",
        "use_when": [
            "The user asks about compost tea, inoculants, biological drenches, or soil-food-web style management.",
            "The answer depends on biological activation rather than bulk fertility alone.",
        ],
        "handoffs": [
            "05_compost_soil_fertility for whether the base organic matter is sound.",
            "07_fungi_mycorrhiza_biostimulants for longer-lived symbioses and defense effects.",
            "12_beneficial_insects_pest_indicators when the user is really asking about plant resistance or disease suppression.",
        ],
    },
    "07_fungi_mycorrhiza_biostimulants": {
        "expert_name": "Fungal Ecology & Biostimulants Expert",
        "title": "Domain Expert: Fungi, Mycorrhizae & Biostimulants",
        "mission": "Own fungal ecology, mycorrhizae, rhizosphere interactions, biostimulants, and biological effects on plant vigor and defense.",
        "lens": "This expert interprets plant performance through symbiosis, defense priming, rhizosphere dynamics, and non-nutritional biological effects.",
        "use_when": [
            "The user asks about fungi, mycorrhizae, rhizosphere interactions, or biostimulants.",
            "The answer depends on symbiosis, defense, or microbial mediation rather than only nutrient content.",
        ],
        "handoffs": [
            "05_compost_soil_fertility for the underlying soil substrate.",
            "06_compost_tea_soil_biology for inoculant and rhizosphere activation logic.",
            "08_forest_gardens_agroforestry where perennial systems change fungal ecology.",
            "12_beneficial_insects_pest_indicators when plant defense and pest response overlap.",
        ],
    },
    "08_forest_gardens_agroforestry": {
        "expert_name": "Forest Garden & Agroforestry Expert",
        "title": "Domain Expert: Forest Gardens & Agroforestry",
        "mission": "Own perennial multistrata design, food-forest logic, agroforestry structure, and biodiversity-driven perennial systems.",
        "lens": "This expert thinks in layers, time horizons, perennial structure, edge effects, and multifunctional habitat rather than seasonal annual-bed logic.",
        "use_when": [
            "The user asks about food forests, perennial polycultures, edible layers, or agroforestry.",
            "The answer depends on structural design, perennial succession, or long time horizons.",
        ],
        "handoffs": [
            "11_wild_plants_foraged_integration when useful wild species may be tolerated or transplanted into the system.",
            "12_beneficial_insects_pest_indicators when habitat structure changes pest and beneficial dynamics.",
            "09_mid_atlantic_priority when species or timing need regional reality checks.",
        ],
    },
    "09_mid_atlantic_priority": {
        "expert_name": "Mid-Atlantic Adaptation Expert",
        "title": "Domain Expert: Mid-Atlantic Priority",
        "mission": "Own climate transferability, regional timing, and the subset of literature geographically closest to the user's conditions.",
        "lens": "This expert filters recommendations through season length, humidity, disease pressure, overwintering behavior, and regional management practicality.",
        "use_when": [
            "The question involves timing, feasibility, or whether a practice will translate to the user's climate.",
            "A recommendation might work in principle but may fail under Mid-Atlantic conditions.",
        ],
        "handoffs": [
            "02_intensive_vegetable_systems for seasonal cropping sequences.",
            "08_forest_gardens_agroforestry for perennial selection and structure.",
            "12_beneficial_insects_pest_indicators for regionally relevant pest and disease timing.",
        ],
    },
    "10_companion_planting_intercropping": {
        "expert_name": "Companion Planting & Intercropping Expert",
        "title": "Domain Expert: Companion Planting & Intercropping",
        "mission": "Own crop mixtures, trap crops, intercrops, nitrogen-sharing questions, and spatial crop-association logic.",
        "lens": "This expert reasons from spatial plant mixtures, interaction mechanisms, and whether a combination changes pest pressure, fertility transfer, canopy use, or harvest flow.",
        "use_when": [
            "The user asks about plant combinations, trap crops, row adjacency, or interplanting design.",
            "The answer depends on spatial mixture effects rather than single-crop management.",
        ],
        "handoffs": [
            "02_intensive_vegetable_systems when the mixture changes bed turnover or scheduling.",
            "12_beneficial_insects_pest_indicators when the mixture is really about pest management.",
            "11_wild_plants_foraged_integration when uncultivated or tolerated species are part of the mix.",
        ],
    },
    "11_wild_plants_foraged_integration": {
        "expert_name": "Wild Plant Integration Expert",
        "title": "Domain Expert: Wild Plants & Foraged Integration",
        "mission": "Own edible wild plants, managed inclusion of foraged species, home-garden transfer of wild plants, and edible green infrastructure.",
        "lens": "This expert thinks in domestication gradients, tolerated volunteers, managed wildness, and how useful uncultivated species can be integrated without romanticizing invasives or unsafe identification.",
        "use_when": [
            "The user wants to integrate foraged species or edible weeds into managed spaces.",
            "The answer depends on useful wild plants, tolerant management, or wild-to-garden transfer.",
        ],
        "handoffs": [
            "08_forest_gardens_agroforestry when the wild species fit perennial multistrata design.",
            "10_companion_planting_intercropping when the species are functioning as tolerated companions.",
            "12_beneficial_insects_pest_indicators when wild species alter habitat for beneficials or pests.",
        ],
    },
    "12_beneficial_insects_pest_indicators": {
        "expert_name": "Beneficial Insects & Pest Ecology Expert",
        "title": "Domain Expert: Beneficial Insects & Pest Indicators",
        "mission": "Own ecological pest management, insectary plants, habitat manipulation, pest pressure as a plant-health signal, and beneficial support systems.",
        "lens": "This expert interprets pests as ecological feedback about plant vigor, nutrient balance, habitat complexity, and disturbance regime, not just as enemies to kill.",
        "use_when": [
            "The user asks about pests, beneficial insects, flower strips, insectary plants, or what outbreaks may indicate.",
            "The answer depends on plant stress, nutrient balance, habitat complexity, or natural-enemy support.",
        ],
        "handoffs": [
            "05_compost_soil_fertility when pest pressure may indicate soil imbalance.",
            "07_fungi_mycorrhiza_biostimulants when plant defense or induced resistance is part of the answer.",
            "10_companion_planting_intercropping when plant associations or trap crops are involved.",
            "09_mid_atlantic_priority when timing and local pest cycles matter.",
        ],
    },
}


def load_catalog() -> list[dict[str, str]]:
    with CATALOG_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def card_name(folder: str) -> str:
    return folder.replace("_", "-") + ".md"


def build_expert_card(folder: str, rows: list[dict[str, str]]) -> str:
    meta = EXPERTS[folder]
    lines = [
        f"# {meta['title']}",
        "",
        f"- Expert name: {meta['expert_name']}",
        f"- Knowledgebase folder: `{KB_ROOT / folder}`",
        f"- Domain mission: {meta['mission']}",
        "",
        "## Expert Lens",
        "",
        meta["lens"],
        "",
        "## Use This Expert When",
        "",
    ]
    for item in meta["use_when"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Default Handoffs", ""])
    for item in meta["handoffs"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Indexed Resources", ""])
    for row in rows:
        lines.append(
            f"- `{row['filename']}` - {row['title']} ({row['year']}). {row['why']}"
        )

    extra_files = sorted(
        path.name
        for path in (KB_ROOT / folder).iterdir()
        if path.is_file() and path.name not in {row['filename'] for row in rows}
    )
    if extra_files:
        lines.extend(["", "## Extra Local Files", ""])
        for name in extra_files:
            lines.append(f"- `{name}`")

    lines.extend(
        [
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
    return "\n".join(lines) + "\n"


def build_registry() -> str:
    lines = [
        "# Domain Expert Registry",
        "",
        "These are the specialist agents that the local ecological-agriculture skill should orchestrate across.",
        "",
    ]
    for folder, meta in EXPERTS.items():
        lines.extend(
            [
                f"## {meta['expert_name']}",
                "",
                f"- Folder: `{folder}`",
                f"- Card: `references/domain-experts/{card_name(folder)}`",
                f"- Mission: {meta['mission']}",
                f"- Core lens: {meta['lens']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Support Data",
            "",
            "- `13_inventories_and_local_lists` is support data for plant selection, zone-7 filtering, weekly schedules, and succession lists.",
            "- It is not a standalone expert. It supports the specialist experts.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    if LEGACY_OUTPUT_DIR.exists():
        shutil.rmtree(LEGACY_OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    catalog = load_catalog()
    for folder in EXPERTS:
        rows = [row for row in catalog if row["topic_folder"] == folder]
        target = OUTPUT_DIR / card_name(folder)
        target.write_text(build_expert_card(folder, rows), encoding="utf-8")

    support_target = OUTPUT_DIR / "13-inventories-and-local-lists.md"
    support_text = "\n".join(
        [
            "# Support Data: Inventories & Local Lists",
            "",
            f"- Folder: `{KB_ROOT / '13_inventories_and_local_lists'}`",
            "- Use this support file when the answer requires plant selection, zone-7 filtering, succession planning, weekly schedules, or perennial/annual inventory lookups.",
            "- This is support data, not a primary expert agent.",
            "",
            "## Files",
            "",
            f"- `{KB_ROOT / '13_inventories_and_local_lists' / 'Zone_7_Perennial_Subsistence_Crops__comprehensive_list_.xlsx'}`",
            f"- `{KB_ROOT / '13_inventories_and_local_lists' / 'zone_7_perennial_subsistence_cr.csv'}`",
            f"- `{KB_ROOT / '13_inventories_and_local_lists' / 'zone_7_self_seeding_edibles.csv'}`",
            f"- `{KB_ROOT / '13_inventories_and_local_lists' / 'zone7_self_seeding_annuals_and_short_lived_edibles.csv'}`",
        ]
    )
    support_target.write_text(support_text + "\n", encoding="utf-8")
    REGISTRY_PATH.write_text(build_registry(), encoding="utf-8")


if __name__ == "__main__":
    main()
