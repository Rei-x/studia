#pragma once


#include <string>
#include <vector>
#include "IEvaluator.h"
#include <random>
#include <windows.h>
#include  "atlstr.h"  //CString
#include  "atlpath.h"
#include  "tools.h"

#include  "NETsimulator.h"
#include  "MyMath.h"

#include "fitness.h"


using namespace std;
using  namespace  NETsimulator;
using namespace  MyMath;

#define s_TESTCASE_FOLDER   "data\\"
#define s_TESTCASE_NET_POSTFIX   ".net"
#define s_TESTCASE_CON_POSTFIX   ".con"
#define s_VIRT_WAY_TEMP_FILE   "temp.cod"


#define i_ASCII_CARRIAGE_RETURN   13
#define i_ASCII_NEW_LINE		  10

#define i_CLONE_ROUNDS			  2

#define i_ERR_FILE_NOT_FOUND   -1
#define i_ERR_FILE_UNEXPECTED_FILE_END   -2

#define i_SHORTEST_WAYS_RANGE			  16

#define i_PENALTY			  10





class  CLFLnetEvaluator;
class  CVirtualWayDatabase;
class  CSingleTrajectorySet;


class  CVirtualWay
{

public:

	int  iId;

	int   iGetWay(long** plWay);
	bool  bSetWay(long* plNewWay, int  iNewWayLength);


	int  iLoadWay(FILE* pfSource, CLFLnetEvaluator* pcTranslator, bool  bTranslate);
	void  vCreateReportFile(FILE* pfReport);

	double  dCountFOM(CNETsimulator* pcNetSim);


	bool  operator==(CVirtualWay& pcOther);

	CVirtualWay();
	~CVirtualWay();

	//the offsprings pointers are returned but handling them is the task of CVirtualWaysDatabase
	int  iCross
	(
		CVirtualWay* pcFather, CVirtualWay** pcChild1, CVirtualWay** pcChild2,
		CVirtualWayDatabase* pCVirtualWays,
		CNETsimulator* pcNetSim = NULL
	);

	int  iMutate
	(
		CVirtualWay** pcNewWay,
		CVirtualWayDatabase* pCVirtualWays,
		CNETsimulator* pcNetSim = NULL
	);


private:

	long* pl_way;
	int   i_way_length;

	void  v_remove_loops_from_way();

};//class  CVirtualWay




class  CVirtualWaysSingleSet
{
	friend  class  CVirtualWayDatabase;//needed for acces to virtual ways list when cloning


public:

	CVirtualWay* pcGetVirtualWayAtOffset(int  iOffset);
	CVirtualWay* pcGetVirtualWay();
	bool  bGet2VirtualWaysWithLowLevelFOM(CNETsimulator* pcNetSim, CVirtualWay** pcMother, CVirtualWay** pcFather = NULL, bool  bTranslated = false);


	int   iLoadVirtualWays(FILE* pfSource, CLFLnetEvaluator* pcTranslator, bool bTranslate);
	int   iInputNewVirtWay(CVirtualWay* pcNewWay, CLFLnetEvaluator* pcTransltor,
		CVirtualWay** pcTheSameWayAsNew = NULL);//**pcTheSameWayAsNew is used for returning an addres of the way that is the same in the database

	//information methods
	long  lGetNumberOfWays(long** plLengthSets, int* piTableLen);
	void  vCreateReportFile(FILE* pfReport);


	CVirtualWaysSingleSet();
	~CVirtualWaysSingleSet();


private:


	CMyList  c_virtual_ways;

};//class  CVirtualWaysSingleSet






class  CVirtualWayDatabase
{

public:
	CVirtualWayDatabase();
	~CVirtualWayDatabase();

	int   iLoadVirtualWays(CString  sFileName, CLFLnetEvaluator* pcTranslator, bool  bTranslate);


	int   iCloneVirtualWays(long lStartNode = -1);
	//start node is needed when we want to generate new ways for a specialized node


	int   iInputNewVirtWay
	(CVirtualWay* pcNewWay, long  lStartNode, long  lFinishNode,
		CVirtualWay** pcTheSameWayAsNew = NULL, bool bTranslated = true);//**pcTheSameWayAsNew is used for returning an addres of the way that is the same in the database);


	int   iGetVirtualWaysNumber(long  lStartNode, long  lFinishNode, bool  bTranslated = true);
	CVirtualWay* pcGetVirtualWay(long  lStartNode, long  lFinishNode, bool  bTranslated = true);
	CVirtualWay* pcGetVirtualWayAtOffset(long  lStartNode, long lFinishNode, int iOffset, bool  bTranslated = true);
	bool  bGet2VirtualWaysWithLowLevelFOM(CNETsimulator* pcNetSim, long  lStartNode, long lFinishNode, CVirtualWay** pcMother, CVirtualWay** pcFather = NULL, bool  bTranslated = true);





