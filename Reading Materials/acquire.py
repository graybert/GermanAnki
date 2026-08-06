#!/usr/bin/env python3
"""Conservative, cross-platform acquisition helper.

It downloads only explicit open dump files and clones public Git repositories.
For web/reference/restricted sources it writes a queue instead of mirroring sites.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

HERE=Path(__file__).resolve().parent
MANIFEST=HERE/'source_manifest.json'
SOURCES={x['source_id']:x for x in json.loads(MANIFEST.read_text(encoding='utf-8'))}

DIRECT = {
 'dewiki_dump': 'https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles-multistream.xml.bz2',
 'dewikivoyage_dump': 'https://dumps.wikimedia.org/dewikivoyage/latest/dewikivoyage-latest-pages-articles.xml.bz2',
 'dewikibooks_dump': 'https://dumps.wikimedia.org/dewikibooks/latest/dewikibooks-latest-pages-articles.xml.bz2',
 'dewikinews_dump': 'https://dumps.wikimedia.org/dewikinews/latest/dewikinews-latest-pages-articles.xml.bz2',
}
GIT = {
 'deplain': 'https://github.com/rstodden/DEPlain.git',
 'simple_german_corpus': 'https://github.com/buschmo/Simple-German-Corpus.git',
 'dwie': 'https://github.com/klimzaporojets/DWIE.git',
 'potec': 'https://github.com/DiLi-Lab/PoTeC.git',
 'plainmedscale': 'https://github.com/GS-Uni-Heidelberg/PlainMedScale.git',
}

def ensure(root:Path):
    for x in ['raw','extracted','normalized','metadata','candidates','indexes','manifests','logs','queues']:
        (root/x).mkdir(parents=True,exist_ok=True)
    shutil.copy2(MANIFEST,root/'manifests'/'source_manifest.json')

def download(url:str,out:Path):
    out.parent.mkdir(parents=True,exist_ok=True)
    tmp=out.with_suffix(out.suffix+'.part')
    headers={}
    mode='wb'
    if tmp.exists():
        headers['Range']=f'bytes={tmp.stat().st_size}-'; mode='ab'
    with requests.get(url,stream=True,headers=headers,timeout=60) as r:
        if r.status_code==200 and mode=='ab':
            mode='wb'
        r.raise_for_status()
        total=int(r.headers.get('content-length') or 0)
        with tmp.open(mode) as f, tqdm(total=total,unit='B',unit_scale=True,desc=out.name) as p:
            for chunk in r.iter_content(1024*1024):
                if chunk: f.write(chunk); p.update(len(chunk))
    tmp.replace(out)

def clone(url:str,out:Path):
    if out.exists():
        subprocess.run(['git','-C',str(out),'pull','--ff-only'],check=True)
    else:
        subprocess.run(['git','clone','--depth','1',url,str(out)],check=True)

def lcc_links(kind:str):
    page='https://wortschatz.uni-leipzig.de/en/download/German'
    html=requests.get(page,timeout=60).text
    soup=BeautifulSoup(html,'html.parser')
    terms={'lcc_news_de_1m':['news','1M'],'lcc_web_de_1m':['web','1M'],'lcc_wikipedia_de_1m':['wikipedia','1M']}[kind]
    found=[]
    for a in soup.find_all('a',href=True):
        href=urljoin(page,a['href']); text=(a.get_text(' ',strip=True)+' '+href).lower()
        if all(t.lower() in text for t in terms) and any(href.endswith(x) for x in ['.tar.gz','.tgz','.zip']):
            found.append(href)
    return sorted(set(found))

def queue(ids,root):
    q=[]
    for sid in ids:
        s=SOURCES[sid]
        q.append({k:s[k] for k in ['source_id','priority_tier','name','direct_url','access_class','command_or_download_hint','rights_and_access_notes','recommended_acquisition_scope']})
    p=root/'queues'/'manual_and_review_queue.json'
    p.write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Wrote {p} ({len(q)} sources)')

def fetch(sid,root):
    s=SOURCES[sid]; dest=root/'raw'/sid; dest.mkdir(parents=True,exist_ok=True)
    meta=root/'metadata'/sid; meta.mkdir(parents=True,exist_ok=True)
    (meta/'manifest_record.json').write_text(json.dumps(s,ensure_ascii=False,indent=2),encoding='utf-8')
    if sid in DIRECT:
        url=DIRECT[sid]; download(url,dest/Path(url).name); return
    if sid in GIT:
        clone(GIT[sid],dest/'repo'); return
    if sid.startswith('lcc_'):
        links=lcc_links(sid)
        (meta/'candidate_download_links.txt').write_text('\n'.join(links),encoding='utf-8')
        if not links:
            print(f'No exact archive auto-detected for {sid}; inspect {s["direct_url"]}',file=sys.stderr); return
        # Download the most recent-looking last sorted candidate only; user can inspect link file.
        url=links[-1]; download(url,dest/Path(url).name); return
    print(f'{sid}: manual/terms-aware acquisition required. Added metadata only: {s["direct_url"]}')

def selected(args):
    if args.ids: return args.ids
    out=[]
    for sid,s in SOURCES.items():
        if args.tier is None or int(s['priority_tier'])<=args.tier: out.append(sid)
    return out

def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest='cmd',required=True)
    pi=sub.add_parser('init'); pi.add_argument('--root',type=Path,required=True)
    pl=sub.add_parser('list'); pl.add_argument('--tier',type=int); pl.add_argument('ids',nargs='*')
    pf=sub.add_parser('fetch'); pf.add_argument('ids',nargs='+'); pf.add_argument('--root',type=Path,required=True)
    pq=sub.add_parser('queue'); pq.add_argument('--tier',type=int); pq.add_argument('--root',type=Path,required=True); pq.add_argument('ids',nargs='*')
    a=p.parse_args()
    if a.cmd=='init': ensure(a.root); print(f'Initialized {a.root}'); return
    if a.cmd=='list':
        for sid in selected(a):
            s=SOURCES[sid]; print(f'{sid:28} T{s["priority_tier"]} {s["access_class"]:20} {s["name"]}')
        return
    ensure(a.root)
    if a.cmd=='fetch':
        for sid in a.ids:
            if sid not in SOURCES: raise SystemExit(f'Unknown source_id: {sid}')
            fetch(sid,a.root)
    elif a.cmd=='queue': queue(selected(a),a.root)
if __name__=='__main__': main()
