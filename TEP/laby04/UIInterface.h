#include "Tree.h"
#include "stringUtils.h"
#include <iostream>

#define EXIT_COMMAND "exit"
#define ENTER_COMMAND "enter"
#define VARS_COMMAND "vars"
#define PRINT_COMMAND "print"
#define COMP_COMMAND "comp"
#define JOIN_COMMAND "join"
#define HELP_COMMAND "help"

template <typename T>
class UIInterface
{
public:
  static void startUI();
};

template <typename T>
void UIInterface<T>::startUI()
{
  Tree<T> startingTree;

  while (true)
  {
    std::string command;
    std::getline(std::cin, command);
    int size = 0;
    std::string *args = splitStringByWhitespace(command, &size);

    if (size == 0)
    {
    }
    else if (args[0] == EXIT_COMMAND)
    {
      return;
    }
    else if (args[0] == ENTER_COMMAND)
    {
      if (size < 2)
      {
        std::cout << "Invalid command, use: " << args[0] << " <formula>" << std::endl;
      }
      else
      {
        std::string formula = join(args + 1, size - 1);
        startingTree.parseFormula(formula);
        std::cout << startingTree.getErrorAndClear() << std::endl;
      }
    }
    else if (args[0] == VARS_COMMAND)
    {
      std::cout << startingTree.getArgumentsList() << std::endl;
    }
    else if (args[0] == PRINT_COMMAND)
    {
      std::cout << startingTree.toString() << std::endl;
    }
    else if (args[0] == COMP_COMMAND)
    {
      std::string formula = join(args + 1, size - 1);

      T result = startingTree.comp(formula);

      if (startingTree.getKnownType() == BOOL_NAME && !startingTree.isError())
      {
        std::cout << "Wynik: " << (result ? "true" : "false") << std::endl;
      }
      else if (startingTree.getKnownType() != BOOL_NAME && !startingTree.isError())
      {

        std::cout << "Wynik: " << result << std::endl;
      }
      else
      {
        std::cout << startingTree.getErrorAndClear() << std::endl;
      }
    }
    else if (args[0] == JOIN_COMMAND)
    {
      if (size < 2)
      {
        std::cout << "Invalid command, use: " << args[0] << " <tree>" << std::endl;
        continue;
      }

      std::string formula = join(args + 1, size - 1);

      Tree<T> tree;
      tree.parseFormula(formula);

      std::cout << tree.getErrorAndClear() << std::endl;

      startingTree = startingTree + tree;
    }
    else if (args[0] == HELP_COMMAND)
    {
      std::cout << "Commands:" << std::endl;
      std::cout << ENTER_COMMAND << " <formula>" << std::endl;
      std::cout << VARS_COMMAND << std::endl;
      std::cout << PRINT_COMMAND << std::endl;
      std::cout << COMP_COMMAND << " <arg0> <arg1> <arg2> ..." << std::endl;
      std::cout << JOIN_COMMAND << " <tree>" << std::endl;
      std::cout << EXIT_COMMAND << std::endl;
    }
    else
    {
      std::cout << "Invalid command" << std::endl;
    }
  }
}