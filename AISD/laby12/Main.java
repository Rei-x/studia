
import java.util.*;

public class Main {

	static Scanner scan; // for input stream

	public static void main(String[] args) {
		System.out.println("START");
		scan = new Scanner(System.in);
		Automaton automaton = new Automaton();
		KMP kmp = new KMP();
		LinesReader reader = new LinesReader();
		boolean halt = false;
		while (!halt) {
			String line = scan.nextLine();
			// empty line and comment line - read next line
			if (line.length() == 0 || line.charAt(0) == '#')
				continue;
			// copy line to output (it is easier to find a place of a mistake)
			System.out.println("!" + line);
			String word[] = line.split(" ");
			// ha
			if (word[0].equalsIgnoreCase("ha") && word.length == 1) {
				halt = true;
				continue;
			}
			// automaton <PatternLines> <TextLines>
			if (word[0].equalsIgnoreCase("automaton") && word.length == 3) {
				int patternLines = Integer.parseInt(word[1]);
				int textLines = Integer.parseInt(word[2]);
				String pattern = reader.concatLines(patternLines, scan);
				String text = reader.concatLines(textLines, scan);
				LinkedList<Integer> result = automaton.validShifts(pattern, text);
				System.out.println(result);
				continue;
			}
			// kmp <PatternLines> <TextLines>
			if (word[0].equalsIgnoreCase("kmp") && word.length == 3) {
				int patternLines = Integer.parseInt(word[1]);
				int textLines = Integer.parseInt(word[2]);
				String pattern = reader.concatLines(patternLines, scan);
				String text = reader.concatLines(textLines, scan);
				LinkedList<Integer> result = kmp.validShifts(pattern, text);
				System.out.println(result);
				continue;
			}
			System.out.println("Wrong command");
		}
		System.out.println("END OF EXECUTION");
		scan.close();
	}

}
