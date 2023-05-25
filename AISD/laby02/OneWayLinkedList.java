import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public class OneWayLinkedList<E> implements IList<E> {

  private class Element {
    public Element(E e) {
      this.object = e;
    }

    E object;
    Element next = null;
  }

  Element sentinel;
  int size;

  private class InnerIterator implements Iterator<E> {
    Element current;

    public InnerIterator() {
      current = sentinel;
    }

    @Override
    public boolean hasNext() {
      return current.next != null;
    }

    @Override
    public E next() {
      current = current.next;
      return current.object;
    }
  }

  public OneWayLinkedList() {
    sentinel = new Element(null);
    size = 0;
  }

  @Override
  public Iterator<E> iterator() {
    return new InnerIterator();
  }

  @Override
  public ListIterator<E> listIterator() {
    throw new UnsupportedOperationException();
  }

  @Override
  public boolean add(E e) {
    Element holder = sentinel;

    while (holder.next != null) {
      holder = holder.next;
    }

    holder.next = new Element(e);
    size++;

    return true;
  }

  @Override
  public void add(int index, E element) throws NoSuchElementException {
    if (index > size() || index < 0) {
      throw new NoSuchElementException("Wrong index");
    }
    Element newElement = new Element(element);
    Element current = sentinel;

    for (int i = 0; i < index; i++) {
      current = current.next;
    }
    newElement.next = current.next;
    current.next = newElement;
    size++;
  }

  @Override
  public void clear() {
    sentinel.next = null;
    size = 0;
  }

  @Override
  public boolean contains(E element) {
    return indexOf(element) != -1;
  }

  @Override
  public E get(int index) throws NoSuchElementException {
    if (index > size() || index < 0) {
      throw new NoSuchElementException();
    }

    Element current = sentinel.next;

    while (index > 0 && current != null) {
      current = current.next;
      index--;
    }

    if (current == null) {
      throw new NoSuchElementException();
    }

    return current.object;
  }

  @Override
  public E set(int index, E element) throws NoSuchElementException {
    Element sentinel = this.sentinel;
    while (index > 0 && sentinel != null) {
      sentinel = sentinel.next;
      index--;
    }

    if (sentinel == null) {
      throw new NoSuchElementException();
    }

    Element holder = sentinel.next;
    sentinel.next = new Element(element);
    sentinel.next.next = holder.next;

    return holder.object;
  }

  @Override
  public int indexOf(E element) {
    int index = 0;
    Element sentinel = this.sentinel;
    while (sentinel.next != null) {
      if (sentinel.next.object.equals(element)) {
        return index;
      }
      sentinel = sentinel.next;
      index++;
    }

    return -1;
  }

  @Override
  public boolean isEmpty() {
    return sentinel.next == null;
  }

  @Override
  public E remove(int index) throws NoSuchElementException {
    Element sentinel = this.sentinel;

    if (index >= this.size() || index < 0) {
      throw new NoSuchElementException();
    }

    while (index > 0) {
      sentinel = sentinel.next;
      index--;
    }

    E holder = sentinel.next.object;
    if (sentinel.next != null) {
      sentinel.next = sentinel.next.next;
    } else {
      sentinel = null;
    }

    size--;

    return holder;
  }

  @Override
  public boolean remove(E e) {
    Element sentinel = this.sentinel;

    while (sentinel.next != null) {
      if (sentinel.next.object.equals(e)) {
        sentinel.next = sentinel.next.next;
        size--;
        return true;
      }
      sentinel = sentinel.next;
    }

    return false;
  }

  @Override
  public int size() {
    return size;
  }

  public void removeEven() {
    Element current = this.sentinel;

    while (current != null && current.next != null) {
      current.next = current.next.next;
      current = current.next;
      size--;
    }
  }

}
