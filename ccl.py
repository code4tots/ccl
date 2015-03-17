class context(object):
  def __init__(self, p):
    self.p = p
    self.d = dict()

  def __getitem__(self, k):
    return self.d[k] if k in self.d else self.p[k]

class number_display(str):
  def eval(self, ctx):
    return float(self)

class parser(object):
  def __init__(self, s):
    self.s = s
    self.j = self.i = 0
    self.ss = [[]]

  @property
  def c(self):
    return self.s[self.i] if self.i < len(self.s) else ''

  def skip_spaces(self):
    while self.c.isspace():
      self.i += 1

  def cut(self, w):
    return self.ss[-1].append(w(self.s[self.j:self.i]))

  def parse_number(self):
    self.skip_spaces()
    if self.c.isdigit() or self.c in ('-', '.'):
      self.j = self.i
      self.i += 1
      while self.c.isdigit() or self.c == '.':
        self.i += 1
      self.cut(number_display)
      return True

p = parser('8')
p.parse_number()

print p.ss[-1].pop().eval(dict())
