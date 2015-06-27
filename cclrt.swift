//: Playground - noun: a place where people can play

import UIKit

var str = "Hello, playground"

class Context {
    let table : NSMutableDictionary = NSMutableDictionary()
    let parent : Context?
    
    init(_ parent: Context?) {
        self.parent = parent
        
        if parent == nil {
            table["__stack__"] = NSMutableArray()
            
            table["print"] = Verb { (ctx) in
                print(ctx.pop())
            }
            
            table["println"] = Verb { (ctx) in
                println(ctx.pop())
            }
            
            table["true"] = true
            table["false"] = false
            
            table["if"] = Verb { (ctx) in
                ctx.stack
                let rhs = ctx.pop() as! Verb
                let lhs = ctx.pop() as! Verb
                let cond = ctx.pop() as! Verb
                
                var choice = lhs
                
                cond.x(ctx)
                
                let v: AnyObject = ctx.pop()
                
                if let b = v as? Bool {
                    choice = b ? lhs : rhs
                } else if let i = v as? Int {
                    choice = i != 0 ? lhs : rhs
                } else if let f = v as? Float {
                    choice = f != 0 ? lhs : rhs
                } else if let s = v as? String {
                    choice = s != "" ? lhs : rhs
                } else {
                    // Assume all other values are true for now
                    choice = lhs
                }
                choice.x(ctx)
            }
        }
    }
    
    subscript(key: String) -> AnyObject? {
        get {
            if let v: AnyObject = table[key] {
                return v
            } else if let p = parent {
                return p[key]
            }
            return nil
        }
        set(value) {
            if let v: AnyObject = table[key] {
                table[key] = value
            } else if let p = parent {
                p[key] = value
            }
            table[key] = value
        }
    }
    
    func push(x: AnyObject) {
        stack.addObject(x)
    }
    
    func pop() -> AnyObject {
        let ret: AnyObject = stack.lastObject!
        stack.removeLastObject()
        return ret
    }
    
    var stack : NSMutableArray {
        return (self["__stack__"] as! NSMutableArray)
    }
}

class Verb {
    let x : (Context) -> Void
    init(x : (Context) -> Void) { self.x = x }
    var description : String {
        return "xx\(x)"
    }
}

func pushvalue(ctx: Context, value: AnyObject) {
    ctx.push(value)
}

func summonid(ctx: Context, name: String) {
    if let val: AnyObject = ctx[name] {
        if let verb = val as? Verb {
            verb.x(ctx)
        } else {
            ctx.push(val)
        }
    } else {
        println("No identifier '" + name + "'\n")
        exit(1)
    }
}

func popandrun(ctx: Context) {
    let cmd = (ctx["__stack__"] as! NSMutableArray).lastObject as! Verb
    (ctx["__stack__"] as! NSMutableArray).removeLastObject()
    cmd.x(ctx)
}

var ctx = Context(nil)
