
import java.util.LinkedList;

public class Automaton implements IStringMatcher {

	public final static int LIMIT = 256;

	@Override
	public LinkedList<Integer> validShifts(String pattern, String text) {
		int patternLength = pattern.length();
		int textLength = text.length();

		LinkedList<Integer> shifts = new LinkedList<>();

		int[][] stateArray = calculateStateArray(pattern, patternLength);

		int nextState = 0;
		for (int i = 0; i < textLength; i++) {
			nextState = stateArray[nextState][text.charAt(i)];
			if (nextState == patternLength) {
				shifts.add(i - patternLength + 1);
			}
		}
		return shifts;
	}

	public int[][] calculateStateArray(String pattern, int patternLength) {
		int[][] stateArray = new int[patternLength + 1][LIMIT];

		for (int i = 0; i <= patternLength; ++i) {
			for (int j = 0; j < LIMIT; ++j) {
				stateArray[i][j] = nextState(pattern, i, j);
			}
		}

		return stateArray;
	}

	public int nextState(String pattern, int patternIndex, int character) {
		int patternLength = pattern.length();

		if (patternIndex < patternLength && character == pattern.charAt(patternIndex)) {
			return patternIndex + 1;
		}

		int i;

		for (int next = patternIndex; next > 0; next--) {
			if (pattern.charAt(next - 1) == character) {
				for (i = 0; i < next - 1; i++) {
					if (pattern.charAt(i) != pattern.charAt(patternIndex - next + 1 + i)) {
						break;
					}
				}

				if (i == next - 1) {
					return next;
				}
			}
		}
		return 0;
	}
}