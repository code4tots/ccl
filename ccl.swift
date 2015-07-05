/*
At least as of Swift 1.2, swift errors messages are not as good as they could be.

Stack traces of assertion failures only show the line number of the assertion,
and not the rest of the stack.

If there is a nil unwrapping error, it doesn't any line numbers.

As a consequence, I have all of these boilerplate assertions to help with debugging.

-----

Testing frameworks need to fight access controls, need time to be set up etc.

Especially with a budding language like Swift it might not be so smooth.

So just using assertions at end as a makeshift testing setup.
*/
import Foundation

class Thing : NSObject,
        NSCopying,
        SequenceType,
        NilLiteralConvertible,
        BooleanLiteralConvertible,
        IntegerLiteralConvertible,
        FloatLiteralConvertible,
        StringLiteralConvertible,
        ArrayLiteralConvertible,
        DictionaryLiteralConvertible {
    /*
    Wrap around existing NSObject.
    Should be one of:
        nil
        NSNumber (double)
        NSString
        NSMutableArray
        NSMutableDictionary
    Subclasses may use different values here if they want to.
    */
    var x : NSObject?
    var n : NSNumber { get { if let y = x as? NSNumber { return y } else { assert(false, "\(x) is not a number")}} set(v) { x = v } }
    var s : NSString { get { if let y = x as? NSString { return y } else { assert(false, "\(x) is not a string")}} set(v) { x = v } }
    var a : NSMutableArray { get { if let y = x as? NSMutableArray { return y } else { assert(false, "\(x) is not a list")}} set(v) { x = v } }
    var d : NSMutableDictionary { get { if let y = x as? NSMutableDictionary { return y } else { assert(false, "\(x) is not a dict")}} set(v) { x = v } }

    init(fromAnyObject x: NSObject?) { // DANGER DANGER! If you use this, you better know what you're doing.
        super.init()
        self.x = x
    }
    init(fromObject x: NSObject?) {
        super.init()
        if x == nil { self.x = nil }
        else if let y = x as? NSNumber { self.x = y }
        else if let y = x as? NSString { self.x = y }
        else if let y = x as? NSMutableArray { self.x = y }
        else if let y = x as? NSMutableDictionary { self.x = y }
        else { assert(false, "\(x.dynamicType) is not supported") }
    }
    convenience init(_ t: Thing) { self.init(fromObject: t.x) }
    convenience required init(booleanLiteral value: BooleanLiteralType) {
        self.init(fromObject: NSNumber(double: Double(value)))
    }
    convenience required init(integerLiteral value: IntegerLiteralType) {
        self.init(fromObject: NSNumber(double: Double(value)))
    }
    convenience required init(floatLiteral value: FloatLiteralType) {
        self.init(fromObject: NSNumber(double: value))
    }
    convenience required init(nilLiteral: ()) {
        self.init(fromObject: nil)
    }
    convenience required init(stringLiteral value: StringLiteralType) {
        self.init(fromObject: NSString(UTF8String: "\(value)"))
    }
    convenience required init(unicodeScalarLiteral value: StringLiteralType) {
        self.init(fromObject: NSString(UTF8String: "\(value)"))
    }
    convenience required init(extendedGraphemeClusterLiteral value: StringLiteralType) {
        self.init(fromObject: NSString(UTF8String: "\(value)"))
    }
    convenience required init(arrayLiteral elements: Thing...) {
        var array = NSMutableArray()
        for element in elements {
            array.addObject(element)
        }
        self.init(fromObject: array)
    }
    convenience required init(dictionaryLiteral elements: (Thing, Thing)...) {
        var dict = NSMutableDictionary()
        for (key, value) in elements {
            dict.setObject(value, forKey: key)
        }
        self.init(fromObject: dict)
    }
    func copyWithZone(zone: NSZone) -> AnyObject {
        return Thing(self)
    }
    func generate() -> GeneratorOf<Thing> {
        if let a = x as? NSMutableArray {
            var gen = a.generate()
            var next = gen.next() as? Thing
            return GeneratorOf<Thing> {
                let ret = next
                if next != nil { next = gen.next() as? Thing }
                return ret
            }
        } else if let d = x as? NSMutableDictionary {
            var gen = d.generate()
            var next = gen.next()
            return GeneratorOf<Thing> {
                let ret = next
                if next != nil { next = gen.next() }
                return ret?.0 as? Thing
            }
        } else {
            assert(false, "You can only iterate over List or Dict types, not \(self)")
        }
    }
    func contains(key: Thing) -> Bool {
        if let d = x as? NSMutableDictionary {
            return d[key] != nil
        } else {
            assert(false, "contains only supported for dictionaries")
        }
    }
    subscript(key: Thing) -> Thing {
        get {
            if let a = x as? NSMutableArray {
                if let k = key.x as? NSNumber {
                    return a[Int(k.doubleValue)] as! Thing
                } else {
                    assert(false, "Key \(key) not supported for List")
                }
            } else if let d = x as? NSMutableDictionary {
                if let v = d[key] as? Thing {
                    return v
                } else {
                    assert(false, "\(d[key]) is not a Thing (key \(key))")
                }
            } else {
                assert(false, "Thing \(self) is not subscriptable (key \(key))")
            }
        }
        set(v) {
            if let a = x as? NSMutableArray {
                if let k = key.x as? NSNumber {
                    a[Int(k.doubleValue)] = v
                } else {
                    assert(false, "Key \(key) not supported for List (val \(v)")
                }
            } else if let d = x as? NSMutableDictionary {
                d[key] = v
            } else {
                assert(false, "Thing \(self) is not subscriptable (key \(key) val \(v))")
            }
        }
    }
    func push(t: Thing) {
        if let a = x as? NSMutableArray {
            a.addObject(t)
        } else {
            assert(false, "push is only supported for List types (\(t))")
        }
    }
    func pop() -> Thing {
        if let a = x as? NSMutableArray {
            let ret = a.lastObject as! Thing
            a.removeLastObject()
            return ret
        } else {
            assert(false, "pop is only supported for List types")
        }
    }
    func pushleft(t: Thing) { // linear time insertion. fix later.
        if let a = x as? NSMutableArray {
            a.insertObject(t, atIndex: 0)
        } else {
            assert(false, "push is only supported for List types (\(t))")
        }
    }
    func popleft() -> Thing { // linear time insertion. fix later.
        if let a = x as? NSMutableArray {
            let ret = self[0]
            a.removeObjectAtIndex(0)
            return ret
        } else {
            assert(false, "pop is only supported for List types")
        }
    }
    var size : Int {
        if let a = x as? NSMutableArray {
            return a.count
        } else if let d = x as? NSMutableDictionary {
            return d.count
        } else {
            assert(false, "Thing \(self) does not support attribute size")
        }
    }
    override var hash : Int { return x == nil ? 0 : x!.hash }
    override var description : String {
        if x == nil {
            return "nil"
        } else if let y = x as? NSNumber {
            return "Num(\(y))"
        } else if let y = x as? NSString {
            return "Str(\(y))"
        } else if let y = x as? NSMutableArray {
            var s = "List("
            for i in y {
                s += "\(i.description)"
            }
            s += ")"
            return s
        } else if let y = x as? NSMutableDictionary {
            var s = "Dict("
            for (k, v) in y {
                s += "\(k.description):\(v.description)"
            }
            s += ")"
            return s
        } else {
            return "<!!! \(x.dynamicType) has not overriden description>"
        }
    }
    var str : String {
        if x == nil {
            return "nil"
        } else if let y = x as? NSNumber {
            return "\(y)"
        } else if let y = x as? NSString {
            return "\(y)"
        } else if let y = x as? NSMutableArray {
            var s = "List("
            for i in y {
                s += "\(i.str)"
            }
            s += ")"
            return s
        } else if let y = x as? NSMutableDictionary {
            var s = "Dict("
            for (k, v) in y {
                s += "\(k.str):\(v.str)"
            }
            s += ")"
            return s
        } else {
            return "<!!! \(x.dynamicType) has not overriden str>"
        }
    }
    override func isEqual(y: AnyObject?) -> Bool {
        if x == nil && y == nil { return true }
        if x == nil || y == nil { return false }
        if let z = y as? Thing { return x!.isEqual(z.x) }
        return false
    }
    func getattr(attr: String) -> Thing {
        switch attr {
        case "eq": return NF { (c: Runtime) in c.push(Thing(booleanLiteral: self == c.pop())) }
        case "p": return NF { (c: Runtime) in println(self) }
        case "print": return NF { (c: Runtime) in print(self.str)}
        case "size": return Thing(integerLiteral: size)
        default:
            if let n = x as? NSNumber {
                switch attr {
                case "+":
                    return NF { (c: Runtime) in
                        c.push(Thing(floatLiteral: Double(n) + Double(c.pop().n)))
                    }
                default: break
                }
            } else if let a = x as? NSMutableArray {
                switch attr {
                case "+":
                    return NF { (c: Runtime) in
                        var ret : Thing = []
                        for item in self { ret.push(item) }
                        for item in c.pop() { ret.push(item) }
                        c.push(ret)
                    }
                default: break
                }
            } else if let d = x as? NSMutableDictionary {
                switch attr {
                case "+":
                    return NF { (c: Runtime) in
                        var ret : Thing = [:]
                        for key in self { ret[key] = self[key] }
                        var rhs = c.pop()
                        for key in rhs { ret[key] = rhs[key] }
                        c.push(ret)
                    }
                default: break
                }
            }
        }
        assert(false, "\(self) does not have attribute \(attr)")
        return 0
    }
}
func ==(lhs: Thing, rhs: Thing) -> Bool { return lhs.isEqual(rhs) }
func T(t: Thing) -> Thing { return t } // convenient for literal convertibles.
func T(x : Int) -> Thing { return Thing(fromObject: NSNumber(integer: x)) }
func T(x : Double) -> Thing { return Thing(fromObject: NSNumber(double: x)) }
func T(x : String) -> Thing { return Thing(fromObject: x as NSString) }
func T(x : NSMutableArray) -> Thing { return Thing(fromObject: x) }
func T(x : NSMutableDictionary) -> Thing { return Thing(fromObject: x) }
let NIL = Thing(nil)
class Verb : Thing {} // Verb is a marker class.
class Native : Verb { // Subclass this to your specific usecase.
    func exec(c: Runtime) {}
}
class NativeFunc : Native {
    var f : (Runtime) -> Void = {(c:Runtime) in}
    override func isEqual(y: AnyObject?) -> Bool { return y != nil && ObjectIdentifier(self) == ObjectIdentifier(y!) }
    override func exec(c: Runtime) { f(c) }
}
func NF(f: (Runtime) -> Void) -> NativeFunc {
    var nf = NativeFunc(0)
    nf.f = f
    return nf
}
class Block : Verb {
    var native : Scope = nil
    override var description : String {
        return "<Block at position \(n)>"
    }
    override func isEqual(y: AnyObject?) -> Bool {
        if let b = y as? Block {
            return x!.isEqual(b.x)
        }
        return false
    }
}
func B(i: Int, c: Scope) -> Block {
    var b = Block(integerLiteral: i)
    b.native = c
    return b
}
class Parser {
    let whitespaces = Set(" \n\t")
    let chs : [Character]
    var a : Int = 0 // token start position
    var b : Int = 0 // token end position
    var tv : String = "" // token value
    var tt : String = "" // token type
    init(_ str: String) {chs = Array(str)}
    func fin() -> Bool {return b >= chs.count}
    func ch() -> Character {return chs[b]}
    func skip_spaces() {while !fin() && whitespaces.contains(ch()) {b++}}
    func skip_empty() {
        while !fin() && (ch() == "#" || whitespaces.contains(ch())) {
            if ch() == "#" {
                while !fin() && ch() != "\n" {
                    b++
                }
            } else {
                skip_spaces()
            }
        }
    }
    func starts_with(xs: [String]) -> Bool {
        return xs.reduce(false) { (t: Bool, x: String) in
            return t || self.starts_with(x)
        }
    }
    func starts_with(x: String) -> Bool {return starts_with(Array(x))}
    func starts_with(x: [Character]) -> Bool {return Array(chs[b..<min(chs.count, b+x.count)]) == x}
    func next_token() {
        skip_empty()
        a = b
        if fin() {
            tt = "eof"
            tv = tt
        } else if Set("()").contains(ch()) { // '(' and ')' are special operators
            tt = String(ch())
            tv = tt
            b++
        } else if starts_with(["r\"", "r'", "'", "\""]) { // quotes
            tt = "str"
            var raw = false
            if ch() == "r" {
                raw = true
                b++
            }
            var quote = String(ch())
            if starts_with(["\"\"\"", "'''"]) {
                quote = String(chs[b...b+3])
            }
            b += Array(quote).count
            tv = ""
            while !starts_with(quote) {
                if fin() {
                    assert(false, "found EOF before end of quote")
                }
                if !raw && ch() == "\\" {
                    b++
                    if fin() { assert(false, "expected string escape but found EOF") }
                    switch ch() {
                    case "\\": tv += "\\"
                    case "n": tv += "\n"
                    default:
                        assert(false, "invalid string escape: \\" + String(ch()))
                    }
                    b++
                } else {
                    tv.append(ch())
                    b++
                }
            }
            b += Array(quote).count
        } else {
            var c = a
            tt = "id"
            if Set(".=,").contains(ch()) {
                switch ch() {
                case ".": tt = "attr"
                case "=": tt = "assign"
                case ",": tt = "lookup"
                default: assert(false, "logic error")
                }
                c++
                b++
            }
            while !fin() && !whitespaces.contains(ch()) && !Set("()\"'").contains(ch()) {
                b++
            }
            assert(b > c, "invalid char: " + String(ch()))
            tv = String(chs[c..<b])
        }
    }
    func parse() -> Thing {
        var ret : Thing = []
        var i : Int = 0
        var stack : [Int] = []
        next_token()
        while tt != "eof" {
            var d : Thing = [
                "type": Thing(stringLiteral: tt),
                "index": Thing(integerLiteral: i),
                "value": Thing(stringLiteral: tv),
                "string start index": Thing(integerLiteral: a),
                "string end index": Thing(integerLiteral: b),
            ]
            switch tt {
            case "(": stack.append(i)
            case ")":
                let j = Thing(integerLiteral: stack.removeLast())
                d["matching parenthesis index"] = j
                ret[j]["matching parenthesis index"] = Thing(integerLiteral: i)
            case "id":
                if let n = NSNumberFormatter().numberFromString(tv)?.doubleValue {
                    d["type"] = "num"
                    d["value"] = Thing(floatLiteral: n)
                }
            case "attr": break
            case "assign": break
            case "str": break
            case "lookup": break
            default: assert(false, "Unexpected token type \(tt)")
            }
            ret.push(d)
            i++
            next_token()
        }
        return ret
    }
}
func parse(s: String) -> Thing { return Parser(s).parse() }
// Scope is just a Dictionary with a few extra convenience methods.
class Scope : Thing {
    var root : Scope {
        if let p = parent {
            return p.root
        } else {
            return self
        }
    }
    var parent : Scope? {
        if contains("__parent__") {
            if let p = self["__parent__"] as? Scope { return p }
            let p = self["__parent__"]
            assert(false, "__parent__ is not a Scope: \(p)")
        }
        return nil
    }
    var cp : Thing { // context pointer
        get { return root["__cp__"] }
        set(v) { root["__cp__"] = v }
    }
    var contexts : Thing { // queue of contexts
        get { return root["__contexts__"] }
        set(v) { root["__contexts__"] = v }
    }
    var context : Thing {
    	get { return contexts[cp] }
        set(v) { contexts[cp] = v }
    }
    var stack : Thing {
        get { return context["__stack__"] }
        set(v) { context["__stack__"] = v }
    }
    var stackstack : Thing {
        get { return context["__stackstack__"] }
        set(v) { context["__stackstack__"] = v }
    }
    var callstack : Thing {
        get { return context["__callstack__"] }
        set(v) { context["__callstack__"] = v }
    }
    var pc : Thing { // program counter
        get { return context["__pc__"] }
        set(v) { context["__pc__"] = v }
    }
    var bytecode : Thing {
        get { return context["__bytecode__"] }
        set(v) { context["__bytecode__"] = v }
    }
    var code : Thing {
        get { return context["__code__"] }
        set(v) { context["__code__"] = v }
    }
    var defaultBytecode : Thing { // default bytecode for context if not overriden
        get { return root["__bytecode__"] }
        set(v) { root["__bytecode__"] = v }
    }
    var defaultCode : Thing { // default code for context if not overriden
        get { return root["__code__"] }
        set(v) { root["__code__"] = v }
    }
    var foreignscope : Thing? {
        get { return self.lookup2("__foreignscope__") }
        set(v) { self["__foreignscope__"] = v! } // WARNING: cannot assign nil.
    }
    override func push(t: Thing) {
        stack.a.addObject(t)
    }
    override func pop() -> Thing {
        return stack.pop()
    }
    func lookup2(key: Thing) -> Thing? {
        if self.contains(key) {
            return self[key]
        } else if let p = parent {
            return p.lookup2(key)
        } else {
            return nil
        }
    }
    func lookup(key: Thing) -> Thing {
        if self.contains(key) {
            return self[key]
        } else if let p = parent {
            return p.lookup(key)
        } else {
            assert(false, "\(key) is not in scope")
        }
    }
    func assign(key: Thing, _ value: Thing) {
        if self.contains(key) {
            self[key] = value
        } else if let p = parent {
            p.assign(key, value)
        } else {
            self[key] = value
            // assert(false, "\(key) is not in scope")
        }
    }
    func addContext(b: Block) {
        addContext(b, withCustomCode: defaultCode.s as String, withCustomBytcode: defaultBytecode)
    }
    func addContext(b: Block, withCustomCode code: String) {
        addContext(b, withCustomCode: code, withCustomBytcode: parse(code))
    }
    func addContext(b: Block, withCustomCode code: String, withCustomBytcode bytecode: Thing) {
        self.contexts.push([
            "__stack__" : [], // stack for calculations
            "__stackstack__" : [], // stack of __stack__; used for creating lists.
            "__callstack__" : [], // call stack keeps track of where to return after calls.
            "__code__": Thing(stringLiteral: code), // raw code string (for error messages)
            "__bytecode__": bytecode, // parsed code (surprise, it's flat!)
            "__pc__": Thing(fromObject: b.n), // program counter
        ])
    }
}
func RootScope(code: String) -> Scope {
    var scope : Scope = [

        "__cp__": 0, // context pointer
        "__contexts__": [], // list of contexts

        // You can use custom code/bytecode, but by default, when creating a new context,
        // we pick up this code/bytecode.
        "__code__": Thing(stringLiteral: code), // raw code string (for error messages)
        "__bytecode__": parse(code), // parsed code (surprise, it's flat!)

        // Builtins library

        "pop" : NF { (c: Runtime) in c.pop() },

        // list builder
        "[" : NF { (c: Runtime) in
            c.root.stackstack.push(c.stack)
            c.stack = []
        },
        "]" : NF { (c: Runtime) in
            let stack = c.stack
            c.stack = c.root.stackstack.pop()
            c.stack.push(stack)
        },

        // dict from list
        "dict" : NF { (c: Runtime) in
            var d : Thing = [:]
            var key : Thing? = nil
            for item in c.pop() {
                if let k = key {
                    d[k] = item
                    key = nil
                } else {
                    key = item
                }
            }
            c.push(d)
        }
    ]
    scope.addContext(0)
    return scope
}
func ChildScope(parent: Scope) -> Scope {
    return ["__parent__": parent]
}
// Runtime is what we use to run things.
class Runtime {
    var scope : Scope
    var root : Scope { return scope.root }
    var stack : Thing {
        get { return scope.stack }
        set(s) { scope.stack = s }
    }
    init(_ scope : Scope) { self.scope = scope }
    func push(t: Thing) { scope.push(t) }
    func pop() -> Thing { return scope.pop() }
    func summon(value: Thing) {
        if let verb = value as? Verb {
            if let block = verb as? Block {
                // Save to callstack
                root.callstack.push([
                    "return index": Thing(integerLiteral: Int(root.pc.n) + 1),
                    "return scope": scope,
                ])
                var newscope = ChildScope(block.native)
                newscope.foreignscope = scope
                scope = newscope
                root.pc = Thing(integerLiteral: Int(block.n) + 1) // move to the start of the block.
            } else if let native = verb as? Native {
                // Execute native swift code.
                native.exec(self)
                // WARNING: to native funcs that modify program counter: once your function finishes,
                // counter will be incremented by 1.
                root.pc = Thing(integerLiteral: Int(root.pc.n) + 1)
            }
        } else {
            push(value)
            root.pc = Thing(integerLiteral: Int(root.pc.n) + 1)
        }
    }
    func step() {
        var instruction = root.bytecode[root.pc] // fetch
        // println(instruction) // debugging
        switch instruction["type"] {
        case "str", "num":
            push(instruction["value"])
            root.pc = Thing(integerLiteral: Int(root.pc.n) + 1)
        case "assign":
            scope.assign(instruction["value"], pop())
            root.pc = Thing(integerLiteral: Int(root.pc.n) + 1)
        case "lookup":
            push(scope.lookup(instruction["value"]))
            root.pc = Thing(integerLiteral: Int(root.pc.n) + 1)
        case "id":
            summon(scope.lookup(instruction["value"]))
        case "attr":
            summon(pop().getattr(instruction["value"].s as String))
        case "(":
            push(B(Int(root.pc.n), scope))
            root.pc = Thing(integerLiteral: Int(instruction["matching parenthesis index"].n) + 1)
        case ")": // We hit end of a block. Return to caller.
            if root.callstack.size == 0 { // If there is nothing left on the callstack, we are finished.
                root.pc = Thing(integerLiteral: root.bytecode.size)
            } else { // Otherwise, we need to return to whoever called us.
                var message = root.callstack.pop()
                root.pc = message["return index"]
                scope = message["return scope"] as! Scope
            }
        default:
            let type = instruction["type"]
            assert(false, "Instruction type \(type) not supported")
        }
    }
    func done() -> Bool {
        return Int(root.pc.n) >= root.bytecode.size
    }
    func ready() -> Bool { // can this context be stepped over right now?
        // TODO: Take into account the stuff we are waiting for.
        return !done()
    }
    func run() { // execute contexts until they can no longer run.
        var i = 0, fin = false
        while !fin {
            fin = true
            for i = 0; i < root.contexts.size; i++ {
                root.cp = Thing(integerLiteral: i) // iterate over each context.
                if ready() {
                    fin = false
                    while ready() { step() }
                }
            }
        }
    }
}
func RuntimeFromCode(code: String) -> Runtime { return Runtime(RootScope(code)) }
func locally(@noescape work: () -> ()) { // pre-Swift 2.0, we didn't have 'do' blocks.
    work()
}
func test() {
    locally { // literal convertibles tests
        let a : Thing = "hi"
        let b : Thing = ["1", 2, []]
        let c : Thing = true
        let d : Thing = [1: 2, "3": 4]
        let e : Thing = Thing(stringLiteral: "x \(a)")
        assert(b.popleft() == "1")
        assert(b.popleft() == 2)
    }
    locally { // Scope tests
        let r = RootScope("")
        let c = ChildScope(r)
        assert(c.root === r, c.root.description)
        assert(r.stack == [], r.stack.description)
        assert(c.stack == r.stack, c.stack.description)
        r.push(1)
        assert(r.stack == [1], r.stack.description)
        assert(r.pop() == 1)
    }
    locally { // Parser tests
        assert(map(parse("( 1 ) a .b ,c =d")) { $0["type"] } ==
               ["(", "num", ")", "id", "attr", "lookup", "assign"])
        assert(map(parse("( 1 ) a .b ,c =d")) { $0["value"] } ==
               ["(", 1, ")", "a", "b", "c", "d"])
    }
    locally { // Execution tests
        locally {
            let c = RuntimeFromCode("1 'a' ( )")
            c.run()
            assert(c.stack == [1, "a", Block(2)], c.stack.description)
        }
        locally {
            let c = RuntimeFromCode("5 =x ,x ,x ,x")
            c.run()
            assert(c.stack == [5, 5, 5], c.stack.description)
        }
        locally {
            let c = RuntimeFromCode("( ) =x x")
            c.run()
            assert(c.stack == [], c.stack.description)
        }
        locally {
            let c = RuntimeFromCode("( ) =x ,x")
            c.run()
            assert(c.stack == [Block(0)], c.stack.description)
        }
        locally {
            let c = RuntimeFromCode("( ) =x ,x")
            c.run()
            assert(c.stack == [Block(0)], c.stack.description)
        }
        locally {
            let c = RuntimeFromCode("[ 1 2 3 ]")
            c.run()
            assert(c.stack == [ [1, 2, 3] ], c.stack.description)
        }
        locally {
            let c = RuntimeFromCode("[ 1 2 3 ] .size")
            c.run()
            assert(c.stack == [ 3 ], c.stack.description)
        }
        locally {
            let c = RuntimeFromCode("[ 1 2 3 4 ] dict")
            c.run()
            assert(c.stack == [ [1 : 2, 3 : 4] ], c.stack.description)
        }
        locally {
            let c = RuntimeFromCode("[ 1 2 3 4 ] dict .size")
            c.run()
            assert(c.stack == [ 2 ], c.stack.description)
        }
        locally {
            let c = RuntimeFromCode("[ 1 2 ] [ 3 4 ] .+ ")
            c.run()
            assert(c.stack == [ [3, 4, 1, 2] ], c.stack.description)
        }
        locally {
            let c = RuntimeFromCode("[ 1 2 ] dict [ 3 4 ] dict .+ ")
            c.run()
            assert(c.stack == [ [1:2, 3:4] ], c.stack.description)
        }
        locally { // multiple contexts test
            let c = RuntimeFromCode("55 =x ( x ) =y")
            c.run()
            // assert(c.root.contexts == [], c.root.contexts.description)
            // assert(c.stack == [ 55 ], c.stack.description)
        }
    }
    println("All core tests pass")
}
