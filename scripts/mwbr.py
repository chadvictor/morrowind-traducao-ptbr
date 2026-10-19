"""Offline patch builder/installer. No network, AI, API keys or original game data."""
from __future__ import annotations
import argparse
import collections
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
RH = struct.Struct('<4sIII')
SH = struct.Struct('<4sI')
MARKER = '# MORROWIND-PTBR'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def require(condition, message):
    if not condition:
        raise ValueError(message)

def safe_relative(base, relative):
    path = (base/relative).resolve()
    require(path.is_relative_to(base.resolve()), f'Caminho fora do pacote: {relative}')
    return path

def records(blob):
    pos = 0
    while pos < len(blob):
        require(pos+16 <= len(blob), 'Cabeçalho TES3 truncado')
        tag, size, unknown, flags = RH.unpack_from(blob, pos)
        end = pos+16+size
        require(end <= len(blob), 'Registro TES3 truncado')
        subs = []
        cur = pos+16
        while cur < end:
            require(cur+8 <= end, 'Cabeçalho de campo truncado')
            field, length = SH.unpack_from(blob, cur)
            require(cur+8+length <= end, 'Campo TES3 truncado')
            subs.append((field, blob[cur+8:cur+8+length]))
            cur += 8+length
        yield tag, unknown, flags, subs
        pos = end

def payload(entry):
    text = entry['text']
    require(isinstance(text, str) and bool(text) and '\0' not in text, f"Texto vazio/NUL: {entry['id']}")
    raw = text.encode('cp1252')
    padding = entry['trailing_nuls']
    if entry['type'] == 'FACT' and entry['field'] == 'RNAM':
        padding = max(1, 32-len(raw))
    return raw + b'\0'*padding

def script_shape(text):
    # Mask only visible quoted arguments; preserve commands, IDs and branches.
    result=[]
    for line in text.splitlines(keepends=True):
        command=re.match(r'^\s*(?:(?:"[^"\r\n]*"|[\w.]+)\s*->\s*)?(MessageBox|Choice|Say)\b',line,re.I)
        if not command:
            result.append(line);continue
        tokens=[];i=command.end()
        while i<len(line):
            if line[i]==';':break
            if line[i]!='"':i+=1;continue
            end=line.find('"',i+1)
            require(end>=0,'Aspas não fechadas em script')
            tokens.append((i+1,end));i=end+1
        if command[1].lower()=='say':tokens=tokens[1:]
        for a,b in reversed(tokens):line=line[:a]+'{TEXTO}'+line[b:]
        result.append(line)
    return sha(''.join(result).encode())

def text_guards(entry):
    text=entry['text']
    # Explicit tokens only: "100% de" is ordinary prose, not a printf token.
    result={'links':sorted(re.findall(r'@[^@#\r\n]+#',text)),
            'tokens':sorted(re.findall(r'%(?:PC[A-Za-z]+|[SsGgDdIiFf]|\.[0-9]+[fFgG])\b',text))}
    if entry['field'] in ('SCTX','BNAM'):result['script_shape']=script_shape(text)
    if entry['type']=='DIAL':result['topic_hash']=sha(text.encode())
    if entry['type']=='BOOK' and entry['field']=='TEXT':result['markup']=re.findall(r'<[^>]*>',text)
    return result

def catalog(root=ROOT):
    manifest = load(root/'compatibilidade/manifesto.json')
    baseline = {e['id']: e for e in load(root/'compatibilidade/identidades.json')}
    guards = load(root/'compatibilidade/regras-textuais.json')
    rows = {}
    frozen = True
    actual = {p.relative_to(root).as_posix() for p in (root/'traducoes').rglob('*.jsonl')}
    require(actual == set(manifest['catalogs']), 'Arquivos de catálogo ausentes ou extras')
    for rel, info in manifest['catalogs'].items():
        path = safe_relative(root, rel)
        frozen &= sha(path.read_bytes()) == info['sha256']
        entries = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
        require(len(entries) == info['entries'], f'Quantidade alterada: {rel}')
        for e in entries:
            uid = e['id']
            require(uid not in rows, f'ID duplicado: {uid}')
            require({k:v for k,v in e.items() if k != 'text'} == baseline.get(uid), f'Identidade alterada: {uid}')
            require(rel.startswith('traducoes/'+uid.split(':')[0].removesuffix('.esm')+'/'), f'Master errado: {uid}')
            payload(e)
            require(text_guards(e)==guards.get(uid), f'Marcadores, tópicos ou lógica de script alterados: {uid}; coordene uma revisão técnica')
            rows[uid] = e
    require(rows.keys() == baseline.keys(), 'IDs ausentes/extras')
    for rel, expected in {**manifest['assets'], **manifest['qt_sources']}.items():
        path = safe_relative(root, rel)
        require(path.is_file(), f'Arquivo ausente: {rel}')
        frozen &= sha(path.read_bytes()) == expected
    validate_assets(root)
    return manifest, rows, frozen

