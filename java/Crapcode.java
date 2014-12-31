/**
 * Totally crap programming language.
 * But might be a lot easier than living in javaland.
 */

import java.util.ArrayList;
import java.util.HashMap;

public class Crapcode {
  public static abstract class Builtin {
    public abstract Object call(HashMap<String, Object> context, ArrayList<Object> args);
  }

  public static void main(String[] args) {
    System.out.println(new Parser("(hi)").items());
  }
}
