from ccl.core import run

def init(scope):
    
    @scope.register
    def __push_scope(stack, scope):
        scope.push()

    @scope.register
    def __pop_scope(stack, scope):
        scope.pop()
    
    @scope.register
    def __print(stack, scope):
        print(stack.pop())
    
    run("""
$__push_scope =(
$__pop_scope =)
$__print =p
""", [], scope)
