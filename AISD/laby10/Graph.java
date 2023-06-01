
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Queue;
import java.util.SortedMap;

public class Graph {
	int arr[][];
	HashMap<String, Integer> name2Int;
	HashMap<Integer, String> int2Name;

	public Graph(SortedMap<String, Document> internet) {
		int size = internet.size();
		arr = new int[size][size];

		name2Int = new HashMap<>();
		int2Name = new HashMap<>();

		int i = 0;
		for (String internetString : internet.keySet()) {
			name2Int.put(internetString, i);
			int2Name.put(i, internetString);
			i++;
		}

		for (i = 0; i < arr.length; i++) {
			for (int j = 0; j < arr.length; j++) {
				Link l = internet.get(int2Name.get(i)).link.get(int2Name.get(j));

				if (l != null) {
					arr[i][j] = l.weight;
				} else if (i == j) {
					arr[i][j] = 0;
				} else {
					arr[i][j] = -1;
				}
			}
		}
	}

	public String bfs(String start) {
		if (!name2Int.containsKey(start))
			return null;

		String ret = "";

		Queue<Integer> queue = new LinkedList<>();
		boolean[] visited = new boolean[arr.length];

		queue.add(name2Int.get(start));

		while (!queue.isEmpty()) {
			int current = queue.poll();
			if (!visited[current]) {
				visited[current] = true;
				ret += int2Name.get(current) + ", ";
				for (int i = 0; i < arr.length; i++) {
					if (arr[current][i] > 0 && visited[i] == false) {
						queue.add(i);
						visited[i] = true;
					}
				}
			}
		}

		return ret.substring(0, ret.length() - 2);
	}

	public String dfs(String start) {
		if (!name2Int.containsKey(start))
			return null;

		boolean[] visited = new boolean[arr.length];
		String result = dfs(name2Int.get(start), visited);
		return result.substring(0, result.length() - 2);
	}

	private String dfs(int start, boolean[] visited) {
		String result = "";

		if (visited[start]) {
			return result;
		}

		visited[start] = true;
		result += int2Name.get(start) + ", ";
		for (int i = 0; i < arr.length; i++) {
			if (arr[start][i] > 0 && !visited[i]) {
				result += dfs(i, visited);
			}
		}
		return result;
	}

	public int connectedComponents() {
		DisjointSetForest dsf = new DisjointSetForest(arr.length);

		for (int i = 0; i < arr.length; i++) {
			dsf.makeSet(i);
		}

		for (int i = 0; i < arr.length; i++) {
			for (int j = 0; j < arr[i].length; j++) {
				if (arr[i][j] > 0) {
					dsf.union(i, j);
				}
			}
		}
		return dsf.countSets();
	}
}
