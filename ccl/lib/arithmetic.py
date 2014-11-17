from ccl.core import run
import math

def init(scope):
    
    @scope.register
    def __add(stack, scope):
        stack.append(stack.pop() + stack.pop())

    @scope.register
    def __subtract(stack, scope):
        stack.append(stack.pop() - stack.pop())
    
    @scope.register
    def __multiply(stack, scope):
        stack.append(stack.pop() * stack.pop())
    
    @scope.register
    def __divide(stack, scope):
        stack.append(stack.pop() / stack.pop())
    
    @scope.register
    def __divide(stack, scope):
        stack.append(stack.pop() / stack.pop())
    
    @scope.register
    def __floor_divide(stack, scope):
        stack.append(stack.pop() // stack.pop())
    
    @scope.register
    def __exponentiate(stack, scope):
        stack.append(stack.pop() ** stack.pop())
    
    @scope.register
    def __square_root(stack, scope):
        stack.append(math.sqrt(stack.pop()))
    
    @scope.register
    def __less_than(stack, scope):
        stack.append(stack.pop() < stack.pop())
    
    @scope.register
    def __xor(stack, scope):
        stack.append(stack.pop() ^ stack.pop())
    
    run("""
$__add =+
$__subtract =-
$__multiply =*
$__divide =/
$__floor_divide =//
$__exponentiate =**
$__square_root =sqrt
$__less_than =lt
$__xor =^
""", [], scope)
