import java.util.Scanner;
import java.util.regex.Pattern;

public class Document {
  public String name;
  public OneWayLinkedList<Link> links;
  final static String regex = "(?i)\\blink\\b=([A-Za-z]{1}[a-zA-Z0-9_]*)";

  public Document(String name, Scanner scan) {
    this.links = new OneWayLinkedList<Link>();
    this.name = name;
    load(scan);
  }

  public void load(Scanner scan) {
    final Pattern pattern = Pattern.compile(regex);
    while (scan.hasNext()) {
      String line = scan.nextLine();

      final java.util.regex.Matcher matcher = pattern.matcher(line);

      while (matcher.find()) {
        String link = matcher.group(1);
        links.add(new Link(link));
      }

      if (line.equalsIgnoreCase("eod")) {
        break;
      }
    }
  }

  @Override
  public String toString() {
    String result = "Document: " + name;

    for (Link link : links) {
      result += "\n" + link.toString();
    }

    return result;
  }

}
