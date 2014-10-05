class CclException(Exception):
    pass

class SyntaxError(CclException):
    def __init__(self, token, message):
        self.token = token
        self.message = message
    
    def __str__(self):
        return '%s\n%s' % (self.message, self.token.location)

class LexError(SyntaxError):
    pass

class UnrecognizedToken(LexError):
    def __init__(self, token):
        super(UnrecognizedToken, self).__init__(
            token,
            'Unrecognized token %r' % (token.value,))

class ParseError(SyntaxError):
    pass

class UnexpectedToken(ParseError):
    def __init__(self, token, expected):
        super(UnexpectedToken, self).__init__(
            token,
            'Expected token of type %r but got token %r' %
                (expected, token))

class ExpectedAtom(ParseError):
    def __init__(self, token):
        super(ExpectedAtom, self).__init__(
            token,
            "Expected an <atom> but <atom>s"
            "can't start with tokens of type %r" % (token.type,))

class RuntimeException(CclException):
    def __init__(self, message):
        self.message = message
        self.callstack = []
    
    def __str__(self):
        s = self.message + '\n'
        for element in self.callstack:
            s += str(element.token.location) + '\n'
        return s

class AttributeError(RuntimeException):
    def __init__(self, value, attribute):
        super(AttributeError, self).__init__(
            '%r does not have attribute %r' % (value, attribute))

class KeyError(RuntimeException):
    def __init__(self, key):
        super(KeyError, self).__init__('No such key %r' % (key,))
