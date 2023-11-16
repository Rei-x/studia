#include "Tree.h"
#include "stringUtils.h"
#include <iostream>
#include <sstream>
#include <valarray>

int stringToNumber(std::string str)
{
  int i = 0;

  std::istringstream(str) >> i;

  return i;
}

std::map<std::string, int> createFunctionMap()
{
  std::map<std::string, int> m;

  m["sin"] = 1;
  m["cos"] = 1;
  m["+"] = 2;
  m["-"] = 2;
  m["*"] = 2;
  m["/"] = 2;

  return m;
}

const std::map<std::string, int> Tree::funMap = createFunctionMap();

void Tree::parseFormula(std::string formule)
{
  if (root != NULL)
    delete root;

  root = new Node();

  bool wasError = false;

  int start = parseNodes(root, formule, 0, &wasError);

  if (formule.length() > start)
  {
    std::cout << "Error: Too many arguments" << std::endl;
    wasError = true;
  }

  if (wasError)
  {
    std::cout << "Corrected formula: " << this->toString() << std::endl;
  }
}

int Tree::parseNodes(Node *currentNode, std::string formule, int start, bool *wasError)
{
  std::string value = "";

  while (formule.length() > start && formule[start] == ' ')
  {
    start++;
  }

  while (formule.length() > start && formule[start] != ' ')
  {
    value += formule[start];
    start++;
  }

  // std::cout << "Current value: \"" << value << "\"" << std::endl;

  value.erase(value.find_last_not_of(' ') + 1);

  std::map<std::string, int>::const_iterator numberOfArgsIterator = Tree::funMap.find(value);

  if (numberOfArgsIterator != Tree::funMap.end())
  {
    currentNode->setNumberOfNodes(numberOfArgsIterator->second);
    currentNode->setNodeType(OPERATOR);

    for (int i = 0; i < currentNode->getNumberOfNodes(); i++)
    {
      if (formule.length() <= start)
      {
        std::cout << "Error: Not enough arguments for operator: " << value << ", substituting 1" << std::endl;
        currentNode->getNode(i)->setNumberOfNodes(0);
        currentNode->getNode(i)->setNodeType(NUMBER);
        currentNode->getNode(i)->setValue("1");

        *wasError = true;
      }
      else
      {
        start = parseNodes(currentNode->getNode(i), formule, start, wasError);
      }
    }
  }
  else if (value.find_first_not_of("0123456789") == std::string::npos)
  {
    currentNode->setNumberOfNodes(0);
    currentNode->setNodeType(NUMBER);
  }
  else if (isValidArgument(value))
  {
    currentNode->setNumberOfNodes(0);
    currentNode->setNodeType(ARGUMENT);

    setArgumentValue(value, -1);
  }
  else
  {
    std::cout << "Error: Unknown operator: " << value << std::endl;
  }

  currentNode->setValue(value);
  // std::cout << "Current number: " << value << std::endl;

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
  if (root == NULL)
  {
    return "";
  }

  return root->toString();
}

int Tree::comp(std::string args)
{
  int size = 0;

  std::string *argsArray = splitStringByWhitespace(args, &size);

  if (size != argsMap.size())
  {
    std::cout << "Error: Wrong number of arguments, expected: " << argsMap.size() << ", got: " << size << std::endl;

    delete[] argsArray;

    return -1;
  }

  for (int i = 0; i < size; i++)
  {
    if (argsArray[i].find_first_not_of("0123456789") == std::string::npos)
    {
      setArgumentValueByIndex(i, stringToNumber(argsArray[i]));
    }
  }

  if (root == NULL)
  {
    std::cout << "Error: No formula" << std::endl;

    delete[] argsArray;

    return -1;
  }

  int result = comp(root);

  delete[] argsArray;

  return result;
}

// output "a b c" without trailing whitespace
std::string Tree::getArgumentsList() const
{
  std::string result = "";

  for (int i = 0; i < argsVector.size(); i++)
  {
    result += argsVector[i];

    if (i != argsVector.size() - 1)
    {
      result += " ";
    }
  }

  return result;
}
// Split string by whitespace
// "Mario and   luigi" -> ["Mario", "and", "luigi"]

void Tree::printNodes() const
{
  for (int i = 0; i < root->getNumberOfNodes(); i++)
  {
    std::cout << root->getNode(i)->toString() << std::endl;
  }
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
    else if (currentNode->getValue() == "sin")
    {
      return static_cast<int>(std::sin(comp(currentNode->getNode(0))));
    }
    else if (currentNode->getValue() == "cos")
    {
      return static_cast<int>(std::cos(comp(currentNode->getNode(0))));
    }
  }
  else if (currentNode->getNodeType() == ARGUMENT)
  {
    std::map<std::string, int>::const_iterator argsIterator = argsMap.find(currentNode->getValue());

    if (argsIterator == argsMap.end())
    {
      std::cout << "Error: Unknown argument: " << currentNode->getValue() << std::endl;
      return -1;
    }

    std::cout << "Argument: " << currentNode->getValue() << " = " << argsIterator->second << std::endl;

    return argsIterator->second;
  }

  return -1;
}
// Consist of letters (both uppercase and lowercase) and digits (if there is any prohibited value in the character string, such as "$," it can be ignored, and the user should be informed about it.)
// There can be any number of letters and digits.
// There must be at least one letter in the variable name.
bool Tree::isValidArgument(std::string value)
{
  if (value.empty())
  {
    return false;
  }

  bool hasLetter = false;
  for (size_t i = 0; i < value.length(); ++i)
  {
    if (isalpha(value[i]))
    {
      hasLetter = true;
    }
    else if (!isdigit(value[i]))
    {
      std::cerr << "Invalid character ignored: " << value[i] << std::endl;
    }
  }

  return hasLetter;
}

void Tree::setArgumentValue(std::string arg, int value)
{
  std::map<std::string, int>::const_iterator argsIterator = argsMap.find(arg);

  if (argsIterator == argsMap.end())
  {
    argsVector.push_back(arg);
  }

  argsMap[arg] = value;
}

void Tree::setArgumentValueByIndex(int index, int value)
{
  if (index >= argsVector.size())
  {
    std::cout << "Error: Index out of bounds: " << index << std::endl;
    return;
  }

  argsMap[argsVector[index]] = value;
}
