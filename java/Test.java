import java.util.ArrayList;
import java.util.Arrays;

class Test {

  public static void eq(Object expected, Object actual) {
    if (!expected.equals(actual)) {
      System.out.println(actual);
      throw new Error();
    }
  }

  public static void ne(Object not_expected, Object actual) {
    eq(false, not_expected.equals(actual));
  }

  public static ArrayList<Object> list(Object... args) {
    return new ArrayList<Object>(Arrays.asList(args));
  }
  
}
