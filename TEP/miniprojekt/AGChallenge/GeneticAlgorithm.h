#pragma once
#include <vector>
#include "Individual.h"
class GeneticAlgorithm
{
public:
	GeneticAlgorithm(int populationSize, float crossProbability, float mutationProbability, IEvaluator* evaluator);
	void runOneIteration();
	void runIterations(int numberOfIterations);
	Individual getBestCandidat();
private:
	std::vector<Individual> population;
	IEvaluator* evaluator;
	Individual bestIndividual;
	float crossProbability;
	float mutationProbability;
	void initializePopulation(int populationSize);
	void evaluatePopulation();
};

