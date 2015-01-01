import java.util.ArrayList;

/**
 * TODO: Instead of throwing Error, throw something more appropriate...
 */
public class Parser {
  private int i;
  private String s;

  public Parser(String text) {
    s = text;
    i = 0;
  }
  
  public ArrayList<Object> all() {
    ArrayList<Object> ii = items();
    if (c() != null) throw new Error();
    return ii;
  }

  public ArrayList<Object> items() {
    ArrayList<Object> ii = new ArrayList<Object>();
    Object it;
    while ((it = item()) != null) ii.add(it);
    return ii;
  }

  public Object item() {
    Object ret;
    ret = number();        if (ret != null) return ret;
    ret = stringLiteral(); if (ret != null) return ret;
    ret = name();          if (ret != null) return ret;
    ret = list();          if (ret != null) return ret;
    ret = dict();          if (ret != null) return ret;
    ret = command();       if (ret != null) return ret;
    return null;
  }

  Character c() { return i < s.length() ? s.charAt(i) : null; }

  void skipSpaces() {
    while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++;
  }

  Double number() {
    skipSpaces();
    if (c() == null || !Character.isDigit(c())) return null;
    int j = i;
    while (c() != null && (Character.isDigit(c()) || c() == '.')) i++;
    return Double.parseDouble(s.substring(j, i));
  }

  ArrayList<Object> stringLiteral() {
    skipSpaces();
    if (c() == null || c() != '"' && c() != '\'') return null;
    int j = i;
    char q = c();
    i++;
    while (c() != null && c() != q) i += (c() == '\\' ? 2 : 1);
    i++;
    // TODO: unescape the string.
    return new ArrayList<Object>(java.util.Arrays.asList(new Object[]{"__literal__", s.substring(j+1, i-1)}));
  }

  String name() {
    skipSpaces();
    if (c() == null || !Character.isJavaIdentifierStart(c())) return null;
    int j = i;
    while (c() != null && Character.isJavaIdentifierPart(c())) i++;
    return s.substring(j, i);
  }

  public ArrayList<Object> list() {
    skipSpaces();
    if (c() == null || c() != '[') return null;
    i++;
    ArrayList<Object> l = items();
    skipSpaces();
    if (c() != ']') throw new Error();
    i++;
    return new ArrayList<Object>(java.util.Arrays.asList(new Object[]{"__list__", l}));
  }

  ArrayList<Object> dict() {
    skipSpaces();
    if (c() == null || c() != '{') return null;
    i++;
    ArrayList<Object> l = items();
    skipSpaces();
    if (c() != '}') throw new Error();
    i++;
    return new ArrayList<Object>(java.util.Arrays.asList(new Object[]{"__dict__", l}));
  }

  ArrayList<Object> command() {
    skipSpaces();
    if (c() == null || c() != '(') return null;
    i++;
    ArrayList<Object> l = items();
    skipSpaces();
    if (c() != ')') throw new Error();
    i++;
    return l;
  }
}
