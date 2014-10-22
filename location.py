class Location(object):
    def __init__(self, string, path, position):
        self.string = string
        self.path = path
        self.position = position
    
    @property
    def line_begin(self):
        return self.string.rfind('\n', 0, self.position) + 1
    
    @property
    def line_end(self):
        e = self.string.find('\n', self.position, len(self.string))
        return len(self.string) if e == -1 else e
    
    @property
    def line(self):
        return self.string[self.line_begin:self.line_end]
    
    @property
    def line_number(self):
        return 1 + self.string.count('\n', 0, self.position)
    
    @property
    def column_number(self):
        return 1 + self.position - self.line_begin
    
    @property
    def column_star(self):
        return (self.column_number - 1) * ' ' + '*'
    
    def __str__(self):
        return 'In %r on line %s, column %s\n%s\n%s' % (
            self.path,
            self.line_number,
            self.column_number,
            self.line,
            self.column_star)
