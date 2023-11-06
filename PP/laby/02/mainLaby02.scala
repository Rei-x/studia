import scala.annotation.tailrec
def cutAndMend[T](a: Int, b: Int)(list: List[T]) = {
  def cutAndAmendAux(
      xs: List[T],
      current: Int
  ): List[T] = {
    (xs, current) match
      case (x :: xs, index) if index >= a && index <= b =>
        cutAndAmendAux(xs, current + 1)
      case (x :: xs, _) =>
        x :: cutAndAmendAux(xs, current + 1)
      case (Nil, _) => Nil

  }
  cutAndAmendAux(list, 0)
}

def split2Rec[A](a: List[A]): (List[A], List[A]) = {
  a match {
    case head :: head2 :: next => {
      val (list1, list2) = split2Rec(next)

      (head :: list1, head2 :: list2)
    }
    case _ => (List(), List())
  }
}

def split2Tail[A](a: List[A]): (List[A], List[A]) = {
  @tailrec
  def split2Aux(a: List[A], acc: (List[A], List[A])): (List[A], List[A]) = {
    a match {
      case head :: head2 :: next => {
        split2Aux(next, (head :: acc._1, head2 :: acc._2))
      }
      case _ => acc
    }
  }
  split2Aux(a, (List(), List()))
}

// substituteIfIn([1;2;3;4;5]) ([2;4], 0) = [1;0;3;0;5]
def substituteIfIn[A](a: List[A])(b: List[A], elementToReplace: A) = {

  def includes(a: List[A], element: A): Boolean = {
    a match {
      case head :: next => {
        if (head == element) true
        else includes(next, element)
      }
      case _ => false
    }
  }

  def substituteIfInAux(a: List[A], b: List[A]): List[A] = {
    a match {
      case head :: next => {
        if (includes(b, head))
          elementToReplace :: substituteIfInAux(next, b)
        else head :: substituteIfInAux(next, b)
      }
      case _ => Nil
    }
  }

  substituteIfInAux(a, b)

}
