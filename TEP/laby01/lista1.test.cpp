#include <iostream>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include <doctest.h>

enum
{
  INTEGER_TO_FILL = 34
};

void v_alloc_table_fill_34(int iSize)
{
  int *piTable = new int[iSize];

  for (int i = 0; i < iSize; i++)
  {
    piTable[i] = INTEGER_TO_FILL;
  }

  char cSeparator = ' ';

  for (int i = 0; i < iSize; i++)
  {
    std::cout << piTable[i] << cSeparator;
  }

  delete[] piTable;
}

bool b_alloc_table_2_dim(int ***piTable, int iSizeX, int iSizeY)
{
  if (iSizeX <= 0 || iSizeY < 0)
  {
    return false;
  }
  if (piTable == NULL)
  {
    return false;
  }
  int **table = new int *[iSizeX];
  for (int i = 0; i < iSizeX; i++)
  {
    table[i] = new int[iSizeY];
  }

  *piTable = table;
  return true;
}

bool b_dealloc_table_2_dim(int **piTable, int iSizeX, int iSizeY)
{
  if (iSizeX <= 0)
  {
    return false;
  }
  if (piTable == NULL)
  {
    return false;
  }
  for (int i = 0; i < iSizeX; i++)
  {
    delete[] piTable[i];
  }
  delete[] piTable;
  return true;
}

// NOLINTBEGIN
TEST_CASE("alloc table")
{
  int **piTable = NULL;
  CHECK(b_alloc_table_2_dim(&piTable, 5, 5));
  CHECK(b_dealloc_table_2_dim(piTable, 5, 5));
}
// NOLINTEND
