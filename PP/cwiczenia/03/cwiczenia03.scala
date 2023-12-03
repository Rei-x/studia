def curry3[A, B, C, D](f: (A, B, C) => D): A => B => C => D = { a => b => c =>
  f(a, b, c)
}

def uncurry3[A, B, C, D](f: A => B => C => D): (A, B, C) => D = { (a, b, c) =>
  f(a)(b)(c)
}

def sumProd(xs: List[Int]): (Int, Int) = {
  xs.foldLeft(0, 1)((accumulator, h) =>
    (accumulator._1 + h, accumulator._2 * h)
  )
}
