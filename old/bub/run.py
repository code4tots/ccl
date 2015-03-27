from . import context
from . import value
from . import parser


def Run(string, ctx=None):
  ctx = ctx or value.Context(context.GLOBAL)
  disp = parser.Parse(string)
  return disp.Eval(ctx, False)
