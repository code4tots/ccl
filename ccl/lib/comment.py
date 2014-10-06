from ccl.scope import register
from ccl.ast import SpecialForm

@register('#')
@SpecialForm
def comment(scope, args, ast):
    pass
