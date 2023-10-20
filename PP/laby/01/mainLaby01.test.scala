class Laby01 extends munit.FunSuite {
  test("reverse") {
    assertEquals(reverse((1, "mario", 3, List(1))), (List(1), 3, "mario", 1))
  }

  test("sumProd") {
    assertEquals(sumProd(2, 6), (14, 120))
    assertEquals(sumProd(-6, 4), (-15, 0))
  }

  test("isPerfect") {
    assert(isPerfect(6))
    assert(!isPerfect(5))
    assert(!isPerfect(2))
    assert(isPerfect(28))
  }

  test("insert") {
    assertEquals(insert(List(1, 3, 4, 5), 2, 1), List(1, 2, 3, 4, 5))
    assertEquals(insert(List(1, 2, 4, 5), 3, 2), List(1, 2, 3, 4, 5))
    assertEquals(insert(List(1, 2, 3, 4), 5, 999), List(1, 2, 3, 4, 5))
  }
}
