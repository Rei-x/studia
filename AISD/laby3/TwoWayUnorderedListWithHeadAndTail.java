import java.util.Iterator;
import java.util.ListIterator;
import java.util.NoSuchElementException;

public class TwoWayUnorderedListWithHeadAndTail<E> implements IList<E> {

	private class Element {
		public Element(E e) {
			object = e;
		}

		E object;
		Element next = null;
		Element prev = null;
	}

	Element head;
	Element tail;
	int size;

	private class InnerIterator implements Iterator<E> {
		Element pos;

		public InnerIterator() {
			pos = head;
		}

		@Override
		public boolean hasNext() {
			return pos != null;
		}

		@Override
		public E next() {
			if (pos == null)
				throw new NoSuchElementException();
			E e = pos.object;
			pos = pos.next;
			return e;
		}
	}

	private class InnerListIterator implements ListIterator<E> {
		Element nextElement;
		Element previousElement;
		int index;

		public InnerListIterator() {
			nextElement = head;
			previousElement = null;

			index = 0;
		}

		@Override
		public void add(E e) {

		}

		@Override
		public boolean hasNext() {
			return nextElement != null;
		}

		@Override
		public boolean hasPrevious() {
			return previousElement != null;
		}

		@Override
		public E next() {
			if (nextElement == null)
				throw new NoSuchElementException();

			E holder = nextElement.object;
			previousElement = nextElement;
			nextElement = nextElement.next;

			index++;
			return holder;
		}

		@Override
		public int nextIndex() {
			return index + 1;
		}

		@Override
		public E previous() {
			if (previousElement == null)
				throw new NoSuchElementException();

			E holder = previousElement.object;
			nextElement = previousElement;
			previousElement = previousElement.prev;

			index--;
			return holder;
		}

		@Override
		public int previousIndex() {
			return index - 1;
		}

		@Override
		public void remove() {
		}

		@Override
		public void set(E e) {

		}
	}

	public TwoWayUnorderedListWithHeadAndTail() {
		// make a head and a tail
		head = null;
		tail = null;
		size = 0;
	}

	@Override
	public boolean add(E e) {
		Element newElement = new Element(e);

		if (head == null) {
			head = newElement;
			tail = newElement;
		} else {
			tail.next = newElement;
			newElement.prev = tail;
			tail = newElement;
		}

		size++;

		return true;
	}

	@Override
	public void add(int index, E element) {
		if (index < 0 || index > size)
			throw new NoSuchElementException();

		Element newElement = new Element(element);

		if (index == 0) {
			if (head == null) {
				head = newElement;
				tail = newElement;
			} else {
				newElement.next = head;
				head.prev = newElement;
				head = newElement;
			}
		} else if (index == size) {
			tail.next = newElement;
			newElement.prev = tail;
			tail = newElement;
		} else {
			Element pos = head;
			for (int i = 0; i < index; i++) {
				pos = pos.next;
			}
			newElement.next = pos;
			newElement.prev = pos.prev;
			pos.prev.next = newElement;
			pos.prev = newElement;
		}

		size++;
	}

	@Override
	public void clear() {
		head = null;
		tail = null;
		size = 0;
	}

	@Override
	public boolean contains(E element) {
		for (E e : this) {
			if (e.equals(element))
				return true;
		}
		return false;
	}

	@Override
	public E get(int index) {
		if (index < 0 || index >= size)
			throw new NoSuchElementException();

		Element pos = head;
		for (int i = 0; i < index; i++) {
			pos = pos.next;
		}
		return pos.object;
	}

	@Override
	public E set(int index, E element) {
		if (index < 0 || index > size)
			throw new NoSuchElementException();

		Element currentElement = head;

		for (int i = 0; i < index; i++) {
			currentElement = currentElement.next;
		}

		E objectToReturn = currentElement.object;
		currentElement.object = element;
		return objectToReturn;
	}

	@Override
	public int indexOf(E element) {
		int index = 0;
		for (E e : this) {
			if (e.equals(element))
				return index;
			index++;
		}
		return -1;
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
		throw new UnsupportedOperationException();
	}

	@Override
	public E remove(int index) {
		if (index < 0 || index >= size)
			throw new NoSuchElementException();

		if (index == 0) {
			E ret = head.object;
			head = head.next;
			head.prev = null;
			size--;
			return ret;
		}

		Element currentElement = head;

		for (int i = 0; i < index - 1; i++) {
			currentElement = currentElement.next;
		}

		E objectToReturn = currentElement.next.object;

		currentElement.next = currentElement.next.next;

		if (currentElement.next != null)
			currentElement.next.prev = currentElement;

		size--;

		return objectToReturn;
	}

	@Override
	public boolean remove(E e) {
		if (head == null)
			return false;

		Element pos = head;

		while (pos != null) {
			if (pos.object.equals(e)) {
				if (pos.prev != null)
					pos.prev.next = pos.next;
				if (pos.next != null)
					pos.next.prev = pos.prev;

				if (pos == head)
					head = pos.next;

				if (pos == tail)
					tail = pos.prev;

				size--;
				return true;
			}
			pos = pos.next;
		}

		return false;
	}

	@Override
	public int size() {
		return size;
	}

	public String toStringReverse() {
		ListIterator<E> iter = new InnerListIterator();
		while (iter.hasNext())
			iter.next();
		String retStr = "";

		while (iter.hasPrevious()) {
			retStr += "\n" + iter.previous();
		}

		return retStr;
	}

	public void add(TwoWayUnorderedListWithHeadAndTail<E> other) {
		if (other == this)
			return;

		if (other.head != null) {
			if (head == null) {
				head = other.head;
				tail = other.tail;
			} else {
				tail.next = other.head;
				other.head.prev = tail;
				tail = other.tail;
			}
			size += other.size;
		}

		other.clear();
	}
}
