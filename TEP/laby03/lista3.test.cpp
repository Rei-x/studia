#include <iostream>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "Tree.h"
#include <doctest.h>

// NOLINTBEGIN
TEST_CASE("Nodes")
{
  Tree firstTree;

  firstTree.parseFormula("+ a b");

  CHECK_EQ(firstTree.toString(), "+ a b");
  std::cout << firstTree.getArgumentsList() << std::endl;
  CHECK_EQ(firstTree.comp("2 3"), 5);
}
// NOLINTEND