	int  iCreateReportFile(CString  sFileName);
	int  iCreateStatisticsReportFile(CString  sFileName);



private:



	int   i_input_new_virt_way
	(CVirtualWay* pcNewWay, long  lTranslatedStartNode, long  lTranslatedFinishNode,
		CVirtualWay** pcTheSameWayAsNew);//**pcTheSameWayAsNew is used for returning an addres of the way that is the same in the database);

	int  i_clone_two_lists(CMyList* pcStartList, CMyList* pcFinishList, CMyList* pcDestList);


	CVirtualWaysSingleSet** pc_virtual_ways_sets;

	CLFLnetEvaluator* pc_translator;


	long  l_number_of_nodes;



};//class  CVirtualWayDatabase






class  CLFLnetEvaluator : public IEvaluator
{
public:
	CLFLnetEvaluator();
	~CLFLnetEvaluator();

	virtual double  dEvaluate(vector<int>* pvSolution);
	virtual int  iGetNumberOfBits() { return(i_number_of_pairs); }
	virtual int  iGetNumberOfValues(int  iPairOffset);



	long  lGetNumberOfNodes() { return(l_number_of_nodes); };
	long  lGetNumberOfLinks() { return(l_number_of_links); };

	long  lTranslateNodeNum(long  lNodeNum);
	long  lTranslateLinkNum(long  lLinkNum);

	int  iCheckConnection(long* plWay, int  iWayLength, long  lCapacity, bool bCheckActualCapacity = true) { return(pc_net_model->iCheckConnection(plWay, iWayLength, lCapacity, bCheckActualCapacity)); };
	int   iInputTrajectorySetToFind(long* plNodePairs, long* plCapacities, int  iNumberOfPairs);


	bool  bConfigure(CString  sNetName);
	CString  sGetNetName() { return(s_net_name_buffer); }
private:
	bool  b_load_topology(CString  sNet);
	int  i_links_count(CString  sFileName);
	long  l_skip_comments_and_open(CString  sFileName, FILE** pfFile, CString* psComments);
	int  i_read_one_node(FILE* pfSource, long* plActualLinkNumber);
	bool  b_get_shortest_ways();
	bool  b_read_demands(CString  sPairsFile);


	long  l_number_of_nodes;
	long* pl_nodes_rename_table;//contains pairs [TFinderNodeNumber, NETsimulatorNumber]
	double* pd_nodes_weights;


	long  l_number_of_links;
	long* pl_links_rename_table;//contains pairs [TFinderLinkNumber, NETsimulatorNumber]
	double* pd_links_weights;



	long* pl_pairs;
	long* pl_capa;
	long  l_pairs_num;


	long* pl_start_finish_pairs;
	long* pl_capacities;
	int   i_number_of_pairs;


	CString  s_net_name_buffer;

	CSingleTrajectorySet* pc_fitness_computer;

	CVirtualWayDatabase  c_virtual_ways;
	CNETsimulator* pc_net_model;

	CFOMfunction* pcFOMcounter;
};//class  CLFLnetEvaluator






class  CSingleTrajectorySet
{
	friend  class CLFLnetEvaluator;

public:

	CSingleTrajectorySet();
	~CSingleTrajectorySet();

	bool  bInit(long* plStartFinishPairs, int  iNumberOfPairs, CVirtualWayDatabase* pcWaysDatabase, CNETsimulator* pcNetSim, CFOMfunction* pcFOMcounter, long* plCapacities, long  lPenalty);

	double  dCountFOM(CFOMfunction* pcFOMcounter, long* plCapacities, long  lPenalty);

	bool  bSetAndRateSolution(vector<int>* pvSolution, double* pdFitness, long* plCapacities, long  lPenalty);
	int  iGetNumberOfValues(int  iPairOffset);

private:
	bool  b_set_all_conns(long* plCapacities);


	CNETsimulator* pc_net_sim;
	CFOMfunction* pc_fitness_counter;

	CVirtualWayDatabase* pc_virtual_ways;

	long* pl_start_finish_pairs;
	int   i_number_of_pairs;

	bool  b_fom_lvl_actual;
	double  d_fom_level_penalized;
	double  d_fom_level_pure;
	double  d_penalty_pure;


	long    l_population_when_created;//statistical information
	bool    b_capacity_extending;

	CVirtualWay** pc_trajectories;

};//class  CSingleTrajectorySet




