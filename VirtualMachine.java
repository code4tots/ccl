/*
Organization of this file:
  class VirtualMachine
  class Context (includes many 'declare' for GLOBAL_CONTEXT)
  abstract class Val
  ... subclasses of Val ...
  abstract class Ast
  ... subclasses of Ast ...
*/
import java.io.InputStream;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Scanner;

public class VirtualMachine {
  public static void main(String[] args) { new VirtualMachine().run(System.in); }

  public Context ctx;

  public VirtualMachine() {
    ctx = new Context(getGlobalContext());
  }

  public Context getGlobalContext() {
    return Context.GLOBAL_CONTEXT;
  }

  public Val run(String code) {
    return Ast.parse(new Scanner(code)).eval(ctx);
  }

  public Val run(InputStream input) {
    return Ast.parse(new Scanner(input)).eval(ctx);
  }

  public static class Context {
    public static Context GLOBAL_CONTEXT;
    static {
      GLOBAL_CONTEXT = new Context(null);
      GLOBAL_CONTEXT.declare("__list__", new FuncVal() {
        public ListVal call(ArrayList<Val> args) {
          return new ListVal(args);
        }
        public String toString() { return "<Builtin '__list__'>"; }
      });
      GLOBAL_CONTEXT.declare("__dict__", new FuncVal() {
        public DictVal call(ArrayList<Val> args) {
          HashMap<Val, Val> m = new HashMap<Val, Val>();
          for (int i = 0; i < args.size(); i += 2) {
            m.put(args.get(i), args.get(i+1));
          }
          return new DictVal(m);
        }
        public String toString() { return "<Builtin '__dict__'>"; }
      });
      GLOBAL_CONTEXT.declare("__setitem__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 3)
            throw new Error("__setitem__ expects exactly three arguments. " +
                            args.toString());
          return args.get(0).setItem(args.get(1), args.get(2));
        }
        public String toString() { return "<Builtin '__setitem__'>"; }
      });
      GLOBAL_CONTEXT.declare("__getitem__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__getitem__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).getItem(args.get(1));
        }
        public String toString() { return "<Builtin '__getitem__'>"; }
      });
      GLOBAL_CONTEXT.declare("__mul__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__mul__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).mul(args.get(1));
        }
        public String toString() { return "<Builtin '__mul__'>"; }
      });
      GLOBAL_CONTEXT.declare("__truediv__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__truediv__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).truediv(args.get(1));
        }
        public String toString() { return "<Builtin '__truediv__'>"; }
      });
      GLOBAL_CONTEXT.declare("__floordiv__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__floordiv__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).floordiv(args.get(1));
        }
        public String toString() { return "<Builtin '__floordiv__'>"; }
      });
      GLOBAL_CONTEXT.declare("__mod__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__mod__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).mod(args.get(1));
        }
        public String toString() { return "<Builtin '__mod__'>"; }
      });
      GLOBAL_CONTEXT.declare("__add__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__add__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).add(args.get(1));
        }
        public String toString() { return "<Builtin '__add__'>"; }
      });
      GLOBAL_CONTEXT.declare("__sub__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__sub__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).sub(args.get(1));
        }
        public String toString() { return "<Builtin '__sub__'>"; }
      });
      GLOBAL_CONTEXT.declare("__lt__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__lt__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).lt(args.get(1));
        }
        public String toString() { return "<Builtin '__lt__'>"; }
      });
      GLOBAL_CONTEXT.declare("__le__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__le__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).le(args.get(1));
        }
        public String toString() { return "<Builtin '__le__'>"; }
      });
      GLOBAL_CONTEXT.declare("__gt__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__gt__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).gt(args.get(1));
        }
        public String toString() { return "<Builtin '__gt__'>"; }
      });
      GLOBAL_CONTEXT.declare("__ge__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__ge__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).ge(args.get(1));
        }
        public String toString() { return "<Builtin '__ge__'>"; }
      });
      GLOBAL_CONTEXT.declare("Print", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() > 0) {
            System.out.print(args.get(0));
            for (int i = 1; i < args.size(); i++) {
              System.out.print(" ");
              System.out.print(args.get(i));
            }
            System.out.println();
          }
          return args.get(args.size() - 1);
        }
        public String toString() { return "<Builtin 'Print'>"; }
      });
    }
    public Context parent;
    public HashMap<String, Val> table;
    public Context(Context parent) {
      this.parent = parent;
      table = new HashMap<String, Val>();
    }
    public Val get(String key) {
      if (table.containsKey(key))
        return table.get(key);
      if (parent != null)
        return parent.get(key);
      throw new Error("Missing key " + key);
    }
    public void declare(String key, Val val) {
      if (table.containsKey(key))
        throw new Error(key + " already declared");
      table.put(key, val);
    }
    public void assign(String key, Val val) {
      if (table.containsKey(key))
        table.put(key, val);
      else if (parent != null)
        parent.assign(key, val);
      else
        throw new Error("Missing key " + key);
    }
  }

  abstract public static class Val {
    abstract public boolean toBoolean();
    public Val setItem(Val n, Val x) { throw new Error(getClass().toString() + " doesn't support 'setItem'"); }
    public Val getItem(Val x) { throw new Error(getClass().toString() + " doesn't support 'getItem'"); }
    public Val mul(Val x) { throw new Error(getClass().toString() + " doesn't support 'mul'"); }
    public Val truediv(Val x) { throw new Error(getClass().toString() + " doesn't support 'truediv'"); }
    public Val floordiv(Val x) { throw new Error(getClass().toString() + " doesn't support 'floordiv'"); }
    public Val mod(Val x) { throw new Error(getClass().toString() + " doesn't support 'mod'"); }
    public Val add(Val x) { throw new Error(getClass().toString() + " doesn't support 'add'"); }
    public Val sub(Val x) { throw new Error(getClass().toString() + " doesn't support 'sub'"); }
    public Val lt(Val x) { throw new Error(getClass().toString() + " doesn't support 'lt'"); }
    public Val le(Val x) { throw new Error(getClass().toString() + " doesn't support 'le'"); }
    public Val gt(Val x) { throw new Error(getClass().toString() + " doesn't support 'gt'"); }
    public Val ge(Val x) { throw new Error(getClass().toString() + " doesn't support 'ge'"); }
  }
  abstract public static class WrapVal extends Val {
    public Object val;
    public WrapVal(Object val) { this.val = val; }
    public String toString() { return val.toString(); }
    public boolean equals(Object x) { return x instanceof WrapVal && val.equals(((WrapVal)x).val); }
    public int hashCode() { return val.hashCode(); }
  }
  public static class StrVal extends WrapVal {
    public StrVal(String v) { super(v); }
    public String getVal() { return (String) val; }
    public boolean toBoolean() { return getVal().length() > 0; }
    public Val mul(Val x) {
      if (x instanceof IntVal) {
        Long n = ((IntVal)x).getVal();
        StringBuilder sb = new StringBuilder();
        String s = getVal();
        for (int i = 0; i < n; i++)
          sb.append(s);
        return new StrVal(sb.toString());
      }
      throw new Error("StrVal can't mul " + x.getClass().toString());
    }
    public Val add(Val x) {
      if (x instanceof StrVal)
        return new StrVal(getVal() + ((StrVal)x).getVal());
      throw new Error("StrVal can't add " + x.getClass().toString());
    }
  }
  public static class FloatVal extends WrapVal {
    public FloatVal(Double v) { super(v); }
    public Double getVal() { return (Double) val; }
    public boolean toBoolean() { return !getVal().equals(new Double(0.0)); }
    public Val add(Val x) {
      if (x instanceof FloatVal)
        return new FloatVal(getVal() + ((FloatVal) x).getVal());
      if (x instanceof IntVal)
        return new FloatVal(getVal() + ((IntVal) x).getVal());
      throw new Error("FloatVal can't add " + x.getClass().toString());
    }
  }
  public static class IntVal extends WrapVal {
    public IntVal(Long v) { super(v); }
    public Long getVal() { return (Long) val; }
    public boolean toBoolean() { return !getVal().equals(0L); }
    public Val add(Val x) {
      if (x instanceof FloatVal)
        return new FloatVal(getVal() + ((FloatVal) x).getVal());
      if (x instanceof IntVal)
        return new IntVal(getVal() + ((IntVal) x).getVal());
      throw new Error("IntVal can't add " + x.getClass().toString());
    }
    public Val sub(Val x) {
      if (x instanceof IntVal)
        return new IntVal(getVal() - ((IntVal) x).getVal());
      throw new Error("IntVal can't add " + x.getClass().toString());
    }
    public Val lt(Val x) {
      if (x instanceof IntVal)
        return new IntVal(getVal().compareTo(((IntVal)x).getVal()) < 0 ? 1L : 0L);
      throw new Error("IntVal can't lt " + x.getClass().toString());
    }
  }
  public static class ListVal extends WrapVal {
    public ListVal(ArrayList<Val> v) { super(v); }
    @SuppressWarnings("unchecked")
    public ArrayList<Val> getVal() { return (ArrayList<Val>) val; }
    public boolean toBoolean() { return getVal().size() > 0; }
  }
  public static class DictVal extends WrapVal {
    public DictVal(HashMap<Val, Val> v) { super(v); }
    @SuppressWarnings("unchecked")
    public HashMap<Val, Val> getVal() { return (HashMap<Val, Val>) val; }
    public boolean toBoolean() { return getVal().size() > 0;  }
    public Val setItem(Val n, Val x) {
      getVal().put(n, x);
      return x;
    }
    public Val getItem(Val x) {
      Val v = getVal().get(x);
      if (v == null)
        throw new Error(x.toString() + " not found in " + toString());
      return v;
    }
  }
  abstract public static class FuncVal extends Val {
    abstract public Val call(ArrayList<Val> args);
    public boolean toBoolean() { return true; }
  }
  public static class LambdaVal extends FuncVal {
    public ArrayList<String> names;
    public String varargsName;
    public Ast body;
    public Context ctx;
    public LambdaVal(ArrayList<String> names, String varargsName,
                     Ast body, Context ctx) {
      this.names = names;
      this.varargsName = varargsName;
      this.body = body;
      this.ctx = ctx;
    }
    public Val call(ArrayList<Val> args) {
      Context ictx = new Context(ctx);
      int i;
      for (i = 0; i < names.size(); i++)
        ictx.declare(names.get(i), args.get(i));
      ArrayList<Val> varargs = new ArrayList<Val>();
      for (; i < args.size(); i++)
        varargs.add(args.get(i));
      ictx.declare(varargsName, new ListVal(varargs));
      return body.eval(ictx);
    }
    public String toString() { return "<lambda>"; }
  }

  abstract public static class Ast {
    public static Ast parse(Scanner sc) {
      String type = sc.next();
      if (type.equals("block"))
        return new BlockAst(sc);
      if (type.equals("if"))
        return new IfAst(sc);
      if (type.equals("while"))
        return new WhileAst(sc);
      if (type.equals("str"))
        return new StrAst(sc);
      if (type.equals("float"))
        return new FloatAst(sc);
      if (type.equals("int"))
        return new IntAst(sc);
      if (type.equals("name"))
        return new NameAst(sc);
      if (type.equals("call"))
        return new CallAst(sc);
      if (type.equals("decl"))
        return new DeclAst(sc);
      if (type.equals("assign"))
        return new AssignAst(sc);
      if (type.equals("lambda"))
        return new LambdaAst(sc);
      throw new Error("Invalid parse type " + type);
    }
    abstract public Val eval(Context ctx);
  }
  public static class BlockAst extends Ast {
    public boolean scope;
    public ArrayList<Ast> stmts;
    public BlockAst(Scanner sc) {
      scope = sc.nextInt() == 1;
      int nstmts = sc.nextInt();
      stmts = new ArrayList<Ast>();
      for (int i = 0; i < nstmts; i++)
        stmts.add(Ast.parse(sc));
    }
    public Val eval(Context ctx) {
      if (scope)
        ctx = new Context(ctx);
      Val last = new IntVal(0L);
      for (int i = 0; i < stmts.size(); i++) {
        last = stmts.get(i).eval(ctx);
      }
      return last;
    }
  }
  public static class IfAst extends Ast {
    public Ast cond, a, b;
    public IfAst(Scanner sc) {
      cond = Ast.parse(sc);
      a = Ast.parse(sc);
      b = Ast.parse(sc);
    }
    public Val eval(Context ctx) {
      return cond.eval(ctx).toBoolean() ? a.eval(ctx) : b.eval(ctx);
    }
  }
  public static class WhileAst extends Ast {
    public Ast cond, body;
    public WhileAst(Scanner sc) {
      cond = Ast.parse(sc);
      body = Ast.parse(sc);
    }
    public Val eval(Context ctx) {
      Val last = new IntVal(0L);
      while (cond.eval(ctx).toBoolean())
        last = body.eval(ctx);
      return last;
    }
  }
  public static class StrAst extends Ast {
    public String value;
    public StrAst(Scanner sc) {
      StringBuilder sb = new StringBuilder();
      int nchars = sc.nextInt();
      for (int i = 0; i < nchars; i++)
        sb.append((char) sc.nextInt());
      value = sb.toString();
    }
    public StrVal eval(Context ctx) { return new StrVal(value); }
  }
  public static class FloatAst extends Ast {
    public double value;
    public FloatAst(Scanner sc) { value = sc.nextDouble(); }
    public FloatVal eval(Context ctx) { return new FloatVal(value); }
  }
  public static class IntAst extends Ast {
    public long value;
    public IntAst(Scanner sc) { value = sc.nextLong(); }
    public IntVal eval(Context ctx) { return new IntVal(value); }
  }
  public static class NameAst extends Ast {
    public String value;
    public NameAst(Scanner sc) { value = sc.next(); }
    public Val eval(Context ctx) { return ctx.get(value); }
  }
  public static class CallAst extends Ast {
    public Ast f;
    public ArrayList<Ast> args;
    public CallAst(Scanner sc) {
      f = Ast.parse(sc);
      int nargs = sc.nextInt();
      args = new ArrayList<Ast>();
      for (int i = 0; i < nargs; i++)
        args.add(Ast.parse(sc));
    }
    public Val eval(Context ctx) {
      FuncVal f = (FuncVal) this.f.eval(ctx);
      ArrayList<Val> args = new ArrayList<Val>();
      for (int i = 0; i < this.args.size(); i++)
        args.add(this.args.get(i).eval(ctx));
      return f.call(args);
    }
  }
  public static class DeclAst extends Ast {
    public String name;
    public Ast value;
    public DeclAst(Scanner sc) {
      name = sc.next();
      value = Ast.parse(sc);
    }
    public Val eval(Context ctx) {
      Val v = value.eval(ctx);
      ctx.declare(name, v);
      return v;
    }
  }
  public static class AssignAst extends Ast {
    public String name;
    public Ast value;
    public AssignAst(Scanner sc) {
      name = sc.next();
      value = Ast.parse(sc);
    }
    public Val eval(Context ctx) {
      Val v = value.eval(ctx);
      ctx.assign(name, v);
      return v;
    }
  }
  public static class LambdaAst extends Ast {
    public ArrayList<String> names;
    public String varargsName;
    public Ast body;
    public LambdaAst(Scanner sc) {
      names = new ArrayList<String>();
      int nnames = sc.nextInt();
      for (int i = 0; i < nnames; i++)
        names.add(sc.next());
      varargsName = sc.next();
      body = Ast.parse(sc);
    }
    public LambdaVal eval(Context ctx) {
      return new LambdaVal(names, varargsName, body, ctx);
    }
  }
}
