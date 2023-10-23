#ifndef TABLE_H
#define TABLE_H

#define TABLE_DEFAULT_NAME "table"
#define TABLE_DEFAULT_SIZE 5
#define TABLE_COPY_SUFFIX "_copy"

#define TABLE_SIZE_INCREASE 1
#define TABLE_VALUE_TO_ADD 1

#include <string>

class Table
{
public:
  Table();
  Table(std::string name, int size);
  Table(Table &otherTable);
  Table(Table &otherTable, int sizeToCopy);
  ~Table();

  void setName(std::string name);
  std::string getName();

  bool setNewSize(int newSize);
  int getSize();

  int *getTable();

  Table *pcClone();

  void printMessage(std::string message);

  void setTestingTable();

  void addOneAndCopy(Table **cCopy);

private:
  int *table;
  int size;
  std::string name;
};

#endif