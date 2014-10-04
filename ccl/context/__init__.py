"""Context is essentially the environment in which
the program is run.

'main.py' contains some foundations.

All other modules in this package adds entries to
the 'global_context'
"""
from ccl.context.main import (
    global_context,
    new_context,
    SpecialForm)

import ccl.context.language
import ccl.context.gui
