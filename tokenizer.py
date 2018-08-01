'''
Created on Dec 19, 2013

@author: aaron.madlon-kay
'''

import sys
import os
import re

import tinysegmenter

BOUNDARY_REGEX = re.compile(r'\b|\Z')
TAG_REGEX = re.compile(r'<[^>]+>')


class Tokenizer(object):
    def __init__(self, lang):
        self.lang = lang

    def tokenize(self, text):
        text = TAG_REGEX.sub('', text)
        tokens = self._tokenize(text)
        if '://' in text or '@' in text:
            tokens = glom_urls(tokens)
        tokens = [tok for tok in tokens if not tok.strip() == '']
        return ' '.join(tokens)

    def _tokenize(self, text):
        '''Override this to implement the actual tokenization: Take string,
return list of tokens.'''
        raise NotImplementedError


class PyJaTokenizer(Tokenizer):
    def __init__(self):
        super(PyJaTokenizer, self).__init__('ja')
        self.ts = tinysegmenter.TinySegmenter()

    def _tokenize(self, text):
        return self.ts.tokenize(text)


class PyEnTokenizer(Tokenizer):
    def __init__(self):
        super(PyEnTokenizer, self).__init__('en')

    def _tokenize(self, text):
        tokens = []
        i = 0
        for m in BOUNDARY_REGEX.finditer(text):
            tokens.append(text[i:m.start()])
            i = m.end()
        return tokens


DEFAULT_TOKENIZER = PyEnTokenizer()


def glom_urls(tokens):
    result = []
    in_url = False
    url = None
    #print 'Before:', str(tokens)
    tokens.reverse()
    while len(tokens):
        tok = tokens.pop()
        if in_url:
            if tok[0] == '<' or tok[0] > u'\u007F':
                result.append(url)
                result.append(tok)
                in_url = False
            else:
                url += tok
                if not len(tokens):
                    result.append(url)
        else:
            if tok in ('://', '@'):
                url = (result.pop() if len(result) else '') + tok
                in_url = True
            else:
                result.append(tok)
    #print 'After:', str(result)
    return result
