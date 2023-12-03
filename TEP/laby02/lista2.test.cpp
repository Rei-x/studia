#include <iostream>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "Number.h"
#include <doctest.h>

// NOLINTBEGIN
TEST_CASE("Addition")
{
  Number number123, number123_v2, number2, number40Minus, number40Minus_v2, number0, number99999, number1, number99999Minus, number10, number120, number40;
  number123 = 123;
  number10 = 10;
  number120 = 1200;
  number40Minus = -40;
  number40 = 40;
  number99999 = 99999;
  number99999Minus = -99999;
  number1 = 1;
  number40Minus_v2 = number40Minus;
  number123_v2 = number123;
  number2 = 2;
  number0 = 0;
  number123_v2 = number123_v2 + number2;

  CHECK_EQ(number123.toString(), "123");
  CHECK_EQ(number123_v2.toString(), "125");
  CHECK_EQ(number0.toString(), "0");
  CHECK_EQ((number0 + number0).toString(), "0");
  CHECK_EQ((number0 + number2).toString(), "2");
  CHECK_EQ((number2 + number0).toString(), "2");
  CHECK_EQ((number123 + number2).toString(), "125");
  CHECK_EQ((number2 + number123).toString(), "125");
  CHECK_EQ((number99999 + number1).toString(), "100000");
  CHECK_EQ((number40Minus + number2).toString(), "-38");
  CHECK_EQ((number40Minus + number40Minus).toString(), "-80");
  CHECK_EQ((number40Minus + number40Minus_v2).toString(), "-80");
  CHECK_EQ((number40Minus + number0).toString(), "-40");
  CHECK_EQ((number40Minus + number1).toString(), "-39");
  CHECK_EQ((number40Minus + number123).toString(), "83");
  CHECK_EQ((number40Minus + number123_v2).toString(), "85");
}

TEST_CASE("subtraction")
{
  Number number123, number123_v2, number2, number40Minus, number40Minus_v2, number0, number99999, number1, number99999Minus, number10, number120, number40;
  number123 = 123;
  number10 = 10;
  number120 = 1200;
  number40Minus = -40;
  number40 = 40;
  number99999 = 99999;
  number99999Minus = -99999;
  number1 = 1;
  number40Minus_v2 = number40Minus;
  number123_v2 = number123;
  number2 = 2;
  number0 = 0;
  number123_v2 = number123_v2 + number2;

  CHECK_EQ((number123 - number2).toString(), "121");
  CHECK_EQ((number123 - number123).toString(), "0");
  CHECK_EQ((number123_v2 - number123).toString(), "2");
  CHECK_EQ((number2 - number0).toString(), "2");
  CHECK_EQ((number2 - number123).toString(), "-121");
  CHECK_EQ((number1 - number99999).toString(), "-99998");
  CHECK_EQ((number99999 - number99999).toString(), "0");
  CHECK_EQ((number99999 - number99999Minus).toString(), "199998");
  CHECK_EQ((number99999Minus - number99999).toString(), "-199998");
  CHECK_EQ((number99999 - number1).toString(), "99998");
  CHECK_EQ((number99999Minus - number1).toString(), "-100000");
  CHECK_EQ((number99999Minus - number99999Minus).toString(), "0");
  CHECK_EQ((number99999Minus - number99999).toString(), "-199998");
  CHECK_EQ((number99999 - number99999Minus).toString(), "199998");
}

