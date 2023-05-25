import java.util.ListIterator;
import java.util.Scanner;
import java.util.regex.Pattern;

public class Document {
  public String name;
  public TwoWayCycledOrderedListWithSentinel<Link> link;
  final static String regex = "\\blink\\b=([a-z]{1}[a-z0-9_]*)(?:\\((\\d+)\\)|$|\\s)";

  public Document(String name, Scanner scan) {
    this.name = name.toLowerCase();
    link = new TwoWayCycledOrderedListWithSentinel<Link>();
    load(scan);
  }

  public void load(Scanner scan) {
    final Pattern pattern = Pattern.compile(regex, Pattern.MULTILINE | Pattern.CASE_INSENSITIVE);
    while (scan.hasNext()) {
      String line = scan.nextLine();

      final java.util.regex.Matcher matcher = pattern.matcher(line);

      while (matcher.find()) {
        String correctLink = matcher.group(1).toLowerCase();
        String weight = matcher.group(2);

        if (weight != null) {
          int weightNumber = Integer.parseInt(weight);
          link.add(new Link(correctLink, weightNumber));
        } else {
          link.add(new Link(correctLink));
        }
      }

      if (line.equalsIgnoreCase("eod")) {
        break;
      }
    }
  }

  public static boolean isCorrectId(String id) {
    return id.matches("[A-Za-z]{1}[a-zA-Z0-9_]*");
  }

  @Override
  public String toString() {
    String result = "Document: " + name;

    int counter = 10;

    for (Link link : this.link) {
      if (counter < 10) {
        result += link.toString() + " ";
      } else {
        result = result.trim();
        result += "\n" + link.toString() + " ";
        counter = 0;
      }
      counter++;
    }
    result = result.trim();
    return result;
  }

  public String toStringReverse() {
    String result = "Document: " + name;
    ListIterator<Link> iter = link.listIterator();
    while (iter.hasNext())
      iter.next();

    int counter = 10;

    while (iter.hasPrevious()) {
      Link link = iter.previous();

      if (counter < 10) {
        result += link.toString() + " ";
      } else {
        result = result.trim();
        result += "\n" + link.toString() + " ";
        counter = 0;
      }
      counter++;
    }

    result = result.trim();
    return result;
  }

}
