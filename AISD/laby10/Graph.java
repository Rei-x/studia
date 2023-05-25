
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.SortedMap;

public class Graph {
	int arr[][];
	HashMap<String, Integer> name2Int;
	Map.Entry<String, Document>[] arrDoc;

	@SuppressWarnings("unchecked")
	public Graph(SortedMap<String, Document> internet) {
		int size = internet.size();
		arr = new int[size][size];

		name2Int = new HashMap<String, Integer>();

		arrDoc = new Map.Entry[size];

		int i = 0;
		for (Map.Entry<String, Document> entry : internet.entrySet()) {
			name2Int.put(entry.getKey(), i);
			arrDoc[i] = entry;
			i++;
		}

		for (i = 0; i < arr.length; i++) {
			for (int j = i; j < arr.length; j++) {
				Link l = arrDoc[i].getValue().link.get(arrDoc[j].getKey());

				if (l != null) {
					arr[i][j] = l.weight;
					arr[j][i] = l.weight;
				} else if (i == j) {
					arr[i][j] = 0;
				} else {
					arr[i][j] = Integer.MAX_VALUE;
					arr[j][i] = Integer.MAX_VALUE;
				}
			}
		}
	}

	/**
	 * Breadth first search
	 * 
	 * @param start
	 * @return
	 */
	public String bfs(String start) {
		int index = name2Int.get(start);
		Queue<Integer> queue = new LinkedList<Integer>();
		Set<Integer> visited = new HashSet<Integer>();
		queue.add(index);
		visited.add(index);
		String ret = arrDoc[index].getKey();
		while (!queue.isEmpty()) {
			int i = queue.poll();
			for (int j = 0; j < arr.length; j++) {
				if (arr[i][j] != 0 && arr[i][j] != Integer.MAX_VALUE && !visited.contains(j)) {
					queue.add(j);
					visited.add(j);
					ret += ", " + arrDoc[j].getKey();
				}
			}
		}
		return ret;
	}

	/**
	 * Depth first search using recursion
	 * 
	 * @param start
	 * @return
	 */
	public String dfs(String start) {
		int index = name2Int.get(start);
		Set<Integer> visited = new HashSet<Integer>();
		String ret = dfs(index, visited);
		return ret;
	}

	private String dfs(int index, Set<Integer> visited) {
		visited.add(index);
		String ret = arrDoc[index].getKey();
		for (int i = 0; i < arr.length; i++) {
			if (arr[index][i] != 0 && arr[index][i] != Integer.MAX_VALUE && !visited.contains(i)) {
				ret += ", " + dfs(i, visited);
			}
		}
		return ret;
	}

	public int connectedComponents() {
		DisjointSetForest dsf = new DisjointSetForest(arr.length);
		for (int i = 0; i < arr.length; i++) {
			dsf.makeSet(i);
		}

		for (int i = 0; i < arr.length; i++) {
			for (int j = i; j < arr.length; j++) {
				if (arr[i][j] != 0 && arr[i][j] != Integer.MAX_VALUE) {
					dsf.union(i, j);
				}
			}
		}

		return dsf.countSets();
	}
}
