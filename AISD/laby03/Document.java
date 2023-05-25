import java.util.Scanner;
import java.util.regex.Pattern;

public class Document {
  public String name;
  public TwoWayUnorderedListWithHeadAndTail<Link> link;
  final static String regex = "(?i)\\blink\\b=([A-Za-z]{1}[a-zA-Z0-9_]*)";

  public Document(String name, Scanner scan) {
    this.name = name;
    link = new TwoWayUnorderedListWithHeadAndTail<Link>();
    load(scan);
  }

  public void load(Scanner scan) {
    final Pattern pattern = Pattern.compile(regex);
    while (scan.hasNext()) {
      String line = scan.nextLine();

      final java.util.regex.Matcher matcher = pattern.matcher(line);

      while (matcher.find()) {
        String correctLink = matcher.group(1);
        link.add(new Link(correctLink));
      }

      if (line.equalsIgnoreCase("eod")) {
        break;
      }
    }
  }

  @Override
  public String toString() {
    String result = "Document: " + name;

    for (Link link : link) {
      result += "\n" + link.toString();
    }

    return result;
  }

  public String toStringReverse() {
    String retStr = "Document: " + name;
    return retStr + link.toStringReverse();
  }

}
