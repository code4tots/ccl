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
            "Expected an <atom> but <atom>s "
            "can't start with tokens of type %r" % (token.type,))

class RuntimeException(CclException):
    def __init__(self, ast, message):
        self.message = message
        self.callstack = []
        if ast is not None:
            self.callstack.append(ast)
    
    def __str__(self):
        s = self.message + '\n'
        for element in self.callstack:
            s += str(element.token.location) + '\n'
        return s

class AttributeError(RuntimeException):
    def __init__(self, ast, value, attribute):
        super(AttributeError, self).__init__(
            ast,
            '%r does not have attribute %r' % (value, attribute))

class KeyError(RuntimeException):
    def __init__(self, ast, key):
        super(KeyError, self).__init__(ast, 'No such key %r' % (key,))

class WrongNumberOfArguments(RuntimeException):
    def __init__(self, ast, expected, got):
        super(WrongNumberOfArguments, self).__init__(
            ast,
            "Expected %s arguments but got %s" % (expected, got))

class NotCallable(RuntimeException):
    def __init__(self, ast, f):
        super(NotCallable, self).__init__(
            ast,
            "%r is not callable" % (f,))
