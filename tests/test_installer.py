import contextlib
import io
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import mwbr

def make_record(tag, fields, flags=7):
    body=b''.join(mwbr.SH.pack(name,len(data))+data for name,data in fields)
    return mwbr.RH.pack(tag,len(body),19,flags)+body

class PatchTests(unittest.TestCase):
    def setUp(self):
        self.source=make_record(b'BOOK',[(b'NAME',b'book_id\0'),(b'FNAM',b'Old title\0'),(b'BKDT',b'\x01\x00\x05\xff')])
        self.entry={'id':'test:0:1','record':0,'subrecord':1,'type':'BOOK','field':'FNAM','text':'Título maior','source_sha256':mwbr.sha(b'Old title\0'),'trailing_nuls':1}

    def test_preserve_headers_identity_and_nontext(self):
        result=mwbr.patch_master(self.source,[self.entry])
        record=list(mwbr.records(result))[0]
        self.assertEqual(record[:3],(b'BOOK',19,7))
        self.assertEqual(record[3],[(b'NAME',b'book_id\0'),(b'FNAM','Título maior\0'.encode('cp1252')),(b'BKDT',b'\x01\x00\x05\xff')])

    def test_wrong_source_rejected(self):
        with self.assertRaisesRegex(ValueError,'Fonte divergente'):
            mwbr.patch_master(self.source.replace(b'Old title',b'New title'),[self.entry])

    def test_truncation_rejected(self):
        with self.assertRaises(ValueError):list(mwbr.records(self.source[:-1]))

    def test_invalid_encoding_rejected(self):
        self.entry['text']='Texto 🎮'
        with self.assertRaises(UnicodeEncodeError):mwbr.payload(self.entry)

    def test_duplicate_patch_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicado'):mwbr.patch_master(self.source,[self.entry,self.entry])

    def test_script_guards_preserve_branches_and_ids(self):
        before='Choice "Aceitar" 1 "Recusar" 2\nAddTopic "Assunto"\n'
        translated='Choice "Sim" 1 "Não" 2\nAddTopic "Assunto"\n'
        self.assertEqual(mwbr.script_shape(before),mwbr.script_shape(translated))
        self.assertNotEqual(mwbr.script_shape(before),mwbr.script_shape(translated.replace(' 2',' 3')))
        self.assertNotEqual(mwbr.script_shape(before),mwbr.script_shape(translated.replace('Assunto','Outro')))

    def test_percent_prose_not_placeholder(self):
        e={'text':'100% de sucesso e %PCName','field':'NAME','type':'INFO'}
        self.assertEqual(mwbr.text_guards(e)['tokens'],['%PCName'])

class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        base=Path(self.temp.name);self.profile=base/'perfil';self.profile.mkdir()
        self.bundle=base/'pacote';self.bundle.mkdir()
        (self.bundle/'mwbr-build.json').write_text('{}')
        mwbr.save(self.bundle/'fallbacks.json',{'Question_1_Question':'Pergunta traduzida'})
        self.cfg=b'data="D:/Original"\r\nresources="D:/OpenMW/resources"\r\ncontent=Morrowind.esm\r\ncontent=Tribunal.esm\r\ncontent=Bloodmoon.esm\r\nfallback=Question_1_Question,Original\r\n'
        self.settings=b'[Video]\nresolution x = 1920\n[General]\npreferred locales = en\n[GUI]\nsubtitles = false\n'
        (self.profile/'openmw.cfg').write_bytes(self.cfg);(self.profile/'settings.cfg').write_bytes(self.settings)

    def test_activate_reapply_restore_exact(self):
        mwbr.activate(self.bundle,self.profile)
        first=(self.profile/'openmw.cfg').read_bytes()
        mwbr.activate(self.bundle,self.profile)
        self.assertEqual((self.profile/'openmw.cfg').read_bytes(),first)
        self.assertIn(b'resolution x = 1920',(self.profile/'settings.cfg').read_bytes())
        mwbr.deactivate(self.profile)
        self.assertEqual((self.profile/'openmw.cfg').read_bytes(),self.cfg)
        self.assertEqual((self.profile/'settings.cfg').read_bytes(),self.settings)

    def test_restore_refuses_changed_profile(self):
        mwbr.activate(self.bundle,self.profile)
        changed=(self.profile/'settings.cfg').read_bytes()+b'\n# user change\n'
        (self.profile/'settings.cfg').write_bytes(changed)
        with self.assertRaisesRegex(ValueError,'Configuração mudou'):mwbr.deactivate(self.profile)
        self.assertEqual((self.profile/'settings.cfg').read_bytes(),changed)

    def test_partial_activation_recoverable(self):
        mwbr.activate(self.bundle,self.profile)
        (self.profile/'settings.cfg').write_bytes(self.settings)
        mwbr.deactivate(self.profile)
        self.assertEqual((self.profile/'openmw.cfg').read_bytes(),self.cfg)

    def test_modded_profile_not_silently_changed(self):
        cfg=self.cfg+b'content=OtherMod.esp\n'
        (self.profile/'openmw.cfg').write_bytes(cfg)
        with self.assertRaisesRegex(ValueError,'perfil limpo'):mwbr.activate(self.bundle,self.profile)
        self.assertEqual((self.profile/'openmw.cfg').read_bytes(),cfg)

if __name__=='__main__':unittest.main()