TEST_CASE("Multiplication")
{
  Number number123, number123_v2, number2, number40Minus, number40Minus_v2, number0, number99999, number1, number99999Minus, number10, number120, number40;
  number123 = 123;
  number10 = 10;
  number120 = 1200;
  number40Minus = -40;
  number40 = 40;
  number99999 = 99999;
  number99999Minus = -99999;
  number1 = 1;
  number40Minus_v2 = number40Minus;
  number123_v2 = number123;
  number2 = 2;
  number0 = 0;
  number123_v2 = number123_v2 + number2;

  CHECK_EQ((number1 * number1).toString(), "1");
  CHECK_EQ((number1 * number2).toString(), "2");
  CHECK_EQ((number2 * number1).toString(), "2");
  CHECK_EQ((number2 * number2).toString(), "4");
  CHECK_EQ((number2 * number40Minus).toString(), "-80");
  CHECK_EQ((number40Minus * number2).toString(), "-80");
  CHECK_EQ((number40Minus * number40Minus).toString(), "1600");
  CHECK_EQ((number40Minus * number40Minus_v2).toString(), "1600");
  CHECK_EQ((number0 * number2).toString(), "0");
  CHECK_EQ((number2 * number0).toString(), "0");
  CHECK_EQ((number40Minus * number0).toString(), "0");
  CHECK_EQ((number0 * number40Minus_v2).toString(), "0");
  CHECK_EQ((number40Minus * number1).toString(), "-40");
  CHECK_EQ((number40Minus * number123).toString(), "-4920");
  CHECK_EQ((number40Minus * number123_v2).toString(), "-5000");
  CHECK_EQ((number123 * number40Minus).toString(), "-4920");
  CHECK_EQ((number123_v2 * number40Minus).toString(), "-5000");
  CHECK_EQ((number123 * number123).toString(), "15129");
}
#ifdef __unix__
TEST_CASE("Division")
{
  Number number123, number123_v2, number2, number40Minus, number40Minus_v2, number0, number99999, number1, number99999Minus, number10, number120, number40;
  number123 = 123;
  number10 = 10;
  number120 = 1200;
  number40Minus = -40;
  number40 = 40;
  number99999 = 99999;
  number99999Minus = -99999;
  number1 = 1;
  number40Minus_v2 = number40Minus;
  number123_v2 = number123;
  number2 = 2;
  number0 = 0;
  number123_v2 = number123_v2 + number2;

  CHECK_EQ((number120 / number10).toString(), "12");
  CHECK_EQ((number2 / number1).toString(), "2");
  CHECK_EQ((number1 / number1).toString(), "1");
  CHECK_EQ((number2 / number2).toString(), "1");
  CHECK_EQ((number10 / number1).toString(), "10");
  CHECK_EQ((number123 / number1).toString(), "123");
  CHECK_EQ((number10 / number2).toString(), "5");
  // CHECK_EQ((number10 / number0).toString(), "0");
  CHECK_EQ((number0 / number10).toString(), "0");
  CHECK_EQ((number40Minus / number2).toString(), "-20");
  CHECK_EQ((number2 / number40Minus).toString(), "0");
  CHECK_EQ((number99999 / number1).toString(), "99999");
  CHECK_EQ((number1 / number99999).toString(), "0");
  CHECK_EQ((number99999 / number99999).toString(), "1");
  CHECK_EQ((number120 / number40Minus).toString(), "-30");
}

TEST_CASE("Multiple operations")
{
  Number number123, number123_v2, number2, number40Minus, number40Minus_v2, number0, number99999, number1, number99999Minus, number10, number120, number40;
  number123 = 123;
  number10 = 10;
  number120 = 1200;
  number40Minus = -40;
  number40 = 40;
  number99999 = 99999;
  number99999Minus = -99999;
  number1 = 1;
  number40Minus_v2 = number40Minus;
  number123_v2 = number123;
  number2 = 2;
  number0 = 0;
  number123_v2 = number123_v2 + number2;

  CHECK_EQ((number2 / number2 + number2 / number2).toString(), "2");
  CHECK_EQ((number2 / number2 + number2 / number2 + number2 / number2).toString(), "3");
  CHECK_EQ(((number0 * number120 + number99999 * number1) / number1).toString(), "99999");
}

TEST_CASE("MODULO")
{
  Number number123, number123_v2, number2, number40Minus, number40Minus_v2, number0, number99999, number1, number99999Minus, number10, number120, number40;
  number123 = 123;
  number10 = 10;
  number120 = 1200;
  number40Minus = -40;
  number40 = 40;
  number99999 = 99999;
  number99999Minus = -99999;
  number1 = 1;
  number40Minus_v2 = number40Minus;
  number123_v2 = number123;
  number2 = 2;
  number0 = 0;
  number123_v2 = number123_v2 + number2;

  Number *result = NULL;
  CHECK_EQ((number123.modulo(number2, &result)).toString(), "1");
  CHECK_EQ((*result).toString(), "61");
  Number *result2 = NULL;
  CHECK_EQ((number40Minus.modulo(number2, &result2)).toString(), "0");
  CHECK_EQ((*result2).toString(), "-20");
  CHECK_EQ((number123.modulo(number40Minus, &result)).toString(), "3");
}
#endif
// NOLINTEND