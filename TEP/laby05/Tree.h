#ifndef TREE
#define TREE

#include "MyPointer.h"
#include "Node.h"
#include "stringUtils.h"
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <valarray>
#include <vector>

#define DEFAULT_STRING_NODE_VALUE "\"KOTEK\""
#define DEFAULT_NODE_VALUE "1"

#define DEFAULT_STRING_ERROR_VALUE "COULDN'T CALCULATE"
#define DEFAULT_ERROR_VALUE -1

#define BOOL_NAME "BOOL"

// const std::string DEFAULT_STRING_ERROR_VALUE = "COULDN'T CALCULATE";
const std::string LIST_OF_NUMBERS = "0123456789";

template <typename T>
class Tree
{
public:
  Tree();
  ~Tree();
  Tree(const Tree &other);
  Tree(Tree &&other) noexcept;
  void parseFormula(std::string formule);
  int parseNodes(Node *currentNode, std::string formule, int start, bool *wasError);
  std::string toString() const;
  T comp(std::string args);
  std::string getArgumentsList() const;
  Tree &operator=(const Tree &newValue);
  Tree &operator=(Tree &&newValue);
  Tree operator+(const Tree &newValue) const;
  Tree operator+(Tree &&newValue) const;
  std::string getErrorAndClear();
  void printNodes() const;
  bool isError();
  std::string getKnownType();
  static T getDefaultNoop();

private:
  Node *root;
  std::stringstream errorStream;
  T comp(Node *currentNode);
  bool isValidValue(std::string value);
  static std::string getDefaultValue();
  static const std::map<std::string, int> funMap;
  typename std::map<std::string, T> argsMap;
  std::vector<std::string> argsVector;
  void removeArgument(std::string arg);
  void setArgumentValue(std::string arg, T value);
  void setArgumentValueByIndex(int index, T value);
  bool isValidArgument(std::string value);
  static T stringToValue(std::string str);
  static std::map<std::string, int> createArgumentsMap();
};

template <typename T>
T Tree<T>::getDefaultNoop()
{
  return T();
}

template <>
int Tree<int>::getDefaultNoop()
{
  return DEFAULT_ERROR_VALUE;
}

template <>
double Tree<double>::getDefaultNoop()
{
  return DEFAULT_ERROR_VALUE;
}

template <>
std::string Tree<std::string>::getDefaultNoop()
{
  return DEFAULT_STRING_ERROR_VALUE;
}

template <typename T>
T Tree<T>::stringToValue(std::string str)
{
  T i = 0;

  std::istringstream(str) >> i;
  return i;
}

template <>
std::string Tree<std::string>::stringToValue(std::string str)
{
  return str.substr(1, str.length() - 2);
}

template <typename T>
std::map<std::string, int> Tree<T>::createArgumentsMap()
{
  std::map<std::string, int> m;

  m["sin"] = 1;
  m["cos"] = 1;
  m["+"] = 2;
  m["-"] = 2;
  m["*"] = 2;
  m["/"] = 2;
  m["#"] = 2;

  return m;
}

template <>
std::map<std::string, int> Tree<std::string>::createArgumentsMap()
{
  std::map<std::string, int> m;

  m["+"] = 2;
  m["-"] = 2;
  m["*"] = 2;
  m["/"] = 2;

  return m;
}

template <typename T>
const std::map<std::string, int> Tree<T>::funMap = Tree<T>::createArgumentsMap();

template <typename T>
void Tree<T>::parseFormula(std::string formule)
{
  if (root != NULL)
    delete root;

  root = new Node();

  bool wasError = false;

  argsMap.clear();
  argsVector.clear();

  int start = parseNodes(root, formule, 0, &wasError);

  if (start != -1 && formule.length() > start)
  {
    errorStream << "Error: Too many arguments" << std::endl;
    wasError = true;
  }

  if (wasError)
  {
    errorStream << "Corrected formula: " << this->toString() << std::endl;
  }
}

