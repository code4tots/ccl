import re
space_re = re.compile(r'[ \t]*')
symbols = ('(',')','{','}', '[', ']', '.', ';', '\n')

res = [(t,re.compile(r)) for t, r in
    [(s,re.escape(s)) for s in symbols] +
    [ ('STRING',
        r'\"(?:\\\"|[^"])*\"' '|'
        r"\'(?:\\\'|[^'])*\'"),
    ('FLOAT', r'\-?\d*\.\d*'), ('INT', r'\-?\d+'), ('NAME', r'\w+')]]

class Token(object):
    def __init__(self, type_, value, string, position):
        self.type = type_
        self.value = value
        self.string = string
        self.position = position
    
    def __repr__(self):
        return '(%r,%r)' % (self.type, self.value)

def lex(s):
    c = space_re
    i = c.match(s).end()
    r = res
    while i < len(s):
        for t, e in r:
            m = e.match(s,i)
            if m is not None:
                yield Token(t, m.group(), s, i)
                i = m.end()
                break
        else:
            m = re.compile(r'\S*').match(s, i)
            raise SyntaxError('invalid token %r' %
                (m.group(),))
        i = c.match(s,i).end()
    yield Token('END', None, s, len(s))
