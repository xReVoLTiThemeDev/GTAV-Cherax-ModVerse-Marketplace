#!/usr/bin/env python3
"""Validate the ModVerse public vehicle catalog and referenced assets.

Checks integrity and Cherax format only; creator redistribution rights require
separate human approval before any asset is published.
"""
from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "marketplace" / "vehicles"
ID = re.compile(r"[0-9]+-[0-9]+\Z")
HASH = re.compile(r"[a-fA-F0-9]{64}\Z")
FILENAME = re.compile(r"mMV_[A-Za-z0-9_-]+\.json\Z")

def check():
    raw = (BASE / "catalog.json").read_bytes()
    if len(raw) > 1024 * 1024:
        raise ValueError("Catalog exceeds 1 MB Cherax client limit")
    catalog = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(catalog, dict) or catalog.get("schema") != "modverse.vehicles.v1" or catalog.get("published") is not True:
        raise ValueError("Unexpected schema/published status")
    items = catalog.get("items")
    if not isinstance(items, list) or len(items) > 500:
        raise ValueError("Items must be a list of <=500")
    ids, filenames = set(), set()
    for num, row in enumerate(items, 1):
        prefix = f"Item {num}: "
        if not isinstance(row, dict):
            raise ValueError(prefix + "not an object")
        ident, name, creator, filename = [row.get(k) for k in ("id","name","creator","filename")]
        sha, thumb_sha = row.get("sha256"), row.get("thumbnail_sha256")
        size, model = row.get("size_bytes"), row.get("model")
        if not isinstance(ident, str) or len(ident) > 55 or not ID.fullmatch(ident) or ident in ids:
            raise ValueError(prefix + "invalid or duplicate ID")
        ids.add(ident)
        if not isinstance(name, str) or not 1 <= len(name.encode("utf-8")) <= 180:
            raise ValueError(prefix + "invalid name")
        if not isinstance(creator, str) or not 1 <= len(creator.encode("utf-8")) <= 100:
            raise ValueError(prefix + "invalid creator")
        if not isinstance(filename, str) or len(filename) > 150 or not FILENAME.fullmatch(filename) or filename in filenames:
            raise ValueError(prefix + "invalid or duplicate mMV filename")
        filenames.add(filename)
        if not isinstance(sha, str) or not HASH.fullmatch(sha) or not isinstance(thumb_sha, str) or not HASH.fullmatch(thumb_sha):
            raise ValueError(prefix + "invalid SHA256 hash")
        if type(size) is not int or not 100 <= size <= 65536:
            raise ValueError(prefix + "invalid JSON size")
        if type(model) is not int or not -2147483648 <= model <= 4294967295:
            raise ValueError(prefix + "invalid model ID")
        payload = (BASE / "files" / (ident + ".json")).read_bytes()
        preview = (BASE / "thumbnails" / (ident + ".jpg")).read_bytes()
        if len(payload) != size or hashlib.sha256(payload).hexdigest().lower() != sha.lower():
            raise ValueError(prefix + "JSON SHA256/size mismatch")
        if hashlib.sha256(preview).hexdigest().lower() != thumb_sha.lower():
            raise ValueError(prefix + "preview SHA256 mismatch")
        if not (preview.startswith(b"\xff\xd8") and preview.endswith(b"\xff\xd9")):
            raise ValueError(prefix + "preview not JPEG")
        vehicle = json.loads(payload.decode("utf-8-sig"))
        if not isinstance(vehicle, dict) or vehicle.get("format") != "Cherax Entity" or vehicle.get("type") != 1 or vehicle.get("model") != model:
            raise ValueError(prefix + "unexpected Cherax vehicle schema/model")
    print(f"PASS: {len(items)} approved ModVerse vehicle(s), with SHA-256 verified JSONs and previews")
    print("Structural checks do not establish creator redistribution rights.")

if __name__ == "__main__":
    try:
        check()
    except (OSError, ValueError, UnicodeError, json.JSONDecodeError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
