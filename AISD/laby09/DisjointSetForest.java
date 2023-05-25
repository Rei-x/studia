
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
		Element rootA = arr[findSet(itemA)];
		Element rootB = arr[findSet(itemB)];

		if (rootA == rootB)
			return false;

		if (rootA.rank > rootB.rank)
			rootB.parent = rootA.parent;
		else if (rootA.rank < rootB.rank)
			rootA.parent = rootB.parent;
		else {
			rootA.parent = rootB.parent;
			rootB.rank++;
		}

		return true;
	}

	@Override
	public String toString() {
		String ret = "Disjoint sets as forest:\n";
		for (int i = 0; i < arr.length; i++)
			ret += i + " -> " + arr[i].parent + "\n";

		ret = ret.substring(0, ret.length() - 1);
		return ret;
	}
}
