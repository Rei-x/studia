package dsaa.lab07;

import java.util.Iterator;
import java.util.ListIterator;

public class TwoWayCycledOrderedListWithSentinel<E> implements IList<E>{

	private class Element{
		public Element(E e) {
			//TODO
		}
		public Element(E e, Element next, Element prev) {
			//TODO
		}
		// add element e after this
		public void addAfter(Element elem) {
			//TODO
		}
		// assert it is NOT a sentinel
		public void remove() {
			//TODO
		}
		E object;
		Element next=null;
		Element prev=null;
	}


	Element sentinel;
	int size;

	private class InnerIterator implements Iterator<E>{
		//TODO
		public InnerIterator() {
			//TODO
		}
		@Override
		public boolean hasNext() {
			//TODO
			return false;
		}

		@Override
		public E next() {
			//TODO
			return null;
		}
	}

	private class InnerListIterator implements ListIterator<E>{
		//TODO
		public InnerListIterator() {
			//TODO
		}
		@Override
		public boolean hasNext() {
			//TODO
			return false;
		}

		@Override
		public E next() {
			//TODO
			return null;
		}
		@Override
		public void add(E arg0) {
			throw new UnsupportedOperationException();
		}
		@Override
		public boolean hasPrevious() {
			//TODO
			return false;
		}
		@Override
		public int nextIndex() {
			throw new UnsupportedOperationException();
		}
		@Override
		public E previous() {
			//TODO
			return null;
		}
		@Override
		public int previousIndex() {
			throw new UnsupportedOperationException();
		}
		@Override
		public void remove() {
			throw new UnsupportedOperationException();
		}
		@Override
		public void set(E arg0) {
			throw new UnsupportedOperationException();
		}
	}
	public TwoWayCycledOrderedListWithSentinel() {
		//TODO
	}

	//@SuppressWarnings("unchecked")
	@Override
	public boolean add(E e) {
		//TODO
		return false;
	}

	private Element getElement(int index) {
		//TODO
		return null;
	}

	private Element getElement(E obj) {
		//TODO
		return null;
	}

	@Override
	public void add(int index, E element) {
		throw new UnsupportedOperationException();

	}

	@Override
	public void clear() {
		//TODO
	}

	@Override
	public boolean contains(E element) {
		//TODO
		return false;
	}

	@Override
	public E get(int index) {
		//TODO
		return null;
	}

	@Override
	public E set(int index, E element) {
		throw new UnsupportedOperationException();
	}

	@Override
	public int indexOf(E element) {
		//TODO
		return -1;
	}

	@Override
	public boolean isEmpty() {
		//TODO
		return true;
	}

	@Override
	public Iterator<E> iterator() {
		return new InnerIterator();
	}

	@Override
	public ListIterator<E> listIterator() {
		return new InnerListIterator();
	}

	@Override
	public E remove(int index) {
		//TODO
		return null;
	}

	@Override
	public boolean remove(E e) {
		//TODO
		return false;
	}

	@Override
	public int size() {
		//TODO
		return -1;
	}

	//@SuppressWarnings("unchecked")
	public void add(TwoWayCycledOrderedListWithSentinel<E> other) {
		//TODO
	}
	
	//@SuppressWarnings({ "unchecked", "rawtypes" })
	public void removeAll(E e) {
		//TODO
	}

}

