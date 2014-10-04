from ccl.context.main import register, SpecialForm
from PySide import QtCore, QtGui

register('QtGui')(QtGui)
register('QtCore')(QtCore)
