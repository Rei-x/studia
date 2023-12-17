class Laby06 extends munit.FunSuite {
  test("imperacci and declaracci") {
    assertEquals(fibonacci(10), 55)
    assertEquals(
      declaracci(1, 10),
      List(1, 2, 5, 13, 34, 89, 233, 610, 1597, 4181)
    )
    assertEquals(
      declaracci(2, 10),
      List(
        1, 3, 8, 21, 55, 144, 377, 987, 2584, 6765
      )
    )

    assertEquals(
      imperacci(1, 10).toList,
      Array(1, 2, 5, 13, 34, 89, 233, 610, 1597, 4181).toList
    )

    assertEquals(
      imperacci(2, 10).toList,
      List(
        1, 3, 8, 21, 55, 144, 377, 987, 2584, 6765
      )
    )

    assertEquals(
      imperacci(5, 3).toList,
      declaracci(5, 3)
    )

    assertEquals(
      imperacci(1, 1).toList,
      declaracci(1, 1)
    )

    assertEquals(
      imperacci(2, 1).toList,
      declaracci(2, 1)
    )

  }
}
