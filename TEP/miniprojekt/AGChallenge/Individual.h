#pragma once
#include <vector>
#include "Evaluator.h"
#include "MyMath.h"

class Individual
{
private:
	std::vector<int> genotype;
	IEvaluator& evaluator;
	double fitness;
	bool isFitnessStale;
public:
	Individual(std::vector<int>&& genotype, IEvaluator& evaluator);
	Individual(Individual&& other);
	Individual(const Individual& other);
	double getFitness();
	void mutate(float probability);
	std::vector<Individual*> mutate();
	std::pair<Individual*, Individual*> cross(Individual* other);
	std::string toString();
};

