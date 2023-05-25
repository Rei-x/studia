
import java.util.*;

public class Main {

	static Scanner scan; // for input stream

	public static void main(String[] args) {
		System.out.println("START");
		scan = new Scanner(System.in);
		HashTable<Document> hashTable = new HashTable<Document>(8);
		Document currentDoc = null;
		boolean halt = false;
		while (!halt) {
			String line = scan.nextLine();
			// empty line and comment line - read next line
			if (line.length() == 0 || line.charAt(0) == '#')
				continue;
			// copy line to output (it is easier to find a place of a mistake)
			System.out.println("!" + line);
			String word[] = line.split(" ");
			// getdoc name - change document to name
			if (word[0].equalsIgnoreCase("getdoc") && word.length == 2) {
				currentDoc = (Document) hashTable.get(new Document(word[1]));
				continue;
			}

			// ld documentName
			if (word[0].equalsIgnoreCase("ld") && word.length == 2) {
				if (Document.isCorrectId(word[1])) {
					currentDoc = new Document(word[1], scan);
					if (!hashTable.add(currentDoc))
						System.out.println("error");
				} else
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
				if (currentDoc != null)
					currentDoc.link.clear();
				else
					System.out.println("no current document");
				continue;
			}
			// show
			if (word[0].equalsIgnoreCase("show") && word.length == 1) {
				if (currentDoc != null)
					System.out.println(currentDoc.toString());
				else
					System.out.println("no current document");
				continue;
			}
			// postorder
			if (word[0].equalsIgnoreCase("postorder") && word.length == 1) {
				if (currentDoc != null)
					System.out.println(currentDoc.toStringPostOrder());
				else
					System.out.println("no current document");
				continue;
			}
			// preorder
			if (word[0].equalsIgnoreCase("preorder") && word.length == 1) {
				if (currentDoc != null)
					System.out.println(currentDoc.toStringPreOrder());
				else
					System.out.println("no current document");
				continue;
			}
			// size
			if (word[0].equalsIgnoreCase("size") && word.length == 1) {
				if (currentDoc != null)
					System.out.println(currentDoc.link.size());
				else
					System.out.println("no current document");
				continue;
			}
			// add str
			if (word[0].equalsIgnoreCase("add") && word.length == 2) {
				if (currentDoc != null) {
					Link link = Document.createLink(word[1]);
					if (link == null)
						System.out.println("error");
					else
						System.out.println(currentDoc.link.add(link));
				} else
					System.out.println("no current document");
				continue;
			}
			// get str
			if (word[0].equalsIgnoreCase("get") && word.length == 2) {
				if (currentDoc != null) {
					Link l = currentDoc.link.getElement(new Link(word[1]));
					if (l != null) {
						System.out.println(l);
					} else {
						System.out.println("error");
					}
				} else
					System.out.println("no current document");
				continue;
			}
			// successor str
			if (word[0].equalsIgnoreCase("successor") && word.length == 2) {
				if (currentDoc != null) {
					Link l = currentDoc.link.successor(new Link(word[1]));
					if (l != null) {
						System.out.println(l);
					} else {
						System.out.println("error");
					}
				} else
					System.out.println("no current document");

				continue;
			}
			// rem str
			if (word[0].equalsIgnoreCase("rem") && word.length == 2) {
				if (currentDoc != null) {
					Link l = currentDoc.link.remove(new Link(word[1]));
					if (l != null) {
						System.out.println(l);
					} else {
						System.out.println("error");
					}
				} else
					System.out.println("no current document");

				continue;
			}
			// ht - show hashtable
			if (word[0].equalsIgnoreCase("ht") && word.length == 1) {
				System.out.print(hashTable.toString());
				continue;
			}

			if (word[0].equalsIgnoreCase("count") && word.length == 1) {
				System.out.println(currentDoc.link.leafsSize());
				continue;
			}

			System.out.println("Wrong command");
		}
		System.out.println("END OF EXECUTION");
		scan.close();

	}

}
