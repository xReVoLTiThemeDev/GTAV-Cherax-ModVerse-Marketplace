#!/usr/bin/env python3
"""Publish owner-approved Cherax vehicle assets already stored in this repository.

The metadata file preserves source uploader credit; original developer identity remains
unverified unless separately established. SHA-256 is computed from repo asset bytes.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "marketplace" / "vehicles"
CATALOG = BASE / "catalog.json"
META = BASE / "approved_119_metadata.txt"
PREFIX = "1256941518036406273"
ID_RE = re.compile(r"[0-9]+-[0-9]+\Z")
NAME_RE = re.compile(r"mMV_[A-Za-z0-9_-]+\.json\Z")
LIMIT = 500

def die(msg):
    raise ValueError(msg)

def main():
    if not META.is_file():
        die("Approved metadata file not present.")
    records = []
    seen = set()
    lines = META.read_text(encoding="utf-8-sig").splitlines()
    for line_num, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("|")
        if len(parts) != 5:
            die(f"Line {line_num}: expected 5 metadata fields, got {len(parts)}")
        suffix, name, shared_by, filename, verified_flag = parts
        ident = PREFIX + "-" + suffix
        if not ID_RE.fullmatch(ident) or len(ident) > 55 or ident in seen:
            die(f"Line {line_num}: invalid/duplicate ID")
        seen.add(ident)
        if not 1 <= len(name.encode("utf-8")) <= 180:
            die(f"{ident}: invalid name")
        if not 1 <= len(shared_by.encode("utf-8")) <= 100:
            die(f"{ident}: invalid uploader credit")
        if not NAME_RE.fullmatch(filename) or len(filename) > 150:
            die(f"{ident}: invalid install filename")
        if verified_flag not in ("0", "1"):
            die(f"{ident}: invalid compatibility status")
        jpath = BASE / "files" / f"{ident}.json"
        ppath = BASE / "thumbnails" / f"{ident}.jpg"
        if not jpath.is_file() or not ppath.is_file():
            die(f"{ident}: one or both approved assets missing")
        raw = jpath.read_bytes()
        preview = ppath.read_bytes()
        if not 100 <= len(raw) <= 65536:
            die(f"{ident}: vehicle JSON size invalid")
        if not (preview.startswith(b"\xff\xd8") and preview.endswith(b"\xff\xd9")):
            die(f"{ident}: thumbnail is not a JPEG")
        vehicle = json.loads(raw.decode("utf-8-sig"))
        if not isinstance(vehicle, dict) or vehicle.get("format") != "Cherax Entity" or vehicle.get("type") != 1:
            die(f"{ident}: not a Cherax Entity saved vehicle")
        model = vehicle.get("model")
        if type(model) is not int or not -2147483648 <= model <= 4294967295:
            die(f"{ident}: invalid numeric model")
        sha = hashlib.sha256(raw).hexdigest()
        if not filename.endswith("_" + sha[:8] + ".json"):
            die(f"{ident}: filename does not match original JSON SHA-256")
        entry = {
            "id": ident,
            "name": name,
            "creator": "Original developer unverified",
            "shared_by": shared_by,
            "creator_credit_basis": "Discord source uploader credited; original developer name pending verification",
            "source_channel_id": PREFIX,
            "source_message_id": suffix,
            "model": model,
            "filename": filename,
            "sha256": sha,
            "size_bytes": len(raw),
            "thumbnail_sha256": hashlib.sha256(preview).hexdigest(),
            "compatibility_status": "user_confirmed_in_game" if verified_flag == "1" else "format_and_sha256_verified_only",
            "rights_basis": "repository_owner_confirms_creator_approval_2026_10_12",
            "notes": f"Original developer not verified. Uploaded by: {shared_by}. Submit a credit correction if known."
        }
        records.append(entry)
    if len(records) != 119:
        die(f"Expected 119 entries, got {len(records)}")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8-sig"))
    if catalog.get("schema") != "modverse.vehicles.v1" or catalog.get("published") is not True:
        die("Existing catalog schema is invalid")
    old = catalog.get("items")
    if not isinstance(old, list):
        die("Existing catalog items are not a list")
    old_ids = {row["id"] for row in old}
    old_names = {row["filename"] for row in old}
    old_hashes = {row["sha256"] for row in old}
    if len(old_ids) != len(old):
        die("Existing catalog duplicates")
    additions = []
    for row in records:
        if row["id"] in old_ids:
            existing = next(x for x in old if x["id"] == row["id"])
            if existing != row:
                die(f"Existing published entry conflicts with metadata: {row['id']}")
            continue
        if row["filename"] in old_names or row["sha256"] in old_hashes:
            die(f"Duplicate filename or vehicle payload: {row['id']}")
        old_ids.add(row["id"])
        old_names.add(row["filename"])
        old_hashes.add(row["sha256"])
        additions.append(row)
    if len(old) + len(additions) > LIMIT:
        die(f"Catalog exceeds {LIMIT} entries")
    catalog["items"] = old + additions
    if additions:
        catalog["catalog_version"] = int(catalog.get("catalog_version", 1)) + 1
        catalog["updated_at"] = datetime.now(timezone.utc).date().isoformat()
        CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"APPROVED VEHICLE CATALOG: +{len(additions)} new, {len(catalog['items'])} total.")
    print(f"User-confirmed in-game among batch: {sum(x['compatibility_status']=='user_confirmed_in_game' for x in records)}")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, UnicodeError, OSError, KeyError, json.JSONDecodeError) as error:
        print("FAILED:", error, file=sys.stderr)
        sys.exit(1)
