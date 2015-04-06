import java.io.InputStream;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Kvm {

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
        if (x instanceof Double) return !x.equals((double) 0.0);
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
    }

    abstract public static class Builtin extends Func {
        public String name;
        public Builtin(String name) { this.name = name; }
        public String toString() { return "<Builtin '" + name + "'>"; }
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

}

