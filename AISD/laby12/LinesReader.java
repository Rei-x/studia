
import java.util.Scanner;

public class LinesReader {

	String concatLines(int howMany, Scanner scanner) {
		StringBuffer result = new StringBuffer();
		while (howMany-- > 0) {
			result.append(scanner.next());
		}
		return result.toString();
	}

}
