from ccl.controller import run
from ccl.scope import global_scope, new_scope

scope = new_scope(global_scope)

run(scope = scope, string = """

= tkinter $ python-import 'tkinter'

""")


global_scope['tkinter'] = scope['tkinter']
