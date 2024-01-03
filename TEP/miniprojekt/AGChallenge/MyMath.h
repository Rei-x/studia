#pragma once
#include  "atlstr.h"  //CString
#include  <math.h>
#include  <time.h>

#include <windows.h>



namespace  MyMath
{
	//sets random seed
	int  iRandomize();


	//returns number from 0 to RAND_MAX
	int     iRand();

	//returns one of numbers starting up from 0
	long  lRand(int iNumberOfPossibilities);

	//returns number from 0 to 1 (excluding 1)
	double  dRand();
	long lRound(double dvalue);

};//namespace  MyMath