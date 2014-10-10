"""Values directly imported from python with little change
"""
from __future__ import print_function

from importlib import import_module

from ccl.scope import global_scope

global_scope.update({
    'None'  : None,
    'True'  : True,
    'False' : False,
    
    'list'  : list,
    'tuple' : tuple,
    'dict'  : dict,
    'set'   : set,
    
    'print'       : print,
    'len'         : len,
    
    'abs'         : abs,
    'all'         : all,
    'any'         : any,
    'bool'        : bool,
    'callable'    : callable,
    'chr'         : chr,
    'classmethod' : classmethod,
    
    'python-import' : import_module
    })