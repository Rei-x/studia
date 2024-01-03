
//#include  "stdafx.h"
#include  "tools.h"
using namespace  Tools;



void  Tools::vShow(CString  sText)
{
	::MessageBox(NULL, sText, sText, MB_OK);
}//void  Tools::vShow(CString  sText)


void  Tools::vShow(int  iVal)
{
	CString  s_buf;
	s_buf.Format("%d", iVal);
	vShow(s_buf);
}//void  Tools::vShow(int  iVal)



void  Tools::vShow(double  dVal)
{
	CString  s_buf;
	s_buf.Format("%.16lf", dVal);
	vShow(s_buf);
}//void  Tools::vShow(int  iVal)





