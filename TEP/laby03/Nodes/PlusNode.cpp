#include "PlusNode.h"

bool PlusNode::isApplicable(const std::string &formule, int start) const
{
  return formule[start] == '+';
}

int PlusNode::execute(Node *node) const
{
}

int PlusNode::getNumberOfArguments() const
{
  return 2;
}