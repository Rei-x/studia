import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public interface IList<E> extends Iterable<E> {
  boolean add(E e); // qdd element to the end of list

  void add(int index, E element) throws NoSuchElementException; // add element on position index

  void clear(); // delete all elements

  boolean contains(E element); // is list containing an element (equals())

  E get(int index) throws NoSuchElementException; // get element from position

  E set(int index, E element) throws NoSuchElementException; // set new value on position

  int indexOf(E element); // where is element (equals())

  boolean isEmpty();

  Iterator<E> iterator();

  ListIterator<E> listIterator() throws UnsupportedOperationException; // for ListIterator

  E remove(int index) throws NoSuchElementException; // remove element from position index

  boolean remove(E e); // remove element

  int size();
}
