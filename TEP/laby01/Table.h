#ifndef TABLE_H
#define TABLE_H

#define TABLE_DEFAULT_NAME "table"
#define TABLE_DEFAULT_SIZE 5
#define TABLE_COPY_SUFFIX "_copy"

#include <string>

class Table
{
public:
  Table();
  Table(std::string name, int size);
  Table(Table &otherTable);
  ~Table();

  void setName(std::string name);
  std::string getName();

  bool setNewSize(int newSize);
  int getSize();

  Table *pcClone();

  void printMessage(std::string message);

private:
  int *table;
  int size;
  std::string name;
};

#endif