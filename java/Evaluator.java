import java.util.Map;
import java.util.ArrayList;

public class Evaluator {
  private Map<String, Object> context;

  public Evaluator(Map<String,Object> context) {
    this.context = context;
  }

  public Map<String, Object> getContext() {
    return context;
  }

  @SuppressWarnings("unchecked")
  public Object evaluate(Object value) {
    if (value instanceof Double) {
      return value;
    } else if (value instanceof String) {
      return context.get(value);
    } else if (value instanceof ArrayList) {
      ArrayList<Object> list = (ArrayList<Object>) value;
      Object function = evaluate(list.get(0));
      ArrayList<Object> argument_thunks = new ArrayList<Object>(list.subList(1, list.size()));

      if (!(function instanceof Function)) {
        throw new Error("Can only call functions");
      }

      return ((Function) function).call(this, argument_thunks);
    } else {
      throw new Error(value.getClass().toString());
    }
  }

  public static abstract class Function {
    public abstract Object call(Evaluator evaluator, ArrayList<Object> args);
  }
}
