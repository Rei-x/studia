#include "Tree.h"
#include <iostream>
#include <sstream>

void Tree::parseFormula(std::string formule)
{
  if (root != NULL)
    delete root;

  root = new Node();

  parseNodes(root, formule, 0);
}

int Tree::parseNodes(Node *currentNode, std::string formule, int start)
{
  std::string value = "";

  while (formule.length() > start && formule[start] != ' ')
  {
    value += formule[start];
    start++;
  }
  start++;
  value.erase(value.find_last_not_of(' ') + 1);
  if (value == "+")
  {
    currentNode->setNumberOfNodes(2);
    currentNode->setNodeType(OPERATOR);

    for (int i = 0; i < currentNode->getNumberOfNodes(); i++)
    {
      start = parseNodes(currentNode->getNode(i), formule, start);
    }
  }
  else if (value == "-")
  {
    currentNode->setNumberOfNodes(2);
    currentNode->setNodeType(OPERATOR);

    for (int i = 0; i < currentNode->getNumberOfNodes(); i++)
    {
      start = parseNodes(currentNode->getNode(i), formule, start);
    }
  }
  else if (value == "*")
  {
    currentNode->setNumberOfNodes(2);
    currentNode->setNodeType(OPERATOR);

    for (int i = 0; i < currentNode->getNumberOfNodes(); i++)
    {
      start = parseNodes(currentNode->getNode(i), formule, start);
    }
  }
  else if (value == "/")
  {
    currentNode->setNumberOfNodes(2);
    currentNode->setNodeType(OPERATOR);

    for (int i = 0; i < currentNode->getNumberOfNodes(); i++)
    {
      start = parseNodes(currentNode->getNode(i), formule, start);
    }
  }
  else if (value.find_first_not_of("0123456789") == std::string::npos)
  {
    currentNode->setNumberOfNodes(0);
    currentNode->setNodeType(NUMBER);
  }
  else
  {
    std::cout << "Error: Unknown operator: " << value << std::endl;
  }

  currentNode->setValue(value);
  std::cout << "Current number: " << value << std::endl;

  return start;
}

Tree::Tree() : root(NULL)
{
}

Tree::~Tree()
{
  delete root;
}

std::string Tree::toString() const
{
  return root->toString();
}

int Tree::comp() const
{
  return comp(root);
}

int Tree::comp(Node *currentNode) const
{
  if (currentNode->getNodeType() == NUMBER)
  {
    int i = 0;

    std::istringstream(currentNode->getValue()) >> i;

    return i;
  }
  else if (currentNode->getNodeType() == OPERATOR)
  {
    if (currentNode->getValue() == "+")
    {
      return comp(currentNode->getNode(0)) + comp(currentNode->getNode(1));
    }
    else if (currentNode->getValue() == "-")
    {
      return comp(currentNode->getNode(0)) - comp(currentNode->getNode(1));
    }
    else if (currentNode->getValue() == "*")
    {
      return comp(currentNode->getNode(0)) * comp(currentNode->getNode(1));
    }
    else if (currentNode->getValue() == "/")
    {
      int secondNodeValue = comp(currentNode->getNode(1));

      if (secondNodeValue == 0)
      {
        throw std::invalid_argument("Division by zero");
      }

      return comp(currentNode->getNode(0)) / secondNodeValue;
    }
  }
  else
  {
    std::cout << "Error: Unknown operator: " << currentNode->getValue() << std::endl;
  }

  return -1;
}
