#include "Individual.h"
#include <sstream>

Individual::Individual(std::vector<int> genotype, IEvaluator* evaluator) : genotype(genotype), evaluator(evaluator), fitness(NULL)
{
}

Individual::Individual() : genotype(std::vector<int>()), evaluator(NULL), fitness(NULL)
{
}

double Individual::getFitness()
{
	if (fitness == NULL) {
		fitness = evaluator->dEvaluate(&genotype);
	}
	return fitness;
}

void Individual::mutate(float probability)
{
	for (int i = 0; i < genotype.size(); i++) {
		if (dRand() < probability) {
			genotype.at(i) = lRand(evaluator->iGetNumberOfValues(i));
		}
	}
}

std::vector<Individual> Individual::cross(Individual& other)
{
	int crossoverPoint = (dRand() * genotype.size());
	std::vector<int> genotype1, genotype2;
	for (int i = 0; i < genotype.size(); i++) {
		if (crossoverPoint < i) {
			genotype1.push_back(genotype.at(i));
			genotype2.push_back(other.genotype.at(i));
		}
		else {
			genotype2.push_back(genotype.at(i));
			genotype1.push_back(other.genotype.at(i));
		}
	}
	return std::vector<Individual> {Individual(genotype1, evaluator), Individual(genotype2, evaluator)};
}

Individual& Individual::operator=(const Individual& other)
{
	if (this == &other) {
		return *this;
	}

	fitness = other.fitness;
	genotype = other.genotype;
	evaluator = other.evaluator;

	return *this;
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
