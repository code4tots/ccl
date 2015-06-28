import Foundation

class Parser {
	let whitespaces = Set(" \n\t")

	let chs : [Character]
	var a : Int = 0 // token start position
	var b : Int = 0 // token end position
	var tv : String = "" // token value
	var tt : String = "" // token type

	init(_ str: String) {
		chs = Array(str)
	}

	func fin() -> Bool {
		return b >= chs.count
	}

	func ch() -> Character {
		return chs[b]
	}

	func skip_spaces() {
		while !fin() && whitespaces.contains(ch()) {
			b++
		}
	}

	func starts_with(xs: [String]) -> Bool {
		return xs.reduce(false) { (t: Bool, x: String) in
			return t || self.starts_with(x)
		}
	}

	func starts_with(x: String) -> Bool {
		return starts_with(Array(x))
	}

	func starts_with(x: [Character]) -> Bool {
		return Array(chs[b..<(b+x.count)]) == x
	}

	func next_token() {
		skip_spaces()
		a = b
		if fin() {
			tt = "eof"
		} else if Set("()").contains(ch()) {
			tt = String(ch())
			b++
		} else if starts_with(["r\"", "r'", "'", "\""]) {
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
					if fin() {
						assert(false, "expected string escape but found EOF")
					}
					if ch() == "\\" {
						tv += "\\"
					} else if ch() == "n" {
						tv += "\n"
					} else {
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
			while !fin() && !whitespaces.contains(ch()) && !Set("()\"'").contains(ch()) {
				b++
			}
			assert(b > a, "invalid char: " + String(ch()))
			tt = "id"
			tv = String(chs[a..<b])
		}
	}

	func parse() -> Ast {
		var stack : [[Ast]] = [[]]
		skip_spaces()
		var start_stack = [b]
		next_token()
		while tt != "eof" {
			if tt == "(" {
				stack.append([])
				start_stack.append(a)
			} else if tt == ")" {
				let start = start_stack.removeLast()
				stack[stack.count-2].append(Block(start, b, stack.removeLast()))
			} else {
				var ast : Ast = Ast(0, 0)
				switch tt {
				case "id":
					if let d = NSNumberFormatter().numberFromString(tv)?.doubleValue {
						ast = NumAst(a, b, d)
					} else {
						ast = Id(a, b, tv)
					}
				case "str":
					ast = StrAst(a, b, tv)
				default:
					assert(false, "invalid token type: " + tt)
				}
				stack[stack.count - 1].append(ast)
			}
			next_token()
		}
		assert(stack.count == 1, toString(stack))
		return Block(start_stack.removeLast(), b, stack[0])
	}
}

func parse(s: String) -> Ast {
	return Parser(s).parse()
}

class Ast : Printable, Equatable {
	var a : Int // ast start position
	var b : Int // ast end position

	init(_ a: Int, _ b: Int) {
		self.a = a
		self.b = b
	}

	convenience init() {
		self.init(0, 0)
	}

	var description: String {
		return "ast"
	}

	func eq(rhs: Ast) -> Bool {
		assert(false, "Not implemented")
		return false
	}

	func exec(c: Context) {
		assert(false, "Not implemented")
	}
}

func ==(lhs: Ast, rhs: Ast) -> Bool {
	return lhs.eq(rhs)
}

class Block : Ast {
	var xs : [Ast]

	init(_ a: Int, _ b: Int, _ xs: [Ast]) {
		self.xs = xs
		super.init(a, b)
	}

	convenience init(_ xs: [Ast]) {
		self.init(0, 0, xs)
	}

	override var description: String {
		return toString(xs)
	}

	override func eq(rhs: Ast) -> Bool {
		if let r = rhs as? Block {
			return xs == r.xs
		}
		return false
	}
}

class NumAst : Ast {
	var x : Double

	init(_ a: Int, _ b: Int, _ x: Double) {
		self.x = x
		super.init(a, b)
	}

	convenience init(_ x: Double) {
		self.init(0, 0, x)
	}

	override var description: String {
		return toString(x)
	}

