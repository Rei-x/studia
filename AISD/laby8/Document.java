
import java.util.Scanner;
import java.util.regex.Pattern;

public class Document implements IWithName {
	public String name;
	public BST<Link> link;
	final static String regex = "\\blink\\b=([a-z]{1}[a-z0-9_]*)(?:\\((\\d+)\\)|$|\\s)";
	final static int NUMBER_OF_DIGITS = 10;

	public Document(String name) {
		this.name = name.toLowerCase();
		link = new BST<Link>();
	}

	public Document(String name, Scanner scan) {
		this.name = name.toLowerCase();
		link = new BST<Link>();
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
	public String getName() {
		return name;
	}

	@Override
	public int hashCode() {
		int[] array = { 7, 11, 13, 17, 19 };

		int result = name.charAt(0);
		final int MODVALUE = 100000000;

		for (int i = 1; i < name.length(); i++) {
			result = (result * array[(i - 1) % array.length] + name.charAt(i)) % MODVALUE;
		}
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (obj instanceof Document) {
			return name.equals(((Document) obj).name);
		}
		return false;
	}

	@Override
	public String toString() {
		String retStr = "Document: " + name + "\n";
		retStr += link.toStringInOrder();
		return retStr;
	}

	public String toStringPreOrder() {
		String retStr = "Document: " + name + "\n";
		retStr += link.toStringPreOrder();
		return retStr;
	}

	public String toStringPostOrder() {
		String retStr = "Document: " + name + "\n";
		retStr += link.toStringPostOrder();
		return retStr;
	}
}
