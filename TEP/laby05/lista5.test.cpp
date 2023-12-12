#include <iostream>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "MyPointer.h"
#include "Tree.h"
#include <doctest.h>

// NOLINTBEGIN
TEST_CASE("Nodes")
{
  Tree<int> firstTree;
  Tree<int> secondTree;
  Tree<int> thirdTree;

  std::cout << "MOVE SEMANTICS" << std::endl;
  firstTree.parseFormula("+ a b");

  secondTree.parseFormula("* 2 1");
  CHECK_EQ(firstTree.toString(), "+ a b");
  CHECK_EQ(secondTree.toString(), "* 2 1");
  CHECK_EQ(firstTree.getArgumentsList(), "a b");
  std::cout << "ASSIGNMENT" << std::endl;
  secondTree = std::move(firstTree);

  CHECK_EQ(secondTree.toString(), "+ a b");
  std::cout << "END OF ASSIGNMENT" << std::endl;
  thirdTree.parseFormula("* 2 4");
  std::cout << "PLUS AND ASSIGNMENT" << std::endl;
  firstTree = std::move(secondTree + std::move(thirdTree));
  std::cout << "END OF MOVE SEMANTICS" << std::endl;
  std::cout << "COPY SEMANTICS" << std::endl;
  firstTree.parseFormula("+ a b");

  secondTree.parseFormula("* 2 1");
  CHECK_EQ(firstTree.toString(), "+ a b");
  CHECK_EQ(secondTree.toString(), "* 2 1");
  CHECK_EQ(firstTree.getArgumentsList(), "a b");
  std::cout << "ASSIGNMENT" << std::endl;
  secondTree = firstTree;

  CHECK_EQ(secondTree.toString(), "+ a b");
  std::cout << "END OF ASSIGNMENT" << std::endl;
  thirdTree.parseFormula("* 2 4");
  std::cout << "PLUS AND ASSIGNMENT" << std::endl;
  firstTree = secondTree + thirdTree;
  std::cout << "END OF COPY SEMANTICS" << std::endl;
}

TEST_CASE("MyPointer")
{
  int *dynamicValue = new int(5);
  {
    MyPointer<int> firstPointer(dynamicValue);
    CHECK_EQ(*dynamicValue, 5);
    CHECK_EQ(*firstPointer, 5);
    CHECK_EQ(firstPointer.getCounter(), 1);
  }

  CHECK_NE(*dynamicValue, 5);

  MyPointer<int> firstPointer(new int(5));

  CHECK_EQ(*firstPointer, 5);
  CHECK_EQ(firstPointer.getCounter(), 1);
  MyPointer<int> secondPointer(new int(10));

  CHECK_EQ(*secondPointer, 10);

  firstPointer = secondPointer;

  CHECK_EQ(*firstPointer, 10);
  CHECK_EQ(*secondPointer, 10);
  CHECK_EQ(firstPointer.getCounter(), 2);
  CHECK_EQ(secondPointer.getCounter(), 2);
}
// NOLINTEND
