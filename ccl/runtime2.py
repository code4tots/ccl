import re

class Display(object):
    pass

class LiteralDisplay(Display):
    def __init__(self, location, value_string):
        self.location = location
        self.value = eval(value_string)

action_regex_pairs = (
    (LiteralDisplay, re.compile(
        r'\"(?:\\\"|[^"])*\"|'
        r"\'(?:\\\'|[^'])*\'|"
        r'\d+\.\d*|'
        r'\d+')),
    (NameDisplay, re.compile(r'[a-zA-Z0-9_\-]+')),
    ((lambda location, value : value),
        re.compile('|'.join(re.escape(s) for s in '[](){}.'))),
    ((lambda location, value : '\n'),
        re.compile(r'\n\s*'))
    ((lambda location, value : None),
        re.compile(r'\s+')))

def lex(string, file_name=''):
    s = string
    i = 0
    p = action_regex_pairs
    while i < len(s):
        for action, regex in p:
            m = regex.match(s,i)
            if m is not None:
                result = action(location, m.group())
                if result is not None:
                    yield result
                i = m.end()
                break
        else:
            raise Exception()

