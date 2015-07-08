/*
Only objects in CCL are NSMutableString and NSMutableArray;
*/
import Foundation

func FOOBAR() {
	assert(false)
}

class Thing : NSObject {
	var a : [Thing] = []
	var s : String = ""
	var i : Int { return (s as NSString).integerValue }
	var d : Double { return (s as NSString).doubleValue }
	var size : Int { return max(a.count, count(s)) }
	var isString : Bool { return a.count == 0 }
	var isArray : Bool { return !isString }
	func extend(x: Thing) {
		if isString { s += x.s }
		else { a += x.a }
	}

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
    func parse() -> NSMutableArray {
        var ret = NSMutableArray()
        var i : Int = 0
        var stack : [Int] = []
        next_token()
        while tt != "eof" {
        	var d = NSMutableArray(array:[
        		NSMutableArray(array: [NSMutableString(string: "type"), NSMutableString(string: tt)]),
        		NSMutableArray(array: [NSMutableString(string: "value"), NSMutableString(string: tv)]),
        		NSMutableArray(array: [NSMutableString(string: "string start index"), NSMutableString(string: toString(a))]),
        		NSMutableArray(array: [NSMutableString(string: "string end index"), NSMutableString(string: toString(b))]),
        		])
            switch tt {
            case "(": stack.append(i)
            case ")":
                let j = stack.removeLast()
                d.addObject(NSMutableArray(array:[
                	NSMutableString(string: "matching parenthesis index"),
                	NSMutableString(string: toString(j))
                	]))
                ret[j].addObject(NSMutableArray(array:[
                	NSMutableString(string: "matching parenthesis index"),
                	NSMutableString(string: toString(i))
                	]))
            case "id": break
            case "attr": break
            case "assign": break
            case "str": break
            case "lookup": break
            default: assert(false, "Unexpected token type \(tt)")
            }
            ret.addObject(d)
            i++
            next_token()
        }
        return ret
    }
}

func parse(s: String) -> NSMutableArray {
	return Parser(s).parse()
}

/* utils */

class Runtime {
}

println(parse("1 2 3") == parse("1 2 3"))
