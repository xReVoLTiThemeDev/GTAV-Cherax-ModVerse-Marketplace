#!/usr/bin/env python3
"""Validate public ModVerse Cherax Outfits and DLCs catalogs and uploaded assets.

Structural and integrity checks cannot establish permission, creator identity,
or in-game compatibility. The release maintainer must verify those separately.
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "marketplace"
ID = re.compile(r"[A-Za-z0-9_-]{3,100}\Z")
SHA = re.compile(r"[0-9a-f]{64}\Z")
SAFE_FILENAME = re.compile(r"[A-Za-z0-9_.-]{1,150}\Z")

def check_category(kind: str):
    folder = ROOT / kind
    raw = (folder / "catalog.json").read_bytes()
    if len(raw) > 1024 * 1024:
        raise ValueError(f"{kind}: catalog exceeds 1 MiB")
    catalog = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(catalog, dict) or catalog.get("schema") != "modverse.cherax.assets.v1":
        raise ValueError(f"{kind}: schema mismatch")
    if catalog.get("published") is not True or catalog.get("category") != kind:
        raise ValueError(f"{kind}: category/published mismatch")
    items = catalog.get("items")
    if not isinstance(items, list) or len(items) > 500:
        raise ValueError(f"{kind}: main items must be an array with 0-500 records")
    pages = catalog.get("pages", [])
    if not isinstance(pages, list) or len(pages) > 9 or pages != list(range(2,len(pages)+2)):
        raise ValueError(f"{kind}: invalid page list (expected 2,3,..., max 10 pages)")
    all_items = list(items)
    for page in pages:
        page_file = folder / f"catalog-{page}.json"
        page_raw = page_file.read_bytes()
        if len(page_raw) > 1024*1024:
            raise ValueError(f"{kind}: catalog-{page} exceeds 1 MiB")
        page_doc = json.loads(page_raw.decode("utf-8-sig"))
        if not isinstance(page_doc,dict) or page_doc.get("schema") != catalog["schema"] or page_doc.get("category") != kind or page_doc.get("published") is not True:
            raise ValueError(f"{kind}: invalid catalog-{page}")
        page_items = page_doc.get("items")
        if not isinstance(page_items,list) or len(page_items) > 500:
            raise ValueError(f"{kind}: invalid catalog-{page} item count")
        all_items.extend(page_items)
    if len(all_items) > 5000:
        raise ValueError(f"{kind}: over 5,000 entries")
    ids, filenames, hashes = set(), set(), set()
    for i, row in enumerate(all_items, 1):
        label = f"{kind}[{i}]"
        if not isinstance(row, dict): raise ValueError(f"{label}: not an object")
        ident, filename = row.get("id"), row.get("filename")
        name, creator, shared = row.get("name"), row.get("creator"), row.get("shared_by")
        sha, size = row.get("sha256"), row.get("size_bytes")
        ext = ".json" if kind == "outfits" else ".rpf"
        if not isinstance(ident, str) or not ID.fullmatch(ident) or ".." in ident or ident in ids:
            raise ValueError(f"{label}: unsafe/duplicate id")
        ids.add(ident)
        if not isinstance(filename, str) or not SAFE_FILENAME.fullmatch(filename) or not filename.endswith(ext) or filename in filenames:
            raise ValueError(f"{label}: invalid/duplicate filename")
        filenames.add(filename)
        for key, txt in (("name", name),("creator",creator),("shared_by", shared)):
            if not isinstance(txt,str) or not 1 <= len(txt.encode("utf-8")) <= 180:
                raise ValueError(f"{label}: invalid {key}")
        if not isinstance(sha,str) or not SHA.fullmatch(sha) or sha in hashes:
            raise ValueError(f"{label}: invalid/duplicate sha256")
        hashes.add(sha)
        if type(size) is not int or not (4096 if kind == "dlcs" else 16) <= size <= (536870912 if kind == "dlcs" else 2097152):
            raise ValueError(f"{label}: invalid size")
        path = folder / "files" / (ident + ext)
        if not path.is_file() or path.stat().st_size != size:
            raise ValueError(f"{label}: missing or incorrect asset size: {path}")
        h = hashlib.sha256()
        with path.open("rb") as stream:
            header = stream.read(24)
            h.update(header)
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                h.update(chunk)
        if h.hexdigest() != sha:raise ValueError(f"{label}: asset checksum mismatch")
        if kind == "outfits":
            doc = json.loads(path.read_text(encoding="utf-8-sig"))
            if not isinstance(doc, (dict, list)) or (isinstance(doc,dict) and doc.get("format") == "Cherax Entity" and doc.get("type") == 1):
                raise ValueError(f"{label}: not a valid outfit JSON")
        else:
            if header[:4] != b"7FPR" or header[12:16] != b"OPEN":
                raise ValueError(f"{label}: DLC must be RPF7 OPEN")
            if size > 128 * 1024 * 1024:
                raise ValueError(f"{label}: exceeds current in-game Lua buffered-download limit")
            count = int.from_bytes(header[4:8], "little")
            names = int.from_bytes(header[8:12], "little")
            if count < 1 or count > 250000 or names < 1 or names > 128 * 1024 * 1024 or 16+count*16+names > size:
                raise ValueError(f"{label}: implausible RPF directory header")
        preview_sha = row.get("thumbnail_sha256")
        if preview_sha is not None:
            if not isinstance(preview_sha, str) or not SHA.fullmatch(preview_sha):
                raise ValueError(f"{label}: invalid thumbnail hash")
            thumbnail = folder / "thumbnails" / (ident + ".jpg")
            data = thumbnail.read_bytes()
            if len(data) < 100 or len(data) > 6*1024*1024 or not data.startswith(bytes([255,216])) or not data.endswith(bytes([255,217])):
                raise ValueError(f"{label}: missing/non-JPEG thumbnail")
            if hashlib.sha256(data).hexdigest() != preview_sha:raise ValueError(f"{label}: JPEG checksum mismatch")
    print(f"PASS: {kind}: {len(all_items)} SHA-256 verified downloadable assets across {1+len(pages)} page(s).")

if __name__ == "__main__":
    try:
        for category in ("outfits","dlcs"):check_category(category)
    except (ValueError,OSError,UnicodeError,json.JSONDecodeError) as e:
        print("FAILED:",e,file=sys.stderr)
        sys.exit(1)
