#pragma once


#include <string>
#include <vector>

#include <random>
#include <windows.h>
#include  "atlstr.h"  //CString
#include  "atlpath.h"
#include  "tools.h"

#include  "NETsimulator.h"
#include  "MyMath.h"


using namespace std;
using  namespace  NETsimulator;
using namespace  MyMath;



class  CFOMfunction
{

public:

	CFOMfunction() {};
	virtual  ~CFOMfunction() {};


	virtual  CString  sGetName() { return("no function"); };

	virtual  double  dCountFOM(CNETsimulator  *pcSimulator, long  lPenalty, bool  *pbCapacityExtending, double *pdFitnessPure, double *pdPenaltyPure) { return(0); };//penalty is used when we allow for the capacity extending

	double  dEvalNumber() { return(d_ffe); };

	//	virtual  int     iLoadWeights(CString  sFileName) {return(0);};


protected:
	double  d_ffe;



};//class  CFOMfunction





class  CFOMfunctionLFL : public  CFOMfunction
{

public:

	CFOMfunctionLFL();
	~CFOMfunctionLFL();



	CString  sGetName() { return("lfl function"); };

	double  dCountFOM(CNETsimulator  *pcSimulator, long  lPenalty, bool  *pbCapacityExtending, double *pdFitnessPure, double *pdPenaltyPure);


private:


};//class  CFOMfunctionWeight