"""Build a conventional TES3 translation plugin from the owner's original masters.

The player only needs the resulting mod. Python is a maintainer dependency.
Dialogue merging follows OpenMW 0.51 components/esm3/infoorder.hpp.
"""
from __future__ import annotations
import argparse
import collections
from pathlib import Path
import shutil
import struct
import zipfile
from mwbr import ROOT, RH, SH, catalog, data_folder, load, patch_master, records, require, save, sha

PLUGIN = 'Morrowind_PTBR.esp'

def field(record, name, default=b''):
    return next((v for k,v in record[3] if k == name), default)

def ident(value):
    # OpenMW string RefIds compare ASCII case-insensitively (not Unicode casefold).
    return value.split(b'\0',1)[0].lower()

def encode(record):
    tag, unknown, flags, subs = record
    body = b''.join(SH.pack(k,len(v))+v for k,v in subs)
    return RH.pack(tag,len(body),unknown,flags)+body

def key(record):
    tag = record[0]
    if tag in (b'MGEF',b'SKIL'):
        return tag, field(record,b'INDX')
    if tag == b'SCPT':
        return tag, ident(field(record,b'SCHD')[:32])
    value = field(record,b'NAME')
    require(bool(value), 'Registro sem identidade: '+repr(tag))
    return tag, ident(value)

def deleted(record):
    return any(k==b'DELE' for k,v in record[3])

class InfoOrder:
    def __init__(self):
        self.order=[]
        self.values={}

    def insert(self, record):
        uid=ident(field(record,b'INAM')); prev=ident(field(record,b'PNAM'))
        if uid in self.values and ident(field(self.values[uid],b'PNAM'))==prev:
            self.values[uid]=record
            return
        if uid in self.values:
            self.order.remove(uid)
        index=0 if not prev else self.order.index(prev)+1 if prev in self.order else len(self.order)
        self.order.insert(index,uid)
        self.values[uid]=record

    def live(self):
        return [self.values[k] for k in self.order if not deleted(self.values[k])]

def snapshot(streams, types):
    regular={}; dialogues={}
    for stream in streams:
        current=None
        for record in records(stream):
            tag=record[0]
            if record[2] & 0x1000:  # ESM::FLAG_Ignored
                continue
            if tag==b'DIAL':
                uid=ident(field(record,b'NAME'))
                if deleted(record):
                    dialogues.pop(uid,None); current=None
                else:
                    if uid not in dialogues: dialogues[uid]=[record,InfoOrder()]
                    else: dialogues[uid][0]=record
                    current=dialogues[uid][1]
            elif tag==b'INFO':
                require(current is not None,'INFO sem DIAL')
                current.insert(record)
            else:
                current=None
                if tag in types:
                    uid=key(record)
                    if deleted(record): regular.pop(uid,None)
                    else: regular[uid]=record
    return regular,{k:(r,order.live()) for k,(r,order) in dialogues.items()}

def semantic_info(record):
    return record[:3],[(k,v) for k,v in record[3] if k not in (b'PNAM',b'NNAM')]

def semantic_dialogue(group):
    return group[0],[semantic_info(r) for r in group[1]]

def relink(infos):
    """Materialize the final order after merging expansions and deleted INFOs.

    Only neighbour links change. IDs, filters, scripts and response bytes stay exact.
    """
    result=[]
    for i,record in enumerate(infos):
        links={b'PNAM':field(infos[i-1],b'INAM') if i else b'\0',
               b'NNAM':field(infos[i+1],b'INAM') if i+1<len(infos) else b'\0'}
        result.append((*record[:3],[(k,links.get(k,v)) for k,v in record[3]]))
    return result

def make_plugin(originals, translated, master_sizes, types):
    before=snapshot(originals,types); after=snapshot(translated,types)
    output=[r for k,r in after[0].items() if before[0].get(k)!=r]
    require(before[0].keys()==after[0].keys(),'Identidade de registro comum foi alterada')
    changed={k for k in before[1].keys()|after[1].keys()
             if before[1].get(k)!=after[1].get(k)}
    # Remove old topic identities and reset changed dialogue groups. All deletions
    # precede additions: a translated name may equal another original topic name.
    for uid in sorted(changed & before[1].keys()):
        output.append((b'DIAL',0,0,[(b'NAME',field(before[1][uid][0],b'NAME')),(b'DELE',b'\0'*3)]))
    for uid in sorted(changed & after[1].keys()):
        record,infos=after[1][uid]
        output.append(record)
        output.extend(relink(infos))
    header=[(b'HEDR',struct.pack('<fI32s256sI',1.3,0,b'chadvictor',
              b'Morrowind PT-BR - OpenMW 0.51. Requires Morrowind, Tribunal and Bloodmoon.',len(output)))]
    for name,size in master_sizes:
        header.extend([(b'MAST',name.encode('ascii')+b'\0'),(b'DATA',struct.pack('<Q',size))])
    plugin=encode((b'TES3',0,0,header))+b''.join(encode(r) for r in output)
    # Reapply the finished plugin to ORIGINAL masters, then compare the complete
    # effective translated state, including all response order and filter bytes.
    applied=snapshot([*originals,plugin],types)
    require(applied[0]==after[0],'Plugin diverge dos registros traduzidos')
    require(applied[1].keys()==after[1].keys(),'Plugin perdeu ou duplicou tópicos')
    for uid,group in after[1].items():
        require(semantic_dialogue(applied[1][uid])==semantic_dialogue(group),
                'Diálogo/filtro/ordem divergente: '+repr(uid))
    stats={'plugin':PLUGIN,'sha256':sha(plugin),'bytes':len(plugin),
           'records':dict(collections.Counter(r[0].decode() for r in output)),
           'effective_dialogues':len(after[1]),
           'effective_infos':sum(len(v[1]) for v in after[1].values()),
           'verified':'original masters + ESP == localized masters; INFO neighbour links normalized'}
    return plugin,stats

