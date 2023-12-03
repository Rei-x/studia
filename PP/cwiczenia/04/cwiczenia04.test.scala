class Cwiczenia04 extends munit.FunSuite {
  test("breadthBT") {
    val tt = Node2(
      1,
      Node2(2, Node2(4, Empty2, Empty2), Empty2),
      Node2(3, Node2(5, Empty2, Node2(6, Empty2, Empty2)), Empty2)
    )

    assertEquals(breadthBT(tt), List(1, 2, 3, 4, 5, 6))
  }

  test("internalBT") {
    val tt = Node2(
      1,
      Node2(2, Node2(4, Empty2, Empty2), Empty2),
      Node2(3, Node2(5, Empty2, Node2(6, Empty2, Empty2)), Empty2)
    )

    assertEquals(internalBT(tt), 9)
  }

  test("externalBT") {
    val tt = Node2(
      1,
      Node2(2, Node2(4, Empty2, Empty2), Empty2),
      Node2(3, Node2(5, Empty2, Node2(6, Empty2, Empty2)), Empty2)
    )

    assertEquals(externalBT(tt), 21)
  }

  test("depthSearch") {
    val graph = Graph((i: Int) =>
      i match {
        case 1 => List(2, 3)
        case 2 => List(4)
        case 3 => List(5, 6)
        case 4 => List(7)
        case 5 => List(8)
        case 6 => List(9)
        case _ => Nil
      }
    )

    assertEquals(depthSearch(graph)(1), List(1, 2, 4, 7, 3, 5, 8, 6, 9))
  }

}
