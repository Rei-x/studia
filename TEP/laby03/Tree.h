#include "Node.h"
#include <string>
class Tree
{
public:
  Tree();
  ~Tree();
  void parseFormula(std::string formule);
  int parseNodes(Node *currentNode, std::string formule, int start);
  std::string toString() const;
  int comp() const;
  Node *root;

private:
  int comp(Node *currentNode) const;
};