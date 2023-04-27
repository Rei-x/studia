package dsaa.lab07;

public class Link implements Comparable<Link>{
	public String ref;
	public int weight;
	public Link(String ref) {
		this.ref=ref;
		weight=1;
	}
	public Link(String ref, int weight) {
		this.ref=ref;
		this.weight=weight;
	}
	@Override
	public boolean equals(Object obj) {
		//TODO
		return false;
	}
	@Override
	public String toString() {
		return ref+"("+weight+")";
	}
	@Override
	public int compareTo(Link another) {
		//TODO
		return 0;
	}
}
