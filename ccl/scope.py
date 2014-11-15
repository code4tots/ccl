class Scope(object):
    def __init__(self, global_table=GLOBAL_TABLE):
        self.tables = [global_table]
    
    def __getitem__(self, key):
        table = self.tables[-1]
        while key not in table and '__parent__' in table:
            table = table['__parent__']
        return table[key]
    
    def __setitem__(self, key, value):
        self.tables[-1][key] = value
    
    # TODO: For now Scope will only support dynamic scoping.
    # However, in the future, push and pop may accept parent arguments
    # so that we may support static typing.
    
    def push(self):
        self.tables.append(dict())
    
    def pop(self):
        self.tables.pop()
