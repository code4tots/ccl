//
//  bytecode.swift
//  ccl
//
//  Created by Kyumin Kim on 7/7/15.
//  Copyright (c) 2015 Kyumin Kim. All rights reserved.
//

import Foundation

class Opcode : DictionaryLiteralConvertible, Printable {
    var type : NSString
    var value : NSObject
    var i : Int { return (value as! NSNumber).integerValue }
    var d : Double { return (value as! NSNumber).doubleValue }
    var s : NSString { return value as! NSString }
    init(type : NSString, value : NSObject) { self.type = type; self.value = value }
    convenience required init(dictionaryLiteral elements: (NSString, NSObject)...) {
        var type : NSString = "", value : NSObject = 0
        for (k, v) in elements {
            if k == "type" {
                type = v as! NSString
            } else if k == "value" {
                value = v
            } else {
                assert(false, toString((k,v)))
            }
        }
        self.init(type: type, value: value)
    }
    var description : String { return "\(type)(\(value))" }
}

