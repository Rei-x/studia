def flatten1[A](xss: List[List[A]]): List[A] = {
  if (xss.length == 0) then List() else xss.head ++: flatten1(xss.tail)
}

def count[A](x: A, xs: List[A]): Int = {
  if (xs.length == 0) then 0
  else ((if xs.head == x then 1 else 0) + count(x, xs.tail))
}

def replicate[A](x: A, n: Int): List[A] = {
  if (n < 0) then throw new RuntimeException("n cannot be negative")
  else if (n == 0) then List()
  else x +: replicate(x, n - 1)
}

val sqrList: List[Int] => List[Int] = (xs) => {
  if (xs.length) == 0 then List()
  else scala.math.pow(xs.head, 2).toInt +: sqrList(xs.tail)
}

def palindrome[A](xs: List[A]): Boolean = {
  if (xs.length == 0 || xs.length == 1) then true
  else xs.head == xs.last && palindrome(xs.drop(1).dropRight(1))
}

def listLength[A](xs: List[A]): Int = {
  if (xs.isEmpty) then 0 else 1 + listLength(xs.tail)
}
