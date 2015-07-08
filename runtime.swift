/*
The only possible objects should be:
  1. NSNumber
  2. NSString
  3. NSMutableArray
  4. NSMutableDictionary
  5. Lambda (custom class)
  6. Builtin (custom class)
*/
import Foundation

class Context {
    var programCounter: Int
    var opcodes: [Opcode]
    var scope: NSMutableDictionary
    var valueStack: [NSObject] = []
    var valueStackStack: [[NSObject]] = []
    var callStack: [(Int, NSMutableDictionary)] = []
    init(opcodes: [Opcode], programCounter: Int, scope: NSMutableDictionary) {
        self.opcodes = opcodes
        self.programCounter = programCounter
        self.scope = scope
    }
    var fin : Bool {
        return programCounter >= opcodes.count
    }
    var ready : Bool {
        return !fin
    }
}

class Lambda: Thing {
    var programCounter: Int
    var scope: NSMutableDictionary
    init(programCounter: Int, scope: NSMutableDictionary) {
        self.programCounter = programCounter
        self.scope = scope
    }
}

class Builtin: NSObject {
    func exec(runtime: Runtime) {}
}

class BuiltinFunction: Builtin {
    var f: (Runtime) -> Void
    init(f: (Runtime) -> Void) {
        self.f = f
    }
    override func exec(runtime: Runtime) {
        self.f(runtime)
    }
}

class Runtime {
    var contextIndex : Int = 0
    var contexts : [Context] = []
    var context : Context {
        return contexts[contextIndex]
    }
    var errorMessage: String? = nil
    func step() {
        let opcode = context.opcodes[context.programCounter]
        switch opcode.type {
        case "str":
            context.valueStack.append(opcode.value as! NSString)
        case "(":
            context.valueStack.append(Lambda(programCounter: context.programCounter+1, scope: context.scope))
        case ")":
            if let pair = context.callStack.last {
                (context.programCounter, context.scope) = pair
            } else {
                context.programCounter = context.opcodes.count
            }
        case "num":
            context.valueStack.append(opcode.value as! NSNumber)
        case "assign":
            let key = opcode.value as! NSString
            if let value = context.valueStack.last {
                context.valueStack.removeLast()
                assign(context.scope, key, value)
            } else {
                errorMessage = "In trying to assign \(key), found empty stack"
                return;
            }
        case "push":
            context.valueStack.append(lookup2(self, context.scope, opcode.value as! NSString))
        case "attr":
            let attr = opcode.value as! NSString
            if let me = context.valueStack.last {
                context.valueStack.removeLast()
                me.getattr(self, attr: attr)
            } else {
                errorMessage = "In trying to call attribute \(attr), found empty stack"
                return;
            }
        case "id":
            let v = lookup2(self, context.scope, opcode.value as! NSString)
            if let builtin = v as? Builtin {
                builtin.exec(self)
            } else if let lambda = v as? Lambda {
                let pair = (context.programCounter, context.scope)
                context.callStack.append(pair)
                context.programCounter = lambda.programCounter-1 // because we increment after switch.
                context.scope = newChildScope(lambda.scope)
            } else {
                context.valueStack.append(v)
            }
        default:
            errorMessage = "Unexpected opcode type \(opcode.type)"
            return;
        }
        context.programCounter++
    }
    func run() {
        var doneForNow = false
        while !doneForNow {
            doneForNow = true
            for contextIndex = 0; contextIndex < contexts.count; contextIndex++ {
                if context.ready {
                    doneForNow = false
                }
                while context.ready {
                    step()
                    if let message = errorMessage {
                        // TODO: better error message (e.g. stack trace).
                        assert(false, message)
                    }
                }
            }
            var newContexts : [Context] = []
            for context in contexts {
                if !context.fin {
                    newContexts.append(context)
                }
            }
            contexts = newContexts
        }
    }
}
