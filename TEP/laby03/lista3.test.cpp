#include <iostream>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "Tree.h"
#include <doctest.h>

// NOLINTBEGIN
TEST_CASE("Nodes")
{
  Tree firstTree;

  firstTree.parseFormula("- + 2 + * 20 4 4 *");

  CHECK_EQ(firstTree.toString(), "- + 2 + * 20 4 4 * ");
  CHECK_EQ(firstTree.comp(), 82);
}
// NOLINTEND