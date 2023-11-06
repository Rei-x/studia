class Cwiczenia01 extends munit.FunSuite {
  test("flatten1") {
    assert(
      flatten1(List(List(1, 2), List(3, 4), List(5, 6))) == List(1, 2, 3, 4, 5,
        6)
    )
    assert(flatten1(List()) == List())
    assert(
      flatten1(List(List("mario", "luigi"), List("luigi", "mario"))) == List(
        "mario",
        "luigi",
        "luigi",
        "mario"
      )
    )

  }

  test("replicate") {
    assert(replicate("la", 3) == List("la", "la", "la"))
    assert(replicate('a', 5) == List('a', 'a', 'a', 'a', 'a'))
    assert(replicate('a', 1) == List('a'))
    assert(replicate("abc", 2) == List("abc", "abc"))
    assert(replicate(1, 2) == List(1, 1))
    assert(replicate(List(1), 3) == List(List(1), List(1), List(1)))
    assert(replicate('s', 0) == List())
    assertEquals(replicate('a', -1), Nil);

  }

  test("count") {
    assert(count('a', List('a', 'l', 'a')) == 2)
    assert(count('a', List()) == 0)
    assert(count('c', List('c', 'c', 'c')) == 3)
    assert(count('c', List('a', 'a', 'a')) == 0)
  }

  test("sqrList") {
    assert(sqrList(List(1, 2, 3, -4)) == List(1, 4, 9, 16))
    assert(sqrList(List(20)) == List(400))
    assert(sqrList(List(-20)) == List(400))
    assert(sqrList(List(0, 0, 0)) == List(0, 0, 0))
    assert(sqrList(List()) == Nil)
  }

  test("palindrome") {
    assert(palindrome(List('a', 'l', 'a')) == true)
    assert(palindrome(List('k', 'a', 'y', 'a', 'k')) == true)
    assert(palindrome(List('k', 'a', 'y', 'a')) == false)
    assert(palindrome(List(1, 2, 3)) == false)
    assert(palindrome(List(3, 2, 3)) == true)
    assert(palindrome(List()) == true)
    assert(palindrome(List('m', 'a', 'a', 'm')) == true)
  }

  test("listLength") {
    assert(listLength(List()) == 0)
    assert(listLength(List(1)) == 1)
    assert(listLength(List(1, 2)) == 2)
    assert(listLength(List(List(1, 2), List(1, 2), List(1, 2))) == 3)
  }

}
