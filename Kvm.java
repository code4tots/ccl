import java.io.InputStream;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

@SuppressWarnings({"serial"})
public class Kvm {

    public static void main(String[] args) {
        new Kvm().run(System.in);
    }

    public Context ctx = buildGlobalContext();
    public Object run(InputStream input) { return eval(parse(input)); }
    public Object run(String code) { return eval(parse(code)); }
    public Object eval(Object ast) { return eval(ctx, ast); }

    //// ------------------------------------------------
    //// ---------- All static below this line ----------
    //// ------------------------------------------------

    /// eval

    public static Object eval(Context ctx, Object astBeforeCast) {
        List ast = (List) astBeforeCast;
        String type = (String) ast.get(0);
        if (type.equals("block")) {
            Object last = BigInteger.ZERO;
            if ((boolean) ast.get(1))
                ctx = new LocalContext(ctx);
            List stmts = (List) ast.get(2);
            for (int i = 0; i < stmts.size(); i++)
                last = eval(ctx, stmts.get(i));
            return last;
        }
        if (type.equals("if"))
            return truthy(eval(ctx, ast.get(1))) ? eval(ctx, ast.get(2)) : eval(ctx, ast.get(3));
        if (type.equals("while")) {
            Object last = BigInteger.ZERO;
            while (truthy(eval(ctx, ast.get(1))))
                last = eval(ctx, ast.get(2));
            return last;
        }
        if (type.equals("str") || type.equals("float") || type.equals("int"))
            return ast.get(1);
        if (type.equals("name"))
            return ctx.get((String) ast.get(1));
        if (type.equals("call")) {
            Func f = (Func) eval(ctx, ast.get(1));
            List argAsts = (List) ast.get(2);
            List args = new List();
            for (int i = 0; i < argAsts.size(); i++)
                args.add(eval(ctx, argAsts.get(i)));
            return f.call(args);
        }
        if (type.equals("decl")) {
            Object value = eval(ctx, ast.get(2));
            ctx.declare((String) ast.get(1), value);
            return value;
        }
        if (type.equals("assign")) {
            Object value = eval(ctx, ast.get(2));
            ctx.set((String) ast.get(1), value);
            return value;
        }
        if (type.equals("lambda"))
            return new Lambda(ctx, (List) ast.get(1), (String) ast.get(2), (List) ast.get(3));
        return null;
    }

    /// eval utils

    public static boolean truthy(Object x) {
        if (x instanceof String) return !x.equals("");
        if (x instanceof Double) return !x.equals(0.0);
        if (x instanceof BigInteger) return !x.equals(BigInteger.ZERO);
        if (x instanceof List) return ((List) x).size() != 0;
        if (x instanceof Dict) return ((Dict) x).size() != 0;
        if (x instanceof Func) return true;
        throw new Error("Unrecognized java type " + x.getClass().toString());
    }

    /// Parse

    public static List parse(InputStream code) { return parse(new Scanner(code)); }
    public static List parse(String code) { return parse(new Scanner(code)); }
    public static List parse(Scanner sc) {
        String type = sc.next();
        if (type.equals("block")) return new List(type, sc.nextInt() != 0, parseList(sc));
        if (type.equals("if")) return new List(type, parse(sc), parse(sc), parse(sc));
        if (type.equals("while")) return new List(type, parse(sc), parse(sc));
        if (type.equals("str")) {
            StringBuilder sb = new StringBuilder();
            int n = sc.nextInt();
            for (int i = 0; i < n; i++)
                sb.append((char) sc.nextInt());
            return new List(type, sb.toString());
        }
        if (type.equals("float")) return new List(type, Double.parseDouble(sc.next()));
        if (type.equals("int")) return new List(type, new BigInteger(sc.next()));
        if (type.equals("name")) return new List(type, sc.next());
        if (type.equals("call")) return new List(type, parse(sc), parseList(sc));
        if (type.equals("decl") || type.equals("assign")) return new List(type, sc.next(), parse(sc));
        if (type.equals("lambda")) return new List(type, parseNames(sc), sc.next(), parse(sc));
        throw new Error("Unknown type '" + type + "'");
    }

