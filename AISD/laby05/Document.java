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

  public static Link createLink(String link) {
    String realLink = "link=" + link;

    final Pattern pattern = Pattern.compile(regex, Pattern.MULTILINE | Pattern.CASE_INSENSITIVE);

    final java.util.regex.Matcher matcher = pattern.matcher(realLink);

    while (matcher.find()) {
      String correctLink = matcher.group(1).toLowerCase();
      String weight = matcher.group(2);

      if (weight != null) {
        int weightNumber = Integer.parseInt(weight);
        return new Link(correctLink, weightNumber);
      } else {
        return new Link(correctLink);
      }
    }

    return null;
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

  public int[] getWeights() {
    int[] weights = new int[link.size()];
    int counter = 0;
    for (Link link : this.link) {
      weights[counter] = link.weight;
      counter++;
    }
    return weights;
  }

  public static void showArray(int[] arr) {
    for (int i = 0; i < arr.length - 1; i++) {
      System.out.print(arr[i] + " ");
    }
    System.out.print(arr[arr.length - 1]);
    System.out.println();
  }

  public void bubbleSort(int[] arr) {
    showArray(arr);

    for (int i = 0; i < arr.length - 1; i++) {
      for (int j = arr.length - 1; j > i; j--) {
        int left = arr[j - 1];
        int right = arr[j];

        if (left > right) {
          swap(arr, j, j - 1);
        }
      }
      showArray(arr);
    }
  }

  public void insertSort(int[] arr) {
    showArray(arr);

    for (int i = arr.length - 2; i >= 0; i--) {
      int previousElement = arr[i];
      int j = i + 1;

      while (j < arr.length && previousElement > arr[j]) {
        swap(arr, j, j - 1);
        j++;
      }
      showArray(arr);
    }
  }

  private void swap(int[] arr, int j, int i) {
    int temp = arr[j];
    arr[j] = arr[i];
    arr[i] = temp;
  }

  public void selectSort(int[] arr) {
    showArray(arr);

    for (int i = arr.length - 1; i > 0; i--) {
      int max = arr[i];
      int maxIndex = i;

      for (int j = i; j >= 0; j--) {
        if (arr[j] > max) {
          max = arr[j];
          maxIndex = j;
        }
      }
      swap(arr, i, maxIndex);

      showArray(arr);
    }
  }

}
