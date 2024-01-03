#include "GeneticAlgorithm.h"

GeneticAlgorithm::GeneticAlgorithm(int populationSize, float crossProbability, float mutationProbability, IEvaluator* evaluator) :
	crossProbability(crossProbability),
	mutationProbability(mutationProbability),
	evaluator(evaluator)
{
	initializePopulation(populationSize);
	bestIndividual = population.at(0);
}



void GeneticAlgorithm::runOneIteration()
{
	vector<Individual> newPopulation;

	while (newPopulation.size() < population.size())
	{
		vector<Individual> parents;

		for (int i = 1; i <= 2; i++)
		{
			Individual firstCandidate = population.at(dRand() * population.size());
			Individual secondCandidate = population.at(dRand() * population.size());

			Individual parent;
			if (firstCandidate.getFitness() > secondCandidate.getFitness())
			{
				parent = firstCandidate;
			}
			else
			{
				parent = secondCandidate;
			}

			// std::cout << "better parent fitness: " << parent.getFitness() << std::endl;
			parents.push_back(parent);
		}

		if (dRand() < crossProbability)
		{
			vector<Individual> children = parents.at(0).cross(parents.at(1));
			newPopulation.push_back(children.at(0));
			// std::cout << "children1: " << children.at(0).getFitness() << std::endl;
			newPopulation.push_back(children.at(1));
			// std::cout << "children1: " << children.at(1).getFitness() << std::endl;
		}
		else
		{
			newPopulation.push_back(parents.at(0));
			newPopulation.push_back(parents.at(1));
		}
	}

	for (int i = 0; i < newPopulation.size(); i++)
	{
		newPopulation.at(i).mutate(mutationProbability);
	}

	population = newPopulation;
}

void GeneticAlgorithm::runIterations(int numberOfIterations)
{
	for (int i = 0; i < numberOfIterations; i++) {
		runOneIteration();
		evaluatePopulation();
		cout << this->getBestCandidat().getFitness() << endl;
	}

}

Individual GeneticAlgorithm::getBestCandidat()
{
	return bestIndividual;
}

void GeneticAlgorithm::initializePopulation(int populationSize)
{
	for (int i = 0; i < populationSize; i++)
	{
		std::vector<int> genotype = std::vector<int>();
		size_t genotypeSize = (size_t)evaluator->iGetNumberOfBits();

		for (size_t j = 0; j < genotypeSize; j++)
		{
			genotype.push_back(lRand(evaluator->iGetNumberOfValues(j)));
		}
		Individual mario(genotype, evaluator);

		population.push_back(mario);
	}
}

void GeneticAlgorithm::evaluatePopulation()
{
	bestIndividual = population.at(0);
	for (int i = 0; i < population.size(); i++)
	{
		if (population.at(i).getFitness() > bestIndividual.getFitness()) {
			bestIndividual = population.at(i);
		}

	}
}
