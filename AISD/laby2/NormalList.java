import java.util.ArrayList;
import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public class NormalList<E> implements IList<E> {
  private ArrayList<E> list;

  public NormalList() {
    list = new ArrayList<E>();
  }

  @Override
  public boolean add(E e) {
    return list.add(e);
  }

  @Override
  public void add(int index, E element) throws NoSuchElementException {
    list.add(index, element);
  }

  @Override
  public void clear() {
    list.clear();
  }

  @Override
  public boolean contains(E element) {
    return list.contains(element);
  }

  @Override
  public E get(int index) throws NoSuchElementException {
    return list.get(index);
  }

  @Override
  public E set(int index, E element) throws NoSuchElementException {
    return list.set(index, element);
  }

  @Override
  public int indexOf(E element) {
    return list.indexOf(element);
  }

  @Override
  public boolean isEmpty() {
    return list.isEmpty();
  }

  @Override
  public Iterator<E> iterator() {
    return list.iterator();
  }

  @Override
  public ListIterator<E> listIterator() throws UnsupportedOperationException {
    throw new UnsupportedOperationException("Not implemented");
  }

  @Override
  public E remove(int index) throws NoSuchElementException {
    return list.remove(index);
  }

  @Override
  public boolean remove(E e) {
    return list.remove(e);
  }

  @Override
  public int size() {
    return list.size();
  }

}
