#pragma once
#include <vector>
#include "Evaluator.h"
#include "MyMath.h"
class Individual
{
private:
	std::vector<int> genotype;
	IEvaluator* evaluator;
	double fitness;
public:
	Individual(std::vector<int> genotype, IEvaluator* evaluator);
	Individual();
	double getFitness();
	void mutate(float probability);
	std::vector<Individual> cross(Individual& other);
	Individual& operator=(const Individual& other);
	std::string toString();
};

