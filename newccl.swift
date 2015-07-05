import Foundation

class Thing : NSObject, NSCopying, SequenceType, Printable {
    var x : NSObject?
    init(_ x: NSObject?) {
        self.x = x
        if let y = x as? Thing {
            assert(false, "Cannot pass a Thing (\(y)) as argument to Thing.init")
        }
    }
    override var hash : Int { if let y = x { return y.hash }; return 0 }
    func copyWithZone(zone: NSZone) -> AnyObject { return Thing(self.x) }
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
        }
        assert(false, "Iteration not supported for \(self.x.dynamicType)")
    }
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
    override func isEqual(y: AnyObject?) -> Bool {
        if x == nil && y == nil { return true }
        if x == nil || y == nil { return false }
        if let z = y as? Thing { return x!.isEqual(z.x) }
        return false
    }
    var size : Int {
        if let y = x as? NSMutableArray { return y.count }
        else if let y = x as? NSMutableDictionary { return y.count }
        assert(false, "size attr not supported for \(self.x.dynamicType)")
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
                assert(false, "Thing \(self.dynamicType) is not subscriptable (key \(key) val \(v))")
            }
        }
    }
    func push(t: Thing) {
        if let a = x as? NSMutableArray {
            a.addObject(t)
        } else {
            assert(false, "push is not supported for \(self.dynamicType) (\(t))")
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
            let ret = self[T(0)]
            a.removeObjectAtIndex(0)
            return ret
        } else {
            assert(false, "pop is only supported for List types")
        }
    }
}
func ==(lhs: Thing, rhs: Thing) -> Bool { return lhs.isEqual(rhs) }
func T(x : Int) -> Thing { return Thing(NSNumber(integer: x)) }
func T(x : Double) -> Thing { return Thing(NSNumber(double: x)) }
func T(x : String) -> Thing { return Thing(x as NSString) }
func T(x : NSMutableArray) -> Thing { return Thing(x) }
func T(x : NSMutableDictionary) -> Thing { return Thing(x) }
let NIL = Thing(nil)
// pre-Swift 2.0, we didn't have 'do' blocks.
func locally(@noescape work: () -> ()) { work() }
func test() {
    locally {
        assert(T(5) == T(5))
        assert(T([T(1), T(2), T(3)]).size == 3, toString(T([T(1), T(2), T(3)]).size))
        let x = T(5)
        assert("\(x)" == "Num(5)", "\(x)")
        locally {
            let x = T([])
            x.push(T("hello"))
            assert(x == T([T("hello")]), x.description)
        }
    }
    println("All core tests pass!")
}
test()
