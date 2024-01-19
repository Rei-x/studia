class Laby09 extends munit.FunSuite {
  test("Rectangle should calculate area correctly") {
    val r = new Rectangle(2, 3)
    assertEquals(r.area, 6.0)
  }

  test("Rectangle should throw exception for negative width") {
    intercept[IllegalArgumentException] {
      new Rectangle(-2, 3)
    }
  }

  test("Rectangle should throw exception for negative height") {
    intercept[IllegalArgumentException] {
      new Rectangle(2, -3)
    }
  }

  test("Rectangle should throw exception for negative width in setter") {
    val r = new Rectangle(2, 3)
    intercept[IllegalArgumentException] {
      r.width = -2
    }
  }

  test("Rectangle should throw exception for negative height in setter") {
    val r = new Rectangle(2, 3)
    intercept[IllegalArgumentException] {
      r.height = -3
    }
  }

  test("Rectangle single parameter constructor should create a square") {
    val r = new Rectangle(2)
    assertEquals(r.width, 2.0)
    assertEquals(r.height, 2.0)
  }

  test(
    "Rectangle single parameter constructor should throw exception for negative side length"
  ) {
    intercept[IllegalArgumentException] {
      new Rectangle(-2)
    }
  }

  test("Splitter should correctly split figures based on area") {
    val s = new Splitter(10.0)
    val smallRectangle = new Rectangle(2, 3)
    val largeRectangle = new Rectangle(4, 4)

    s(smallRectangle)
    s(largeRectangle)

    val smallOut = new java.io.ByteArrayOutputStream
    Console.withOut(smallOut) {
      s.printSmallFigures()
    }
    assertEquals(smallOut.toString, "Small figures:\n6.0\n")

    val largeOut = new java.io.ByteArrayOutputStream
    Console.withOut(largeOut) {
      s.printLargeFigures()
    }
    assertEquals(largeOut.toString, "Large figures:\n16.0\n")
  }
}