template <typename T>
int Tree<T>::parseNodes(Node *currentNode, std::string formule, int start, bool *wasError)
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

  value.erase(value.find_last_not_of(' ') + 1);

  std::map<std::string, int>::const_iterator numberOfArgsIterator = Tree::funMap.find(value);

  currentNode->setValue(value);

  if (numberOfArgsIterator != Tree::funMap.end())
  {
    if (numberOfArgsIterator->second == 1 && getKnownType() == BOOL_NAME)
    {
      errorStream << "YOU SHALL NOT PASS" << std::endl;
      return -1;
    }

    currentNode->setNumberOfNodes(numberOfArgsIterator->second);
    currentNode->setNodeType(OPERATOR);

    for (int i = 0; i < currentNode->getNumberOfNodes(); i++)
    {
      if (formule.length() <= start)
      {
        errorStream << "Error: Not enough arguments for operator: " << value << ", substituting 1" << std::endl;
        currentNode->getNode(i)->setNumberOfNodes(0);
        currentNode->getNode(i)->setNodeType(VALUE);
        currentNode->getNode(i)->setValue(getDefaultValue());

        *wasError = true;
      }
      else
      {
        start = parseNodes(currentNode->getNode(i), formule, start, wasError);
      }
    }
  }
  else if (isValidValue(value))
  {
    currentNode->setNumberOfNodes(0);
    currentNode->setNodeType(VALUE);
  }
  else if (isValidArgument(value))
  {
    currentNode->setNumberOfNodes(0);
    currentNode->setNodeType(ARGUMENT);

    setArgumentValue(value, getDefaultNoop());
  }
  else
  {
    errorStream << "Error: Unknown operator: " << value << std::endl;
  }

  return start;
}
template <typename T>
Tree<T>::Tree() : root(NULL), argsMap(), argsVector()
{
}

template <typename T>
Tree<T>::~Tree()
{
  if (root != NULL)
  {
    delete root;
  }
}

template <typename T>
Tree<T>::Tree(const Tree<T> &other) : root(NULL)
{
  if (other.root != NULL)
  {
    root = new Node(*other.root);
  }

  argsMap = other.argsMap;
  argsVector = other.argsVector;
}

template <typename T>
Tree<T> &Tree<T>::operator=(const Tree<T> &newValue)
{
  std::cout << "TREE COPY" << std::endl;
  if (this == &newValue)
  {
    return *this;
  }

  if (root != NULL)
  {
    delete root;
  }

  if (newValue.root != NULL)
  {
    root = new Node(*newValue.root);
  }

  for (int i = 0; i < newValue.argsVector.size(); i++)
  {
    setArgumentValue(newValue.argsVector[i], getDefaultNoop());
  }

  return *this;
}

template <typename T>
std::string Tree<T>::toString() const
{
  if (root == NULL)
  {
    return "";
  }

  return root->toString();
}

template <typename T>
T Tree<T>::comp(std::string args)
{

  std::vector<std::string> argsArray = splitStringByWhitespace(args);

  if (argsArray.size() != argsMap.size())
  {
    errorStream << "Error: Wrong number of arguments, expected: " << argsMap.size() << ", got: " << argsArray.size() << std::endl;

    return getDefaultNoop();
  }

  for (int i = 0; i < argsArray.size(); i++)
  {
    if (isValidValue(argsArray[i]))
    {
      setArgumentValueByIndex(i, stringToValue(argsArray[i]));
    }
    else
    {
      errorStream << "Error: Invalid argument: " << argsArray[i] << std::endl;

      return getDefaultNoop();
    }
  }

  if (root == NULL)
  {
    errorStream << "Error: No formula" << std::endl;

    return getDefaultNoop();
  }

  T result = comp(root);

  return result;
}

template <typename T>
std::string Tree<T>::getArgumentsList() const
{
  std::string result = "";

  for (int i = 0; i < argsVector.size(); i++)
  {
    result += argsVector[i] + " ";
  }

  if (result.length() > 0)
  {
    result = result.substr(0, result.length() - 1);
  }

  return result;
}
template <typename T>
Tree<T> Tree<T>::operator+(const Tree<T> &newValue) const
{
  Tree result = *this;

  if (result.root == NULL)
  {
    result.root = new Node(*newValue.root);
  }

  Node *currentNode = result.root;
  Node *parent = NULL;

  while (currentNode->getNumberOfNodes() > 0)
  {
    parent = currentNode;
    currentNode = currentNode->getNode(currentNode->getNumberOfNodes() - 1);
  }

  Node *newNode = new Node(*newValue.root);

  if (currentNode->getNodeType() == ARGUMENT)
  {
    result.removeArgument(currentNode->getValue());
  }

  if (parent != NULL)
  {
    parent->setNode(parent->getNumberOfNodes() - 1, *newNode);
  }
  else
  {
    result.root = newNode;
  }

  for (int i = 0; i < newValue.argsVector.size(); i++)
  {
    result.setArgumentValue(newValue.argsVector[i], getDefaultNoop());
  }

  return result;
}

