#!/usr/bin/env python3
"""Import an approved ModVerse vehicle batch after validating all supplied assets.

Runs in GitHub Actions, entirely in the repository checkout. Does not access private
approval evidence. Does not change Lua scripts, themes or existing catalog rows.
"""
from __future__ import annotations
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'marketplace' / 'vehicles'
SOURCE = BASE / 'inbox' / 'modverse-approved-119.zip'
CATALOG = BASE / 'catalog.json'
ID = re.compile(r'[0-9]+-[0-9]+\Z')
HASH = re.compile(r'[a-f0-9]{64}\Z')
INSTALL_NAME = re.compile(r'mMV_[A-Za-z0-9_-]+\.json\Z')
EXPECTED = 119

def fail(msg):
    raise ValueError(msg)

def check_hash(blob, sha, label):
    if not isinstance(sha, str) or not HASH.fullmatch(sha):
        fail(f'{label}: invalid hash')
    if hashlib.sha256(blob).hexdigest() != sha:
        fail(f'{label}: SHA256 mismatch')

def main():
    if not SOURCE.is_file():
        print('No approved batch ZIP found, skipping.'); return 0
    if SOURCE.stat().st_size > 25_000_000:
        fail('ZIP exceeds 25MB upload limit')
    catalog = json.loads(CATALOG.read_text(encoding='utf-8-sig'))
    if catalog.get('schema') != 'modverse.vehicles.v1' or catalog.get('published') is not True:
        fail('Existing public catalog invalid')
    old = catalog.get('items')
    if not isinstance(old, list): fail('Existing items missing')
    byid = {x['id']:x for x in old}
    oldnames = {x['filename'] for x in old}
    oldhashes = {x['sha256'].lower() for x in old}
    if len(byid) != len(old): fail('Existing duplicate IDs')
    pending = []
    existing = 0
    with zipfile.ZipFile(SOURCE) as z:
        members = z.namelist()
        if len(members) != len(set(members)): fail('Duplicate ZIP members')
        if len(members) > 242: fail('Too many ZIP entries')
        if sum(info.file_size for info in z.infolist()) > 85_000_000:
            fail('Expanded ZIP exceeds size cap')
        if 'batch-manifest.json' not in members: fail('Manifest missing')
        manifest_bytes = z.read('batch-manifest.json')
        if len(manifest_bytes) > 900_000: fail('Manifest too large')
        manifest = json.loads(manifest_bytes.decode('utf-8-sig'))
        if manifest.get('schema') != 'modverse.vehicles.import-batch.v1' or manifest.get('expected_count') != EXPECTED:
            fail('Unexpected manifest schema/count')
        items = manifest.get('items')
        if not isinstance(items,list) or len(items) != EXPECTED:
            fail(f'Expected exactly {EXPECTED} approved records')
        approved_files = {'batch-manifest.json','README_UPLOAD_TO_GITHUB_FIRST.txt'}
        seen_ids = set(); seen_names = set(); seen_hashes = set()
        for row in items:
            if not isinstance(row,dict):fail('Non-object manifest item')
            ident = row.get('id')
            name = row.get('name')
            creator = row.get('creator')
            contributor = row.get('shared_by')
            filename = row.get('filename')
            size = row.get('size_bytes')
            model = row.get('model')
            if not isinstance(ident,str) or len(ident)>55 or not ID.fullmatch(ident):fail('Unsafe catalog ID')
            if not isinstance(filename,str) or len(filename)>150 or not INSTALL_NAME.fullmatch(filename):fail(f'{ident}: unsafe filename')
            if not isinstance(name,str) or not 1 <= len(name.encode('utf-8')) <= 180:fail(f'{ident}: invalid name')
            if not isinstance(creator,str) or not 1 <= len(creator.encode('utf-8')) <= 100:fail(f'{ident}: missing creator field')
            if not isinstance(contributor,str) or not 1 <= len(contributor.encode('utf-8')) <= 100:fail(f'{ident}: missing shared-by')
            if type(size) is not int or not 100 <= size <= 65536:fail(f'{ident}: invalid size')
            if type(model) is not int or not -2147483648 <= model <= 4294967295:fail(f'{ident}: invalid model')
            if ident in seen_ids or filename in seen_names or row.get('sha256') in seen_hashes:
                fail('Duplicate item in batch')
            seen_ids.add(ident); seen_names.add(filename); seen_hashes.add(row['sha256'])
            if ident in byid:
                if byid[ident] != row:fail(f'{ident}: conflicts with existing public entry')
                existing += 1
            else:
                if filename in oldnames or row['sha256'].lower() in oldhashes:
                    fail(f'{ident}: collides with existing public vehicle')
            jp=f'marketplace/vehicles/files/{ident}.json'
            pp=f'marketplace/vehicles/thumbnails/{ident}.jpg'
            approved_files.add(jp);approved_files.add(pp)
            if jp not in members or pp not in members:fail(f'{ident}: asset missing from ZIP')
            j=z.read(jp);p=z.read(pp)
            if len(j)!=size:fail(f'{ident}: JSON size mismatch')
            check_hash(j,row.get('sha256'),f'{ident} JSON')
            check_hash(p,row.get('thumbnail_sha256'),f'{ident} JPEG')
            if not(p.startswith(b'\xff\xd8') and p.endswith(b'\xff\xd9')):
                fail(f'{ident}: preview must be JPEG')
            doc=json.loads(j.decode('utf-8-sig'))
            if not isinstance(doc,dict) or doc.get('format')!='Cherax Entity' or doc.get('type')!=1 or doc.get('model')!=model:
                fail(f'{ident}: invalid Cherax Entity vehicle')
            for relative, blob in [(jp,j),(pp,p)]:
                dst=ROOT/relative
                if dst.exists() and dst.read_bytes()!=blob:
                    fail(f'{ident}: destination already exists with different bytes')
            pending.append((row,j,p))
        if set(members)!=approved_files:
            fail('Unapproved extra ZIP members found')
    if len(old)+len(pending)-existing>500:fail('Catalog limit exceeded')
    # All assets passed validation before writes begin.
    for row,j,p in pending:
        ident=row['id']
        a=BASE/'files'/f'{ident}.json'
        b=BASE/'thumbnails'/f'{ident}.jpg'
        a.parent.mkdir(parents=True,exist_ok=True)
        b.parent.mkdir(parents=True,exist_ok=True)
        if not a.exists():a.write_bytes(j)
        if not b.exists():b.write_bytes(p)
    new=[row for row,_,_ in pending if row['id'] not in byid]
    catalog['items']=old+new
    if new:
        catalog['catalog_version']=int(catalog.get('catalog_version',1))+1
        catalog['updated_at']='2026-10-12'
    CATALOG.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    SOURCE.unlink() # Keep only published assets in working tree after commit.
    print(f'IMPORTED: new={len(new)}, already_present={existing}, total={len(catalog["items"])}')
    print('NOTE: No claim of in-game compatibility for untested vehicles or independently verified original developers.')
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,KeyError,OSError,UnicodeError,zipfile.BadZipFile,json.JSONDecodeError) as error:
        print('IMPORT FAILED:',error,file=sys.stderr)
        sys.exit(1)
