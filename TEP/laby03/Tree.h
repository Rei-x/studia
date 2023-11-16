#pragma once
#include "Node.h"
#include <map>
#include <string>
#include <vector>
class Tree
{
public:
  Tree();
  ~Tree();
  void parseFormula(std::string formule);
  int parseNodes(Node *currentNode, std::string formule, int start, bool *wasError);
  std::string toString() const;
  int comp(std::string args);
  std::string getArgumentsList() const;
  Node *root;
  void printNodes() const;

private:
  int comp(Node *currentNode) const;
  static const std::map<std::string, int> funMap;
  std::map<std::string, int> argsMap;
  std::vector<std::string> argsVector;
  void setArgumentValue(std::string arg, int value);
  void setArgumentValueByIndex(int index, int value);
  static bool isValidArgument(std::string value);
};