template <typename T>
Tree<T> Tree<T>::operator+(Tree<T> &&newValue) const
{
  std::cout << "TREE PLUS MOVE" << std::endl;
  Tree result = *this;
  std::cout << "AFTER COPY" << std::endl;

  if (result.root == NULL)
  {
    result.root = newValue.root;
    newValue.root = NULL;
  }

  Node *currentNode = result.root;

  Node *parent = NULL;

  while (currentNode->getNumberOfNodes() > 0)
  {
    parent = currentNode;
    currentNode = currentNode->getNode(currentNode->getNumberOfNodes() - 1);
  }

  if (currentNode->getNodeType() == ARGUMENT)
  {
    result.removeArgument(currentNode->getValue());
  }

  if (parent != NULL)
  {
    parent->setNode(parent->getNumberOfNodes() - 1, std::move(*newValue.root));
  }
  else
  {
    result.root = newValue.root;
  }

  for (int i = 0; i < newValue.argsVector.size(); i++)
  {
    result.setArgumentValue(newValue.argsVector[i], getDefaultNoop());
  }

  return std::move(result);
}

template <typename T>
std::string Tree<T>::getErrorAndClear()
{
  std::string error = this->errorStream.str();

  errorStream.str("");

  return error;
}

template <typename T>
void Tree<T>::printNodes() const
{
  if (root != NULL)
  {
    for (int i = 0; i < root->getNumberOfNodes(); i++)
    {
      std::cout << root->getNode(i)->toString() << std::endl;
    }
  }
}

template <typename T>
std::string Tree<T>::getKnownType()
{
  return "UNKNOWN";
}

template <>
std::string Tree<int>::getKnownType()
{
  return "INT";
}

template <>
std::string Tree<double>::getKnownType()
{
  return "DOUBLE";
}

template <>
std::string Tree<std::string>::getKnownType()
{
  return "STRING";
}

template <>
std::string Tree<bool>::getKnownType()
{
  return "BOOL";
}

template <typename T>
T Tree<T>::comp(Node *currentNode)
{
  if (currentNode->getNodeType() == VALUE)
  {
    return stringToValue(currentNode->getValue());
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
      if (getKnownType() == "BOOL")
      {
        return !(comp(currentNode->getNode(0)) * comp(currentNode->getNode(1)));
      }

      T secondNodeValue = comp(currentNode->getNode(1));

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
    typename std::map<std::string, T>::const_iterator argsIterator = argsMap.find(currentNode->getValue());

    if (argsIterator == argsMap.end())
    {
      errorStream << "Error: Unknown argument: " << currentNode->getValue() << std::endl;
      return getDefaultNoop();
    }

    return argsIterator->second;
  }

  return getDefaultNoop();
}

template <typename T>
bool Tree<T>::isError()
{
  return errorStream.str().length() > 0;
}