    private static List parseList(Scanner sc) {
        List list = new List();
        int n = sc.nextInt();
        for (int i = 0; i < n; i++)
            list.add(parse(sc));
        return list;
    }

    private static List parseNames(Scanner sc) {
        List list = new List();
        int n = sc.nextInt();
        for (int i = 0; i < n; i++)
            list.add(sc.next());
        return list;
    }

    /// Wrappers

    public static class List extends ArrayList<Object> {
        public List(Object... args) {
            for (int i = 0; i < args.length; i++)
                add(args[i]);
        }
    }

    public static class Dict extends HashMap<Object, Object> {
        public Dict(Object... args) {
            for (int i = 0; i < args.length; i += 2)
                put(args[i], args[i+1]);
        }
    }

    abstract public static class Func {
        abstract public Object call(List args);
    }

    public static class Lambda extends Func {
        public Context ctx;
        public List names;
        public String varargsName;
        public List body;
        public Lambda(Context ctx, List names, String varargsName, List body) {
            this.ctx = ctx;
            this.names = names;
            this.varargsName = varargsName;
            this.body = body;
        }
        public Object call(List args) {
            Context ictx = new LocalContext(ctx);
            int i;
            for (i = 0; i < names.size(); i++)
                ictx.declare((String) names.get(i), args.get(i));
            List varargs = new List();
            for (; i < args.size(); i++)
                varargs.add(args.get(i));
            ictx.declare(varargsName, varargs);
            return eval(ictx, body);
        }
        public String toString() {
            return "<lambda " + Integer.toString(hashCode(), 16) + ">";
        }
    }

    abstract public static class Builtin extends Func {
        public String name;
        public Builtin(String name) { this.name = name; }
        public String toString() { return "<Builtin '" + name + "'>"; }
        public void assertArgsLength(List args, int length) {
            if (args.size() != length)
                throw new Error(name + " expects " + Integer.toString(length) + " arguments " +
                                "but found " + Integer.toString(args.size()) + ": " +
                                args.toString());
        }
        public Error typesNotSupported(List args) {
            StringBuilder sb = new StringBuilder();
            sb.append("Applying " + name + " on ");
            for (int i = 0; i < args.size(); i++) {
                sb.append(args.get(i).getClass().toString());
                sb.append(" ");
            }
            sb.append("is not supported");
            return new Error(sb.toString());
        }
    }

    /// Context

    abstract public static class Context {
        protected Map<String, Object> table = new HashMap<String, Object>();

        abstract public Object get(String key);
        abstract public void set(String key, Object val);

        public void declare(String key, Object val) {
            if (table.containsKey(key))
                throw new Error(key + " is already declared in current context");
            table.put(key, val);
        }
    }

    public static class GlobalContext extends Context {
        public Object get(String key) {
            if (!table.containsKey(key))
                throw new Error(key + " not found");
            return table.get(key);
        }

        public void set(String key, Object val) {
            if (!table.containsKey(key))
                throw new Error(key + " not found");
            table.put(key, val);
        }
    }

    public static class LocalContext extends Context {
        private Context parent;

        public LocalContext(Context p) {
            parent = p;
        }

        public Object get(String key) {
            return table.containsKey(key) ? table.get(key) : parent.get(key);
        }

        public void set(String key, Object val) {
            if (table.containsKey(key))  table.put(key, val);
            else                         parent.set(key, val);
        }
    }

    //// ----------------------------------------
    //// ---------- buildGlobalContext ----------
    //// ----------------------------------------

