def fibonacci(n: Int): Int = {
  if (n == 1) 1
  else if (n == 2) 1
  else fibonacci(n - 1) + fibonacci(n - 2)
}
def declaracci(n: Int, m: Int): List[Int] = {
  def declaracciAux(n: Int, m: Int): Int = {
    if (m == 1) fibonacci(n)
    else declaracciAux(n, m - 1) + declaracciAux(n + 1, m - 1)
  }

  List.range(1, m + 1).map((i) => declaracciAux(n, i))
}

def fibonacciImperative(n: Int): Int = {
  var firstFib = 1
  var secondFib = 1
  var i = 2
  while (i < n) {
    val newFib = firstFib + secondFib
    firstFib = secondFib
    secondFib = newFib
    i += 1
  }
  return secondFib
}

def imperacci(n: Int, m: Int): Array[Int] = {
  var result = Array.ofDim[Int](m);

  var helperIndex = 0

  var currentResultIndex = 0
  while (currentResultIndex < m) {
    if (helperIndex % 2 == 1) {
      result(currentResultIndex) = fibonacciImperative(helperIndex + n - 1);
      currentResultIndex += 1
    }
    helperIndex += 1
  }

  result
}
