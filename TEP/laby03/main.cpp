#include "Tree.h"
#include "stringUtils.h"
#include <iostream>

bool startsWith(std::string str, std::string prefix)
{
  return str.rfind(prefix, 0) == 0;
}

int main()
{
  Tree startingTree;

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
        continue;
      }

      std::string formula = "";

      for (int i = 1; i < size; i++)
      {
        formula += args[i] + " ";
      }

      formula = formula.substr(0, formula.length() - 1);

      startingTree.parseFormula(formula);
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
      std::string formula = "";

      for (int i = 1; i < size; i++)
      {
        formula += args[i] + " ";
      }

      if (size > 1)
      {
        formula = formula.substr(0, formula.length() - 1);
      }

      std::cout << startingTree.comp(formula) << std::endl;
    }
    else if (args[0] == "join")
    {
      std::cout << "Join" << std::endl;
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