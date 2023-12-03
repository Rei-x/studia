sealed trait BT[+A]
case object Empty2 extends BT[Nothing]
case class Node2[+A](elem: A, left: BT[A], right: BT[A]) extends BT[A]

val tt = Node2(
  1,
  Node2(2, Node2(4, Empty2, Empty2), Empty2),
  Node2(3, Node2(5, Empty2, Node2(6, Empty2, Empty2)), Empty2)
)

def breadthBT[A](tree: BT[A]) = {
  def breadthBTAux(list: List[BT[A]]): List[A] = list match {
    case List()         => List()
    case Empty2 :: tail => breadthBTAux(tail)
    case Node2(value, left, right) :: tail =>
      value :: breadthBTAux(tail ::: List(left, right))
  }
  breadthBTAux(List(tree))
}

def internalBT[A](tree: BT[A]) = {
  def internalBTAux(internalTree: BT[A], acc: Int): Int = internalTree match {
    case Empty2                       => 0
    case Node2(value, Empty2, Empty2) => acc
    case Node2(value, left, Empty2)   => acc + internalBTAux(left, acc + 1)
    case Node2(value, Empty2, right)  => acc + internalBTAux(right, acc + 1)
    case Node2(value, left, right) =>
      acc + internalBTAux(left, acc + 1) + internalBTAux(right, acc + 1)
  }

  internalBTAux(tree, 0)
}

def externalBT[A](tree: BT[A]) = {
  def externalBTAux(internalTree: BT[A], acc: Int): Int = internalTree match {
    case Empty2                       => acc
    case Node2(value, Empty2, Empty2) => 2 * (acc + 1)
    case Node2(value, left, Empty2)   => acc + 1 + externalBTAux(left, acc + 1)
    case Node2(value, Empty2, right)  => acc + 1 + externalBTAux(right, acc + 1)
    case Node2(value, left, right) =>
      externalBTAux(left, acc + 1) + externalBTAux(right, acc + 1)
  }

  externalBTAux(tree, 0)
}

sealed trait Graphs[A]
case class Graph[A](succ: A => List[A]) extends Graphs[A]

def depthSearch[A](graph: Graph[A])(startNode: A) = {
  def depthSearchAUX(visited: List[A])(toVisit: List[A]): List[A] =
    toVisit match {
      case List() => List()
      case head :: tail if (visited contains head) =>
        depthSearchAUX(visited)(tail)
      case head :: tail =>
        head :: depthSearchAUX(head :: visited)((graph succ head) ::: tail)
    }

  depthSearchAUX(List())(List(startNode))
}
