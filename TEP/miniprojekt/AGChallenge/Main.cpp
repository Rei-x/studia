#include "Evaluator.h"
#include "GeneticAlgorithm.h"
#include "Timer.h"

#include <exception>
#include <iostream>
#include <random>

using namespace TimeCounters;

using namespace std;

#define POPULATION_SIZE 10
#define CROSS_PROBABILITY 0.90
#define MUTATION_PROBABILITY 0.001
#define NUMBER_OF_ITERATIONS 10
// RESULT at 10000 iterations: 0.000163465

void vRunExperiment(CLFLnetEvaluator& cConfiguredEvaluator)
{
	try
	{
		GeneticAlgorithm c_optimizer(POPULATION_SIZE, CROSS_PROBABILITY, MUTATION_PROBABILITY, cConfiguredEvaluator);

		c_optimizer.runIterations(NUMBER_OF_ITERATIONS);
		cout << "BEST CANDIDAT: " << c_optimizer.getBestCandidat()->getFitness() << endl;
	}//try
	catch (exception& c_exception)
	{
		cout << c_exception.what() << endl;
	}//catch (exception &c_exception)
}//void vRunExperiment(const CEvaluator &cConfiguredEvaluator)



void  vRunLFLExperiment(CString  sNetName)
{
	CLFLnetEvaluator c_lfl_eval;
	c_lfl_eval.bConfigure(sNetName);
	vRunExperiment(c_lfl_eval);

}//void vRunRastriginExperiment(int iNumberOfBits, int iBitsPerFloat, int iMaskSeed)



void main(int iArgCount, char** ppcArgValues)
{
	vRunLFLExperiment("104b00");

	/*vRunIsingSpinGlassExperiment(81, 0, i_mask_seed);
	vRunIsingSpinGlassExperiment(81, 0, iSEED_NO_MASK);

	vRunLeadingOnesExperiment(50, i_mask_seed);
	vRunLeadingOnesExperiment(50, iSEED_NO_MASK);

	vRunMaxSatExperiment(25, 0, 4.27f, i_mask_seed);
	vRunMaxSatExperiment(25, 0, 4.27f, iSEED_NO_MASK);

	vRunNearestNeighborNKExperiment(100, 0, 4, i_mask_seed);
	vRunNearestNeighborNKExperiment(100, 0, 4, iSEED_NO_MASK);

	vRunOneMaxExperiment(100, i_mask_seed);
	vRunOneMaxExperiment(100, iSEED_NO_MASK);

	vRunRastriginExperiment(200, 10, i_mask_seed);
	vRunRastriginExperiment(200, 10, iSEED_NO_MASK);*/
}//void main(int iArgCount, char **ppcArgValues)