	override func eq(rhs: Ast) -> Bool {
		if let r = rhs as? NumAst {
			return x == r.x
		}
		return false
	}
}

class StrAst : Ast {
	var x : String

	init(_ a: Int, _ b: Int, _ x: String) {
		self.x = x
		super.init(a, b)
	}

	convenience init(_ x: String) {
		self.init(0, 0, x)
	}

	override var description: String {
		return toString(x)
	}

	override func eq(rhs: Ast) -> Bool {
		if let r = rhs as? StrAst {
			return x == r.x
		}
		return false
	}
}

class Id : Ast {
	var x : String = ""

	init(_ a: Int, _ b: Int, _ x: String) {
		self.x = x
		super.init(a, b)
	}

	convenience init(_ x: String) {
		self.init(0, 0, x)
	}

	override var description: String {
		return toString(x)
	}

	override func eq(rhs: Ast) -> Bool {
		if let r = rhs as? Id {
			return x == r.x
		}
		return false
	}
}

class Context {
	var table : [String: Any] = ["__stack__": [] as [Any]]
	var root : Context {
		return self
	}

	var stack : [Any] {
		get {
			return root["__stack__"] as! [Any]
		}
		set(v) {
			root["__stack__"] = v
		}
	}

	subscript(i: String) -> Any? {
		get {
			return table[i]
		}
		set(v) {
			table[i] =  v
		}
	}
}

class ChildContext : Context {
	let parent : Context

	override var root : Context {
		get {
			return parent.root
		}
	}

	init(_ parent: Context) {
		self.parent = parent
		super.init()
	}

	override subscript(i: String) -> Any? {
		get {
			return (table[i] != nil) ? table[i] : parent[i]
		}
		set(v) {
			if table[i] != nil {
				table[i] = v
			} else if parent[i] != nil {
				parent[i] = v
			} else {
				table[i] = v
			}
		}
	}
}

class Thing : Hashable, Printable, Equatable {
	var hashValue : Int {
		return 0
	}
	var description : String {
		return "thing"
	}
	func eq(rhs: Thing) -> Bool {
		assert(false, "not implemented")
		return false
	}
}

func ==(lhs: Thing, rhs: Thing) -> Bool {
	return lhs.eq(rhs)
}

// error: classes derived from generic classes must also be generic
// So Ugh. A lot of boilerplate to follow.

class Num : Thing {
	var x : Double
	init(_ xx: Double) { x = xx }
	override func eq(rhs: Thing) -> Bool {
		if let r = rhs as? Num {
			return x == r.x
		}
		return false
	}
}

class Str : Thing {
	var x : String
	init(_ xx: String) { x = xx }
	override func eq(rhs: Thing) -> Bool {
		if let r = rhs as? Str {
			return x == r.x
		}
		return false
	}
}

class List : Thing {
	var x : [Thing]
	init(_ xx: [Thing]) { x = xx }
	override func eq(rhs: Thing) -> Bool {
		if let r = rhs as? List {
			return x == r.x
		}
		return false
	}
}

class Dict : Thing {
	var x : [Thing:Thing]
	init(_ xx: [Thing:Thing]) { x = xx }
	override func eq(rhs: Thing) -> Bool {
		if let r = rhs as? Dict {
			return x == r.x
		}
		return false
	}
}

// poor man's tests
var p = Parser("abc\n'hi' 78")
assert(p.starts_with("a"))
assert(!p.starts_with("b"))
assert(p.starts_with(["a", "b"]))
assert(p.starts_with(["b", "a"]))
p.next_token()
assert(p.tt == "id")
assert(p.tv == "abc", p.tv)
p.next_token()
assert(p.tt == "str")
assert(p.tv == "hi", p.tv)
p.next_token()
assert(p.tt == "id")
assert(p.tv == "78", p.tv)
let r = parse("a ( b c 'hi' r'\\n' ) 44")
assert(r == Block([
	Id("a"),
	Block([
		Id("b"),
		Id("c"),
		StrAst("hi"),
		StrAst("\\n"),
	]),
	NumAst(44),
	]), "xxx")
var rc = Context()
var cc = ChildContext(rc)

