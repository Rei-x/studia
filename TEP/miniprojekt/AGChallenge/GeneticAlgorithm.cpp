#include "GeneticAlgorithm.h"

GeneticAlgorithm::GeneticAlgorithm(int populationSize, float crossProbability, float mutationProbability, IEvaluator& evaluator)
	: evaluator(evaluator), crossProbability(crossProbability), mutationProbability(mutationProbability)
{
	initializePopulation(populationSize);
	bestIndividual = new Individual(*population.at(0));
}

GeneticAlgorithm::~GeneticAlgorithm()
{
	if (bestIndividual != NULL) {
		delete bestIndividual;
	}

	for (int i = 0; i < population.size(); i++) {
		delete population.at(i);
	}
}

void GeneticAlgorithm::runOneIteration()
{
	vector<Individual*> newPopulation;
	while (false)
	{
		Individual* candidate1 = population[dRand() * population.size()];
		Individual* candidate2 = population[dRand() * population.size()];

		Individual* parent1 = candidate1->getFitness() > candidate2->getFitness() ? new Individual(*candidate1) : new Individual(*candidate2);

		Individual* candidate3 = population[dRand() * population.size()];
		Individual* candidate4 = population[dRand() * population.size()];

		Individual* parent2 = candidate3->getFitness() > candidate4->getFitness() ? new Individual(*candidate3) : new Individual(*candidate4);

		if (dRand() < crossProbability)
		{
			std::pair<Individual*, Individual*> childrens = parent1->cross(parent2);
			newPopulation.push_back(childrens.first);
			newPopulation.push_back(childrens.second);

			delete parent1, parent2;
		}
		else
		{
			newPopulation.push_back(parent1);
			newPopulation.push_back(parent2);
		}
	}
	while (newPopulation.size() < population.size()) {
		Individual* candidat = population[dRand() * population.size()];

		vector<Individual*> newIndividuals = std::move(candidat->mutate());

		for (int i = 0; i < newIndividuals.size(); i++) {

			newPopulation.push_back(newIndividuals.at(i));
		}
	}

	while (newPopulation.size() > population.size()) {
		delete newPopulation.back();
		newPopulation.pop_back();
	}

	for (int i = 0; i < newPopulation.size(); i++)
	{
		newPopulation.at(i)->mutate(mutationProbability);
	}

	for (int i = 0; i < population.size(); i++) {
		delete population[i];
	}

	population = newPopulation;
}

void GeneticAlgorithm::runIterations(int numberOfIterations)
{

	for (int i = 0; i < numberOfIterations; i++) {
		runOneIteration();
		evaluatePopulation();
		cout << getBestCandidat()->getFitness() << endl;
	}

}

Individual* GeneticAlgorithm::getBestCandidat()
{
	return bestIndividual;
}

void GeneticAlgorithm::initializePopulation(int populationSize)
{
	for (int i = 0; i < populationSize; i++)
	{
		std::vector<int> genotype;
		size_t genotypeSize = (size_t)evaluator.iGetNumberOfBits();

		for (size_t j = 0; j < genotypeSize; j++)
		{
			genotype.push_back(lRand(evaluator.iGetNumberOfValues(j)));
		}

		population.push_back(new Individual(std::move(genotype), evaluator));
	}

}

void GeneticAlgorithm::evaluatePopulation()
{
	Individual* oldBest = bestIndividual;

	for (int i = 0; i < population.size(); i++)
	{
		if (population.at(i)->getFitness() > oldBest->getFitness()) {
			oldBest = population.at(i);
		}
	}

	bestIndividual = new Individual(*oldBest);
}
