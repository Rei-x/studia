class Laby02 extends munit.FunSuite {
  test("reverse") {
    val cutAndMend15 = cutAndMend(1, 5)
    assertEquals(cutAndMend15(Range(1, 100).toList), 1 :: Range(7, 100).toList)
    assertEquals(cutAndMend15(List()), List())
    val cutAndMendLOL = cutAndMend(-10, 0)
    assertEquals(cutAndMendLOL(List("1", "2", "3")), List("2", "3"))
  }

  test("split2Rec") {
    val firstSplit = split2Rec(List("1", "2", "3", "4"))
    assertEquals(firstSplit._1.length, firstSplit._2.length)
    assertEquals(firstSplit._1.length, 2)
    val secondSplit = split2Rec(List("1", "2", "3"))
    assertEquals(secondSplit._1.length, secondSplit._2.length)
    assertEquals(secondSplit._1.length, 1)
    val thirdSplit = split2Rec(Range(0, 1001).toList)
    assertEquals(thirdSplit._1.length, thirdSplit._2.length)
    assertEquals(thirdSplit._1.length, 500)
    val fourthSplit = split2Rec(List())
    assertEquals(fourthSplit._1.length, fourthSplit._2.length)
    assertEquals(fourthSplit._1.length, 0)

  }

  test("split2Tail") {
    val firstSplit = split2Tail(List("1", "2", "3", "4"))
    assertEquals(firstSplit._1.length, firstSplit._2.length)
    assertEquals(firstSplit._1.length, 2)
    val secondSplit = split2Tail(List("1", "2", "3"))
    assertEquals(secondSplit._1.length, secondSplit._2.length)
    assertEquals(secondSplit._1.length, 1)
    val thirdSplit = split2Tail(Range(0, 1001).toList)
    assertEquals(thirdSplit._1.length, thirdSplit._2.length)
    assertEquals(thirdSplit._1.length, 500)
    val fourthSplit = split2Tail(List())
    assertEquals(fourthSplit._1.length, fourthSplit._2.length)
  }

  test("substitue") {

    assertEquals(
      substituteIfIn(List(1, 2, 3, 4, 5))(List(2, 4), 0),
      List(1, 0, 3, 0, 5)
    )

    assertEquals(
      substituteIfIn(List(1, 2, 3, 4, 5))(List(4, 5), 0),
      List(1, 2, 3, 0, 0)
    )

    val substitueFrom2 = substituteIfIn(List("mario", "luigi", "pean"));
    assertEquals(
      substitueFrom2(List("luigi"), "bartek"),
      List("mario", "bartek", "pean")
    )

  }

}
