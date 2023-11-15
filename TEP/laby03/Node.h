#include <string>
#include <vector>

enum NodeType
{
  UNINITIALIZED,
  OPERATOR,
  NUMBER,
  ARGUMENT
};

class Node
{
public:
  Node();
  ~Node();
  std::string toString() const;
  Node *getNodes() const;
  Node *getNode(int index) const;
  std::string getValue() const;
  int getNumberOfNodes() const;
  NodeType getNodeType() const;
  void setNumberOfNodes(int numberOfNodes);
  void setNodeType(NodeType type);
  void setValue(std::string value);

private:
  NodeType type;
  std::string value;
  Node *nodes;
  int numberOfNodes;
};