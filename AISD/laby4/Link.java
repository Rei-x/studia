
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
    if (obj instanceof Link) {
      return ref.equals(((Link) obj).ref);
    }
    return false;
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
