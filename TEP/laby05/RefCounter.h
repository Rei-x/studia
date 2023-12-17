class RefCounter
{
public:
  RefCounter();
  int add();
  int dec();
  int get();

private:
  int refCount;
};