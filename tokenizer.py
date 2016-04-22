'''
Created on Dec 19, 2013

@author: aaron.madlon-kay
'''

import sys
import os
import re

import tinysegmenter

BOUNDARY_REGEX = re.compile(r'\b|\Z')


class Tokenizer(object):
    def __init__(self, lang):
        self.lang = lang
    def tokenize(self, text):
        '''Override this to return tokenized text.'''
        return text


class PyJaTokenizer(Tokenizer):
    def __init__(self):
        super(PyJaTokenizer, self).__init__('ja')
        
    def tokenize(self, text):
        tokenizer = tinysegmenter.TinySegmenter()
        tokens = tokenizer.tokenize(text)
        if '<' in text:
            tokens = glom_tags(tokens)
        if '://' in text or '@' in text:
            tokens = glom_urls(tokens)
        return ' '.join(tokens)


class PyEnTokenizer(Tokenizer):
    def __init__(self):
        super(PyEnTokenizer, self).__init__('en')

    def tokenize(self, text):
        tokens = []
        i = 0
        for m in BOUNDARY_REGEX.finditer(text):
            tokens.append(text[i:m.start()])
            i = m.end()
        return ' '.join([tok for tok in tokens if not tok.strip() == ''])

    
DEFAULT_TOKENIZER = PyEnTokenizer()


def glom_tags(tokens):
    result = []
    in_tag = False
    tag = None
    #print 'Before:', str(tokens)
    tokens.reverse()
    while len(tokens):
        tok = tokens.pop()
        if in_tag:
            if tok == '>':
                result.append(tag + tok)
                in_tag = False
            elif tok.startswith('>'):
                result.append(tag + '>')
                in_tag = False
                tokens.append(tok[1:])
            elif tok.startswith('/>'):
                result.append(tag + '/>')
                in_tag = False
                tokens.append(tok[2:])
            else:
                tag += tok
        else:
            if tok in ('<', '</'):
                tag = tok
                in_tag = True
            elif tok.endswith('<'):
                tag = '<'
                in_tag = True
                result.append(tok[:-1])
            elif tok.endswith('</'):
                tag = '</'
                in_tag = True
                result.append(tok[:-2])
            else:
                result.append(tok)
    #print 'After:', str(result)
    return glom_multitags(result)


def is_tag(token):
    return len(token) > 2 and token[0] == '<' and token[-1] == '>'


def glom_multitags(tokens):
    result = []
    #print 'Before:', str(tokens)
    tokens.reverse()
    while len(tokens):
        tok = tokens.pop()
        if is_tag(tok) and len(tokens):
            next_tok = tokens.pop()
            if is_tag(next_tok):
                tokens.append(tok + next_tok)
            else:
                result.append(tok)
                result.append(next_tok)
        else:
            result.append(tok)
    #print 'After:', str(result)
    return result


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
