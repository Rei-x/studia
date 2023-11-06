#include "Number.h"
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>

Number::Number() : numbers(new int[DEFAULT_NUMBER_LENGTH]), length(DEFAULT_NUMBER_LENGTH), isNegative(false)
{
  for (int i = 0; i < length; i++)
  {
    numbers[i] = 0;
  }
}

Number::Number(const Number &other) : numbers(new int[other.length]), length(other.length), isNegative(other.isNegative)
{
  for (int i = 0; i < length; i++)
  {
    numbers[i] = other.numbers[i];
  }
}

Number::~Number()
{
  delete[] numbers;
}

std::string Number::toString()
{
  std::string result = "";

  if (isNegative)
  {
    result += "-";
  }

  for (int i = length - 1; i >= 0; i--)
  {
    char c = '0' + numbers[i];

    result += c;
  }

  return result;
}

void Number::reduceTableSize()
{
  while (this->length > 1 && this->numbers[this->length - 1] == 0)
  {
    this->length--;
  }

  int *newNumbers = new int[this->length];

  for (int i = 0; i < this->length; i++)
  {
    newNumbers[i] = this->numbers[i];
  }
  delete[] this->numbers;
  this->numbers = newNumbers;
}

Number &Number::operator=(const Number &newValue)
{
  if (this == &newValue)
  {
    return *this;
  }

  this->isNegative = newValue.isNegative;
  this->length = newValue.length;

  delete[] this->numbers;

  this->numbers = new int[length];

  for (int i = 0; i < length; i++)
  {
    this->numbers[i] = newValue.numbers[i];
  }

  return *this;
}

Number &Number::operator=(int newValue)
{
  delete[] this->numbers;

  this->isNegative = newValue < 0;
  int absoluteNewValue = abs(newValue);
  int temp = absoluteNewValue;

  int newLength = 0;
  while (temp > 0)
  {
    temp /= NUMBER_BASE;
    newLength++;
  }

  int i = 0;
  this->length = newLength == 0 ? 1 : newLength;
  this->numbers = new int[this->length];

  for (int i = 0; i < length; i++)
  {
    this->numbers[i] = absoluteNewValue % NUMBER_BASE;
    absoluteNewValue /= NUMBER_BASE;
  }

  return *this;
}

bool Number::operator>(Number &newValue)
{
  if (this->isNegative && !newValue.isNegative)
  {
    return false;
  }
  else if (!this->isNegative && newValue.isNegative)
  {
    return true;
  }
  else if (this->isNegative && newValue.isNegative)
  {
    Number negatedNewValue = newValue;
    negatedNewValue.isNegative = !negatedNewValue.isNegative;
    return !(*this < negatedNewValue);
  }

  if (this->length > newValue.length)
  {
    return true;
  }
  else if (this->length < newValue.length)
  {
    return false;
  }

  for (int i = this->length - 1; i >= 0; i--)
  {
    // NOLINTNEXTLINE
    if (this->numbers[i] > newValue.numbers[i])
    {
      return true;
    }
    else if (this->numbers[i] < newValue.numbers[i])
    {
      return false;
    }
  }

  return false;
}

bool Number::operator<(Number &newValue)
{
  if (this->isNegative && !newValue.isNegative)
  {
    return true;
  }
  else if (!this->isNegative && newValue.isNegative)
  {
    return false;
  }
  else if (this->isNegative && newValue.isNegative)
  {
    Number negatedNewValue = newValue;
    negatedNewValue.isNegative = !negatedNewValue.isNegative;
    return !(*this > negatedNewValue);
  }

  if (this->length < newValue.length)
  {
    return true;
  }
  else if (this->length > newValue.length)
  {
    return false;
  }

  for (int i = this->length - 1; i >= 0; i--)
  {
    if (this->numbers[i] < newValue.numbers[i])
    {
      return true;
    }
    else if (this->numbers[i] > newValue.numbers[i])
    {
      return false;
    }
  }

  return false;
}

