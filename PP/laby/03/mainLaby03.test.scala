class Laby03 extends munit.FunSuite {
  test("prime") {
    assertEquals(prime(1), List());
    assertEquals(prime(2), List(2));
    assertEquals(prime(3), List(2, 3));
    assertEquals(prime(10), List(2, 3, 5, 7));
    assertEquals(prime(20), List(2, 3, 5, 7, 11, 13, 17, 19));
    assertEquals(prime(30), List(2, 3, 5, 7, 11, 13, 17, 19, 23, 29));
    assertEquals(prime(40), List(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37));
    assertEquals(
      prime(50),
      List(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
    );
    assertEquals(
      prime(60),
      List(
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59
      )
    );
  }

}
