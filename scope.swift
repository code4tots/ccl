//
//  scope.swift
//  ccl
//
//  Created by Kyumin Kim on 7/7/15.
//  Copyright (c) 2015 Kyumin Kim. All rights reserved.
//

import Foundation

func lookup(scope: NSMutableDictionary, key: NSString) -> NSObject? {
    if let value = scope[key] as? NSObject {
        return value
    } else if let parent = scope["__parent__"] as? NSMutableDictionary {
        return lookup(parent, key)
    }
    return nil
}

func lookup2(runtime: Runtime, scope: NSMutableDictionary, key: NSString) -> NSObject {
    let val = lookup(scope, key)
    if let v = val {
        return v
    } else {
        runtime.errorMessage = "Name \(key) not in scope"
        return ""
    }
}

func assign(scope: NSMutableDictionary, key: NSString, value: NSObject) {
    if scope[key] != nil {
        scope[key] = value
        return;
    } else if let parent = scope["__parent__"] as? NSMutableDictionary {
        if lookup(parent, key) != nil {
            assign(parent, key, value)
            return;
        }
    }
    scope[key] = value
    return;
}

func newRootScope() -> NSMutableDictionary {
    return [
        "p": BuiltinFunction { (runtime: Runtime) in
            let value = runtime.context.valueStack.last
            runtime.context.valueStack.removeLast()
            if let v = value {
                println(v)
            } else {
                println("nil")
            }
        },
        "[": BuiltinFunction { (runtime:Runtime) in
            let context = runtime.context
            context.valueStackStack.append(context.valueStack)
            context.valueStack = []
        },
        "]": BuiltinFunction { (runtime:Runtime) in
            let context = runtime.context
            if var newValueStack = context.valueStackStack.last {
                newValueStack.append(NSMutableArray(array: context.valueStack))
                context.valueStack = newValueStack
            } else {
                runtime.errorMessage = "When trying to process ']', found empty stack"
            }
        },
    ]
}

func newChildScope(parentScope: NSMutableDictionary) -> NSMutableDictionary {
    return ["__parent__": parentScope]
}
