from ccl.core import run, Scope

run("""
:ccl.lib.language python-import
:ccl.lib.arithmetic python-import

:hello_world! p

55 sqrt p

""", [], Scope())
