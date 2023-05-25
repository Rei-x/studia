import java.util.*;

public class Main {
	static Scanner scan; // for input stream

	public static void main(String[] args) {
		System.out.println("START");
		scan = new Scanner(System.in);
		Document[] doc = null;
		int currentDocNo = 0;
		int maxNo = -1;
		boolean halt = false;
		while (!halt) {
			String line = scan.nextLine();
			// empty line and comment line - read next line
			if (line.length() == 0 || line.charAt(0) == '#')
				continue;
			// copy line to output (it is easier to find a place of a mistake)
			System.out.println("!" + line);
			String word[] = line.split(" ");
			// go n - start with array of the length n
			if (word[0].equalsIgnoreCase("go") && word.length == 2) {
				maxNo = Integer.parseInt(word[1]);
				doc = new Document[maxNo];
				continue;
			}
			// ch - change index
			if (word[0].equalsIgnoreCase("ch") && word.length == 2) {
				currentDocNo = Integer.parseInt(word[1]);
				continue;
			}

			// ld documentName
			if (word[0].equalsIgnoreCase("ld") && word.length == 2) {
				if (Document.isCorrectId(word[1]))
					doc[currentDocNo] = new Document(word[1], scan);
				else
					System.out.println("incorrect ID");
				continue;
			}
			// ha
			if (word[0].equalsIgnoreCase("ha") && word.length == 1) {
				halt = true;
				continue;
			}
			// clear
			if (word[0].equalsIgnoreCase("clear") && word.length == 1) {
				doc[currentDocNo].link.clear();
				continue;
			}
			// show
			if (word[0].equalsIgnoreCase("show") && word.length == 1) {
				System.out.println(doc[currentDocNo].toString());
				continue;
			}
			// reverse
			if (word[0].equalsIgnoreCase("reverse") && word.length == 1) {
				System.out.println(doc[currentDocNo].toStringReverse());
				continue;
			} // size
			if (word[0].equalsIgnoreCase("size") && word.length == 1) {
				System.out.println(doc[currentDocNo].link.size());
				continue;
			}
			// add str
			if (word[0].equalsIgnoreCase("add") && word.length == 2) {
				Link link = Document.createLink(word[1]);
				if (link == null)
					System.out.println("error");
				else
					System.out.println(doc[currentDocNo].link.add(link));
				continue;
			}
			// addi index str
			if (word[0].equalsIgnoreCase("addi") && word.length == 3) {
				int index = Integer.parseInt(word[1]);
				try {
					doc[currentDocNo].link.add(index, new Link(word[2]));
				} catch (NoSuchElementException e) {
					System.out.println("error");
				}
				continue;
			}
			// get index
			if (word[0].equalsIgnoreCase("get") && word.length == 2) {
				int index = Integer.parseInt(word[1]);
				try {
					Link l = doc[currentDocNo].link.get(index);
					System.out.println(l.ref);
				} catch (NoSuchElementException e) {
					System.out.println("error");
				}
				continue;
			}
			// set index str
			if (word[0].equalsIgnoreCase("set") && word.length == 3) {
				int index = Integer.parseInt(word[1]);
				try {
					Link l = doc[currentDocNo].link.set(index, new Link(word[2]));
					System.out.println(l.ref);
				} catch (NoSuchElementException e) {
					System.out.println("error");
				}

				continue;
			}
			// index str
			if (word[0].equalsIgnoreCase("index") && word.length == 2) {
				int index = doc[currentDocNo].link.indexOf(new Link(word[1]));
				System.out.println(index);
				continue;
			}
			// remi index
			if (word[0].equalsIgnoreCase("remi") && word.length == 2) {
				int index = Integer.parseInt(word[1]);
				try {
					Link l = doc[currentDocNo].link.remove(index);
					System.out.println(l);
				} catch (NoSuchElementException e) {
					System.out.println("error");
				}
				continue;
			}
			// rem str
			if (word[0].equalsIgnoreCase("rem") && word.length == 2) {
				System.out.println(doc[currentDocNo].link.remove(new Link(word[1])));
				continue;
			}
			// remall str
			if (word[0].equalsIgnoreCase("remall") && word.length == 2) {
				doc[currentDocNo].link.removeAll(new Link(word[1]));
				continue;
			} // addl <indexOfListArray>
			if (word[0].equalsIgnoreCase("addl") && word.length == 2) {
				int number = Integer.parseInt(word[1]);
				doc[currentDocNo].link.add(doc[number].link);
				continue;
			}
			if (word[0].equalsIgnoreCase("bubblesort") && word.length == 1) {
				doc[currentDocNo].bubbleSort(doc[currentDocNo].getWeights());
				continue;
			}

			if (word[0].equalsIgnoreCase("insertsort") && word.length == 1) {
				doc[currentDocNo].insertSort(doc[currentDocNo].getWeights());
				continue;
			}

			if (word[0].equalsIgnoreCase("selectsort") && word.length == 1) {
				doc[currentDocNo].selectSort(doc[currentDocNo].getWeights());
				continue;
			}
			if (word[0].equalsIgnoreCase("mergesort") && word.length == 1) {

				doc[currentDocNo].iterativeMergeSort(doc[currentDocNo].getWeights());

				continue;
			}
			if (word[0].equalsIgnoreCase("radixsort") && word.length == 1) {

				doc[currentDocNo].radixSort(doc[currentDocNo].getWeights());

				continue;
			}

			System.out.println("Wrong command");
		}
		System.out.println("END OF EXECUTION");
		scan.close();

	}

}
