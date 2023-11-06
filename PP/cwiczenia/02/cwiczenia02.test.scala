class Cwiczenia02 extends munit.FunSuite {
  test("fib") {
    fib(42)
  }

  test("fibTail") {
    fibTail(42)
  }

  test("replaceNth") {
    assertEquals(replaceNth(List(1, 2, 3, 4), 2, 0), List(1, 2, 0, 4))
  }

}
