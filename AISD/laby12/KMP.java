import java.util.LinkedList;

public class KMP implements IStringMatcher {

	@Override
	public LinkedList<Integer> validShifts(String pattern, String text) {
		final int patternLength = pattern.length();
		final int textLength = text.length();
		LinkedList<Integer> shifts = new LinkedList<>();

		int preSuffixArray[] = calculatePreSuffixArray(pattern);

		int patternIndex = 0;
		int textIndex = 0;

		while (textIndex < textLength) {
			if (pattern.charAt(patternIndex) == text.charAt(textIndex)) {
				patternIndex++;
				textIndex++;
			}

			if (patternIndex == patternLength) {
				shifts.add(textIndex - patternIndex);
				patternIndex = preSuffixArray[patternIndex - 1];
			} else if (textIndex < textLength &&
					pattern.charAt(patternIndex) != text.charAt(textIndex)) {
				if (patternIndex != 0) {
					patternIndex = preSuffixArray[patternIndex - 1];
				} else {
					textIndex = textIndex + 1;
				}
			}
		}

		return shifts;
	}

	public int[] calculatePreSuffixArray(String pattern) {
		int patternLength = pattern.length();

		int preSuffixArray[] = new int[patternLength];

		int skipValue = 0;

		int currentCharacterIndex = 1;

		preSuffixArray[0] = 0;

		while (currentCharacterIndex < patternLength) {
			if (pattern.charAt(currentCharacterIndex) == pattern.charAt(skipValue)) {
				skipValue++;
				preSuffixArray[currentCharacterIndex] = skipValue;
				currentCharacterIndex++;
			} else {
				if (skipValue != 0) {
					skipValue = preSuffixArray[skipValue - 1];
				} else {
					preSuffixArray[currentCharacterIndex] = skipValue;
					currentCharacterIndex++;
				}
			}
		}

		return preSuffixArray;
	}

}