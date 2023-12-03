#include "UIInterface.h"
#include "Tree.h"
#include "stringUtils.h"
#include <iostream>

void UIInterface::startUI()
{
  Tree<int> startingTree;

  while (true)
  {
    std::string command;
    std::getline(std::cin, command);
    int size = 0;
    std::string *args = splitStringByWhitespace(command, &size);

    if (size == 0)
    {
      continue;
    }

    if (args[0] == "exit")
    {
      break;
    }
    else if (args[0] == "enter")
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
    else if (args[0] == "vars")
    {
      std::cout << startingTree.getArgumentsList() << std::endl;
    }
    else if (args[0] == "print")
    {
      std::cout << startingTree.toString() << std::endl;
    }
    else if (args[0] == "comp")
    {
      std::string formula = join(args + 1, size - 1);
      int result = startingTree.comp(formula);

      if (result != -1)
      {
        std::cout << "Wynik: " << result << std::endl;
      }
      else
      {
        std::cout << startingTree.getErrorAndClear() << std::endl;
      }
    }
    else if (args[0] == "join")
    {
      if (size < 2)
      {
        std::cout << "Invalid command, use: " << args[0] << " <tree>" << std::endl;
        continue;
      }

      std::string formula = join(args + 1, size - 1);

      Tree<int> tree;
      tree.parseFormula(formula);

      std::cout << tree.getErrorAndClear() << std::endl;

      startingTree = startingTree + tree;
    }
    else if (args[0] == "help")
    {
      std::cout << "Commands:" << std::endl;
      std::cout << "enter <formula>" << std::endl;
      std::cout << "vars" << std::endl;
      std::cout << "print" << std::endl;
      std::cout << "comp <arg0> <arg1> <arg2> ..." << std::endl;
      std::cout << "join <tree>" << std::endl;
      std::cout << "exit" << std::endl;
    }
    else
    {
      std::cout << "Invalid command" << std::endl;
    }
  }
}