from ccl.core import run, Scope

run("""
:ccl.lib.language python-import

:hello_world! p

""", [], Scope())
