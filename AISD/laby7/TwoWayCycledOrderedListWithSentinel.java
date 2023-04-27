
import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public class TwoWayCycledOrderedListWithSentinel<E extends Comparable<E>> implements IList<E> {

	private class Element {
		public Element(E e) {
			object = e;
		}

		public void addAfter(Element newNext) {
			Element previousNext = next;
			next = newNext;
			newNext.prev = this;
			newNext.next = previousNext;
			previousNext.prev = newNext;
		}

		public void remove() {
			if (this == sentinel)
				throw new NoSuchElementException();

			size--;
			prev.next = next;
			next.prev = prev;
		}

		E object;
		Element next = null;
		Element prev = null;
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
			return current.next != sentinel;
		}

		@Override
		public E next() {
			current = current.next;
			return current.object;
		}
	}

	private class InnerListIterator implements ListIterator<E> {
		Element current;

		public InnerListIterator() {
			current = sentinel;
		}

		@Override
		public boolean hasNext() {
			return current.next != sentinel;
		}

		@Override
		public E next() {
			current = current.next;
			return current.object;
		}

		@Override
		public void add(E arg0) {
			throw new UnsupportedOperationException();
		}

		@Override
		public boolean hasPrevious() {
			return current != sentinel;
		}

		@Override
		public int nextIndex() {
			throw new UnsupportedOperationException();
		}

		@Override
		public E previous() {
			E result = current.object;
			current = current.prev;

			return result;
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
		clear();
	}

	@Override
	public boolean add(E e) {
		Element current = sentinel;

		while (current.next != sentinel && current.next.object.compareTo(e) <= 0) {
			current = current.next;
		}

		Element elem = new Element(e);
		current.addAfter(elem);
		size++;

		return true;
	}

	private Element getElement(int index) {
		if (index < 0 || index >= size)
			throw new NoSuchElementException();

		Element current = sentinel.next;

		for (int i = 0; i < index; i++) {
			current = current.next;
		}

		return current;
	}

	private Element getElement(E obj) {
		Element current = sentinel.next;

		while (current != sentinel && !current.object.equals(obj)) {
			current = current.next;
		}

		if (current == sentinel)
			throw new NoSuchElementException();

		return current;
	}

	@Override
	public void add(int index, E element) {
		throw new UnsupportedOperationException();
	}

	@Override
	public void clear() {
		this.sentinel = new Element(null);
		this.sentinel.next = this.sentinel;
		this.sentinel.prev = this.sentinel;
		size = 0;
	}

	@Override
	public boolean contains(E element) {
		try {
			getElement(element);
			return true;
		} catch (NoSuchElementException e) {
			return false;
		}
	}

	@Override
	public E get(int index) {
		return getElement(index).object;
	}

	@Override
	public E set(int index, E element) {
		throw new UnsupportedOperationException();
	}

	@Override
	public int indexOf(E element) {
		Element current = sentinel.next;
		int index = 0;

		while (current != sentinel && !current.object.equals(element)) {
			current = current.next;
			index++;
		}

		if (current == sentinel)
			return -1;

		return index;
	}

	@Override
	public boolean isEmpty() {
		return size == 0;
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
		Element current = getElement(index);
		E result = current.object;

		current.remove();

		return result;
	}

	@Override
	public boolean remove(E e) {
		try {
			Element current = getElement(e);
			current.remove();
			return true;
		} catch (NoSuchElementException ex) {
			return false;
		}
	}

	@Override
	public int size() {
		return size;
	}

	public void add(TwoWayCycledOrderedListWithSentinel<E> other) {
		if (other == null || other.size() == 0 || other == this) {
			return;
		}

		Element current = sentinel;

		if (current.next == sentinel) {
			sentinel.prev = other.sentinel.prev;
			sentinel.next = other.sentinel.next;
			size = other.size;
			other.clear();
			return;
		}

		Element otherElement = other.sentinel.next;

		for (int i = 0; i < other.size(); i++) {
			while (current.next != sentinel && current.next.object.compareTo(otherElement.object) <= 0) {
				current = current.next;
			}
			Element previousNext = otherElement.next;

			current.addAfter(otherElement);

			current = current.next;
			otherElement = previousNext;
			size++;
		}
		other.clear();
	}

	public void removeAll(E e) {
		Element current = sentinel;

		while (current.next != sentinel) {
			if (current.next.object.equals(e)) {
				current.next.remove();
			} else {
				current = current.next;
			}
		}
	}

	public void removeEven() {
		Element current = sentinel;

		while (current.next != sentinel) {
			if (current.next.object.hashCode() % 2 == 0) {
				current.next.remove();
			} else {
				current = current.next;
			}
		}
	}

}
