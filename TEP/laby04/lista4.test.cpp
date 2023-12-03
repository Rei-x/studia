#include <iostream>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "Tree.h"
#include <doctest.h>

// NOLINTBEGIN
TEST_CASE("Nodes")
{
  Tree<int> firstTree;

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

  Tree<int> secondTree;

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
  Tree<int> thirdTree;
  thirdTree = firstTree + secondTree;

  firstTree = firstTree;
  CHECK_EQ(firstTree.toString(), "+ a b");
  CHECK_EQ(firstTree.getArgumentsList(), "a b");
  CHECK_EQ(thirdTree.toString(), "+ a * 2 1");
  CHECK_EQ(thirdTree.getArgumentsList(), "a");
  CHECK_EQ(secondTree.toString(), "* 2 1");

  // doesn't work
  // Tree hashtagTree;

  // hashtagTree.parseFormula("# 1000 3");

  // CHECK_EQ(hashtagTree.comp(""), 1);

  // hashtagTree.parseFormula("# r + 7 8");
  // CHECK_EQ(hashtagTree.comp("2"), 6);
}

TEST_CASE("Nodes double")
{
  Tree<double> firstTree;

  CHECK_EQ(firstTree.getKnownType(), "DOUBLE");

  firstTree.parseFormula("+ a");

  CHECK_EQ(firstTree.toString(), "+ a 1");
  CHECK_EQ(firstTree.getArgumentsList(), "a");

  firstTree.parseFormula("+ 3.2");

  CHECK_EQ(firstTree.toString(), "+ 3.2 1");

  firstTree.parseFormula("+ 3 20 30 40");
  CHECK_EQ(firstTree.toString(), "+ 3 20");

  firstTree.parseFormula("+ a b");
  CHECK_EQ(firstTree.getArgumentsList(), "a b");

  CHECK_EQ(firstTree.toString(), "+ a b");
  CHECK_EQ(firstTree.comp("1.2 2 3"), -1);
  CHECK_EQ(firstTree.comp("1 2.5"), 3.5);

  Tree<double> secondTree;

  secondTree.parseFormula("* 2 1");
  CHECK_EQ(firstTree.toString(), "+ a b");
  CHECK_EQ(secondTree.toString(), "* 2 1");
  CHECK_EQ(firstTree.getArgumentsList(), "a b");
  secondTree = firstTree;
  CHECK_EQ(firstTree.getArgumentsList(), "a b");
  CHECK_EQ(secondTree.toString(), "+ a b");
  CHECK_EQ(secondTree.getArgumentsList(), "a b");
  CHECK_EQ(firstTree.toString(), "+ a b");
  secondTree.parseFormula("* 2.99 1.23");
  CHECK_EQ(secondTree.toString(), "* 2.99 1.23");
  Tree<double> thirdTree;
  thirdTree = firstTree + secondTree;

  firstTree = firstTree;
  CHECK_EQ(firstTree.toString(), "+ a b");
  CHECK_EQ(firstTree.getArgumentsList(), "a b");
  CHECK_EQ(thirdTree.toString(), "+ a * 2.99 1.23");
  CHECK_EQ(thirdTree.getArgumentsList(), "a");
  CHECK_EQ(secondTree.toString(), "* 2.99 1.23");

  // doesn't work
  // Tree hashtagTree;

  // hashtagTree.parseFormula("# 1000 3");

  // CHECK_EQ(hashtagTree.comp(""), 1);

  // hashtagTree.parseFormula("# r + 7 8");
  // CHECK_EQ(hashtagTree.comp("2"), 6);
}

TEST_CASE("Nodes string")
{
  Tree<std::string> firstTree;

  firstTree.parseFormula("+ + \"ala\" \"ma\" kota");

  CHECK_EQ(firstTree.toString(), "+ + \"ala\" \"ma\" kota");
  CHECK_EQ(firstTree.comp("\"kota\""), "alamakota");

  firstTree.parseFormula("- \"alaxalaxala\" \"ala\"");

  CHECK_EQ(firstTree.toString(), "- \"alaxalaxala\" \"ala\"");
  CHECK_EQ(firstTree.comp(""), "alaxalax");
}
// NOLINTEND