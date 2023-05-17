
public class Link implements Comparable<Link> {
	public String ref;
	public int weight;

	public Link(String ref) {
		this.ref = ref;
		weight = 1;
	}

	public Link(String ref, int weight) {
		this.ref = ref;
		this.weight = weight;
	}

	@Override
	public boolean equals(Object obj) {
		return ((Link) obj).ref.equalsIgnoreCase(ref);
	}

	@Override
	public String toString() {
		return ref + "(" + weight + ")";
	}

	@Override
	public int compareTo(Link another) {
		return ref.compareTo(another.ref);
	}
}
