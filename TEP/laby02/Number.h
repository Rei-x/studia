#define DEFAULT_NUMBER_LENGTH 1
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
  Number getFirstXNumbers(int n);
  Number getLastXNumbers(int n);
  Number partial(int start, int end);
  void append(int digit);
  bool operator>(Number &newValue);
  bool operator<(Number &newValue);
  bool operator>=(Number &newValue);
  bool operator<=(Number &newValue);
  bool operator==(Number &newValue);
  std::string toString();

private:
  int *numbers;
  int length;
  bool isNegative;

  void reduceTableSize();
};