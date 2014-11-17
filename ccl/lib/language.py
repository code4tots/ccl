from ccl.core import run, summon

def init(scope):
    
    @scope.register
    def __push_scope(stack, scope):
        scope.push()

    @scope.register
    def __pop_scope(stack, scope):
        scope.pop()
    
    @scope.register
    def __duplicate_stack(stack, scope):
        stack.extend(stack[-stack.pop():])
    
    @scope.register
    def __print(stack, scope):
        print(stack.pop())
    
    @scope.register
    def __true(stack, scope):
        stack.append(True)
    
    @scope.register
    def __false(stack, scope):
        stack.append(False)
    
    @scope.register
    def __test(stack, scope):
        test = stack.pop()
        if scope['__debug']:
            summon(test, stack, scope)
    
    @scope.register
    def __assert(stack, scope):
        assert stack.pop()
    
    @scope.register
    def __equal(stack, scope):
        stack.append(stack.pop() == stack.pop())
    
    run("""
$__push_scope =(
$__pop_scope =)
$__duplicate_stack =dup
$__print =p
$__true =true
$__false =false
true =True
false =False
$__test =test
$__assert =assert
$__equal =eq

true =__debug

[ (
    [ make sure that 'true' is True ] =
    true assert
    
    [ make sure that False is equal to False ] =
    false false eq assert
    
    [ make sure dup works as intended ] =
    5 6 2 dup
        6 eq assert
        5 eq assert
        6 eq assert
        5 eq assert
    
) ] test
""", [], scope)
