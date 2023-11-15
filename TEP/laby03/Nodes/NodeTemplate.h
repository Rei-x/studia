#include "Node.h"
#include <string>

class NodeTemplate
{
public:
  virtual bool isApplicable(const std::string &formule, int start) const = 0;
  virtual int execute(Node *nodes) const = 0;
  virtual ~NodeTemplate(){};
  virtual int getNumberOfArguments() const = 0;
};