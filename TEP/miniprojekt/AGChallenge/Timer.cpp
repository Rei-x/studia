
//#include  "stdafx.h"
#include  "timer.h"
using namespace  TimeCounters;



CTimeCounter::CTimeCounter()
{
	b_start_inited  =  false;
	b_finish_inited  =  false;
}//CTimeCounter::CTimeCounter()



void  CTimeCounter::vSetStartNow()
{
	b_start_inited  =  true;
	QueryPerformanceFrequency(&li_freq);
	QueryPerformanceCounter(&li_start_position);
}//void  CTimeCounter::vSetStartNow()


//if returned value is false it means the timer was not set on start
bool  CTimeCounter::bGetTimePassed(double  *pdTimePassedSec)
{
	if  (b_start_inited  ==  false)  return(false);

	LARGE_INTEGER  li_now;
	QueryPerformanceCounter(&li_now);

	double  d_result;

	d_result  =  (li_now.QuadPart  -  li_start_position.QuadPart);
	d_result  =  d_result  /  li_freq.QuadPart;
	
	*pdTimePassedSec  =  d_result;

	return(true);
}//bool  CTimeCounter::bGetTimePassed(double  *pdTimePassedMs)


bool  CTimeCounter::bSetFinishOn(double  dTimeToFinishSec)
{
	if  ( (b_start_inited  ==  false)||(dTimeToFinishSec <= 0) )  return(false);

	b_finish_inited  =  true;

	li_finish_position.QuadPart  =  
		li_start_position.QuadPart  
		+  
		li_freq.QuadPart * dTimeToFinishSec;

	return(true);
}//bool  CTimeCounter::bSetFinishOn(double  dTimeToFinishMs)


bool  CTimeCounter::bIsFinished()
{
	if  ( (b_start_inited  !=  true)||(b_finish_inited  !=  true) )
		return(true);

	LARGE_INTEGER  li_now;
	QueryPerformanceCounter(&li_now);
	if  (li_now.QuadPart  >  li_finish_position.QuadPart)
		return(true);
	else
		return(false);
};//bool  CTimeCounter::bIsFinished()






