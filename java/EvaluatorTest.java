import java.util.HashMap;

class EvaluatorTest extends Test {

  public static void main(String[] args) {

    Evaluator e = new Evaluator(new HashMap<String, Object>());

    // test Double
    eq(4.4, e.evaluate(4.4));

    System.out.println("All tests pass!");
  }

}
