public class DisjointSetLinkedList implements DisjointSetDataStructure {

	private class Element {
		int representant;
		int next;
		int length;
		int last;
	}

	private static final int NULL = -1;

	Element arr[];

	public DisjointSetLinkedList(int size) {
		arr = new Element[size];
		for (int i = 0; i < size; i++) {
			arr[i] = new Element();
			arr[i].representant = i;
			arr[i].next = NULL;
			arr[i].length = 1;
			arr[i].last = i;
		}
	}

	@Override
	public void makeSet(int item) {
		arr[item].representant = item;
		arr[item].next = NULL;
		arr[item].length = 1;
		arr[item].last = item;
	}

	@Override
	public int findSet(int item) {
		return arr[item].representant;
	}

	@Override
	public boolean union(int itemA, int itemB) {
		int rootA = findSet(itemA);
		int rootB = findSet(itemB);
		if (rootA == rootB)
			return false;
		if (arr[rootA].length > arr[rootB].length) {
			arr[rootA].length += arr[rootB].length;
			arr[rootA].last = arr[rootB].last;
			arr[rootB].representant = rootA;
			arr[rootB].next = rootA;
		} else {
			arr[rootB].length += arr[rootA].length;
			arr[rootB].last = arr[rootA].last;
			arr[rootA].representant = rootB;
			arr[rootA].next = rootB;
		}
		return true;
	}

	@Override
	public String toString() {
		String ret = "";
		for (int i = 0; i < arr.length; i++)
			ret += i + " -> " + arr[i].representant + "\n";
		return ret;
	}

}
