import re

literals = '()[]{}.;$\n'
tokens = tuple((t, re.compile(r)) for t, r in (
    ('String', r'\"(?:\\\"|[^"])*\"' '|' r"\'(?:\\\'|[^'])*\'"),
    ('Float' , r'\-?\d+\.\d*|\-?\.\d+'),
    ('Int'   , r'\-?\d+'),
    ('Name'  , r'[0-9a-zA-Z_\\\-\+\*\/\<\>\=]+')) +
    tuple((s, re.escape(s)) for s in literals))

class Location(object):
    def __init__(self, string, position, line_number, file_name):
        self.string = string
        self.position = position
        self.line_number = line_number
        self.file_name = file_name
    
    @property
    def line_start(self):
        return self.string.rfind('\n', 0, self.position) + 1
    
    @property
    def line_end(self):
        end = self.string.find('\n', self.position + 1)
        if end == -1:
            end = len(self.string)
        return end
    
    @property
    def line(self):
        return self.string[self.line_start:self.line_end]
    
    @property
    def column_number(self):
        return self.position - self.line_start + 1
    
    @property
    def column_indicator(self):
        return ' ' * (self.column_number - 1) + '*'
    
    def __str__(self):
        return 'In file %r on line %s column %s\n%s\n%s\n' % (
            self.file_name,
            self.line_number,
            self.column_number,
            self.line,
            self.column_indicator)

class Token(object):
    def __init__(self, type_, value, location):
        self.type = type_
        self.value = value
        self.location = location
    
    def __repr__(self):
        return '(%r,%r)' % (self.type, self.value)

def lex(string, file_name = ''):
    from ccl.exception import UnrecognizedToken
    s = string    # string to parse (aliased for convenience)
    f = file_name # file name
    i = 0         # current lex position
    p = tokens    # token type regex pairs
    l = 1         # line number
    
    def current_location():
        return Location(s, i, l, f)
    
    while i < len(s) and s[i] in ' \t': i += 1
    while i < len(s):
        for t, r in tokens:
            m = r.match(s, i)
            if m is not None:
                g = m.group()
                yield Token(t, g, current_location())
                i = m.end()
                l += g.count('\n')
                break
        else:
            m = re.compile(r'\S*').match(s, i)
            g = m.group()
            raise UnrecognizedToken(Token(None, g, current_location()))
        while i < len(s) and s[i] in ' \t': i += 1
    yield Token(None, None, current_location())
