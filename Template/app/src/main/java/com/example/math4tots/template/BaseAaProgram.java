package com.example.math4tots.template;
import java.io.InputStream;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

@SuppressWarnings({"serial"})
public class BaseAaProgram {

    /// Wrappers

    public static boolean truthy(Object x) {
        if (x instanceof String) return !x.equals("");
        if (x instanceof Double) return !x.equals(0.0);
        if (x instanceof BigInteger) return !x.equals(BigInteger.ZERO);
        if (x instanceof Integer) return !x.equals(0);
        if (x instanceof List) return ((List) x).size() != 0;
        if (x instanceof Dict) return ((Dict) x).size() != 0;
        if (x instanceof Function) return true;
        throw new Error("Unrecognized java type " + x.getClass().toString());
    }

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

    abstract public static class Function {
        abstract public Object call(Object... args);
    }

    /// Context

    public static class Context {
    	ArrayList<Scope> stack = new ArrayList<Scope>();

    	public Context() {
    		GlobalScope globalScope = new GlobalScope();
    		globalScope.declare("Print", new Function() {
	            public Object call(Object... args) {
	                if (args.length > 0) {
	                    System.out.print(args[0]);
	                    for (int i = 1; i < args.length; i++) {
	                        System.out.print(" ");
	                        System.out.print(args[i]);
	                    }
	                }
	                System.out.println();
	                return args[args.length - 1];
	            }
	        });
    		stack.add(globalScope);
    	}

    	public void push() {
    		push(stack.get(stack.size()-1));
    	}

    	public void push(Scope scope) {
    		stack.add(scope);
    	}

    	public Scope pop() {
    		return stack.remove(stack.size() - 1);
    	}

    	public Scope peek() {
    		return stack.get(stack.size() - 1);
    	}

    	public Object get(String key) {
    		return peek().get(key);
    	}

    	public Object declare(String key, Object val) {
    		return peek().declare(key, val);
    	}

    	public Object assign(String key, Object val) {
    		return peek().assign(key, val);
    	}
    }

    abstract public static class Scope {
        protected Map<String, Object> table = new HashMap<String, Object>();

        abstract public Object get(String key);
        abstract public Object assign(String key, Object val);

        public Object declare(String key, Object val) {
            if (table.containsKey(key))
                throw new Error(key + " is already declared in current context");
            table.put(key, val);
            return val;
        }
    }

    public static class GlobalScope extends Scope {
        public Object get(String key) {
            if (!table.containsKey(key))
                throw new Error(key + " not found");
            return table.get(key);
        }

        public Object assign(String key, Object val) {
            if (!table.containsKey(key))
                throw new Error(key + " not found");
            table.put(key, val);
            return val;
        }
    }

    public static class LocalScope extends Scope {
        private Scope parent;

        public LocalScope(Scope p) {
            parent = p;
        }

        public Object get(String key) {
            return table.containsKey(key) ? table.get(key) : parent.get(key);
        }

        public Object assign(String key, Object val) {
            if (table.containsKey(key))  table.put(key, val);
            else                         parent.assign(key, val);
            return val;
        }
    }
}