Number Number::operator+(Number &newValue)
{
  if (this->isNegative && !newValue.isNegative)
  {
    Number negatedThis = *this;
    negatedThis.isNegative = !negatedThis.isNegative;
    return newValue - negatedThis;
  }
  else if (!this->isNegative && newValue.isNegative)
  {
    Number negatedNewValue = newValue;
    negatedNewValue.isNegative = !negatedNewValue.isNegative;
    return *this - negatedNewValue;
  }
  else if (this->isNegative && newValue.isNegative)
  {
    Number negatedThis = *this;
    negatedThis.isNegative = !negatedThis.isNegative;
    Number negatedNewValue = newValue;
    negatedNewValue.isNegative = !negatedNewValue.isNegative;
    Number result = negatedThis + negatedNewValue;
    result.isNegative = true;
    return result;
  }

  int newLen = this->length > newValue.length ? this->length : newValue.length;
  int *result = new int[newLen + 1];

  int carry = 0;

  for (int i = 0; i < newLen; i++)
  {
    if (i >= this->length)
    {
      result[i] = newValue.numbers[i] + carry;
    }
    else if (i >= newValue.length)
    {
      result[i] = this->numbers[i] + carry;
    }
    else
    {
      result[i] = this->numbers[i] + newValue.numbers[i] + carry;
    }

    if (result[i] >= NUMBER_BASE)
    {
      result[i] -= NUMBER_BASE;
      carry = 1;
    }
    else
    {
      carry = 0;
    }
  }

  result[newLen] = carry;

  Number newNumber;
  delete[] newNumber.numbers;
  newNumber.length = newLen + 1;
  newNumber.numbers = result;

  newNumber.reduceTableSize();

  return newNumber;
}

Number Number::operator-(Number &newValue)
{
  if (newValue.isNegative)
  {
    Number negatedNewValue = newValue;
    negatedNewValue.isNegative = !negatedNewValue.isNegative;
    return *this + negatedNewValue;
  }

  if (*this < newValue)
  {
    Number result = newValue - *this;
    result.isNegative = true;
    return result;
  }

  int newLen = this->length > newValue.length ? this->length : newValue.length;
  int *result = new int[newLen];

  int carry = 0;

  for (int i = 0; i < newLen; i++)
  {
    if (i >= this->length)
    {
      result[i] = newValue.numbers[i] - carry;
    }
    else if (i >= newValue.length)
    {
      result[i] = this->numbers[i] - carry;
    }
    else
    {
      result[i] = this->numbers[i] - newValue.numbers[i] - carry;
    }

    if (result[i] < 0)
    {
      result[i] += NUMBER_BASE;
      carry = 1;
    }
    else
    {
      carry = 0;
    }
  }

  Number newNumber;

  delete[] newNumber.numbers;

  newNumber.length = newLen;
  newNumber.numbers = result;

  newNumber.reduceTableSize();

  return newNumber;
}

Number Number::operator*(Number &newValue)
{
  int newLen = this->length + newValue.length;
  int *result = new int[newLen];

  for (int i = 0; i < newLen; i++)
  {
    result[i] = 0;
  }

  for (int i = 0; i < this->length; i++)
  {
    for (int j = 0; j < newValue.length; j++)
    {
      // NOLINTNEXTLINE
      result[i + j] += this->numbers[i] * newValue.numbers[j];
    }
  }

  for (int i = 0; i < newLen - 1; i++)
  {
    // NOLINTNEXTLINE
    result[i + 1] += result[i] / NUMBER_BASE;
    result[i] %= NUMBER_BASE;
  }

  Number newNumber;

  delete[] newNumber.numbers;

  newNumber.length = newLen;
  newNumber.numbers = result;

  newNumber.reduceTableSize();

  if (this->isNegative != newValue.isNegative && !(newNumber.length == 1 && newNumber.numbers[0] == 0))
  {
    newNumber.isNegative = true;
  }

  return newNumber;
}

