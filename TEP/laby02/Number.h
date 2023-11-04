#define DEFAULT_NUMBER_LENGTH 0
#include <string>
class Number
{
public:
  Number();
  Number(const Number &other);
  ~Number();
  Number &operator=(const Number &newValue);
  Number &operator=(int newValue);
  Number operator+(Number &newValue);
  Number operator*(Number &newValue);
  Number operator-(Number &newValue);
  Number operator/(Number &newValue);
  bool isLargerThan(Number *other);
  std::string toString();

private:
  int *numbers;
  int length;
  bool isNegative;

  void reduceTableSize();
};