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
  public static void main(String[] args) {
    read(System.in).eval(Context.GLOBAL_CONTEXT);
  }
  public static Ast read(InputStream input) {
    return Ast.parse(new Scanner(input));
  }

  public static class Context {

    public static Context GLOBAL_CONTEXT;

    static {
      GLOBAL_CONTEXT = new Context(null);

      GLOBAL_CONTEXT.declare("__list__", new FuncVal() {
        public ListVal call(ArrayList<Val> args) {
          return new ListVal(args);
        }
        public String toString() {
          return "<Builtin '__list__'>";
        }
      });

      GLOBAL_CONTEXT.declare("__dict__", new FuncVal() {
        public DictVal call(ArrayList<Val> args) {
          HashMap<Val, Val> m = new HashMap<Val, Val>();
          for (int i = 0; i < args.size(); i += 2) {
            m.put(args.get(i), args.get(i+1));
          }
          return new DictVal(m);
        }
        public String toString() {
          return "<Builtin '__dict__'>";
        }
      });

      GLOBAL_CONTEXT.declare("__add__", new FuncVal() {
        public Val call(ArrayList<Val> args) {
          if (args.size() != 2)
            throw new Error("__add__ expects exactly two arguments. " +
                            args.toString());
          return args.get(0).add(args.get(1));
        }
        public String toString() {
          return "<Builtin '__add__'>";
        }
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
        public String toString() {
          return "<Builtin 'Print'>";
        }
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
      throw new Error("Missing key " + key);
    }
  }

  abstract public static class Val {
    abstract public boolean toBoolean();

    public Val add(Val x) {
      throw new Error(getClass().toString() + " doesn't support 'add'");
    }

  }

  public static class StrVal extends Val {
    public String val;
    StrVal(String s) {
      val = s;
    }
    public boolean toBoolean() {
      return val.length() > 0;
    }
    public String toString() {
      return val;
    }
    public boolean equals() {
      
    }
    public int hashCode() {
      return val.hashCode();
    }
    public Val add(Val x) {
      if (x instanceof StrVal)
        return new StrVal(val + ((StrVal)x).val);
      throw new Error("StrVal can't add " + x.getClass().toString());
    }
  }

  public static class FloatVal extends Val {
    public Double val;
    FloatVal(Double d) {
      val = d;
    }
    public boolean toBoolean() {
      return val != 0.0;
    }
    public String toString() {
      return val.toString();
    }
    public int hashCode() {
      return val.hashCode();
    }
    public Val add(Val x) {
      if (x instanceof FloatVal)
        return new FloatVal(val + ((FloatVal) x).val);
      if (x instanceof IntVal)
        return new FloatVal(val + ((IntVal) x).val);
      throw new Error("FloatVal can't add " + x.getClass().toString());
    }
  }

  public static class IntVal extends Val {
    public Long val;
    IntVal(Long i) {
      val = i;
    }
    public boolean toBoolean() {
      return val != 0;
    }
    public String toString() {
      return val.toString();
    }
    public int hashCode() {
      return val.hashCode();
    }
    public Val add(Val x) {
      if (x instanceof FloatVal)
        return new FloatVal(val + ((FloatVal) x).val);
      if (x instanceof IntVal)
        return new IntVal(val + ((IntVal) x).val);
      throw new Error("FloatVal can't add " + x.getClass().toString());
    }
  }

  public static class ListVal extends Val {
    public ArrayList<Val> val;
    ListVal(ArrayList<Val> al) {
      val = al;
    }
    public boolean toBoolean() {
      return val.size() > 0;
    }
    public String toString() {
      return val.toString();
    }
    public int hashCode() {
      return val.hashCode();
    }
  }

  public static class DictVal extends Val {
    public HashMap<Val, Val> val;
    public DictVal(HashMap<Val, Val> map) {
      val = map;
    }
    public boolean toBoolean() {
      return val.size() > 0;
    }
    public String toString() {
      return val.toString();
    }
    public int hashCode() {
      return val.hashCode();
    }
  }

  abstract public static class FuncVal extends Val {
    abstract public Val call(ArrayList<Val> args);
    public boolean toBoolean() {
      return true;
    }
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
    public String toString() {
      return "<lambda>";
    }
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
      throw new Error(type);
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
      while (cond.eval(ctx).toBoolean()) {
        last = body.eval(ctx);
      }
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
    public StrVal eval(Context ctx) {
      return new StrVal(value);
    }
  }

  public static class FloatAst extends Ast {
    public double value;
    public FloatAst(Scanner sc) {
      value = sc.nextDouble();
    }
    public FloatVal eval(Context ctx) {
      return new FloatVal(value);
    }
  }

  public static class IntAst extends Ast {
    public long value;
    public IntAst(Scanner sc) {
      value = sc.nextLong();
    }
    public IntVal eval(Context ctx) {
      return new IntVal(value);
    }
  }

  public static class NameAst extends Ast {
    public String value;
    public NameAst(Scanner sc) {
      value = sc.next();
    }
    public Val eval(Context ctx) {
      return ctx.get(value);
    }
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
      body = Ast.parse(sc);
    }
    public LambdaVal eval(Context ctx) {
      return new LambdaVal(names, varargsName, body, ctx);
    }
  }
}
