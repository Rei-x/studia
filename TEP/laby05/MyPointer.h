#ifndef MYPOINTER_H
#define MYPOINTER_H
#include "RefCounter.h"

template <typename T>
class MyPointer
{
public:
  MyPointer(T *pcPointer);
  MyPointer(const MyPointer &pcOther);
  ~MyPointer();
  MyPointer &operator=(const MyPointer &pcOther);

  T &operator*();
  T *operator->();

  int getCounter() const;

private:
  RefCounter *pc_counter;
  T *pc_pointer;
};

template <typename T>
MyPointer<T>::MyPointer(T *pcPointer) : pc_counter(new RefCounter()), pc_pointer(pcPointer)
{
  pc_counter->add();
}

template <typename T>
MyPointer<T>::MyPointer(const MyPointer &pcOther) : pc_counter(pcOther.pc_counter), pc_pointer(pcOther.pc_pointer)
{
  pc_counter->add();
}

template <typename T>
MyPointer<T>::~MyPointer()
{
  if (pc_counter->dec() == 0)
  {
    delete pc_pointer;
    delete pc_counter;
  }
}

template <typename T>
MyPointer<T> &MyPointer<T>::operator=(const MyPointer &pcOther)
{
  if (pc_counter->dec() == 0)
  {
    delete pc_pointer;
    delete pc_counter;
  }
  pc_counter = pcOther.pc_counter;
  pc_pointer = pcOther.pc_pointer;
  pc_counter->add();
  return *this;
}

template <typename T>
int MyPointer<T>::getCounter() const
{
  return pc_counter->get();
}
template <typename T>
T &MyPointer<T>::operator*()
{
  return *pc_pointer;
}

template <typename T>
T *MyPointer<T>::operator->()
{
  return pc_pointer;
}

#endif