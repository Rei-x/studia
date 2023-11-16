#include <string>

std::string *splitStringByWhitespace(std::string str, int *size)
{
  std::string *result = new std::string[str.length()];

  int resultIndex = 0;

  std::string currentString = "";

  for (int i = 0; i < str.length(); i++)
  {
    if (str[i] == ' ')
    {
      if (currentString.length() > 0)
      {
        result[resultIndex] = currentString;
        resultIndex++;
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
    result[resultIndex] = currentString;
    resultIndex++;
  }

  *size = resultIndex;

  return result;
}