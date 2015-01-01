/**
 * Ghetto tests, cuz I'm too lazy to use JUnit.
 */

import java.util.ArrayList;
import java.util.Arrays;

public class ParserTest extends Test {

  public static void main(String[] args) {

    // test number()
    eq(4.0, new Parser("4").number());
    ne(4  , new Parser("4").number());

    // test stringLiteral()
    eq(list("__literal__", "hi"), new Parser("'hi'").stringLiteral());

    // test name()
    eq(true, Character.isJavaIdentifierStart('h'));
    eq(true, Character.isJavaIdentifierPart('h'));
    eq("hi", new Parser("hi").name());

    // test dict()
    eq(list("__dict__", list(1.0, 2.0)), new Parser("{1 2}").dict());

    // test item()
    eq(list("hi", "there"), new Parser("(hi there)").item());
    eq(3.5,                 new Parser("3.50").item());

    // test end to end (items)
    eq(list("hi", "there"), new Parser("hi there").items());
    eq(list("hi", 3.5), new Parser("hi 3.5").items());
    eq(list(1.0, list("hi", "there"), 3.5), new Parser("1 (hi there) 3.5").items());

    System.out.println("All tests pass!");
  }

}