def build(game, destination, development=False, root=ROOT):
    manifest,rows,frozen=catalog(root)
    require(frozen or development,'Catálogos editados: use --development para teste local')
    game=data_folder(game); destination=Path(destination).resolve()
    require(not destination.exists(),'Escolha um destino novo; não sobrescrevemos pacotes')
    originals=[]; translated=[]; sizes=[]
    for info in manifest['masters']:
        name=info['name']; original=(game/name).read_bytes()
        require(sha(original)==info['source_sha256'],'Master incompatível: '+name)
        print('Validando e convertendo '+name,flush=True)
        target=patch_master(original,[e for e in rows.values() if e['id'].startswith(name+':')])
        if frozen: require(sha(target)==info['output_sha256'],'Tradução diverge: '+name)
        originals.append(original);translated.append(target);sizes.append((name,len(original)))
    types={e['type'].encode() for e in rows.values()}-{b'DIAL',b'INFO'}
    require(not types & {b'CELL',b'LAND',b'PGRD'},'Registros de mundo não suportados pelo exportador')
    plugin,stats=make_plugin(originals,translated,sizes,types)
    data=destination/'Data Files'; data.mkdir(parents=True)
    shutil.copytree(root/'conteudo/data',data,dirs_exist_ok=True)
    # Translation maps load by content-file stem. All three legacy maps must agree.
    for suffix in ('.cel','.top','.mrk'):
        values=[(data/(Path(n).stem+suffix)).read_bytes() for n,_ in sizes]
        require(all(v==values[0] for v in values),'Mapas por master divergentes')
        (data/(Path(PLUGIN).stem+suffix)).write_bytes(values[0])
        for n,_ in sizes: (data/(Path(n).stem+suffix)).unlink()
    (data/PLUGIN).write_bytes(plugin)
    extra=destination/'Extras';extra.mkdir()
    fallbacks=load(root/'conteudo/fallbacks.json')
    (extra/'openmw-fallbacks.cfg').write_text(''.join('fallback='+k+','+v+'\n' for k,v in sorted(fallbacks.items())),encoding='utf-8')
    (extra/'settings-idioma.cfg').write_text('[General]\npreferred locales = pt_BR, en\n\n[GUI]\nsubtitles = true\n',encoding='utf-8')
    shutil.copytree(root/'conteudo/resources/translations',extra/'launcher/translations')
    shutil.copytree(root/'interface/qt',extra/'launcher/fontes-qt')
    shutil.copytree(root/'LICENSES',destination/'LICENSES')
    for name in ('LICENSE','THIRD_PARTY_NOTICES.md'):
        shutil.copy2(root/name,destination/name)
    shutil.copy2(root/'docs/JOGAR.txt',destination/'LEIA-ME.txt')
    stats.update(version=manifest['version'],masters=[{'name':n,'sha256':sha(b)} for (n,_),b in zip(sizes,originals)],frozen=frozen)
    save(destination/'manifesto-mod.json',stats)
    return destination,stats

def package(folder, version):
    archive=folder.parent/f'morrowind-ptbr-openmw-mod-{version}.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(folder.rglob('*')):
            if p.is_file():
                require(p.suffix.lower() not in {'.esm','.bsa','.exe','.py','.bat'},'Arquivo indevido no mod: '+p.name)
                info=zipfile.ZipInfo('Morrowind-PTBR/'+p.relative_to(folder).as_posix(),date_time=(2026,1,1,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                z.writestr(info,p.read_bytes())
    with zipfile.ZipFile(archive) as z: require(z.testzip() is None,'ZIP corrompido')
    archive.with_suffix('.zip.sha256').write_text(sha(archive.read_bytes())+'  '+archive.name+'\n',encoding='ascii')
    return archive

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--game',required=True);p.add_argument('--output',required=True)
    p.add_argument('--development',action='store_true');p.add_argument('--zip',action='store_true')
    args=p.parse_args();folder,stats=build(args.game,args.output,args.development)
    print(stats)
    if args.zip: print(package(folder,stats['version']))

if __name__=='__main__':main()
