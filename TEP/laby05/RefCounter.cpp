#include "RefCounter.h"

RefCounter::RefCounter() : refCount(0)
{
}

int RefCounter::add()
{
  return ++refCount;
}

int RefCounter::dec()
{
  return --refCount;
}

int RefCounter::get()
{
  return refCount;
}