Number Number::operator/(Number &newValue)
{
  Number zeroNumber, baseNumber;
  zeroNumber = 0;
  baseNumber = NUMBER_BASE;

  if (newValue == zeroNumber)
  {
    return zeroNumber;
  }

  Number currentNumber = *this;
  currentNumber.isNegative = false;
  Number divisor = newValue;
  divisor.isNegative = false;

  if (currentNumber < divisor)
  {
    return zeroNumber;
  }

  int newLen = currentNumber.length - divisor.length + 1;
  int *result = new int[newLen];

  for (int i = 0; i < newLen; i++)
  {
    result[i] = 0;
  }

  int currentIndex = 1;
  int insertIndex = 0;
  int currentDividendIndex = 0;
  while (currentDividendIndex < this->length)
  {
    Number temp;
    temp = currentNumber.getFirstXNumbers(currentIndex);

    while (temp < divisor && !((currentIndex - 1) == currentNumber.length))
    {
      currentIndex++;
      currentDividendIndex++;
      temp = currentNumber.getFirstXNumbers(currentIndex);
    }

    int digit = 0;

    Number tempReduced = temp;
    tempReduced.reduceTableSize();
    while (temp >= divisor && !(tempReduced == zeroNumber))
    {
      temp = temp - divisor;
      digit++;
    }

    result[insertIndex] = digit;
    insertIndex++;

    if ((currentNumber.length - currentIndex) > 0)
    {
      currentNumber = currentNumber.getLastXNumbers(currentNumber.length - currentIndex);
    }
    tempReduced = temp;
    tempReduced.reduceTableSize();

    if (!(tempReduced == zeroNumber))
    {
      for (int i = 0; i < temp.length; i++)
      {

        currentNumber.append(temp.numbers[i]);
      }
    }

    currentIndex = 1;
    currentDividendIndex++;
  }
  Number newNumber;

  delete[] newNumber.numbers;
  newNumber.length = insertIndex;

  int *realResult = new int[insertIndex];

  for (int i = 0; i < insertIndex; i++)
  {
    realResult[i] = result[i];
  }

  delete[] result;

  for (int i = 0; i < insertIndex / 2; i++)
  {
    int temp = realResult[i];
    realResult[i] = realResult[insertIndex - 1 - i];
    realResult[insertIndex - 1 - i] = temp;
  }

  newNumber.numbers = realResult;

  if (this->isNegative != newValue.isNegative && !(newNumber.length == 1 && newNumber.numbers[0] == 0))
  {
    newNumber.isNegative = true;
  }

  return newNumber;
}

Number Number::getFirstXNumbers(int n)
{
  Number newNumber;
  delete[] newNumber.numbers;
  newNumber.length = n;
  newNumber.numbers = new int[n];

  for (int i = 0; i < n; i++)
  {
    newNumber.numbers[n - 1 - i] = this->numbers[this->length - 1 - i];
  }

  return newNumber;
}

Number Number::getLastXNumbers(int n)
{
  Number newNumber;
  delete[] newNumber.numbers;
  newNumber.length = n;
  newNumber.numbers = new int[n];

  for (int i = 0; i < n; i++)
  {
    newNumber.numbers[i] = this->numbers[i];
  }

  return newNumber;
}

void Number::append(int digit)
{
  int *newNumbers = new int[this->length + 1];

  for (int i = 0; i < this->length; i++)
  {
    newNumbers[i] = this->numbers[i];
  }

  newNumbers[this->length] = digit;

  this->length++;

  delete[] this->numbers;

  this->numbers = newNumbers;
}

bool Number::operator>=(Number &newValue)
{
  return *this > newValue || *this == newValue;
}

bool Number::operator<=(Number &newValue)
{
  return *this < newValue || *this == newValue;
}

bool Number::operator==(Number &newValue)
{
  if (this->isNegative != newValue.isNegative)
  {
    return false;
  }

  if (this->length != newValue.length)
  {
    return false;
  }

  for (int i = 0; i < this->length; i++)
  {
    if (this->numbers[i] != newValue.numbers[i])
    {
      return false;
    }
  }

  return true;
}