    public static Context buildGlobalContext() {
        Context ctx = new GlobalContext();
        ctx.declare("__list__", new Builtin("__list__") {
            public List call(List args) { return args; }
        });
        ctx.declare("__dict__", new Builtin("__dict__") {
            public Dict call(List args) {
                Dict d = new Dict();
                for (int i = 0; i < args.size(); i += 2)
                    d.put(args.get(i), args.get(i+1));
                return d;
            }
        });
        ctx.declare("__setitem__", new Builtin("__setitem__") {
            public Object call(List args) {
                assertArgsLength(args, 3);
                if (args.get(0) instanceof List) {
                    if (args.get(1) instanceof BigInteger)
                        ((List)args.get(0)).set(((BigInteger)args.get(1)).intValue(), args.get(2));
                    else throw typesNotSupported(args);
                }
                else if (args.get(0) instanceof Dict) ((Dict)args.get(0)).put(args.get(1), args.get(2));
                else throw typesNotSupported(args);
                return args.get(2);
            }
        });
        ctx.declare("__getitem__", new Builtin("__getitem__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof List) {
                    if (args.get(1) instanceof BigInteger)
                        return ((List)args.get(0)).get(((BigInteger)args.get(1)).intValue());
                }
                else if (args.get(0) instanceof Dict) return ((Dict)args.get(0)).get(args.get(1));
                throw typesNotSupported(args);
            }
        });
        ctx.declare("__mul__", new Builtin("__mul__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof String) {
                    if (args.get(1) instanceof BigInteger)
                        return repeatString(args.get(0).toString(), ((BigInteger)args.get(1)).intValue());
                }
                if (args.get(0) instanceof Double) {
                    if (args.get(1) instanceof Double)
                        return ((Double)args.get(0)).doubleValue() * ((Double)args.get(1)).doubleValue();
                    if (args.get(1) instanceof BigInteger)
                        return ((Double)args.get(0)).doubleValue() * ((BigInteger)args.get(1)).doubleValue();
                }
                if (args.get(0) instanceof BigInteger) {
                    if (args.get(1) instanceof String)
                        return repeatString(args.get(1).toString(), ((BigInteger)args.get(0)).intValue());
                    if (args.get(1) instanceof Double)
                        return ((BigInteger)args.get(0)).doubleValue() * ((Double)args.get(1)).doubleValue();
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).multiply((BigInteger)args.get(1));
                    if (args.get(1) instanceof List)
                        return repeatList((List) args.get(1), ((BigInteger)args.get(0)).intValue());
                }
                if (args.get(0) instanceof List) {
                    if (args.get(1) instanceof BigInteger)
                        return repeatList((List) args.get(0), ((BigInteger)args.get(1)).intValue());
                }
                throw typesNotSupported(args);
            }
        });
        Builtin truediv;
        ctx.declare("__truediv__", truediv = new Builtin("__truediv__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof Double) {
                    if (args.get(1) instanceof Double)
                        return ((Double)args.get(0)).doubleValue() / ((Double)args.get(1)).doubleValue();
                    if (args.get(1) instanceof BigInteger)
                        return ((Double)args.get(0)).doubleValue() / ((BigInteger)args.get(1)).doubleValue();
                }
                if (args.get(0) instanceof BigInteger) {
                    if (args.get(1) instanceof Double)
                        return ((BigInteger)args.get(0)).doubleValue() / ((Double)args.get(1)).doubleValue();
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).doubleValue() / ((BigInteger)args.get(1)).doubleValue();
                }
                throw typesNotSupported(args);
            }
        });
        ctx.declare("__floordiv__", new Builtin("__floordiv__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof BigInteger)
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).divide((BigInteger)args.get(1));
                return new BigInteger(truediv.call(args).toString().split("\\.")[0]);
            }
        });
        ctx.declare("__mod__", new Builtin("__mod__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof String) {
                    if (args.get(1) instanceof List) {
                        List vals = (List) args.get(1);
                        return String.format(args.get(0).toString(), vals.toArray(new Object[vals.size()]));
                    }
                }
                if (args.get(0) instanceof BigInteger) {
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).mod((BigInteger)args.get(1));
                }
                throw typesNotSupported(args);
            }
        });
        ctx.declare("__add__", new Builtin("__add__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof String) {
                    if (args.get(1) instanceof String)
                        return args.get(0).toString() + args.get(1).toString();
                }
                if (args.get(0) instanceof Double) {
                    if (args.get(1) instanceof Double)
                        return ((Double)args.get(0)).doubleValue() + ((Double)args.get(1)).doubleValue();
                    if (args.get(1) instanceof BigInteger)
                        return ((Double)args.get(0)).doubleValue() + ((BigInteger)args.get(1)).doubleValue();
                }
                if (args.get(0) instanceof BigInteger) {
                    if (args.get(1) instanceof Double)
                        return ((BigInteger)args.get(0)).doubleValue() + ((Double)args.get(1)).doubleValue();
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).add((BigInteger)args.get(1));
                }
                if (args.get(0) instanceof List) {
                    if (args.get(1) instanceof List)
                        return appendLists((List)args.get(0), (List)args.get(1));
                }
                if (args.get(0) instanceof Dict) {
                    if (args.get(1) instanceof Dict)
                        return appendDicts((Dict)args.get(0), (Dict)args.get(1));
                }
                throw typesNotSupported(args);
            }
        });
        ctx.declare("__sub__", new Builtin("__sub__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof Double) {
                    if (args.get(1) instanceof Double)
                        return ((Double)args.get(0)).doubleValue() - ((Double)args.get(1)).doubleValue();
                    if (args.get(1) instanceof BigInteger)
                        return ((Double)args.get(0)).doubleValue() - ((BigInteger)args.get(1)).doubleValue();
                }
                if (args.get(0) instanceof BigInteger) {
                    if (args.get(1) instanceof Double)
                        return ((BigInteger)args.get(0)).doubleValue() - ((Double)args.get(1)).doubleValue();
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).subtract((BigInteger)args.get(1));
                }
                throw typesNotSupported(args);
            }
        });
        ctx.declare("__eq__", new Builtin("__eq__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof Double) {
                    if (args.get(1) instanceof Double)
                        return ((Double)args.get(0)).doubleValue() == ((Double)args.get(1)).doubleValue() ? 1 : 0;
                    if (args.get(1) instanceof BigInteger)
                        return ((Double)args.get(0)).doubleValue() == ((BigInteger)args.get(1)).doubleValue() ? 1 : 0;
                }
                if (args.get(0) instanceof BigInteger) {
                    if (args.get(1) instanceof Double)
                        return ((BigInteger)args.get(0)).doubleValue() == ((Double)args.get(1)).doubleValue() ? 1 : 0;
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).equals((BigInteger)args.get(1)) ? 1 : 0;
                }
                return args.get(0).equals(args.get(1));
            }
        });
        ctx.declare("__lt__", new Builtin("__lt__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof String) {
                    if (args.get(1) instanceof String)
                        return args.get(0).toString().compareTo(args.get(1).toString()) < 0 ? 1 : 0;
                }
                if (args.get(0) instanceof Double) {
                    if (args.get(1) instanceof Double)
                        return ((Double)args.get(0)).doubleValue() < ((Double)args.get(1)).doubleValue() ? 1 : 0;
                    if (args.get(1) instanceof BigInteger)
                        return ((Double)args.get(0)).doubleValue() < ((BigInteger)args.get(1)).doubleValue() ? 1 : 0;
                }
                if (args.get(0) instanceof BigInteger) {
                    if (args.get(1) instanceof Double)
                        return ((BigInteger)args.get(0)).doubleValue() < ((Double)args.get(1)).doubleValue() ? 1 : 0;
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).compareTo((BigInteger)args.get(1)) < 0 ? 1 : 0;
                }
                throw typesNotSupported(args);
            }
        });
        ctx.declare("__le__", new Builtin("__le__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof String) {
                    if (args.get(1) instanceof String)
                        return args.get(0).toString().compareTo(args.get(1).toString()) <= 0 ? 1 : 0;
                }
                if (args.get(0) instanceof Double) {
                    if (args.get(1) instanceof Double)
                        return ((Double)args.get(0)).doubleValue() <= ((Double)args.get(1)).doubleValue() ? 1 : 0;
                    if (args.get(1) instanceof BigInteger)
                        return ((Double)args.get(0)).doubleValue() <= ((BigInteger)args.get(1)).doubleValue() ? 1 : 0;
                }
                if (args.get(0) instanceof BigInteger) {
                    if (args.get(1) instanceof Double)
                        return ((BigInteger)args.get(0)).doubleValue() <= ((Double)args.get(1)).doubleValue() ? 1 : 0;
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).compareTo((BigInteger)args.get(1)) <= 0 ? 1 : 0;
                }
                throw typesNotSupported(args);
            }
        });
        ctx.declare("__gt__", new Builtin("__gt__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof String) {
                    if (args.get(1) instanceof String)
                        return args.get(0).toString().compareTo(args.get(1).toString()) > 0 ? 1 : 0;
                }
                if (args.get(0) instanceof Double) {
                    if (args.get(1) instanceof Double)
                        return ((Double)args.get(0)).doubleValue() > ((Double)args.get(1)).doubleValue() ? 1 : 0;
                    if (args.get(1) instanceof BigInteger)
                        return ((Double)args.get(0)).doubleValue() > ((BigInteger)args.get(1)).doubleValue() ? 1 : 0;
                }
                if (args.get(0) instanceof BigInteger) {
                    if (args.get(1) instanceof Double)
                        return ((BigInteger)args.get(0)).doubleValue() > ((Double)args.get(1)).doubleValue() ? 1 : 0;
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).compareTo((BigInteger)args.get(1)) > 0 ? 1 : 0;
                }
                throw typesNotSupported(args);
            }
        });
        ctx.declare("__ge__", new Builtin("__ge__") {
            public Object call(List args) {
                assertArgsLength(args, 2);
                if (args.get(0) instanceof String) {
                    if (args.get(1) instanceof String)
                        return args.get(0).toString().compareTo(args.get(1).toString()) >= 0 ? 1 : 0;
                }
                if (args.get(0) instanceof Double) {
                    if (args.get(1) instanceof Double)
                        return ((Double)args.get(0)).doubleValue() >= ((Double)args.get(1)).doubleValue() ? 1 : 0;
                    if (args.get(1) instanceof BigInteger)
                        return ((Double)args.get(0)).doubleValue() >= ((BigInteger)args.get(1)).doubleValue() ? 1 : 0;
                }
                if (args.get(0) instanceof BigInteger) {
                    if (args.get(1) instanceof Double)
                        return ((BigInteger)args.get(0)).doubleValue() >= ((Double)args.get(1)).doubleValue() ? 1 : 0;
                    if (args.get(1) instanceof BigInteger)
                        return ((BigInteger)args.get(0)).compareTo((BigInteger)args.get(1)) >= 0 ? 1 : 0;
                }
                throw typesNotSupported(args);
            }
        });
        ctx.declare("Print", new Builtin("Print") {
            public Object call(List args) {
                if (args.size() > 0) {
                    System.out.print(args.get(0));
                    for (int i = 1; i < args.size(); i++) {
                        System.out.print(" ");
                        System.out.print(args.get(i));
                    }
                }
                System.out.println();
                return args.get(args.size() - 1);
            }
        });
        return ctx;
    }

    public static String repeatString(String s, int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++)
            sb.append(s);
        return sb.toString();
    }

    public static List repeatList(List x, int n) {
        List r = new List();
        for (int i = 0; i < n; i++)
            r.addAll(x);
        return r;
    }

    public static List appendLists(List... lists) {
        List r = new List();
        for (int i = 0; i < lists.length; i++)
            r.addAll(lists[i]);
        return r;
    }

    public static Dict appendDicts(Dict... dicts) {
        Dict r = new Dict();
        for (int i = 0; i < dicts.length; i++)
            r.putAll(dicts[i]);
        return r;
    }
}