def validate_assets(root):
    # YAML files deliberately use one JSON-quoted key/value pair per line.
    for p in (root/'conteudo/data/l10n').rglob('*.yaml'):
        keys = set()
        for line in p.read_text(encoding='utf-8').splitlines():
            pair = json.loads('{'+line+'}')
            require(len(pair) == 1, f'Linha YAML inválida: {p}')
            k, v = next(iter(pair.items()))
            require(k not in keys and isinstance(v, str), f'Chave duplicada/valor inválido: {p}')
            keys.add(k)
    for p in (root/'conteudo/data/mygui').glob('*.layout'):
        ET.parse(p)
    for p in (root/'interface/qt').glob('*.ts'):
        tree = ET.parse(p)
        for msg in tree.findall('.//message'):
            translation = msg.find('translation')
            require(translation is not None, f'Tradução Qt ausente: {p}')
    for p in (root/'conteudo/data').glob('*'):
        if p.suffix in ('.cel', '.top', '.mrk'):
            seen = set()
            for line in p.read_bytes().decode('cp1252').splitlines():
                key, value = line.split('\t')
                require(key not in seen and value, f'Mapa inválido: {p.name}/{key}')
                seen.add(key)
    for key, value in load(root/'conteudo/fallbacks.json').items():
        require(value and '\n' not in value and '\r' not in value, f'Fallback inválido: {key}')

def data_folder(game):
    game = Path(game).resolve()
    return game/'Data Files' if (game/'Data Files').is_dir() else game

def patch_master(original, entries):
    patches = {(e['record'], e['subrecord']):e for e in entries}
    require(len(patches) == len(entries), 'Destino de campo duplicado')
    out = bytearray()
    used = set()
    for ri, (tag, unknown, flags, subs) in enumerate(records(original)):
        body = bytearray()
        for si, (field, raw) in enumerate(subs):
            key = (ri, si)
            if key in patches:
                e = patches[key]
                require(tag.decode() == e['type'] and field.decode() == e['field'], f"Campo divergente: {e['id']}")
                require(sha(raw) == e['source_sha256'], f"Fonte divergente: {e['id']}")
                raw = payload(e)
                used.add(key)
            body.extend(SH.pack(field, len(raw))+raw)
        out.extend(RH.pack(tag, len(body), unknown, flags)+body)
    require(used == patches.keys(), 'Patches não aplicados')
    # Reparse and compare every field outside the intended patch set.
    for ri, (before, after) in enumerate(zip(records(original), records(out), strict=True)):
        require(before[:3] == after[:3], 'Cabeçalhos divergentes')
        for si, (a, b) in enumerate(zip(before[3], after[3], strict=True)):
            require(a[0] == b[0], 'Ordem de campos divergente')
            require(b[1] == (payload(patches[(ri, si)]) if (ri, si) in patches else a[1]), 'Campo alterado inesperadamente')
    return bytes(out)

