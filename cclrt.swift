//: Playground - noun: a place where people can play

import UIKit

var str = "Hello, playground"

class Context {
    let table : NSMutableDictionary = NSMutableDictionary()
    let parent : Context?
    
    init(_ parent: Context?) {
        self.parent = parent
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

class Block {
    let x : (Context) -> Void
    init(x : (Context) -> Void) { self.x = x }
    var description : String {
        return "xx\(x)"
    }
}

class Verb : Block {}

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
    let cmd = (ctx["__stack__"] as! NSMutableArray).lastObject as! Block
    (ctx["__stack__"] as! NSMutableArray).removeLastObject()
    cmd.x(ctx)
}

var ctx = Context(nil)
ctx.table["__stack__"] = NSMutableArray()

ctx.table["print"] = Verb { (ctx) in
    println(ctx.pop())
}

ctx.table["false"] = false
ctx.table["true"] = true

ctx.table["if"] = Verb { (ctx) in
    ctx.stack
    let rhs = ctx.pop() as! Block
    let lhs = ctx.pop() as! Block
    let cond = ctx.pop() as! Block
    
    var choice = lhs
    
    cond.x(ctx)
    
    if let b = ctx.pop() as? Bool {
        if b {
            choice = lhs
        } else {
            choice = rhs
        }
    } else {
        // Assume all other values are true for now
        choice = lhs
    }
    choice.x(ctx)
}
