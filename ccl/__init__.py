from ccl.scope import global_scope, new_scope
from ccl.parser import parse
from ccl.controller import run, repl, run_file

# ccl.controller already loads ccl.lib
# However, all code in ccl.lib is python
# ccl.libccl is all essentially ccl
import ccl.libccl
