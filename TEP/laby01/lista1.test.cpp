#include <iostream>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "Table.h"
#include "lista1.test.h"
#include <doctest.h>

void allocTableAndFillWithVALUE(int size)
{
  int *tablePointer = new int[size];

  for (int i = 0; i < size; i++)
  {
    tablePointer[i] = VALUE_TO_FILL_THE_TABLE;
  }

  for (int i = 0; i < size; i++)
  {
    std::cout << tablePointer[i] << ' ';
  }

  std::cout << std::endl;

  delete[] tablePointer;
}

bool allocTwoDimensionalTable(int ***table, int sizeX, int sizeY)
{
  if (sizeX <= 0 || sizeY <= 0)
  {
    return false;
  }

  if (table == NULL)
  {
    return false;
  }

  int **tablePlaceholder = new int *[sizeX];

  for (int i = 0; i < sizeX; i++)
  {
    tablePlaceholder[i] = new int[sizeY];
  }

  *table = tablePlaceholder;

  return true;
}

bool deallocTwoDimensionalTable(int **table, int sizeX, int sizeY)
{
  if (sizeX <= 0 || sizeY <= 0)
  {
    return false;
  }

  if (table == NULL)
  {
    return false;
  }

  for (int i = 0; i < sizeX; i++)
  {
    delete[] table[i];
  }

  delete[] table;
  return true;
}

// NOLINTBEGIN
TEST_CASE("alloc table")
{
  int **piTable = NULL;
  CHECK(allocTwoDimensionalTable(&piTable, 5, 5));
  CHECK(deallocTwoDimensionalTable(piTable, 5, 5));

  CHECK(!allocTwoDimensionalTable(&piTable, 0, 0));
  CHECK(!allocTwoDimensionalTable(&piTable, 0, 5));
  CHECK(!allocTwoDimensionalTable(&piTable, 5, 0));

  CHECK(!allocTwoDimensionalTable(NULL, 5, 5));
  CHECK(!allocTwoDimensionalTable(&piTable, -5, 5));
  CHECK(!allocTwoDimensionalTable(&piTable, 5, -5));

  Table *table = new Table;

  CHECK_EQ(table->getName(), TABLE_DEFAULT_NAME);
  table->setName("mario");

  CHECK_EQ(table->getName(), "mario");
  CHECK_EQ(table->getSize(), TABLE_DEFAULT_SIZE);

  Table *tableCopy = new Table(*table);

  CHECK_EQ(tableCopy->getName(), "mario_copy");
  CHECK_EQ(tableCopy->getSize(), TABLE_DEFAULT_SIZE);

  delete table;

  CHECK_EQ(tableCopy->getName(), "mario_copy");

  allocTableAndFillWithVALUE(10);
}
// NOLINTEND
