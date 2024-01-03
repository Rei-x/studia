#include  "MyMath.h"
using namespace  MyMath;




//sets random seed
int  MyMath::iRandomize()
{
	unsigned int i_seed;
	i_seed = (unsigned)time( NULL );
	//i_seed = 55;
	srand(i_seed);
	return(i_seed);
}//void  vRandomize()





//returns number from 0 to RAND_MAX
int  MyMath::iRand()
{
	return(rand());
}//int  iRand()






long  MyMath::lRand(int iNumberOfPossibilities)
{

	double  d_rand;
	double  d_div;

	long    l_result;

	d_rand  =  rand();

	d_div  =  RAND_MAX;
	d_div++;//it is in order to never achieve the result of 1 after the division

	d_rand  =  d_rand / d_div;


	d_rand  *=  iNumberOfPossibilities;

	l_result  =  (long) d_rand;
	
	
	
	return(l_result);

}//int  iRand(int iNumberOfPossibilities)







//returns number from 0 to 1 (excluding 1)
double  MyMath::dRand()
{
	double  d_rand, d_div;

	d_rand  =  rand();
	d_div   =  RAND_MAX;
	d_div++;

	return(d_rand / d_div);
}//double  dRand()








long MyMath::lRound(double dvalue)
{
    
    double dint, dfract;
    long li;
    

	dfract  =  modf(dvalue,&dint);
	li  =  (long)  dint;

	if  (dfract >= 0.5)  li++;
	else
		if  (dfract <= -0.5)  li--;

    return li;        
};








