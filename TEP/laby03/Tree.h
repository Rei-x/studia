#ifndef TREE
#define TREE

#include "Node.h"
#include <map>
#include <sstream>
#include <string>
#include <vector>

const std::string LIST_OF_NUMBERS = "0123456789";

class Tree
{
public:
  Tree();
  ~Tree();
  Tree(const Tree &other);
  void parseFormula(std::string formule);
  int parseNodes(Node *currentNode, std::string formule, int start, bool *wasError);
  std::string toString() const;
  int comp(std::string args);
  std::string getArgumentsList() const;
  Tree &operator=(const Tree &newValue);
  Tree operator+(const Tree &newValue) const;
  std::string getErrorAndClear();
  void printNodes() const;

private:
  Node *root;
  std::stringstream errorStream;
  int comp(Node *currentNode);
  static const std::map<std::string, int> funMap;
  std::map<std::string, int> argsMap;
  std::vector<std::string> argsVector;
  void removeArgument(std::string arg);
  void setArgumentValue(std::string arg, int value);
  void setArgumentValueByIndex(int index, int value);
  bool isValidArgument(std::string value);
  static int stringToNumber(std::string str);
};

#endif