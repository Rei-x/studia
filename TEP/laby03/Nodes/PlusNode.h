#include "NodeTemplate.h"

class PlusNode : public NodeTemplate
{
public:
  bool isApplicable(const std::string &formule, int start) const;
  int execute(Node *nodes) const;
  int getNumberOfArguments() const;
  ~PlusNode(){};
};