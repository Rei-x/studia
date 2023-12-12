#include <string>
#include <vector>

std::vector<std::string> splitStringByWhitespace(std::string str)
{
  std::vector<std::string> result;

  std::string currentString = "";

  for (int i = 0; i < str.length(); i++)
  {
    if (str[i] == ' ')
    {
      if (currentString.length() > 0)
      {
        result.push_back(currentString);
        currentString = "";
      }
    }
    else
    {
      currentString += str[i];
    }
  }

  if (currentString.length() > 0)
  {
    result.push_back(currentString);
  }

  return result;
}

std::string join(std::vector<std::string> strings)
{
  std::string result = "";

  for (int i = 0; i < strings.size(); i++)
  {
    result += strings[i] + " ";
  }

  if (strings.size() > 0)
  {
    result = result.substr(0, result.length() - 1);
  }

  return result;
}