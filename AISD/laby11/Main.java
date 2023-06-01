
import java.util.*;

public class Main {

	static Scanner scan; // for input stream

	public static void main(String[] args) {
		System.out.println("START");
		scan = new Scanner(System.in);
		SortedMap<String, Document> sortedMap = new TreeMap<String, Document>();
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
				currentDoc = (Document) sortedMap.get(word[1]);
				continue;
			}

			// ld documentName
			if (word[0].equalsIgnoreCase("ld") && word.length == 2) {
				if (Document.isCorrectId(word[1])) {
					currentDoc = new Document(word[1], scan);
					sortedMap.put(currentDoc.name, currentDoc);
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
			// it depends of the representation so it will be NOT in tests
			if (word[0].equalsIgnoreCase("show") && word.length == 1) {
				if (currentDoc != null)
					System.out.println(currentDoc.toString());
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
					else {
						currentDoc.link.put(link.ref, link);
						System.out.println("true");
					}
				} else
					System.out.println("no current document");
				continue;
			}
			// get str
			if (word[0].equalsIgnoreCase("get") && word.length == 2) {
				if (currentDoc != null) {
					Link l = currentDoc.link.get(word[1]);
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
					Link l = currentDoc.link.remove(word[1]);
					if (l != null) {
						// write the removed link
						System.out.println(l);
					} else {
						System.out.println("error");
					}
				} else
					System.out.println("no current document");

				continue;
			}

			// bfs str
			if (word[0].equalsIgnoreCase("bfs") && word.length == 2) {
				Graph graph = new Graph(sortedMap);
				String str = graph.bfs(word[1]);
				if (str != null) {
					System.out.println(str);
				} else {
					System.out.println("error");
				}
				continue;
			}
			// dfs str
			if (word[0].equalsIgnoreCase("dfs") && word.length == 2) {
				Graph graph = new Graph(sortedMap);
				String str = graph.dfs(word[1]);
				if (str != null) {
					System.out.println(str);
				} else {
					System.out.println("error");
				}
				continue;
			}
			// cc
			if (word[0].equalsIgnoreCase("cc") && word.length == 1) {
				Graph graph = new Graph(sortedMap);
				int str = graph.connectedComponents();
				System.out.println(str);
				continue;
			}
			// graph
			if (word[0].equalsIgnoreCase("graph") && word.length == 1) {
				Graph graph = new Graph(sortedMap);
				System.out.println(graph);
				continue;
			}
			// sssp str
			if (word[0].equalsIgnoreCase("sssp") && word.length == 2) {
				Graph graph = new Graph(sortedMap);
				String str = graph.DijkstraSSSP(word[1]);
				if (str != null) {
					System.out.print(str);
				} else {
					System.out.println("error");
				}
				continue;
			}
			System.out.println("Wrong command");
		}
		System.out.println("END OF EXECUTION");
		scan.close();
	}

}
