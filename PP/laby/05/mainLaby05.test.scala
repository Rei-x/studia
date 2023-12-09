class Laby05 extends munit.FunSuite {
  test("skipTakeL") {
    val lazyList = LazyList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    assertEquals(
      skipTakeL(lazyList).take(10).toList,
      List(1, 3, 6, 10)
    )

    val infiniteLazyListSimple = LazyList.from(1)

    assertEquals(
      skipTakeL(infiniteLazyListSimple).take(10).toList,
      List(1, 3, 6, 10, 15, 21, 28, 36, 45, 55)
    )

    val infiniteLazyListCustomStep = LazyList.from(0, 2)

    assertEquals(
      skipTakeL(infiniteLazyListCustomStep).take(10).toList,
      List(0, 4, 10, 18, 28, 40, 54, 70, 88, 108)
    )
  }
}
