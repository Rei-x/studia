class Laby04 extends munit.FunSuite {
  test("tree3") {
    val tree1 = Node(1, Empty, Empty, Empty)

    val tree2 = Node(
      1,
      Node(2, Empty, Empty, Empty),
      Node(3, Empty, Empty, Empty),
      Empty
    )

    val tree3 = Node(
      1,
      Node(2, Node(19, Empty, Empty, Empty), Empty, Empty),
      Node(3, Empty, Empty, Empty),
      Node(4, Empty, Empty, Empty)
    )

    assertEquals(map3(tree1)((x: Int) => x * 2), Node(2, Empty, Empty, Empty))

    assertEquals(
      map3(tree2)((x: Int) => x * 2),
      Node(2, Node(4, Empty, Empty, Empty), Node(6, Empty, Empty, Empty), Empty)
    )

    assertEquals(
      map3(tree3)((x: Int) => x * 2),
      Node(
        2,
        Node(4, Node(38, Empty, Empty, Empty), Empty, Empty),
        Node(6, Empty, Empty, Empty),
        Node(8, Empty, Empty, Empty)
      )
    )
  }

  test("Disk") {
    val disk = Disk(
      "C",
      List(
        File("a.txt", "a"),
        File("b.txt", "b"),
        Dir(
          "dir1",
          List(
            File("c.txt", "c"),
            File("d.txt", "d"),
            Dir(
              "dir2",
              List(
                File("e.txt", "e"),
                File("f.txt", "f"),
                Dir(
                  "dir3",
                  List(
                    File("g.txt", "g"),
                    File("h.txt", "h"),
                    Dir(
                      "dir4",
                      List(
                        File("i.txt", "i"),
                        File("j.txt", "j"),
                        Dir(
                          "dir5",
                          List(
                            File("k.txt", "k"),
                            File("l.txt", "l"),
                            Dir(
                              "dir6",
                              List(
                                File("m.txt", "m"),
                                File("n.txt", "n"),
                                Dir(
                                  "dir7",
                                  List(
                                    File("o.txt", "o"),
                                    File("p.txt", "p"),
                                    Dir(
                                      "dir8",
                                      List(
                                        File("q.txt", "q"),
                                        File("r.txt", "r"),
                                        Dir(
                                          "dir9",
                                          List(
                                            File("s.txt", "s"),
                                            File("t.txt", "t"),
                                            Dir(
                                              "dir10",
                                              List(
                                                File("u.txt", "u"),
                                                File("v.txt", "v"),
                                                Dir(
                                                  "dir11",
                                                  List(
                                                    File("w.txt", "w"),
                                                    File("x.txt", "x"),
                                                    Dir(
                                                      "dir12",
                                                      List(
                                                        File("y.txt", "y"),
                                                        File("z.txt", "z")
                                                      )
                                                    )
                                                  )
                                                )
                                              )
                                            )
                                          )
                                        )
                                      )
                                    )
                                  )
                                )
                              )
                            )
                          )
                        )
                      )
                    )
                  )
                )
              )
            )
          )
        )
      )
    )

    assertEquals(path(disk, "a.txt"), Some("C:\\a.txt"))

    assertEquals(path(disk, "b.txt"), Some("C:\\b.txt"))

    assertEquals(
      path(disk, "dir2"),
      Some("C:\\dir1\\dir2")
    )

    assertEquals(path(disk, "g.txt"), Some("C:\\dir1\\dir2\\dir3\\g.txt"))

    assertEquals(path(disk, "does not exist.php"), None)
  }

}
