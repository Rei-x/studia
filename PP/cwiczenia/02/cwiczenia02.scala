import scala.compiletime.ops.boolean
def fib(n: Int): Int = {
  if (n == 0 || n == 1) then n
  else fib(n - 1) + fib(n - 2)
}

def fibTail(n: Int): Int = {
  def fibTailRec(n: Int, a: Int, b: Int): Int = {
    if (n == 0) then a
    else fibTailRec(n - 1, b, a + b)
  }
  fibTailRec(n, 0, 1)
}

// def root3(a: Double): Double = {
//   val accuracy = scala.math.pow(10, -15);
//   def root3Rec(x: Double, result: Double): Double = {

//   }
//   root3Rec(a, 0);
// }

def zwiazanie() = {
  val _ :: _ :: x :: _ = List(-2, -1, 0, 1, 2): @unchecked
  val l :: (y, _) :: g = List((1, 2), (0, 1)): @unchecked
}

def replaceNth[A](xs: List[A], n: Int, x: A): List[A] = {
  xs match {
    case head :: next if (n == 0) => x :: next
    case head :: next             => head :: replaceNth(next, n - 1, x)
    case Nil                      => Nil
  }
}

def isStartOfAnotherList[A](startList: List[A], endList: List[A]): Boolean = {
  (startList, endList) match {
    case (Nil, _) => true
    case (head1 :: next1, head2 :: next2) if (head1 == head2) =>
      isStartOfAnotherList(next1, next2)
    case _ => false
  }
}
