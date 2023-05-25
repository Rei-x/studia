
import java.util.ArrayList;
import java.util.Scanner;
import java.util.regex.Pattern;

public class Document {
	final static String regex = "(?i)\\blink\\b=([A-Za-z]{1}[a-zA-Z0-9_]*)";

	public static void loadDocument(String name, Scanner scan) {
		final Pattern pattern = Pattern.compile(regex);

		while (scan.hasNext()) {
			String nextline = scan.nextLine();

			final java.util.regex.Matcher matcher = pattern.matcher(nextline);

			while (matcher.find()) {
				String link = matcher.group(1);
				System.out.println(link.toLowerCase());
			}

			if (nextline.equals("eod")) {
				break;
			}
		}
	}
}
