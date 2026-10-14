#!/usr/bin/env python3
"""ModVerse Cherax Outfit/DLC catalog validator. Supports GitHub Release RPFs.

Outfit JSON blobs are immutable Git files. DLC RPFs are SHA-256-pinned GitHub
Release assets. CI validates release digest/size against GitHub metadata.
"""
import hashlib,json,os,re,sys,urllib.request
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent/'marketplace'
REPO='xReVoLTiThemeDev/GTAV-Cherax-ModVerse-Marketplace'
SAFE=re.compile(r'^[A-Za-z0-9_-]{3,100}$')
NAME=re.compile(r'^mMV_[A-Za-z0-9_-]+\.(json|rpf)$')
HASH=re.compile(r'^[a-f0-9]{64}$')
release_cache={}

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as fp:
  for b in iter(lambda:fp.read(1048576),b''):h.update(b)
 return h.hexdigest()

def published_release(tag):
 if tag in release_cache:return release_cache[tag]
 if not SAFE.fullmatch(tag):raise ValueError('Unsafe release tag')
 url=f'https://api.github.com/repos/{REPO}/releases/tags/{tag}'
 headers={'Accept':'application/vnd.github+json','User-Agent':'ModVerse-Catalog-Validator'}
 token=os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
 if token:headers['Authorization']='Bearer '+token
 with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=25) as r:
  d=json.loads(r.read(10*1024*1024))
 if d.get('tag_name')!=tag:raise ValueError('Release tag mismatch')
 assets={a['name']:a for a in d.get('assets',[])}
 release_cache[tag]=assets
 return assets

def valid():
 for kind in ('outfits','dlcs'):
  folder=BASE/kind
  main=json.loads((folder/'catalog.json').read_text(encoding='utf-8-sig'))
  if main.get('schema')!='modverse.cherax.assets.v1' or main.get('published') is not True or main.get('category')!=kind:raise ValueError('Catalog schema invalid: '+kind)
  pages=main.get('pages',[])
  if not isinstance(pages,list) or len(pages)>9 or pages!=list(range(2,len(pages)+2)):raise ValueError('Unexpected pagination')
  docs=[main]
  for pg in pages:
   data=(folder/f'catalog-{pg}.json').read_bytes()
   if len(data)>1048576:raise ValueError('Catalog exceeds 1MiB')
   docs.append(json.loads(data.decode('utf-8-sig')))
  seen_ids=set();seen_names=set();n=0
  for doc in docs:
   if doc.get('schema')!=main['schema'] or doc.get('category')!=kind or doc.get('published') is not True:raise ValueError('Page header mismatch')
   rows=doc.get('items')
   if not isinstance(rows,list) or len(rows)>500:raise ValueError('Page too many items')
   for row in rows:
    ident=row.get('id');filename=row.get('filename');digest=row.get('sha256');size=row.get('size_bytes')
    if not isinstance(ident,str) or not SAFE.fullmatch(ident) or ident in seen_ids:raise ValueError('Bad/duplicate id')
    if not isinstance(filename,str) or not NAME.fullmatch(filename) or not filename.endswith('.json' if kind=='outfits' else '.rpf') or filename in seen_names:raise ValueError('Bad filename')
    if not isinstance(digest,str) or not HASH.fullmatch(digest):raise ValueError('Bad SHA')
    if type(size)!=int or not (16 if kind=='outfits' else 4096)<=size<=(2097152 if kind=='outfits' else 128*1024*1024):raise ValueError('Bad size')
    if not isinstance(row.get('name'),str) or not row.get('name') or not isinstance(row.get('shared_by'),str) or not row.get('shared_by'):raise ValueError('Missing name/uploader')
    seen_ids.add(ident);seen_names.add(filename);n+=1
    if kind=='outfits':
     path=folder/'files'/(ident+'.json')
     if not path.is_file() or path.stat().st_size!=size or sha(path)!=digest:raise ValueError('Missing/changed outfit: '+ident)
     doc=json.loads(path.read_text(encoding='utf-8-sig'))
     if not isinstance(doc,dict) or doc.get('format')!='Cherax Entity' or doc.get('type')!=2 or not isinstance(doc.get('components'),dict) or not isinstance(doc.get('props'),dict):raise ValueError('Non-outfit source: '+ident)
    else:
     tag=row.get('release_tag');name=row.get('asset_name')
     if not isinstance(tag,str) or not SAFE.fullmatch(tag) or name!=filename:raise ValueError('DLC release source invalid')
     asset=published_release(tag).get(name)
     if not asset or asset.get('size')!=size or asset.get('digest')!='sha256:'+digest:raise ValueError('DLC Release asset mismatch: '+ident)
  if n>5000:raise ValueError('Combined catalog exceeds client limit')
  print('PASS:',kind,n,'catalog entries, '+('local source files SHA-256 verified' if kind=='outfits' else 'GitHub Release SHA-256/size verified'))
if __name__=='__main__':
 try:valid()
 except Exception as e:print('FAILED:',e,file=sys.stderr);sys.exit(1)
