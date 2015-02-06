from .core import Parser
from . import langlib

def translate(string):
	return Parser(string).translate()
