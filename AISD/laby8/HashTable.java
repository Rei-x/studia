import java.util.LinkedList;

public class HashTable<E extends IWithName> {
	LinkedList<E> arr[]; // use pure array
	private final static int defaultInitSize = 8;
	private final static double defaultMaxLoadFactor = 0.7;
	private int size;
	private final double maxLoadFactor;

	public HashTable() {
		this(defaultInitSize);
	}

	public HashTable(int size) {
		this(size, defaultMaxLoadFactor);
	}

	@SuppressWarnings("unchecked")
	public HashTable(int initCapacity, double maxLF) {
		arr = new LinkedList[initCapacity];
		this.maxLoadFactor = maxLF;
	}

	public boolean add(E elem) {
		if (get(elem) != null)
			return false;

		if (elem == null)
			return false;

		if (((double) size + 1) / arr.length >= maxLoadFactor)
			doubleArray();

		int index = hash(elem.hashCode());
		if (arr[index] == null)
			arr[index] = new LinkedList<E>();

		arr[index].add(elem);
		size++;

		return true;
	}

	private int hash(int hashCode) {
		return hashCode % arr.length;
	}

	@SuppressWarnings("unchecked")
	private void doubleArray() {
		LinkedList<E> oldArr[] = arr;
		arr = new LinkedList[oldArr.length * 2];

		for (LinkedList<E> list : oldArr) {
			if (list != null) {
				for (E elem : list) {
					int index = hash(elem.hashCode());
					if (arr[index] == null)
						arr[index] = new LinkedList<E>();

					arr[index].add(elem);
				}
			}
		}
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		int i = 0;
		for (LinkedList<E> list : arr) {
			sb.append(i++ + ":");
			if (list != null) {
				sb.append(" ");
				for (E elem : list) {
					sb.append(elem.getName() + ", ");
				}

				sb.delete(sb.length() - 2, sb.length());
			}

			sb.append("\n");
		}

		return sb.toString();
	}

	public Object get(E toFind) {
		int index = hash(toFind.hashCode());
		if (arr[index] == null)
			return null;

		for (E elem : arr[index]) {
			if (elem.equals(toFind))
				return elem;
		}

		return null;
	}

}
