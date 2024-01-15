#include "Individual.h"
#include <sstream>
#include <tuple>

Individual::Individual(std::vector<int>&& genotype, IEvaluator& evaluator) : genotype(genotype), evaluator(evaluator), fitness(NULL), isFitnessStale(true)
{
}

Individual::Individual(Individual&& other) : evaluator(other.evaluator)
{
	genotype = std::move(other.genotype);
}

Individual::Individual(const Individual& other) : evaluator(other.evaluator), genotype(other.genotype), fitness(other.fitness), isFitnessStale(other.isFitnessStale)
{
}

double Individual::getFitness()
{
	if (isFitnessStale || fitness == NULL) {
		fitness = evaluator.dEvaluate(&genotype);
	}
	return fitness;
}

void Individual::mutate(float probability)
{
	for (int i = 0; i < genotype.size(); i++) {
		if (dRand() < probability) {
			genotype.at(i) = lRand(evaluator.iGetNumberOfValues(i));
		}
	}
	isFitnessStale = true;
}

std::vector<Individual*> Individual::mutate()
{
	int randomGenotypeIndex = dRand() * this->genotype.size();

	int maxGenotypeValue = evaluator.iGetNumberOfValues(randomGenotypeIndex);
	int genToOmit = this->genotype.at(randomGenotypeIndex);

	std::vector<Individual*> newIndividuals;
	newIndividuals.reserve(maxGenotypeValue + 1);

	for (int i = 0; i < maxGenotypeValue; i++) {
		std::vector<int> newGenotype = genotype;
		newGenotype.at(randomGenotypeIndex) = i;
		newIndividuals.push_back(new Individual(std::move(newGenotype), evaluator));
	}

	return newIndividuals;
}

std::pair<Individual*, Individual*> Individual::cross(Individual* other)
{
	int crossoverPoint = (dRand() * genotype.size());
	std::vector<int> genotype1, genotype2;

	for (int i = 0; i < genotype.size(); i++) {
		if (crossoverPoint < i) {
			genotype1.push_back(genotype.at(i));
			genotype2.push_back(other->genotype.at(i));
		}
		else {
			genotype2.push_back(genotype.at(i));
			genotype1.push_back(other->genotype.at(i));
		}
	}
	return std::make_pair(new Individual(std::move(genotype1), evaluator), new Individual(std::move(genotype2), evaluator));
}

std::string Individual::toString()
{
	stringstream ss;
	for (int i = 0; i < genotype.size(); i++)
	{
		if (i != 0)
		{
			ss << ", ";
		}
		ss << genotype.at(i);
	}

	return ss.str();
}
