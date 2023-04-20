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

				if (left < right) {
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

			while (j < arr.length && previousElement < arr[j]) {
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
				if (arr[j] < max) {
					max = arr[j];
					maxIndex = j;
				}
			}
			swap(arr, i, maxIndex);

			showArray(arr);
		}
	}

	public void iterativeMergeSort(int[] arr) {
		showArray(arr);

		int size = arr.length;

		int maximumArrayIndex = size - 1;

		for (int currentSize = 1; currentSize <= maximumArrayIndex; currentSize = 2 * currentSize) {
			for (int leftStart = 0; leftStart < size - 1; leftStart += 2 * currentSize) {
				int leftEnd = Math.min(leftStart + currentSize - 1, maximumArrayIndex);
				int rightEnd = Math.min(leftStart + 2 * currentSize - 1, maximumArrayIndex);

				merge(arr, leftStart, leftEnd, rightEnd);
			}
			showArray(arr);
		}
	}

	public static void copyArrayWithOffset(int[] from, int[] to, int offset) {
		for (int i = 0; i < to.length; i++) {
			to[i] = from[i + offset];
		}
	}

	private static void copyArray(int[] from, int[] to) {
		copyArrayWithOffset(from, to, 0);
	}

	public static void merge(int arr[], int left, int mid, int right) {
		int leftArrayLength = mid - left + 1;
		int rightArrayLength = right - mid;

		int leftArray[] = new int[leftArrayLength];
		int rightArray[] = new int[rightArrayLength];

		copyArrayWithOffset(arr, leftArray, left);
		copyArrayWithOffset(arr, rightArray, mid + 1);

		int currentLeftArrayIndex = 0;
		int currentRightArrayIndex = 0;
		int index = left;

		while (currentLeftArrayIndex < leftArrayLength && currentRightArrayIndex < rightArrayLength) {
			if (leftArray[currentLeftArrayIndex] <= rightArray[currentRightArrayIndex]) {
				arr[index] = leftArray[currentLeftArrayIndex++];
			} else {
				arr[index] = rightArray[currentRightArrayIndex++];
			}
			index++;
		}

		while (currentLeftArrayIndex < leftArrayLength) {
			arr[index++] = leftArray[currentLeftArrayIndex++];
		}

		while (currentRightArrayIndex < rightArrayLength) {
			arr[index++] = rightArray[currentRightArrayIndex++];
		}
	}

	public void radixSort(int[] arr) {
		showArray(arr);
		int max = 999;

		for (int exp = 1; max / exp > 0; exp *= 10) {
			countSort(arr, exp);
			showArray(arr);
		}
	}

	public static void countSort(int arr[], int digitPlace) {
		int tempOutput[] = new int[arr.length];

		int digitCount[] = countDigits(arr, digitPlace);

		final int NUMBER_OF_DIGITS = 10;

		for (int i = 1; i < NUMBER_OF_DIGITS; i++) {
			digitCount[i] += digitCount[i - 1];
		}

		for (int i = arr.length - 1; i >= 0; i--) {
			int digit = getDigit(arr[i], digitPlace);
			tempOutput[digitCount[digit] - 1] = arr[i];
			digitCount[digit]--;
		}


		copyArray(tempOutput, arr);
	}

	private static int[] countDigits(int[] arr, int digitPlace) {
		int count[] = new int[10];

		for (int i = 0; i < arr.length; i++) {
			int digit = getDigit(arr[i], digitPlace);
			count[digit]++;
		}

		return count;
	}

	public static int getDigit(int number, int digitPlace) {
		return (number / digitPlace) % 10;
	}
}
