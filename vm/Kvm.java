import java.math.BigInteger;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Kvm {

    public Context ctx = new GlobalContext();

    public Object run(String code) {
        return eval(parse(code));
    }

    public Object eval(Object ast) {
        return eval(ctx, ast);
    }

    //// ------------------------------------------------
    //// ---------- All static below this line ----------
    //// ------------------------------------------------

    /// eval

    public static Object eval(Context ctx, Object astBeforeCast) {
        List ast = (List) astBeforeCast;
        String type = (String) ast.get(0);

        return null;
    }

    /// Parse

    public static List parse(String code) {
        return parse(new Scanner(code));
    }

    public static List parse(Scanner sc) {
        String type = sc.next();

        if (type.equals("block")) {
            int scope = sc.nextInt();
            int nstmts = sc.nextInt();
            List stmts = new List();
            for (int i = 0; i < nstmts; i++)
                stmts.add(parse(sc));
            return new List("block", scope, stmts);
        }

        if (type.equals("if"))
            return new List("if", parse(sc), parse(sc), parse(sc));

        if (type.equals("while"))
            return new List("while", parse(sc), parse(sc));

        if (type.equals("str")) {
            StringBuilder sb = new StringBuilder();
            int strlen = sc.nextInt();
            for (int i = 0; i < strlen; i++)
                sb.append((char) sc.nextInt());
            return new List("str", sb.toString());
        }

        if (type.equals("float"))
            return new List("float", Double.parseDouble(sc.next()));

        if (type.equals("int"))
            return new List("int", new BigInteger(sc.next()));

        if (type.equals("name"))
            return new List("name", sc.next());

        throw new Error("Unknown type '" + type + "'");
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
}

