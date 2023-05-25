
import java.util.Scanner;
import java.util.regex.Pattern;
import java.util.*;

public class Document implements IWithName {
	public String name;
	final static String regex = "\\blink\\b=([a-z]{1}[a-z0-9_]*)(?:\\((\\d+)\\)|$|\\s)";
	public SortedMap<String, Link> link;

	public Document(String name) {
		this.name = name.toLowerCase();
		link = new TreeMap<String, Link>();
	}

	public Document(String name, Scanner scan) {
		this.name = name.toLowerCase();
		link = new TreeMap<String, Link>();
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
					link.put(correctLink, new Link(correctLink, weightNumber));
				} else {
					link.put(correctLink, new Link(correctLink));
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
		String ret = "Document: " + name + "\n";
		for (Map.Entry<String, Link> entry : link.entrySet()) {
			ret += entry.getValue().toString() + "\n";
		}
		ret = ret.substring(0, ret.length() - 1);
		return ret;
	}

}
