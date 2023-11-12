def prime(n: Int): List[Int] = {
  if (n < 2) List()
  else
    for (
      x <- List.range(2, n + 1);
      if (for (
        y <- List.range(2, scala.math.sqrt(x).toInt + 1); if (x % y == 0)
      )
        yield y) == List()
    ) yield x
}
