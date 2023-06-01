
import java.util.ArrayList;
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

	public String DijkstraSSSP(String startVertexStr) {
		if (!name2Int.containsKey(startVertexStr))
			return "error\n";

		int startVertex = name2Int.get(startVertexStr);
		int[] distance = new int[arr.length];
		int[] previous = new int[arr.length];
		boolean[] visited = new boolean[arr.length];

		for (int i = 0; i < arr.length; i++) {
			distance[i] = Integer.MAX_VALUE;
			previous[i] = -1;
		}

		distance[startVertex] = 0;

		for (int i = 0; i < arr.length; i++) {
			int min = Integer.MAX_VALUE;
			int minIndex = -1;

			for (int j = 0; j < arr.length; j++) {
				if (distance[j] < min && !visited[j]) {
					min = distance[j];
					minIndex = j;
				}
			}

			if (minIndex == -1)
				break;

			visited[minIndex] = true;

			for (int j = 0; j < arr.length; j++) {
				if (arr[minIndex][j] > 0 && !visited[j]) {
					int newDistance = distance[minIndex] + arr[minIndex][j];
					if (newDistance < distance[j]) {
						distance[j] = newDistance;
						previous[j] = minIndex;
					}
				}
			}
		}

		String result = "";
		for (int i = 0; i < arr.length; i++) {
			if (distance[i] == Integer.MAX_VALUE) {
				result += "no path to " + int2Name.get(i) + "\n";
			} else {

				int current = i;
				ArrayList<Integer> path = new ArrayList<>();

				while (current != -1) {
					path.add(current);
					current = previous[current];
				}

				for (int j = path.size() - 1; j >= 0; j--) {
					result += int2Name.get(path.get(j));
					if (j != 0)
						result += "->";
				}

				result += "=" + distance[i] + "\n";
			}
		}
		return result;
	}

}