def build(game, engine, destination, development=False, lrelease=None, root=ROOT):
    manifest, rows, frozen = catalog(root)
    require(frozen or development, 'Catálogo modificado. Valide e use --development para testar contribuições.')
    game = data_folder(game)
    engine = Path(engine).resolve()
    destination = Path(destination).resolve()
    require(not destination.is_relative_to(game) and not destination.is_relative_to(engine), 'Escolha destino fora do jogo e do OpenMW')
    inputs = {}
    for info in manifest['masters']:
        p = game/info['name']
        require(p.is_file(), f'Arquivo obrigatório ausente: {p.name}')
        b = p.read_bytes()
        require(sha(b) == info['source_sha256'], f"{p.name}: edição incompatível. Veja docs/COMPATIBILIDADE.md; originais não foram alterados.")
        inputs[p.name] = b
    for rel, expected in manifest['engine_inputs'].items():
        p = safe_relative(engine/'resources', rel)
        require(p.is_file() and sha(p.read_bytes()) == expected, f'Recurso OpenMW incompatível: {rel}. Use a versão suportada.')
    package_id = sha(json.dumps({rel:sha((root/rel).read_bytes()) for rel in sorted([*manifest['catalogs'],*manifest['assets'],*manifest['qt_sources']])}, sort_keys=True).encode())
    if destination.exists():
        state = destination/'mwbr-build.json'
        require(state.is_file(), 'Destino já existe e não pertence a este instalador; escolha outra pasta')
        old = load(state)
        require(old['package_id'] == package_id, 'Outra versão já está neste destino; escolha uma nova pasta')
        require(all((destination/p).is_file() and sha((destination/p).read_bytes()) == h for p,h in old['files'].items()), 'Instalação local foi alterada; escolha outra pasta')
        print('Pacote idêntico já preparado; nenhum arquivo alterado.')
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.mwbr-staging-', dir=destination.parent))
    try:
        shutil.copytree(root/'conteudo/data', stage/'data')
        shutil.copytree(engine/'resources', stage/'resources')
        shutil.copytree(root/'conteudo/resources', stage/'resources', dirs_exist_ok=True)
        shutil.copy2(root/'conteudo/fallbacks.json', stage/'fallbacks.json')
        for rel, expected in manifest['qt_sources'].items():
            if sha((root/rel).read_bytes()) != expected:
                require(lrelease, 'TS Qt alterado: informe --lrelease CAMINHO para recompilar')
                subprocess.run([str(lrelease), str(root/rel), '-qm', str(stage/'resources/translations'/(Path(rel).stem+'.qm'))], check=True)
        outputs = {}
        for info in manifest['masters']:
            name = info['name']
            print('Preparando '+name+'...', flush=True)
            translated = patch_master(inputs[name], [e for e in rows.values() if e['id'].startswith(name+':')])
            if frozen:
                require(sha(translated) == info['output_sha256'], 'Resultado diverge da versão validada: '+name)
            (stage/'data'/name).write_bytes(translated)
            outputs[name] = sha(translated)
        files = {p.relative_to(stage).as_posix():sha(p.read_bytes()) for p in stage.rglob('*') if p.is_file()}
        save(stage/'mwbr-build.json', {'version':manifest['version'],'package_id':package_id,'frozen':frozen,'masters':outputs,'files':files})
        stage.rename(destination)
        print('Pacote preparado: '+str(destination))
        return destination
    finally:
        # stage is a newly created sibling under the explicitly chosen destination.
        if stage.exists():
            require(stage.resolve().parent == destination.parent and stage.name.startswith('.mwbr-staging-'), 'Staging inesperado')
            shutil.rmtree(stage)

def quoted(path):
    return '"'+str(path).replace('&','&&').replace('"','&"')+'"'

def setting(text, section, key, value):
    lines=text.splitlines();current=None;done=False;out=[]
    for line in lines:
        match=re.fullmatch(r'\s*\[([^\]]+)\]\s*',line)
        if match:
            if current==section and not done:out.append(key+' = '+value);done=True
            current=match[1]
        if current==section and re.match(r'^\s*'+re.escape(key)+r'\s*=',line):
            if not done:out.append(key+' = '+value);done=True
        else:out.append(line)
    if not done:
        if current!=section:out.extend(['','['+section+']'])
        out.append(key+' = '+value)
    return '\n'.join(out)+'\n'

