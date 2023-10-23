#include <iostream>
#include <string>

#include "Table.h"

Table::Table() : table(new int[TABLE_DEFAULT_SIZE]), size(TABLE_DEFAULT_SIZE), name(TABLE_DEFAULT_NAME)
{
  printMessage("bezp");
}

Table::Table(std::string name, int size) : table(new int[size]), name(name), size(size)
{
  printMessage("parametr");
}

Table::Table(Table &otherTable) : table(new int[otherTable.size]), size(otherTable.size)
{
  this->name = otherTable.name + TABLE_COPY_SUFFIX;
  printMessage("kopiuj: " + otherTable.name);

  std::copy(otherTable.table, otherTable.table + otherTable.size, this->table);
}

Table::~Table()
{
  printMessage("usuwam");
  delete[] table;
}

void Table::setName(std::string name)
{
  this->name = name;
}

std::string Table::getName()
{
  return name;
}

int Table::getSize()
{
  return size;
}

int *Table::getTable()
{
  return table;
}

bool Table::setNewSize(int newSize)
{
  if (newSize < 0)
  {
    return false;
  }

  int *newTable = new int[newSize];

  std::copy(table, table + std::min(size, newSize), newTable);

  delete[] table;

  table = newTable;
  size = newSize;

  return true;
}

Table *Table::pcClone()
{
  return new Table(*this);
}

void Table::printMessage(std::string message)
{
  std::cout << name << " -> " << message << std::endl;
}

// modyfikacja

void Table::setTestingTable()
{
  delete[] table;
  table = new int[4];

  table[0] = 1;
  table[1] = 2;
  table[2] = 3;
  table[3] = 4;
}

Table::Table(Table &otherTable, int sizeToCopy) : table(new int[sizeToCopy]), size(sizeToCopy)
{
  this->name = otherTable.name + TABLE_COPY_SUFFIX;
  printMessage("kopiuj: " + otherTable.name);

  std::copy(otherTable.table, otherTable.table + sizeToCopy, this->table);
}

void Table::addOneAndCopy(Table **tablePointerToBeCopied)
{
  *tablePointerToBeCopied = new Table(*this, size + TABLE_SIZE_INCREASE);
  Table *tableCopy = *tablePointerToBeCopied;
  tableCopy->table[size] = TABLE_VALUE_TO_ADD;
}
