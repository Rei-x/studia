
import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public interface IList<E> extends Iterable<E> {
  boolean add(E e); // add element to the list on proper position

  void add(int index, E element) throws NoSuchElementException; // not implemented

  void clear(); // delete all elements

  boolean contains(E element); // is list containing an element (equals())

  E get(int index) throws NoSuchElementException; // get element from position

  E set(int index, E element) throws NoSuchElementException; // not implemented

  int indexOf(E element); // where is element (equals())

  boolean isEmpty();

  Iterator<E> iterator();

  ListIterator<E> listIterator() throws UnsupportedOperationException; // for ListIterator

  E remove(int index) throws NoSuchElementException; // remove element from position index

  boolean remove(E e); // remove element

  int size();
}
