#pragma once
#include <vector>
class IEvaluator
{
public:
	virtual double dEvaluate(std::vector<int>* pvSolution) = 0;
	virtual int iGetNumberOfValues(int iPairOffset) = 0;
	virtual int iGetNumberOfBits() = 0;
};

