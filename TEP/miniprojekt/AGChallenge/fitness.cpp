#include "fitness.h"

//------------------------------------------------------------------------------------------
//------------------implementation of  CFOMfunctionLFL-----------------------------------

CFOMfunctionLFL::CFOMfunctionLFL()
{
	d_ffe = 0;
}//CFOMfunctionLFL::CFOMfunctionLFL(CTopologyTranslator)



CFOMfunctionLFL::~CFOMfunctionLFL()
{

}//CFOMfunctionLFL::~CFOMfunctionLFL()









double  CFOMfunctionLFL::dCountFOM(CNETsimulator  *pcSimulator, long  lPenalty, bool  *pbCapacityExtending, double *pdFitnessPure, double *pdPenaltyPure)
{
	d_ffe++;

	double  d_result;



	d_result = 0;
	*pbCapacityExtending = false;

	bool  b_capacity_ext;
	*pdPenaltyPure = 0;
	*pdFitnessPure = 0;

	for (long li = 0; li < pcSimulator->lGetNodesNum(); li++)
	{
		d_result += pcSimulator->dCountNodeLFL(li, lPenalty, &b_capacity_ext, pdFitnessPure, pdPenaltyPure);
		if (b_capacity_ext)  *pbCapacityExtending = true;
	}//for  (long  li = 0; li < l_number_of_nodes; li++)


	d_result = d_result + *pdPenaltyPure;
	d_result = 1.0 / (d_result + 1.0);



	return(d_result);


}//double  CFOMfunctionLFL::dCountFOM(CTopologyTranslator  *pcTranslator)
