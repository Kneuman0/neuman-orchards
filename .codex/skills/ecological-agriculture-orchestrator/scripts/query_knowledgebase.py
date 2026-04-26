from __future__ import annotations

import argparse
import csv
from pathlib import Path


KB_ROOT = Path(r"G:\My Drive\Home Docs\Garden\knowledgebase")
CATALOG_PATH = KB_ROOT / "catalog.csv"
INVENTORY_DIR = KB_ROOT / "13_inventories_and_local_lists"

TOPIC_ALIASES = {
    "core": "01_core_microfarm_permaculture",
    "microfarm": "01_core_microfarm_permaculture",
    "intensive": "02_intensive_vegetable_systems",
    "vegetables": "02_intensive_vegetable_systems",
    "biochar": "03_biochar",
    "bokashi": "04_bokashi_em",
    "em": "04_bokashi_em",
    "compost": "05_compost_soil_fertility",
    "compost-tea": "06_compost_tea_soil_biology",
    "tea": "06_compost_tea_soil_biology",
    "fungi": "07_fungi_mycorrhiza_biostimulants",
    "mycorrhiza": "07_fungi_mycorrhiza_biostimulants",
    "forest": "08_forest_gardens_agroforestry",
    "agroforestry": "08_forest_gardens_agroforestry",
    "mid-atlantic": "09_mid_atlantic_priority",
    "midatlantic": "09_mid_atlantic_priority",
    "companion": "10_companion_planting_intercropping",
    "intercropping": "10_companion_planting_intercropping",
    "wild": "11_wild_plants_foraged_integration",
    "foraged": "11_wild_plants_foraged_integration",
    "beneficials": "12_beneficial_insects_pest_indicators",
    "pests": "12_beneficial_insects_pest_indicators",
}

INVENTORY_FILES = [
    "zone_7_perennial_subsistence_cr.csv",
    "zone_7_self_seeding_edibles.csv",
    "zone7_self_seeding_annuals_and_short_lived_edibles.csv",
]


def load_catalog() -> list[dict[str, str]]:
    with CATALOG_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_topic(raw: str) -> str:
    value = raw.strip().lower()
    return TOPIC_ALIASES.get(value, raw.strip())


def row_text(row: dict[str, str]) -> str:
    return " ".join(
        row.get(field, "")
        for field in ("title", "authors", "year", "filename", "doi", "source_url", "why")
    ).lower()


def match_catalog(
    rows: list[dict[str, str]], topics: list[str], keyword: str
) -> list[dict[str, str]]:
    normalized_topics = {normalize_topic(topic) for topic in topics if topic}
    keyword_bits = [bit.strip().lower() for bit in keyword.split() if bit.strip()]
    matches: list[dict[str, str]] = []
    for row in rows:
        if normalized_topics and row["topic_folder"] not in normalized_topics:
            continue
        haystack = row_text(row)
        if keyword_bits and not all(bit in haystack for bit in keyword_bits):
            continue
        matches.append(row)
    return matches


def search_inventories(keyword: str, limit: int) -> list[tuple[str, dict[str, str]]]:
    matches: list[tuple[str, dict[str, str]]] = []
    keyword_bits = [bit.strip().lower() for bit in keyword.split() if bit.strip()]
    for filename in INVENTORY_FILES:
        path = INVENTORY_DIR / filename
        if not path.exists():
            continue
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                text = " ".join(f"{k} {v}" for k, v in row.items()).lower()
                if keyword_bits and not all(bit in text for bit in keyword_bits):
                    continue
                matches.append((filename, row))
                if len(matches) >= limit:
                    return matches
    return matches


def print_topics(rows: list[dict[str, str]]) -> None:
    seen = sorted({row["topic_folder"] for row in rows})
    for topic in seen:
        count = sum(1 for row in rows if row["topic_folder"] == topic)
        print(f"{topic}\t{count}")


def print_catalog_matches(rows: list[dict[str, str]], limit: int) -> None:
    for row in rows[:limit]:
        path = KB_ROOT / row["topic_folder"] / row["filename"]
        print(f"- {row['topic_folder']}")
        print(f"  Title: {row['title']} ({row['year']})")
        print(f"  File: {path}")
        print(f"  Why: {row['why']}")
        if row.get("doi"):
            print(f"  DOI: {row['doi']}")
        print()


def print_inventory_matches(matches: list[tuple[str, dict[str, str]]]) -> None:
    for filename, row in matches:
        path = INVENTORY_DIR / filename
        label = row.get("Common name") or row.get("common_name") or row.get("Scientific name") or ""
        print(f"- {filename}")
        print(f"  File: {path}")
        print(f"  Match: {label}")
        for key in ("Category", "Scientific name", "Zone 7 self-seeding fit", "Primary edible use", "Notes"):
            if key in row and row[key]:
                print(f"  {key}: {row[key]}")
        print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query the ecological agriculture knowledgebase.")
    parser.add_argument("--list-topics", action="store_true", help="List topic folders and counts.")
    parser.add_argument("--topic", action="append", default=[], help="Filter by topic folder or alias. Repeatable.")
    parser.add_argument("--keyword", default="", help="Full-text keyword filter across the catalog or inventories.")
    parser.add_argument("--inventory", action="store_true", help="Search the inventory CSV files instead of the paper catalog.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of matches to print.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.inventory:
        matches = search_inventories(args.keyword, args.limit)
        print_inventory_matches(matches)
        return

    rows = load_catalog()
    if args.list_topics:
        print_topics(rows)
        return

    matches = match_catalog(rows, args.topic, args.keyword)
    print_catalog_matches(matches, args.limit)


if __name__ == "__main__":
    main()
