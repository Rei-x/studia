#include <iostream>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "Tree.h"
#include <doctest.h>

// NOLINTBEGIN
TEST_CASE("Nodes")
{
  Tree firstTree;

  firstTree.parseFormula("+ a");

  CHECK_EQ(firstTree.toString(), "+ a 1");
  CHECK_EQ(firstTree.getArgumentsList(), "a");

  firstTree.parseFormula("+ 3");

  CHECK_EQ(firstTree.toString(), "+ 3 1");

  firstTree.parseFormula("+ 3 20 30 40");
  CHECK_EQ(firstTree.toString(), "+ 3 20");

  firstTree.parseFormula("+ a b");
  CHECK_EQ(firstTree.getArgumentsList(), "a b");

  CHECK_EQ(firstTree.toString(), "+ a b");
  CHECK_EQ(firstTree.comp("1 2 3"), -1);
  CHECK_EQ(firstTree.comp("1 2"), 3);

  Tree secondTree;

  secondTree.parseFormula("* 2 1");
  CHECK_EQ(firstTree.toString(), "+ a b");
  CHECK_EQ(secondTree.toString(), "* 2 1");
  CHECK_EQ(firstTree.getArgumentsList(), "a b");
  secondTree = firstTree;
  CHECK_EQ(firstTree.getArgumentsList(), "a b");
  CHECK_EQ(secondTree.toString(), "+ a b");
  CHECK_EQ(secondTree.getArgumentsList(), "a b");
  CHECK_EQ(firstTree.toString(), "+ a b");
  secondTree.parseFormula("* 2 1");
  CHECK_EQ(secondTree.toString(), "* 2 1");
  Tree thirdTree;
  thirdTree = firstTree + secondTree;

  firstTree = firstTree;
  CHECK_EQ(firstTree.toString(), "+ a b");
  CHECK_EQ(firstTree.getArgumentsList(), "a b");
  CHECK_EQ(thirdTree.toString(), "+ a * 2 1");
  CHECK_EQ(thirdTree.getArgumentsList(), "a");
  CHECK_EQ(secondTree.toString(), "* 2 1");
}
// NOLINTEND