def atomic_write(path, data):
    fd, name = tempfile.mkstemp(prefix='.mwbr-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data);f.flush();os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):os.unlink(name)

def activate(bundle, profile):
    bundle=Path(bundle).resolve();profile=Path(profile).resolve()
    statefile=profile/'morrowind-ptbr-install.json'
    require((bundle/'mwbr-build.json').is_file(), 'Prepare o pacote antes de ativar')
    built=load(bundle/'mwbr-build.json')
    for rel,expected_hash in built.get('files',{}).items():
        path=safe_relative(bundle,rel)
        require(path.is_file() and sha(path.read_bytes())==expected_hash, 'Pacote local foi alterado: '+rel)
    if statefile.exists():
        old=load(statefile)
        require(old['bundle']==str(bundle), 'Desative a versão anterior antes de ativar outra')
        require(all((profile/n).is_file() and sha((profile/n).read_bytes())==h for n,h in old['after'].items()), 'Perfil mudou desde a ativação; consulte a desinstalação manual')
        print('Esta tradução já está ativa.');return
    require((profile/'openmw.cfg').is_file(), 'Selecione o perfil que contém openmw.cfg; abra o OpenMW original antes')
    before={n:(profile/n).read_bytes() if (profile/n).exists() else None for n in ('openmw.cfg','settings.cfg')}
    cfg=before['openmw.cfg'].decode('utf-8-sig')
    encodings=re.findall(r'^\s*encoding\s*=\s*(\S+)',cfg,re.M)
    require(not encodings or encodings[-1]=='win1252','O perfil deve usar encoding=win1252 para esta tradução')
    require(MARKER not in cfg, 'Outra ativação foi encontrada no perfil; verifique o backup')
    content=[m.strip() for m in re.findall(r'^\s*content\s*=\s*(.+)$',cfg,re.M)]
    expected=['Morrowind.esm','Tribunal.esm','Bloodmoon.esm']
    require(content==expected, 'Esta beta exige somente Morrowind.esm, Tribunal.esm e Bloodmoon.esm nesta ordem no perfil selecionado; use um perfil limpo sem mods.')
    fallbacks=load(bundle/'fallbacks.json');lines=[]
    for line in cfg.splitlines():
        m=re.match(r'^\s*fallback\s*=\s*([^,]+),',line)
        if re.match(r'^\s*resources\s*=',line) or (m and m[1] in fallbacks):continue
        lines.append(line)
    lines.extend(['',MARKER+' BEGIN','data='+quoted(bundle/'data'),'resources='+quoted(bundle/'resources')])
    lines.extend('fallback='+k+','+v for k,v in fallbacks.items())
    lines.append(MARKER+' END')
    settings=(before['settings.cfg'] or b'').decode('utf-8-sig')
    settings=setting(settings,'General','preferred locales','pt_BR, en')
    settings=setting(settings,'GUI','subtitles','true')
    after={'openmw.cfg':('\n'.join(lines)+'\n').encode(),'settings.cfg':settings.encode()}
    stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup=profile/'backups'/('morrowind-ptbr-'+stamp);backup.mkdir(parents=True)
    for n,b in before.items():
        if b is not None:(backup/n).write_bytes(b)
    state={'bundle':str(bundle),'backup':str(backup),'before':{n:sha(b) if b is not None else None for n,b in before.items()},'after':{n:sha(b) for n,b in after.items()}}
    require(all(((profile/n).read_bytes() if (profile/n).exists() else None)==b for n,b in before.items()), 'Perfil mudou durante a preparação; nenhum arquivo alterado')
    # Persist recovery information first, so interruption remains recoverable.
    atomic_write(statefile,(json.dumps(state,ensure_ascii=False,indent=2)+'\n').encode())
    for n,b in after.items():atomic_write(profile/n,b)
    print('Tradução ativa. Backup em '+str(backup))

def deactivate(profile):
    profile=Path(profile).resolve();statefile=profile/'morrowind-ptbr-install.json'
    if not statefile.exists():print('Nenhuma instalação registrada neste perfil.');return
    state=load(statefile);backup=Path(state['backup']).resolve()
    require(backup.is_relative_to(profile/'backups'), 'Backup fora do perfil')
    for n in ('openmw.cfg','settings.cfg'):
        p=profile/n;current=sha(p.read_bytes()) if p.exists() else None
        require(current in (state['after'][n],state['before'][n]), 'Configuração mudou após instalar. Nada foi sobrescrito; consulte docs/INSTALACAO.md para reversão manual.')
        if state['before'][n] is not None:
            require((backup/n).is_file() and sha((backup/n).read_bytes())==state['before'][n], 'Backup alterado ou ausente')
    for n in ('openmw.cfg','settings.cfg'):
        if state['before'][n] is None:
            if (profile/n).exists():(profile/n).unlink()
        else:atomic_write(profile/n,(backup/n).read_bytes())
    statefile.unlink()
    print('Configuração anterior restaurada. Saves, pacote e backups preservados.')

def context(uid, game):
    _,rows,_=catalog();require(uid in rows,'ID não encontrado')
    e=rows[uid];name=uid.split(':')[0]
    blob=(data_folder(game)/name).read_bytes()
    rec=next(r for i,r in enumerate(records(blob)) if i==e['record'])
    raw=rec[3][e['subrecord']][1]
    require(sha(raw)==e['source_sha256'],'Edição original incompatível')
    print(json.dumps({'id':uid,'context':{k:v for k,v in e.items() if k not in ('text','source_sha256')},
                      'original':raw.rstrip(b'\0').decode('cp1252'),'translation':e['text']},ensure_ascii=False,indent=2))

def gui(remove=False):
    import tkinter as tk
    from tkinter import filedialog, messagebox
    app=tk.Tk();app.withdraw()
    def choose(title):
        result=filedialog.askdirectory(title=title)
        if not result:raise InterruptedError('Cancelado; nenhuma ativação foi feita.')
        return Path(result)
    try:
        if remove:
            profile=choose('Selecione o perfil OpenMW (pasta que contém openmw.cfg)')
            deactivate(profile)
            messagebox.showinfo('Morrowind PT-BR','Tradução desativada. Saves e arquivos originais preservados.')
        else:
            messagebox.showinfo('Morrowind PT-BR — beta','Feche o OpenMW e o launcher.\nRequer Morrowind GOTY em inglês, OpenMW 0.51.0 e perfil sem mods.\nVocê escolherá jogo, OpenMW, perfil e destino. Os originais serão preservados.')
            game=choose('1/4 — Pasta do Morrowind (contém Data Files)')
            engine=choose('2/4 — Pasta do OpenMW (contém resources e openmw.exe)')
            profile=choose('3/4 — Perfil OpenMW (contém openmw.cfg)')
            parent=choose('4/4 — Onde guardar a tradução? Escolha uma pasta gravável fora do jogo')
            dest=parent/('Morrowind-PTBR-'+load(ROOT/'compatibilidade/manifesto.json')['version'])
            if not messagebox.askokcancel('Confirmar instalação',f'Pacote: {dest}\nPerfil: {profile}\n\nSerá criado um backup da configuração. Continuar?'):return
            bundle=build(game,engine,dest)
            activate(bundle,profile)
            messagebox.showinfo('Pronto','Tradução ativada. Abra o OpenMW pelo atalho habitual e inicie um jogo novo.\nNão mova a pasta instalada. Leia as limitações da beta no README.')
    except InterruptedError:
        pass
    except Exception as exc:
        messagebox.showerror('Não foi possível concluir',str(exc))
        raise
    finally:
        app.destroy()

def main():
    parser=argparse.ArgumentParser(description='Instalador offline da tradução Morrowind PT-BR para OpenMW')
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('validate')
    p=sub.add_parser('build');p.add_argument('--game',required=True);p.add_argument('--openmw',required=True);p.add_argument('--output',required=True);p.add_argument('--development',action='store_true');p.add_argument('--lrelease')
    p=sub.add_parser('activate');p.add_argument('--bundle',required=True);p.add_argument('--profile',required=True)
    p=sub.add_parser('deactivate');p.add_argument('--profile',required=True)
    p=sub.add_parser('context');p.add_argument('id');p.add_argument('--game',required=True)
    p=sub.add_parser('gui');p.add_argument('--remove',action='store_true')
    args=parser.parse_args()
    if args.command=='validate':
        _,rows,frozen=catalog();print(f'{len(rows):,} campos válidos; versão intacta: {frozen}')
    elif args.command=='build':build(args.game,args.openmw,args.output,args.development,args.lrelease)
    elif args.command=='activate':activate(args.bundle,args.profile)
    elif args.command=='deactivate':deactivate(args.profile)
    elif args.command=='context':context(args.id,args.game)
    elif args.command=='gui':gui(args.remove)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('ERRO: '+str(exc),file=sys.stderr)
        sys.exit(1)
