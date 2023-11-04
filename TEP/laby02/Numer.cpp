#include "Number.h"
#include <cstdlib>
#include <iostream>
#include <string>

Number::Number() : numbers(new int[DEFAULT_NUMBER_LENGTH]), length(DEFAULT_NUMBER_LENGTH), isNegative(false)
{
  for (int i = 0; i < length; i++)
  {
    numbers[i] = 0;
  }
}

Number::~Number()
{
  std::cout << "DESTRUKCJA: " << this->toString() << std::endl;
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

  // delete[] numbers;
}

Number &Number::operator=(const Number &newValue)
{
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
  this->isNegative = newValue < 0;
  int absoluteNewValue = abs(newValue);
  int temp = absoluteNewValue;

  int newLength = 0;
  while (temp > 0)
  {
    temp /= 10;
    newLength++;
  }

  int i = 0;
  this->numbers = new int[newLength];
  this->length = newLength;

  for (int i = 0; i < length; i++)
  {
    this->numbers[i] = absoluteNewValue % 10;
    absoluteNewValue /= 10;
  }

  return *this;
}

Number Number::operator+(Number &newValue)
{
  int newLen = this->length > newValue.length ? this->length : newValue.length;
  int *result = new int[newLen + 1];

  int carry = 0;

  for (int i = 0; i < newLen; i++)
  {
    int sum = this->numbers[i] + newValue.numbers[i] + carry;
    result[i] = sum % 10;
    carry = sum / 10;
  }

  result[newLen] = carry;

  Number newNumber;

  newNumber.length = newLen + 1;
  newNumber.numbers = result;

  newNumber.reduceTableSize();

  return newNumber;
}

Number Number::operator-(Number &newValue)
{
  int maxLen = std::max(this->length, newValue.length);

  // Create temporary arrays to store reversed numbers
  int *temp1 = new int[maxLen];
  int *temp2 = new int[maxLen];

  // Initialize temporary arrays with the numbers, padding with zeros if necessary
  for (int i = 0; i < maxLen; i++)
  {
    temp1[i] = (i < this->length) ? this->numbers[i] : 0;
    temp2[i] = (i < newValue.length) ? newValue.numbers[i] : 0;
  }

  // Subtract temp2 from temp1, considering borrow
  int borrow = 0;
  int *result = new int[maxLen];

  for (int i = 0; i < maxLen; i++)
  {
    int diff = temp1[i] - temp2[i] - borrow;
    if (diff < 0)
    {
      diff += 10;
      borrow = 1;
    }
    else
    {
      borrow = 0;
    }

    result[i] = diff;
  }

  // Create a new Number object to hold the result
  Number newNumber;

  // If there's a leading zero in the result, reduce the length
  int newLen = maxLen;
  if (result[maxLen - 1] == 0)
  {
    newLen--;
  }

  // Set the properties of the new Number object
  newNumber.isNegative = (this->isNegative && !newValue.isNegative) || (!this->isNegative && newValue.isNegative);
  newNumber.length = newLen;
  newNumber.numbers = new int[newLen];
  for (int i = 0; i < newLen; i++)
  {
    newNumber.numbers[i] = result[i];
  }

  newNumber.reduceTableSize();

  // Clean up temporary arrays
  delete[] temp1;
  delete[] temp2;
  delete[] result;

  return newNumber;
}
