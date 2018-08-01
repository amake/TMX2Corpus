# -*- coding: utf-8; -*-

import unittest
import logging
import tmx2corpus
from tokenizer import PyJaTokenizer
from tmx2corpus import BufferOutput

logging.basicConfig(level=logging.DEBUG)


class TestTMX2Corpus(unittest.TestCase):

    def test_file(self):
        output = BufferOutput()
        tmx2corpus.convert('test.tmx', tokenizers=[
                           PyJaTokenizer()], output=output)
        self.assertDictEqual({'ja': ['こんにちは、世界！'],
                              'en': ['Hello, world!'],
                              'tok.ja': ['こん にち は 、 世界 ！'],
                              'tok.en': ['Hello ,  world !']},
                             output.buckets)


if __name__ == '__main__':
    unittest.main(verbosity=2)
