def reverse[A, B, C, D](tuple: (A, B, C, D)) =
  (tuple._4, tuple._3, tuple._2, tuple._1)

def sumProd(lowerBound: Int, upperBound: Int): (Int, Int) = {
  if (lowerBound >= upperBound) then (0, 1)
  else {
    val (sum, prod) = sumProd(lowerBound + 1, upperBound)
    (sum + lowerBound, prod * lowerBound)
  }
}

def sumDivisors(checkedNumber: Int, currentNumber: Int): Int = {
  if (currentNumber == 0) then 0
  else if checkedNumber % currentNumber == 0 then
    currentNumber + sumDivisors(checkedNumber, currentNumber - 1)
  else sumDivisors(checkedNumber, currentNumber - 1)
}

def isPerfect(n: Int) = {
  if (n <= 1) then false
  else sumDivisors(n, n / 2 + 1) == n
}

def insert[A](list: List[A], element: A, index: Int): List[A] = {
  if (list == Nil) then List(element)
  else if (index == 0) then element :: list
  else list.head :: insert(list.tail, element, index - 1)
}

def argmax(xs: List[Int]): List[Int] = {
  def findmax(
      xs: List[Int],
      currentMax: Int,
      currentIndex: Int
  ): (List[Int], Int) = {
    if (xs == List()) then (List(), currentMax)
    else {
      val (indexes, max) = findmax(xs.tail, currentMax, currentIndex + 1)
      if (xs.head > max) then (List(currentIndex), xs.head)
      else if (xs.head == max) then (currentIndex :: indexes, max)
      else (indexes, max)
    }
  }
  if (xs == List()) then List() else findmax(xs, xs.head, 0)._1
}
