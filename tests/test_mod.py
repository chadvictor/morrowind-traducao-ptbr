"""Synthetic redistribution/merge tests; no commercial fixtures."""
import struct
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_mod as m
import mwbr

def rec(tag, **fields):
    return tag.encode(),0,0,[(k.encode(),v.encode()+b'\0') for k,v in fields.items()]

def dial(name):
    return b'DIAL',0,0,[(b'NAME',name.encode()+b'\0'),(b'DATA',b'\0')]

def info(uid,prev='',nxt='',text='test',deleted=False):
    r=rec('INFO',INAM=uid,PNAM=prev,NNAM=nxt,NAME=text,ONAM='actor_id',BNAM='set quest to 1')
    if deleted:r[3].append((b'DELE',b'\0'*4))
    return r

def stream(*rows):
    return b''.join(m.encode(r) for r in rows)

class ModTests(unittest.TestCase):
    def test_expansion_overrides_last_record_and_omits_unchanged(self):
        base=stream(rec('BOOK',NAME='book',FNAM='Old',TEXT='original'),rec('MISC',NAME='untouched',FNAM='Keep'))
        expansion=stream(rec('BOOK',NAME='book',FNAM='New',TEXT='expansion'))
        localized=stream(rec('BOOK',NAME='book',FNAM='Novo',TEXT='expansao'))
        plugin,stats=m.make_plugin([base,expansion],[base,localized],[('Morrowind.esm',len(base)),('Tribunal.esm',len(expansion))],{b'BOOK',b'MISC'})
        rows=list(mwbr.records(plugin))
        self.assertEqual([r[0] for r in rows],[b'TES3',b'BOOK'])
        self.assertEqual(m.field(rows[1],b'TEXT'),b'expansao\0')
        self.assertEqual(struct.unpack('<I',m.field(rows[0],b'HEDR')[-4:])[0],1)
        self.assertEqual([v for k,v in rows[0][3] if k==b'MAST'],[b'Morrowind.esm\0',b'Tribunal.esm\0'])

    def test_renamed_topic_collision_does_not_merge_unrelated_responses(self):
        original=stream(dial('old'),info('1',text='one'),dial('target'),info('2',text='two'))
        target=stream(dial('target'),info('1',text='um'),dial('other'),info('2',text='dois'))
        plugin,_=m.make_plugin([original],[target],[('Morrowind.esm',len(original))],set())
        effective=m.snapshot([original,plugin],set())[1]
        self.assertEqual(set(effective),{b'target',b'other'})
        self.assertEqual([m.field(r,b'INAM') for r in effective[b'target'][1]],[b'1\0'])

    def test_info_merge_preserves_filters_and_order_after_deletions(self):
        base=stream(dial('topic'),info('1',nxt='2'),info('2',prev='1',nxt='3'),info('3',prev='2'))
        override=stream(dial('topic'),info('2',prev='1',nxt='3',deleted=True),info('4',prev='1',text='added'))
        translated=stream(dial('assunto'),info('2',prev='1',nxt='3',deleted=True),info('4',prev='1',text='novo'))
        target_base=stream(dial('assunto'),info('1',nxt='2'),info('2',prev='1',nxt='3'),info('3',prev='2'))
        plugin,_=m.make_plugin([base,override],[target_base,translated],[('Morrowind.esm',len(base))],set())
        infos=m.snapshot([base,override,plugin],set())[1][b'assunto'][1]
        self.assertEqual([m.field(r,b'INAM') for r in infos],[b'1\0',b'4\0',b'3\0'])
        self.assertTrue(all(m.field(r,b'ONAM')==b'actor_id\0' for r in infos))
        self.assertTrue(all(m.field(r,b'BNAM')==b'set quest to 1\0' for r in infos))

    def test_same_previous_replaces_in_place(self):
        order=m.InfoOrder()
        for r in [info('a'),info('b',prev='a'),info('c',prev='a'),info('b',prev='a',text='changed')]: order.insert(r)
        self.assertEqual(order.order,[b'a',b'c',b'b'])

    def test_changed_previous_moves_response(self):
        order=m.InfoOrder()
        for r in [info('a'),info('b',prev='a'),info('c',prev='b'),info('b',prev='c')]: order.insert(r)
        self.assertEqual(order.order,[b'a',b'c',b'b'])

    def test_regular_identity_change_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'Identidade'):
            m.make_plugin([stream(rec('BOOK',NAME='id',FNAM='Book'))],
                          [stream(rec('BOOK',NAME='translated_id',FNAM='Livro'))],[],{b'BOOK'})

if __name__=='__main__':unittest.main()
