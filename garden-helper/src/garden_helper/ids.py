from __future__ import annotations

import re
import uuid


EMOJI_RE = re.compile(r"^[^\w]+", re.UNICODE)
NON_SLUG_RE = re.compile(r"[^a-z0-9]+")


def strip_display_label(label: str) -> str:
    cleaned = EMOJI_RE.sub("", label or "").strip()
    return re.sub(r"\s+", " ", cleaned)


def slugify(value: str) -> str:
    base = strip_display_label(value).lower()
    slug = NON_SLUG_RE.sub("-", base).strip("-")
    return slug or "unknown"


def stable_plant_id(display_name: str) -> str:
    return f"plant-{slugify(display_name)}"


def new_prefixed_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4()}"
