from __future__ import annotations

import argparse
import json
from pathlib import Path

from .farmbot import write_farmbot_bundle
from .memory import DEFAULT_DB_PATH, GardenMemoryStore
from .sync import GardenTwinService, pretty_json
from .stack import DEFAULT_RUNTIME_DIR


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Garden twin helper CLI")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="SQLite database path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-db", help="Initialize the SQLite database")

    import_parser = subparsers.add_parser("import-snapshot", help="Import a canonical garden snapshot")
    import_parser.add_argument("snapshot", help="Path to garden_snapshot.json")

    export_parser = subparsers.add_parser("export-memory-context", help="Export memory context from SQLite")
    export_parser.add_argument("--out", help="Optional output file path")

    farmbot_export_parser = subparsers.add_parser(
        "export-farmbot-bundle",
        help="Export a FarmBot resource bundle from memory or a snapshot file",
    )
    farmbot_export_parser.add_argument(
        "snapshot",
        nargs="?",
        help="Optional canonical snapshot path. Defaults to exporting the current memory state.",
    )
    farmbot_export_parser.add_argument("--out", help="Optional output file path")

    farmbot_import_parser = subparsers.add_parser(
        "import-farmbot-bundle",
        help="Import a FarmBot resource bundle into the local memory store",
    )
    farmbot_import_parser.add_argument("bundle", help="Path to farmbot_bundle.json")

    prepare_parser = subparsers.add_parser(
        "prepare-farmbot-stack",
        help="Clone or update the official FarmBot Web App and write a local .env",
    )
    prepare_parser.add_argument(
        "--runtime-dir",
        default=str(DEFAULT_RUNTIME_DIR),
        help="Target directory for the FarmBot Web App checkout",
    )
    prepare_parser.add_argument("--host", help="Override detected API/MQTT host")
    prepare_parser.add_argument("--port", type=int, default=3000, help="FarmBot API port")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init-db":
        store = GardenMemoryStore(args.db)
        store.connection.execute("SELECT 1")
        print(f"Initialized database at {store.db_path}")
        store.close()
        return 0

    if args.command == "prepare-farmbot-stack":
        service = GardenTwinService(db_path=args.db)
        try:
            payload = service.prepare_farmbot_stack(
                runtime_dir=args.runtime_dir,
                host=args.host,
                port=args.port,
            )
            print(pretty_json(payload))
            return 0
        finally:
            service.close()

    service = GardenTwinService(db_path=args.db)
    try:
        if args.command == "import-snapshot":
            report = service.import_snapshot(args.snapshot, source_path=str(Path(args.snapshot).resolve()))
            print(pretty_json(report))
            return 0

        if args.command == "export-memory-context":
            payload = service.export_memory_context()
            if args.out:
                target = Path(args.out)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f"{json.dumps(payload, indent=2)}\n", encoding="utf-8")
                print(f"Wrote memory context to {target}")
            else:
                print(pretty_json(payload))
            return 0

        if args.command == "export-farmbot-bundle":
            payload = service.export_farmbot_bundle(args.snapshot) if args.snapshot else service.export_farmbot_bundle()
            if args.out:
                target = write_farmbot_bundle(args.out, payload)
                print(f"Wrote FarmBot bundle to {target}")
            else:
                print(pretty_json(payload))
            return 0

        if args.command == "import-farmbot-bundle":
            report = service.import_farmbot_bundle(args.bundle, source_path=str(Path(args.bundle).resolve()))
            print(pretty_json(report))
            return 0
    finally:
        service.close()

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
