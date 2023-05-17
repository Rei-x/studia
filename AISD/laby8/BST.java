import java.util.NoSuchElementException;

public class BST<T extends Comparable<T>> {
	private class Node {
		T value;
		Node left, right, parent;

		public Node(T v) {
			value = v;
		}
	}

	private Node root = null;
	private int size = 0;

	public BST() {
	}

	public T getElement(T toFind) {
		Node curr = root;

		while (curr != null) {
			int cmp = toFind.compareTo(curr.value);

			if (cmp < 0) {
				curr = curr.left;
			} else if (cmp > 0) {
				curr = curr.right;
			} else {
				return curr.value;
			}
		}

		throw new NoSuchElementException();
	}

	public T successor(T elem) {
		Node node = findNode(elem);
		if (node == null)
			throw new NoSuchElementException();

		if (node.right != null) {
			Node next = node.right;
			while (next.left != null)
				next = next.left;
			return next.value;
		} else {
			Node parent = node.parent;
			Node current = node;
			while (parent != null && current == parent.right) {
				current = parent;
				parent = parent.parent;
			}
			return parent != null ? parent.value : null;
		}

	}

	public boolean add(T elem) {
		if (root == null) {
			root = new Node(elem);
			size++;
			return true;
		}

		Node parent = null;
		Node current = root;

		while (current != null) {
			parent = current;
			if (elem.compareTo(current.value) < 0) {
				current = current.left;
			} else if (elem.compareTo(current.value) > 0) {
				current = current.right;
			} else {
				return false;
			}
		}

		Node newNode = new Node(elem);
		newNode.parent = parent;

		if (elem.compareTo(parent.value) < 0)
			parent.left = newNode;
		else
			parent.right = newNode;
		size++;
		return true;

	}

	public T remove(T value) {
		Node node = findNode(value);
		if (node == null)
			return null;

		T oldValue = node.value;

		if (node.left != null && node.right != null) {
			Node successor = findMinimalNode(node.right);
			node.value = successor.value;
			node = successor;
		}

		Node pullUp = node.left != null ? node.left : node.right;

		if (pullUp != null) {
			pullUp.parent = node.parent;
			if (node.parent == null)
				root = pullUp;
			else if (node == node.parent.left)
				node.parent.left = pullUp;
			else
				node.parent.right = pullUp;
		} else if (node.parent == null) {
			root = null;
		} else {
			if (node == node.parent.left)
				node.parent.left = null;
			else
				node.parent.right = null;
		}

		size--;
		return oldValue;
	}

	private Node findMinimalNode(Node node) {
		while (node.left != null) {
			node = node.left;
		}
		return node;
	}

	private Node findNode(T value) {
		Node current = root;

		while (current != null) {
			int compareValue = value.compareTo(current.value);
			if (compareValue == 0) {
				return current;
			} else if (compareValue < 0) {
				current = current.left;
			} else {
				current = current.right;
			}
		}
		return null;
	}

	public void clear() {
		size = 0;
		root = null;
	}

	public int size() {
		return size;
	}

	public String toStringInOrder() {
		StringBuilder sb = new StringBuilder();
		inOrder(root, sb);
		if (sb.length() == 0)
			return " ";
		return sb.toString().trim().substring(0, sb.length() - 2);
	}

	public String toStringPreOrder() {
		StringBuilder sb = new StringBuilder();

		preOrder(root, sb);

		if (sb.length() == 0) {
			return " ";
		}

		return sb.toString().trim().substring(0, sb.length() - 2);
	}

	public String toStringPostOrder() {
		StringBuilder sb = new StringBuilder();

		postOrder(root, sb);

		if (sb.length() == 0) {
			return " ";
		}

		return sb.toString().trim().substring(0, sb.length() - 2);
	}

	private void inOrder(Node node, StringBuilder sb) {
		if (node == null) {
			return;
		}

		inOrder(node.left, sb);
		sb.append(node.value + ", ");
		inOrder(node.right, sb);
	}

	private void preOrder(Node node, StringBuilder sb) {
		if (node == null) {
			return;
		}

		sb.append(node.value + ", ");
		preOrder(node.left, sb);
		preOrder(node.right, sb);
	}

	private void postOrder(Node node, StringBuilder sb) {
		if (node == null) {
			return;
		}

		postOrder(node.left, sb);
		postOrder(node.right, sb);
		sb.append(node.value + ", ");
	}

	private int countLeafs(Node node) {
		if (node == null) {
			return 0;
		}
		if (node.left == null && node.right == null) {
			return 1;
		} else {
			return countLeafs(node.left) + countLeafs(node.right);
		}
	}

	public int leafsSize() {
		return countLeafs(root);
	}

}