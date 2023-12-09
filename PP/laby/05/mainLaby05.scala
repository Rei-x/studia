def skipTakeL[A](lazyList: LazyList[A]): LazyList[A] = {
  def go(innerLazyList: LazyList[A], numberOfElementsToSkip: Int): LazyList[A] =
    innerLazyList match {
      case x #:: xs =>
        x #:: go(
          xs.drop(numberOfElementsToSkip),
          numberOfElementsToSkip + 1
        )
      case _ =>
        LazyList.empty
    }

  go(lazyList, 1)
}
