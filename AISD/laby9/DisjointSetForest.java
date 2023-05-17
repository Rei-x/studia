
public class DisjointSetForest implements DisjointSetDataStructure {

	private class Element {
		int rank;
		int parent;
	}

	Element[] arr;

	public DisjointSetForest(int size) {
		arr = new Element[size];
		for (int i = 0; i < size; i++) {
			arr[i] = new Element();
			arr[i].rank = 0;
			arr[i].parent = i;
		}
	}

	@Override
	public void makeSet(int item) {
		arr[item].rank = 0;
		arr[item].parent = item;
	}

	@Override
	public int findSet(int item) {
		if (arr[item].parent != item)
			arr[item].parent = findSet(arr[item].parent);
		return arr[item].parent;
	}

	@Override
	public boolean union(int itemA, int itemB) {
		int rootA = findSet(itemA);
		int rootB = findSet(itemB);
		if (rootA == rootB)
			return false;
		if (arr[rootA].rank > arr[rootB].rank)
			arr[rootB].parent = rootA;
		else if (arr[rootA].rank < arr[rootB].rank)
			arr[rootA].parent = rootB;
		else {
			arr[rootB].parent = rootA;
			arr[rootA].rank++;
		}
		return true;
	}

	@Override
	public String toString() {
		String ret = "";
		for (int i = 0; i < arr.length; i++)
			ret += i + " -> " + arr[i].parent + "\n";
		return ret;
	}
}
