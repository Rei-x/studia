#include <iostream>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "Number.h"
#include <doctest.h>

TEST_CASE("alloc table")
{
  Number number123, number123_v2, number2, number40Minus;
  number123 = 123;
  number40Minus = -40;
  number123_v2 = number123;
  number2 = 2;
  number123_v2 = number123_v2 + number2;
  CHECK(number123.toString() == "123");
  CHECK(number40Minus.toString() == "-40");
  CHECK((number123 + number123_v2).toString() == "248");
  CHECK((number123 - number40Minus).toString() == "0");
  // CHECK((number123 * number123_v2).toString() == "15375");
  // CHECK((number2 + number40Minus).toString() == "-38");
  // CHECK((number123 - number123_v2).toString() == "0");
  // CHECK((number123 / number123_v2).toString() == "1");
}