template <>
std::string Tree<std::string>::comp(Node *currentNode)
{
  if (currentNode->getNodeType() == VALUE)
  {
    return stringToValue(currentNode->getValue());
  }
  else if (currentNode->getNodeType() == OPERATOR)
  {
    if (currentNode->getValue() == "+")
    {
      return comp(currentNode->getNode(0)) + comp(currentNode->getNode(1));
    }
    else if (currentNode->getValue() == "-")
    {
      std::string firstNodeValue = comp(currentNode->getNode(0));

      int pos = firstNodeValue.rfind(comp(currentNode->getNode(1)));

      if (pos != std::string::npos)
      {
        firstNodeValue.erase(pos, comp(currentNode->getNode(0)).length());
      }

      return firstNodeValue;
    }
    else if (currentNode->getValue() == "*")
    {

      std::string secondValue = comp(currentNode->getNode(1));
      std::string firstValue = comp(currentNode->getNode(0));

      if (secondValue.length() < 1)
      {
        return firstValue;
      }

      std::string newString = "";

      std::string stringToCopy = secondValue.substr(1);

      for (int i = 0; i < firstValue.length(); i++)
      {
        newString += firstValue[i];
        if (firstValue[i] == secondValue[0])
        {
          newString += stringToCopy;
        }
      }

      return newString;
    }
    else if (currentNode->getValue() == "/")
    {
      std::string secondValue = comp(currentNode->getNode(1));
      std::string firstValue = comp(currentNode->getNode(0));

      if (secondValue.length() < 1)
      {
        return firstValue;
      }

      std::string newString = "";

      for (int i = 0; i < firstValue.length(); i++)
      {
        newString += firstValue[i];

        if (firstValue.substr(i, secondValue.length()) == secondValue)
        {
          i += secondValue.length() - 1;
        }
      }

      return newString;
    }
  }
  else if (currentNode->getNodeType() == ARGUMENT)
  {
    std::map<std::string, std::string>::const_iterator argsIterator = argsMap.find(currentNode->getValue());

    if (argsIterator == argsMap.end())
    {
      errorStream << "Error: Unknown argument: " << currentNode->getValue() << std::endl;
      return getDefaultNoop();
    }

    return argsIterator->second;
  }

  return getDefaultNoop();
}

template <typename T>
bool Tree<T>::isValidValue(std::string value)
{
  return true;
}

template <>
bool Tree<int>::isValidValue(std::string value)
{
  return value.find_first_not_of(LIST_OF_NUMBERS) == std::string::npos;
}

template <>
bool Tree<double>::isValidValue(std::string value)
{
  double ld = 0;
  return ((std::istringstream(value) >> ld >> std::ws).eof());
}

template <>
bool Tree<std::string>::isValidValue(std::string value)
{
  if (value.length() < 3)
  {
    return false;
  }

  if (value.at(0) != '"' || value.at(value.length() - 1) != '"')
  {
    return false;
  }

  return true;
}

template <typename T>
std::string Tree<T>::getDefaultValue()
{
  return DEFAULT_NODE_VALUE;
}

template <>
std::string Tree<std::string>::getDefaultValue()
{
  return DEFAULT_STRING_NODE_VALUE;
}

template <>
std::string Tree<bool>::getDefaultValue()
{
  return DEFAULT_NODE_VALUE;
}

template <typename T>
bool Tree<T>::isValidArgument(std::string value)
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
      errorStream << "Invalid character ignored: " << value[i] << std::endl;
    }
  }

  return hasLetter;
}

template <typename T>
void Tree<T>::setArgumentValue(std::string arg, T value)
{
  typename std::map<std::string, T>::const_iterator argsIterator = argsMap.find(arg);

  if (argsIterator == argsMap.end())
  {
    argsVector.push_back(arg);
  }

  argsMap[arg] = value;
}

template <typename T>
void Tree<T>::removeArgument(std::string arg)
{
  typename std::map<std::string, T>::const_iterator argsIterator = argsMap.find(arg);

  if (argsIterator != argsMap.end())
  {
    argsMap.erase(arg);
  }

  for (int i = 0; i < argsVector.size(); i++)
  {
    if (argsVector[i] == arg)
    {
      argsVector.erase(argsVector.begin() + i);
      break;
    }
  }
}

template <typename T>
void Tree<T>::setArgumentValueByIndex(int index, T value)
{
  if (index >= argsVector.size())
  {
    return;
  }

  argsMap[argsVector[index]] = value;
}

#endif

template <typename T>
Tree<T>::Tree(Tree &&other) noexcept : root(other.root),
                                       argsMap(std::move(other.argsMap)),
                                       argsVector(std::move(other.argsVector))
{

  other.root = nullptr;

  errorStream << other.errorStream.str();

  other.errorStream.str("");
}

template <typename T>
Tree<T> &Tree<T>::operator=(Tree<T> &&newValue)
{
  std::cout << "TREE MOVE" << std::endl;
  if (this != &newValue)
  {
    delete root;
    root = newValue.root;
    newValue.root = nullptr;

    argsMap = std::move(newValue.argsMap);
    argsVector = std::move(newValue.argsVector);

    errorStream.str(newValue.errorStream.str());
    newValue.errorStream.str("");
  }

  return *this;
}
