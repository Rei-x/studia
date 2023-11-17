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
  Tree(const Tree &other);
  void parseFormula(std::string formule);
  int parseNodes(Node *currentNode, std::string formule, int start, bool *wasError);
  std::string toString() const;
  int comp(std::string args);
  std::string getArgumentsList() const;
  Node *root;
  Tree &operator=(const Tree &newValue);
  Tree operator+(const Tree &newValue) const;
  void printNodes() const;

private:
  int comp(Node *currentNode) const;
  static const std::map<std::string, int> funMap;
  std::map<std::string, int> argsMap;
  std::vector<std::string> argsVector;
  void removeArgument(std::string arg);
  void setArgumentValue(std::string arg, int value);
  void setArgumentValueByIndex(int index, int value);
  static bool isValidArgument(std::string value);
};