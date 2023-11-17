#include "Node.h"
#include <iostream>
#include <sstream>
#include <string>

Node::Node() : numberOfNodes(0), nodes(new Node[0]), type(UNINITIALIZED)
{
}

Node::Node(const Node &otherNode) : type(otherNode.type), value(otherNode.value), numberOfNodes(otherNode.numberOfNodes)
{
  this->nodes = new Node[numberOfNodes];

  for (int i = 0; i < numberOfNodes; i++)
  {
    this->nodes[i] = otherNode.nodes[i];
  }
}

Node::~Node()
{
  if (nodes != NULL)
  {
    delete[] nodes;
  }
}

std::string Node::toString() const
{
  std::string result = value;

  for (int i = 0; i < numberOfNodes; i++)
  {
    result += " " + nodes[i].toString();
  }

  return result;
}

Node *Node::getNodes() const
{
  return nodes;
}

Node *Node::getNode(int index) const
{
  return &nodes[index];
}

std::string Node::getValue() const
{
  return value;
}

int Node::getNumberOfNodes() const
{
  return numberOfNodes;
}

NodeType Node::getNodeType() const
{
  return type;
}

Node &Node::operator=(const Node &newValue)
{
  if (this == &newValue)
  {
    return *this;
  }

  if (nodes != NULL)
  {
    delete[] nodes;
  }

  this->type = newValue.type;
  this->value = newValue.value;
  this->numberOfNodes = newValue.numberOfNodes;

  this->nodes = new Node[numberOfNodes];

  for (int i = 0; i < numberOfNodes; i++)
  {
    this->nodes[i] = newValue.nodes[i];
  }

  return *this;
}

void Node::setNumberOfNodes(int numberOfNodes)
{
  this->numberOfNodes = numberOfNodes;
  this->nodes = new Node[numberOfNodes];
}

void Node::setNodeType(NodeType type)
{
  this->type = type;
}

void Node::setValue(std::string value)
{
  this->value = value;
}

void Node::setNode(int index, Node &node)
{
  if (index >= numberOfNodes)
  {
    return;
  }

  this->nodes[index] = node;
}
