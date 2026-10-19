"""Check the public inventory and package a release without game/AI files."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import zipfile
from mwbr import ROOT, catalog, require

DIRECTORIES={'traducoes','conteudo','interface','compatibilidade','scripts','tests','docs','LICENSES','.github'}
FILES={'README.md','CONTRIBUTING.md','LICENSE','THIRD_PARTY_NOTICES.md','CHANGELOG.md','.gitignore','.gitattributes','INSTALAR.bat','DESINSTALAR.bat'}
FORBIDDEN={'.esm','.esp','.bsa','.exe','.dll','.sqlite','.sqlite3','.db','.log','.pyc'}

def inventory():
    result=[]
    for path in sorted(ROOT.rglob('*')):
        relative=path.relative_to(ROOT)
        if not path.is_file() or '.git' in relative.parts or '__pycache__' in relative.parts or relative.parts[0] in ('dist','build'):
            continue
        require(relative.parts[0] in DIRECTORIES or relative.as_posix() in FILES, 'Arquivo fora da lista pública: '+str(relative))
        require(path.suffix.lower() not in FORBIDDEN, 'Arquivo privado/comercial proibido: '+str(relative))
        if path.suffix.lower() in {'.md','.json','.jsonl','.py','.yml','.yaml','.ts','.layout','.bat','.txt'}:
            text=path.read_text(encoding='utf-8-sig')
            require(not re.search(r'sk-(?:or-v1-)?[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{24,}',text), 'Possível credencial: '+str(relative))
            require(not re.search(r'C:[/\\]+Users[/\\]+[^/\\\s"<>]+',text,re.I), 'Caminho pessoal: '+str(relative))
        result.append(path)
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args()
    manifest,rows,frozen=catalog()
    files=inventory()
    if args.check_only:
        print(f'Inventário público: {len(files)} arquivos; sem masters, executáveis, bancos ou credenciais reconhecidas.')
        return
    require(frozen,'Catálogos editados; um mantenedor precisa validar e fechar os hashes da nova versão antes de empacotar')
    dest=ROOT/'dist';dest.mkdir(exist_ok=True)
    archive=dest/f"morrowind-ptbr-openmw-{manifest['version']}.zip"
    folder=archive.stem
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for path in files:
            info=zipfile.ZipInfo(folder+'/'+path.relative_to(ROOT).as_posix(),date_time=(2026,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644 << 16
            z.writestr(info,path.read_bytes())
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None,'ZIP corrompido')
    checksum=hashlib.sha256(archive.read_bytes()).hexdigest()
    (dest/'SHA256SUMS.txt').write_text(checksum+'  '+archive.name+'\n',encoding='ascii')
    print(f'{archive.name}: {archive.stat().st_size/1048576:.2f} MiB; SHA256 {checksum}')

if __name__=='__main__':main()
