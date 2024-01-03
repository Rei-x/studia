#include "Evaluator.h"

#include <algorithm>
#include <iostream>
#include <random>
#include <stdexcept>





CLFLnetEvaluator::CLFLnetEvaluator()
{
	pl_nodes_rename_table = NULL;
	pl_links_rename_table = NULL;

	pd_nodes_weights = NULL;
	pd_links_weights = NULL;


	pcFOMcounter = NULL;

	pc_net_model = new  CNETsimulatorSimplyfied;

	pl_capa = NULL;
	pl_pairs = NULL;

	pl_start_finish_pairs = NULL;
	pl_capacities = NULL;

	pc_fitness_computer = NULL;
}//CLFLnetEvaluator::CLFLnetEvaluator() 


CLFLnetEvaluator::~CLFLnetEvaluator()
{
	if (pl_nodes_rename_table != NULL)
		delete[]  pl_nodes_rename_table;

	if (pl_links_rename_table != NULL)
		delete[]  pl_links_rename_table;

	if (pd_nodes_weights != NULL)
		delete[]  pd_nodes_weights;

	if (pd_links_weights != NULL)
		delete[]  pd_links_weights;


	if (pc_net_model != NULL)  delete  pc_net_model;

	if (pcFOMcounter != NULL)  delete  pcFOMcounter;

	if (pl_capa != NULL)  delete[]  pl_capa;
	if (pl_pairs != NULL)  delete[]  pl_pairs;

	if (pl_capacities != NULL)	delete[]  pl_capacities;
	if (pl_start_finish_pairs != NULL)  delete[]  pl_start_finish_pairs;

	if (pc_fitness_computer == NULL)  delete  pc_fitness_computer;
}//CLFLnetEvaluator::~CLFLnetEvaluator()




double  CLFLnetEvaluator::dEvaluate(vector<int>* pvSolution)
{
	double  d_result;
	pc_fitness_computer->bSetAndRateSolution(pvSolution, &d_result, pl_capacities, i_PENALTY);
	return(d_result);
}//double  CLFLnetEvaluator::dEvaluate(vector<int>  *pvSolution)



int  CLFLnetEvaluator::iGetNumberOfValues(int  iPairNumber)
{
	return(pc_fitness_computer->iGetNumberOfValues(iPairNumber));
}//int  CLFLnetEvaluator::iGetNumberOfValues(int  iPairNumber)



bool  CLFLnetEvaluator::bConfigure(CString  sNetName)
{
	s_net_name_buffer = sNetName;
	//FILE  *pf_net;
	CString  s_net_path, s_con_path;

	s_net_path = s_TESTCASE_FOLDER + sNetName + "\\" + sNetName + s_TESTCASE_NET_POSTFIX;
	s_con_path = s_TESTCASE_FOLDER + sNetName + "\\" + sNetName + s_TESTCASE_CON_POSTFIX;

	if (b_load_topology(s_net_path) == false)  return(false);
	pc_net_model->iCreateBasicVirtualDatabaseFile(s_VIRT_WAY_TEMP_FILE);
	c_virtual_ways.iLoadVirtualWays(s_VIRT_WAY_TEMP_FILE, this, false);

	for (int ii = 0; ii < i_CLONE_ROUNDS; ii++)
	{
		if (c_virtual_ways.iCloneVirtualWays() != 1)  return(false);
	}//for  (long  li = 0; li < lCloneRoundsNumber; li++)


	if (b_get_shortest_ways() == false)  return(false);
	pcFOMcounter = new  CFOMfunctionLFL();



	if (b_read_demands(s_con_path) == false)  return(false);


	if (iInputTrajectorySetToFind(pl_pairs, pl_capa, l_pairs_num) != 1) return(false);


	pc_fitness_computer = new CSingleTrajectorySet();
	pc_fitness_computer->bInit(pl_start_finish_pairs, i_number_of_pairs, &c_virtual_ways, pc_net_model, pcFOMcounter, pl_capacities, i_PENALTY);


	double  d_test = pc_fitness_computer->dCountFOM(pcFOMcounter, pl_capacities, i_PENALTY);
	//::Tools::vShow(d_test);

	return(true);
};//bool  CLFLnetEvaluator::bConfigure(CString  sNetName)



/*
returned values:
1  -  ok
0  -  memory allocation problem
*/
int   CLFLnetEvaluator::iInputTrajectorySetToFind(long* plNodePairs, long* plCapacities, int  iNumberOfPairs)
{

	i_number_of_pairs = 0;

	if (pl_start_finish_pairs != NULL)
		delete[]  pl_start_finish_pairs;

	//	if  (pc_population  !=  NULL)
	//		delete []  pc_population;


	if (pl_capacities != NULL)
		delete[]  pl_capacities;



	pl_start_finish_pairs = new  long[iNumberOfPairs * 2];
	if (pl_start_finish_pairs == NULL)  return(0);


	pl_capacities = new  long[iNumberOfPairs];
	if (pl_capacities == NULL)  return(0);



	i_number_of_pairs = iNumberOfPairs;

	for (int ii = 0; ii < i_number_of_pairs * 2; ii++)
		pl_start_finish_pairs[ii] = lTranslateNodeNum(plNodePairs[ii]);


	for (int ii = 0; ii < i_number_of_pairs; ii++)
		pl_capacities[ii] = plCapacities[ii];



	return(1);
}//int   CTrajectorySetsFinder::iInputTrajectorySetToFind(long  *plNodePairs,  int  iNumberOfPairs)





bool  CLFLnetEvaluator::b_read_demands(CString  sPairsFile)
{

	FILE* pf_pairs;
	CString  s_comments;

	l_skip_comments_and_open(sPairsFile, &pf_pairs, &s_comments);


	CString  s_buf;
	if (pf_pairs == NULL)  return(false);


	long  l_num_of_pairs;

	fscanf(pf_pairs, "%ld\n", &l_num_of_pairs);
	l_pairs_num = l_num_of_pairs;


	if (pl_capa != NULL)  delete[]  pl_capa;
	if (pl_pairs != NULL)  delete[]  pl_pairs;

	pl_capa = new  long[l_num_of_pairs];
	pl_pairs = new  long[l_num_of_pairs * 2];


	long  l_buf;
	for (long li = 0; li < l_num_of_pairs; li++)
	{

		fscanf(pf_pairs, "%ld\n", &l_buf);


		fscanf(pf_pairs, "%ld", &l_buf);
		pl_pairs[li * 2] = l_buf;

		fscanf(pf_pairs, "%ld", &l_buf);
		pl_pairs[li * 2 + 1] = l_buf;

		fscanf(pf_pairs, "%ld\n", &l_buf);
		//l_buf = l_buf / 4;//prw remove
		//if  (l_buf <= 0)  l_buf = 1;//prw remove
		pl_capa[li] = l_buf;
		//pl_capa[li] = 10;//l_buf;


	}//for  (long  li = 0; li < l_num_of_pairs; li++)




	fclose(pf_pairs);

	return(true);
};//int  CHefanSystem::iCreatePairs(CString  sPairsFile)






bool  CLFLnetEvaluator::b_get_shortest_ways()
{
	vector  <long*>  v_virt_ways;
	vector  <long>  v_virt_ways_lengths;

	if (pc_net_model->iGetShortestWays(i_SHORTEST_WAYS_RANGE, &v_virt_ways, &v_virt_ways_lengths) != 1)
	{
		for (int ii = 0; ii < (int)v_virt_ways.size(); ii++)
			delete[]  v_virt_ways.at(ii);

		return(false);
	}//if (pc_net_model->iGetShortestWays(i_SHORTEST_WAYS_RANGE, &v_virt_ways, &v_virt_ways_lengths) != 1)

	CVirtualWay* pc_new_vw, * pc_vw_buf;
	int  i_vw_input_res;

	for (int ii = 0; ii < (int)v_virt_ways.size(); ii++)
	{
		//now we create the proper virtual way and try to insert it into the virtual way database
		pc_new_vw = new  CVirtualWay;

		if (pc_new_vw->bSetWay(v_virt_ways.at(ii), v_virt_ways_lengths.at(ii)) == false)
		{
			for (int ii = 0; ii < (int)v_virt_ways.size(); ii++)
				delete[]  v_virt_ways.at(ii);

			return(-1);
		}//if  (pc_new_vw->bSetWay(v_virt_ways.at(ii), v_virt_ways_lengths.at(ii))  ==  false)

		i_vw_input_res = c_virtual_ways.iInputNewVirtWay
		(
			pc_new_vw, v_virt_ways.at(ii)[0], v_virt_ways.at(ii)[v_virt_ways_lengths.at(ii) - 1],
			&pc_vw_buf, true
		);


		//virtual way not inserted because it already exists
		if (i_vw_input_res != 1)
		{
			delete  pc_new_vw;
		}//if  (i_vw_input_res  ==  2)

	}//for  (int  ii = 0; ii < (int) v_virt_ways.size(); ii++)

	for (int ii = 0; ii < (int)v_virt_ways.size(); ii++)
		delete[](long*)  v_virt_ways.at(ii);

	return(true);
}//bool  CLFLnetEvaluator::b_get_shortest_ways()




bool  CLFLnetEvaluator::b_load_topology(CString  sNet)
{
	FILE* pf_source;

	//before we really start we have to count the number of links in the net
	l_number_of_links = i_links_count(sNet);

	if (l_number_of_links <= 0)  return(false);


	//if the number of links is properly found we create the links rename table
	if (pl_links_rename_table != NULL)  delete[]  pl_links_rename_table;
	pl_links_rename_table = new  long[l_number_of_links * 2];

	if (pl_links_rename_table == NULL)  return(-2);




	CString  s_buf;
	if (l_skip_comments_and_open(sNet, &pf_source, &s_buf) == -1)  return(0);


	if (feof(pf_source) == 0)
		fscanf(pf_source, "%ld", &l_number_of_nodes);
	else
		return(false);




	//now when we have the number of nodes we input them into the web and
	//create the nodes rename table
	if (pl_nodes_rename_table != NULL)  delete[] pl_nodes_rename_table;

	pl_nodes_rename_table = new  long[l_number_of_nodes * 2];
	if (pl_nodes_rename_table == 0)  return(false);


	for (long li = 0; li < l_number_of_nodes; li++)
	{

		pl_nodes_rename_table[li * 2] = li + 1;
		pl_nodes_rename_table[li * 2 + 1] = pc_net_model->lAddNewNode(0, "");

		if (pl_nodes_rename_table[li * 2 + 1] == -1)  return(-3);

	}//for  (long  li = 0; li < l_number_of_nodes; li++)





	//before we start to create links we must create a tool for enumarating them...
	long  l_link_number = 1;

	for (long li = 0; li < l_number_of_nodes; li++)
	{

		if (i_read_one_node(pf_source, &l_link_number) == 10)  return(-1);

	}//for  (long  li = 0; li < l_number_of_nodes)*/




	fclose(pf_source);


	//pc_net_model->iPresentNetwork("networkCheck.dat");
	//::Tools::vShow("modelOK");


	return(1);
}//bool  CLFLnetEvaluator::b_load_topology(CString  sNet)




/*
returned values:
1..n  -  modeling system node num
-2    -  node num too small
-1    -  node num too high
*/
long  CLFLnetEvaluator::lTranslateNodeNum(long  lNodeNum)
{

	if (lNodeNum < 1)  return(-2);
	if (l_number_of_nodes < lNodeNum)  return(-1);

	return(pl_nodes_rename_table[(lNodeNum - 1) * 2 + 1]);

}//long  CTopologyTranslator::lTranslateNodeNum(long  lNodeNum)




/*
returned values:
1..n  -  modeling system link num
-2    -  link num too small
-1    -  link num too high
*/
long  CLFLnetEvaluator::lTranslateLinkNum(long  lLinkNum)
{

	if (lLinkNum < 1)  return(-2);
	if (l_number_of_links < lLinkNum)  return(-1);

	return(pl_links_rename_table[(lLinkNum - 1) * 2 + 1]);

}//long  CTopologyTranslator::lTranslateNodeNum(long  lNodeNum)


int  CLFLnetEvaluator::i_links_count(CString  sFileName)
{
	FILE* pf_source;
	CString  s_buf;


	int  i_links_num;
	long  l_buf;
	long  l_num_of_conn_nodes;


	i_links_num = 0;


	if (l_skip_comments_and_open(sFileName, &pf_source, &s_buf) == -1)  return(i_ERR_FILE_NOT_FOUND);



	//first we have to read the number of nodes
	int  i_nodes_num;
	fscanf(pf_source, "%ld", &i_nodes_num);
	//::Tools::vShow(i_nodes_num);



	//now we count the number of links
	long  li, lj;
	for (li = 0; li < i_nodes_num; li++)
	{
		//now we read in the node number
		if (feof(pf_source) == 0)
			fscanf(pf_source, "%ld", &l_buf);
		else
		{
			fclose(pf_source);
			return(-2);
		}


		//now it is the number of connected nodes (which means links in this case)
		if (feof(pf_source) == 0)
			fscanf(pf_source, "%ld", &l_num_of_conn_nodes);
		else
		{
			fclose(pf_source);
			return(i_ERR_FILE_UNEXPECTED_FILE_END);
		}//else  if (feof(pf_source) == 0)


		i_links_num += l_num_of_conn_nodes;


		for (lj = 0; lj < l_num_of_conn_nodes * 2; lj++)
		{
			if (feof(pf_source) == 0)
				fscanf(pf_source, "%ld", &l_buf);
			else
			{
				fclose(pf_source);
				return(i_ERR_FILE_UNEXPECTED_FILE_END);
			}//else if (feof(pf_source) == 0)
		}//for  (long  lj = 0; lj < l_num_of_conn_nodes; lj++)
	}//for  (long  li = 0; li < l_nodes_num; li++)


	fclose(pf_source);

	return(i_links_num);
}//long  CLFLnetEvaluator::l_count_number_of_links(CString  sFileName)




long  CLFLnetEvaluator::l_skip_comments_and_open(CString  sFileName, FILE** pfFile, CString* psComments)
{

	char  c_buf;
	int  i_num_of_comm_lines = 0;
	bool  b_comment;


	*pfFile = fopen((LPCSTR)sFileName, "r+");
	if (*pfFile == NULL)  return(-1);

	b_comment = true;

	while (b_comment == true)
	{
		b_comment = false;

		fscanf(*pfFile, "%c", &c_buf);
		if (c_buf == '/')
		{
			fscanf(*pfFile, "%c", &c_buf);
			if (c_buf == '/')
			{
				b_comment = true;
				i_num_of_comm_lines++;

				for (; c_buf != '\n';)
				{
					fscanf(*pfFile, "%c", &c_buf);
					if (c_buf != '\n')
						*psComments += c_buf;
					else
					{
						c_buf = i_ASCII_CARRIAGE_RETURN;
						*psComments += c_buf;
						c_buf = i_ASCII_NEW_LINE;
						*psComments += c_buf;
					}//else  if  (c_buf  !=  '\n')  

				}//for  (;c_buf  !=  '\n';)

			}//if  (c_buf  ==  '/')	
		}//if  (c_buf  ==  '/')
	}//while  (b_comment  ==  true)

	fclose(*pfFile);

	*pfFile = fopen((LPCSTR)sFileName, "r+");
	while (i_num_of_comm_lines > 0)
	{
		c_buf = 'a';
		for (; c_buf != '\n';)  fscanf(*pfFile, "%c", &c_buf);
		i_num_of_comm_lines--;
	}//while  (i_num_of_comm_lines  >  0)

}//void  CLFLnetEvaluator::v_read_comments(CString  *psComments)



/*
returned values:
1  -  ok
10 -  unexpected end of file
-3 - link creation process unsuccessfull
-4 - node capacity setting unsuccessfull
-5 - node number for link creation is not valid
-6 - unexpected link number (link number is too big)
*/
int  CLFLnetEvaluator::i_read_one_node(FILE* pfSource, long* plActualLinkNumber)
{

	long  l_node_number;
	int   i_connected_nodes;

	long  l_connected_node_num;
	long  l_link_capacity;

	long  l_new_link_id;




	//initialization of data
	if (feof(pfSource) == 0)
		fscanf(pfSource, "%ld", &l_node_number);
	else
		return(10);


	if (feof(pfSource) == 0)
		fscanf(pfSource, "%d", &i_connected_nodes);
	else
		return(10);


	//	printf("Node number:%ld\n", l_node_number);
	//	printf("Number of connected nodes:%d\n",i_connected_nodes);


		//node and link creating
	long  l_summary_capacity = 0;
	for (int ii = 0; ii < i_connected_nodes; ii++)
	{

		if (feof(pfSource) == 0)
			fscanf(pfSource, "%ld", &l_connected_node_num);
		else
			return(10);


		//		printf("Connected node num:%ld\n",l_connected_node_num);



		if (feof(pfSource) == 0)
			fscanf(pfSource, "%ld", &l_link_capacity);
		else
			return(10);


		//		printf("Connected node link capacity:%ld\n",l_link_capacity);



				//now we create a proper links
		if (
			(l_node_number - 1 < l_number_of_nodes) &&
			(l_connected_node_num - 1 < l_number_of_nodes)
			)
		{
			l_new_link_id =
				pc_net_model->lCreateLink(
					pl_nodes_rename_table[(l_node_number - 1) * 2 + 1],
					pl_nodes_rename_table[(l_connected_node_num - 1) * 2 + 1],
					l_link_capacity);

			if (l_new_link_id < 0)  return(-3);

			if (*plActualLinkNumber - 1 >= l_number_of_links)  return(-6);

			pl_links_rename_table[(*plActualLinkNumber - 1) * 2] = *plActualLinkNumber;
			pl_links_rename_table[(*plActualLinkNumber - 1) * 2 + 1] = l_new_link_id;

			(*plActualLinkNumber)++;

		}//if
		else
			return(-5);


		l_summary_capacity += l_link_capacity;


	}//for  (int  ii = 0; ii < i_connected_nodes; ii++)


	l_summary_capacity *= 2;


	//now we must set the node capactiy so this is able to maintain all links
	if (
		pc_net_model->iSetNodeCapacity(
			pl_nodes_rename_table[(l_node_number - 1) * 2 + 1],
			l_summary_capacity)
		!=
		1
		)
		return(-4);



	//	printf("\n\n");



	return(1);

}//int  CTopologyTranslator::i_read_one_node(FILE  pfSource)







//-------------------------------------------------------------------------------------------
//--------------------------implementation of class CVirtualWayDatabase--------------------------



CVirtualWayDatabase::CVirtualWayDatabase()
{

	pc_virtual_ways_sets = NULL;
	l_number_of_nodes = 0;

}//CVirtualWayDatabase::CVirtualWayDatabase()





CVirtualWayDatabase::~CVirtualWayDatabase()
{


	if (pc_virtual_ways_sets != NULL)
	{

		for (long li = 0; li < l_number_of_nodes; li++)
			delete[]  pc_virtual_ways_sets[li];

		delete[] pc_virtual_ways_sets;

	}//if  (pl_virtual_ways  !=  NULL)



}//CVirtualWayDatabase::CVirtualWayDatabase()



/*
returned values:
1  -  ok
0  -  file not found
-1 -  unexpected end of file
-2 -  memory allocation problems
-3 -  node creation unsuccessfull
*/
int  CVirtualWayDatabase::iLoadVirtualWays(CString  sFileName, CLFLnetEvaluator* pcTranslator, bool  bTranslate)
{


	FILE* pf_source;

	long  l_number_of_ways;


	pc_translator = pcTranslator;



	pf_source = fopen((LPCSTR)sFileName, "r+");
	if (pf_source == NULL)  return(0);



	if (feof(pf_source) == 0)
		fscanf(pf_source, "%ld", &l_number_of_ways);
	else
		return(10);



	l_number_of_nodes = pcTranslator->lGetNumberOfNodes();




	pc_virtual_ways_sets = new  CVirtualWaysSingleSet * [l_number_of_nodes];

	if (pc_virtual_ways_sets == NULL)
	{
		fclose(pf_source);
		return(-2);
	}//if  (pc_virtual_ways_sets  ==  NULL)


	long  li;
	for (li = 0; li < l_number_of_nodes; li++)
	{

		pc_virtual_ways_sets[li] = new  CVirtualWaysSingleSet[l_number_of_nodes];


		if (pc_virtual_ways_sets[li] == NULL)
		{

			for (long lj = 0; lj < li; lj++)
				delete[]  pc_virtual_ways_sets[lj];

			delete[]  pc_virtual_ways_sets;

			fclose(pf_source);

			return(-2);

		}//if  (pc_virtual_ways_sets[li]  ==  NULL)

	}//for  (li = 0; li < l_number_of_nodes; li++)





	//from this point we start to read the data in...
	long  l_start_node, l_finish_node;
	int   i_buf;
	for (li = 0; li < l_number_of_ways; li++)
	{

		//read one set of virtual ways
		if (feof(pf_source) == 0)
			fscanf(pf_source, "%ld", &l_start_node);
		else
			return(-1);

		if (feof(pf_source) == 0)
			fscanf(pf_source, "%ld", &l_finish_node);
		else
			return(-1);


		if (bTranslate == true)
		{
			i_buf =
				pc_virtual_ways_sets
				[pcTranslator->lTranslateNodeNum(l_start_node)]
				[pcTranslator->lTranslateNodeNum(l_finish_node)]
				.iLoadVirtualWays(pf_source, pcTranslator, bTranslate);
		}//if  (bTranslate  ==  true)
		else
		{
			i_buf =
				pc_virtual_ways_sets
				[l_start_node]
				[l_finish_node]
				.iLoadVirtualWays(pf_source, pcTranslator, bTranslate);
		}//else  if  (bTranslate  ==  true)

		if (i_buf != 1)
		{

			//	printf("result:%d start:%ld  finish:%ld\n\n", i_buf, l_start_node, l_finish_node);

			fclose(pf_source);
			return(i_buf);
		}//if  (i_buf  !=  1)


	}//for  (li = 0; li < l_number_of_ways; li++)




	fclose(pf_source);



	return(1);

}//int  CVirtualWayDatabase::iLoadVirtualWays(CString  sFileName, CTopologyTranslator *pcTranslator)




CVirtualWay* CVirtualWayDatabase::pcGetVirtualWay(long  lStartNode, long lFinishNode, bool  bTranslated)
{

	if (bTranslated == false)
		return
		(
			pc_virtual_ways_sets
			[pc_translator->lTranslateNodeNum(lStartNode)]
			[pc_translator->lTranslateNodeNum(lFinishNode)].pcGetVirtualWay()
			);
	else
		return
		(
			pc_virtual_ways_sets
			[lStartNode]
			[lFinishNode].pcGetVirtualWay()
			);

}//CVirtualWay*  CVirtualWayDatabase::pcGetVirtualWay(long  lStartNode, long lFinishNode)



int   CVirtualWayDatabase::iGetVirtualWaysNumber(long  lStartNode, long  lFinishNode, bool  bTranslated /*= true*/)
{

	if (bTranslated == false)
		return
		(
			pc_virtual_ways_sets
			[pc_translator->lTranslateNodeNum(lStartNode)]
			[pc_translator->lTranslateNodeNum(lFinishNode)].lGetNumberOfWays(NULL, NULL)
			);
	else
		return
		(
			pc_virtual_ways_sets
			[lStartNode]
			[lFinishNode].lGetNumberOfWays(NULL, NULL)
			);

}//CVirtualWay*  CVirtualWayDatabase::pcGetVirtualWay(long  lStartNode, long lFinishNode)



CVirtualWay* CVirtualWayDatabase::pcGetVirtualWayAtOffset(long  lStartNode, long lFinishNode, int iOffset, bool  bTranslated /*= true*/)
{

	if (bTranslated == false)
		return
		(
			pc_virtual_ways_sets
			[pc_translator->lTranslateNodeNum(lStartNode)]
			[pc_translator->lTranslateNodeNum(lFinishNode)].pcGetVirtualWayAtOffset(iOffset)
			);
	else
		return
		(
			pc_virtual_ways_sets
			[lStartNode]
			[lFinishNode].pcGetVirtualWayAtOffset(iOffset)
			);

}//CVirtualWay*  CVirtualWayDatabase::pcGetVirtualWay(long  lStartNode, long lFinishNode)




/*
returned values:
1  -  ok
0  -
-1 -  wrong start node
-2 -  wrong finish node
*/
int   CVirtualWayDatabase::iInputNewVirtWay
(CVirtualWay* pcNewWay, long  lStartNode, long  lFinishNode,
	CVirtualWay** pcTheSameWayAsNew, bool bTranslated)//**pcTheSameWayAsNew is used for returning an addres of the way that is the same in the database)
{

	if (bTranslated == false)
		return(
			i_input_new_virt_way
			(pcNewWay,
				pc_translator->lTranslateNodeNum(lStartNode),
				pc_translator->lTranslateNodeNum(lFinishNode),
				pcTheSameWayAsNew
			)
			);
	else
		return(
			i_input_new_virt_way
			(pcNewWay,
				lStartNode,
				lFinishNode,
				pcTheSameWayAsNew
			)
			);

}//int   CVirtualWayDatabase::iInputNewVirtWay


/*
returned values:
1  -  ok
0  -  memory allocation problems
-1 -  wrong start node number
*/
int   CVirtualWayDatabase::iCloneVirtualWays(long lStartNode)
{

	CMyList*** pc_new_ways;


	if (
		(lStartNode != -1) &&
		((lStartNode < 0) || (lStartNode >= l_number_of_nodes))
		)
		return(-1);



	//now we create a new virtual ways database
	pc_new_ways = new  CMyList * *[l_number_of_nodes];
	if (pc_new_ways == NULL)  return(0);

	long  li, lj;
	for (li = 0; li < l_number_of_nodes; li++)
	{

		pc_new_ways[li] = new  CMyList * [l_number_of_nodes];

		if (pc_new_ways[li] == NULL)
		{

			for (lj = 0; lj < li; lj++)
				delete[]  pc_new_ways[lj];

			delete[] pc_new_ways;

			return(0);

		}//if  (pc_new_ways[li]  =  NULL)

	}//for  (long  li = 0; li < l_number_of_nodes; li++)



	//now for all of the poniters we allocate the list
	for (li = 0; li < l_number_of_nodes; li++)
	{

		for (lj = 0; lj < l_number_of_nodes; lj++)
		{

			pc_new_ways[li][lj] = new  CMyList;

			if (pc_new_ways[li][lj] == NULL)
			{

				for (long lx = 0; lx < lj; lx++)
					delete  pc_new_ways[li][lx];

				for (long ly = 0; ly < li; ly++)
					for (long lx = 0; lx < l_number_of_nodes; lx++)
						delete  pc_new_ways[ly][lx];


				for (long lx = 0; lx < l_number_of_nodes; lx++)
					delete[] pc_new_ways[lx];

				delete[] pc_new_ways;


				return(0);

			}//if  (pc_new_ways[li][lj]  ==  NULL)

		}//for  (lj = 0; lj < l_number_of_nodes; lj++)

	}//for  (li = 0; li < l_number_of_nodes; li++)





	//now we clone all ways we have
	CMyList* pc_list1;
	CMyList* pc_list2;
	long  lk;

	//this if-construction is not the best one because the only diffrence is in li but it was the easiest one to carry up
	if (lStartNode == -1)
	{
		for (li = 0; li < l_number_of_nodes; li++)
		{

			for (lj = 0; lj < l_number_of_nodes; lj++)
			{

				if (li != lj)
				{
					pc_list1 = &(pc_virtual_ways_sets[li][lj].c_virtual_ways);

					for (lk = 0; lk < l_number_of_nodes; lk++)
					{
						if ((lk != li) && (lk != lj))
						{

							pc_list2 = &(pc_virtual_ways_sets[lj][lk].c_virtual_ways);

							i_clone_two_lists(pc_list1, pc_list2, pc_new_ways[li][lk]);

						}//if  ( (lk != li)&&(lk != lj) )

					}//for  (lk = 0; lk < l_number_of_nodes; lk++)

				}//if  (li != lj)

			}//for  (lj = 0; lj < l_number_of_nodes; lj++)

		}//for  (li = 0; li < l_number_of_nodes; li++)
	}//if  (lStartNode  !=  -1)
	else
	{
		li = lStartNode;

		for (lj = 0; lj < l_number_of_nodes; lj++)
		{

			if (li != lj)
			{
				pc_list1 = &(pc_virtual_ways_sets[li][lj].c_virtual_ways);

				for (lk = 0; lk < l_number_of_nodes; lk++)
				{
					if ((lk != li) && (lk != lj))
					{

						pc_list2 = &(pc_virtual_ways_sets[lj][lk].c_virtual_ways);

						i_clone_two_lists(pc_list1, pc_list2, pc_new_ways[li][lk]);

					}//if  ( (lk != li)&&(lk != lj) )

				}//for  (lk = 0; lk < l_number_of_nodes; lk++)

			}//if  (li != lj)

		}//for  (lj = 0; lj < l_number_of_nodes; lj++)

	}//else  if  (lStartNode  !=  -1)





	//now for all lists we try to input them into the virtual way database
	for (li = 0; li < l_number_of_nodes; li++)
	{

		for (lj = 0; lj < l_number_of_nodes; lj++)
		{

			if (pc_new_ways[li][lj]->bFirst() == true)
			{

				for (lk = 0; lk < pc_new_ways[li][lj]->lGetCapacity(); lk++)
				{
					if
						(
							pc_virtual_ways_sets[li][lj].iInputNewVirtWay
							(
								(CVirtualWay*)pc_new_ways[li][lj]->pcGetNode()->pvGetObject(),
								pc_translator
							)
							!= 1
							)
					{
						//if the way was not inputted we MUST destroy if
						delete  (CVirtualWay*)pc_new_ways[li][lj]->pcGetNode()->pvGetObject();
						//printf("One not inptutted\n");
					}//if
					/*else
						printf("One inptutted\n");*/

					pc_new_ways[li][lj]->bNext();

				}//for  (lk = 0; lk < pc_new_ways[li][lj].lGetCapacity(); lk++)

			}//if  (pc_new_way[li][lj].bFirst()  ==  true)


		}//for  (lj = 0; lj < l_number_of_nodes; lj++)

	}//for  (li = 0; li < l_number_of_nodes; li++)




	//now we destroy the lists
	for (li = 0; li < l_number_of_nodes; li++)
		for (lj = 0; lj < l_number_of_nodes; lj++)
			delete  pc_new_ways[li][lj];

	for (li = 0; li < l_number_of_nodes; li++)
		delete  pc_new_ways[li];

	delete  pc_new_ways;



	return(1);
}//int   CVirtualWayDatabase::iCloneVirtualWays(int iNumberOfRepetations, long lStartNode = -1)







/*
1  -  ok
0  -  memory allocation problems
*/
int  CVirtualWayDatabase::i_clone_two_lists(CMyList* pcStartList, CMyList* pcFinishList, CMyList* pcDestList)
{

	if (pcStartList->bFirst() == false)  return(1);
	if (pcFinishList->bFirst() == false)  return(1);



	CVirtualWay* pc_mother, * pc_father, * pc_child;
	long* pl_mother_way, * pl_father_way, * pl_child_way;
	int   i_mother_length, i_father_length, i_child_length;
	long  li, lj, lk;

	for (li = 0; li < pcStartList->lGetCapacity(); li++)
	{

		pc_mother = (CVirtualWay*)pcStartList->pcGetNode()->pvGetObject();
		i_mother_length = pc_mother->iGetWay(&pl_mother_way);

		for (lj = 0; lj < pcFinishList->lGetCapacity(); lj++)
		{

			pc_father = (CVirtualWay*)pcFinishList->pcGetNode()->pvGetObject();
			i_father_length = pc_father->iGetWay(&pl_father_way);


			pc_child = new  CVirtualWay;
			if (pc_child == NULL)  return(0);

			i_child_length = i_mother_length + i_father_length - 1;
			pl_child_way = new  long[i_child_length];

			if (pl_child_way == NULL)
			{
				delete  pc_child;
				return(0);
			}//if  (pl_child_way  ==  NULL)

			//now rewrite the way
			for (lk = 0; lk < i_mother_length; lk++)
			{
				pl_child_way[lk] = pl_mother_way[lk];
				//	printf("child way[%ld]: %ld (mother part)\n",lk,pl_mother_way[lk]);
			}//for  (lk = 0; lk < i_mother_length; lk++)

			for (lk = 0; lk < i_father_length; lk++)
			{
				pl_child_way[i_mother_length - 1 + lk] = pl_father_way[lk];
				//	printf("child way[%ld]: %ld (father part)\n",lk,pl_father_way[lk]);
			}//for  (lk = 0; lk < i_father_length; lk++)


			if (pc_child->bSetWay(pl_child_way, i_child_length) == false)
			{
				delete  pc_child;
				delete[] pl_child_way;
				return(0);
			}//if  (pc_child->bSetWay(pl_child_way, i_child_way_length)  == false)


			if (pcDestList->bAdd(pc_child) == false)
			{
				delete  pc_child;
				delete[] pl_child_way;
				return(0);
			}//if  (pcDestList->bAdd(pc_child)  ==  false)


			delete[] pl_child_way;

			pcFinishList->bNext();

		}//for  (lj = 0;  pcFinishList->lGetCapacity(); lj++)


		pcStartList->bNext();

	}//for  (li = 0;  pcStartList->lGetCapacity(); li++)



	return(1);

}//int  CVirtualWayDatabase::i_clone_two_lists(CMyList  *pcStartList,  CMyList  *pcFinishList,  CMyList  *pcDestList)




/*
returned values:
1  -  ok
0  -
-1 -  wrong start node
-2 -  wrong finish node
-3 -  virtual ways database is missing
*/
int   CVirtualWayDatabase::i_input_new_virt_way
(CVirtualWay* pcNewWay, long  lTranslatedStartNode, long  lTranslatedFinishNode,
	CVirtualWay** pcTheSameWayAsNew)//**pcTheSameWayAsNew is used for returning an addres of the way that is the same in the database)
{

	long* pl_way;
	int  i_way_length;

	i_way_length = pcNewWay->iGetWay(&pl_way);

	//now we check the start and finish node if they are not proper we retrun an error
	if (pl_way[0] != lTranslatedStartNode)  return(-1);
	if (pl_way[i_way_length - 1] != lTranslatedFinishNode)  return(-2);





	if (pc_virtual_ways_sets == NULL)  return(-3);






	return
		(
			pc_virtual_ways_sets
			[lTranslatedStartNode]
			[lTranslatedFinishNode].iInputNewVirtWay(pcNewWay, pc_translator, pcTheSameWayAsNew)
			);

}//int   CVirtualWayDatabase::iInputNewVirtWay






//-------------------------------------------------------------------------------------------
//--------------------------implementation of class CVirtualWay--------------------------



CVirtualWay::CVirtualWay()
{

	pl_way = NULL;
	i_way_length = 0;

}//CVirtualWay::CVirtualWay()





CVirtualWay::~CVirtualWay()
{

	if (pl_way != NULL)
	{

		delete[]  pl_way;

	}//if  (pl_way  !=  NULL)



}//CVirtualWay::~CVirtualWay()



double  CVirtualWay::dCountFOM(CNETsimulator* pcNetSim)
{
	double  d_specie_fom;
	double  d_buf;

	d_specie_fom = 0;
	for (int ii = 1; ii < i_way_length; ii += 2)
	{
		d_buf = pcNetSim->lGetActLinkCapacity(pl_way[ii]);

		if (d_buf < 0)
		{
			d_buf = d_buf * (-1.0) + 1;
			d_specie_fom += d_buf;
		}//if  (l_buf  <=  0)
		else
		{
			d_buf += 1;
			d_buf *= d_buf;
			d_specie_fom += 1 / d_buf;
		}//else  if  (l_buf  <=  0)

	}//for  (int  ii = 0; ii < i_buf; ii+=2)

	d_specie_fom = 1.0 / d_specie_fom;

	return(d_specie_fom);
}//double  CVirtualWay::dCountFOM(CTopologyTranslator  *pcTranslator)



//returns the returned way length
int  CVirtualWay::iGetWay(long** plWay)
{

	if (i_way_length > 0)
	{

		*plWay = pl_way;
		return(i_way_length);

	}//if  (i_way_length  >  0)


	return(0);

}//int  CVirtualWay::iGetWay(long  **plWay)








bool  CVirtualWay::bSetWay(long* plNewWay, int  iNewWayLength)
{

	long* pl_new_way;


	pl_new_way = new  long[iNewWayLength];


	if (pl_new_way == NULL)  return(false);


	for (int ii = 0; ii < iNewWayLength; ii++)
		pl_new_way[ii] = plNewWay[ii];



	if (pl_way != NULL)
		delete[]  pl_way;


	pl_way = pl_new_way;
	i_way_length = iNewWayLength;


	v_remove_loops_from_way();


	return(true);



}//bool  CVirtualWay::bSetWay(long  *plNewWay,  int  iNewWayLength)





/*
1  -  ok
0  -  memory allocation problems
-1 -  unable to communicate with other objects
*/
int  CVirtualWay::iCross
(
	CVirtualWay* pcFather, CVirtualWay** pcChild1, CVirtualWay** pcChild2,
	CVirtualWayDatabase* pCVirtualWays,
	CNETsimulator* pcNetSim
)
{

	CVirtualWay* pc_child1, * pc_child2;

	*pcChild1 = NULL;
	*pcChild2 = NULL;


	pc_child1 = new  CVirtualWay;
	if (pc_child1 == NULL)  return(false);

	pc_child2 = new  CVirtualWay;
	if (pc_child2 == NULL)
	{
		delete  pc_child1;
		return(0);
	}//if  (pc_child2  ==  NULL)



	//now we extract ways from mother and father virtual way
	long* pl_mother_way, * pl_father_way;
	int  i_mother_way_len, i_father_way_len;


	i_mother_way_len = iGetWay(&pl_mother_way);
	i_father_way_len = pcFather->iGetWay(&pl_father_way);



	if ((i_mother_way_len == 0) || (i_father_way_len == 0))
	{

		delete  pc_child1;
		delete  pc_child2;

		return(-1);

	}//if  ( (i_mother_way_len  ==  0)||(i_father_way_len  ==  0) )




	//now when we have extracted all data we cross to way sets

	//first we pick up mother and father crossing point
	int  i_mother_crossing_node;
	int  i_father_crossing_node;


	//we must remeber that way length is inpair and every second number is a link id
	i_mother_crossing_node = (int)lRand((i_mother_way_len + 1) / 2);
	i_father_crossing_node = (int)lRand((i_father_way_len + 1) / 2);

	i_mother_crossing_node *= 2;
	i_father_crossing_node *= 2;


	long  l_mother_cross_node_id;
	long  l_father_cross_node_id;

	l_mother_cross_node_id = pl_mother_way[i_mother_crossing_node];
	l_father_cross_node_id = pl_father_way[i_father_crossing_node];



	//now if these two nodes are not the same we must find a a virtual way connecting them both
	CVirtualWay* pc_moth_fath_way, * pc_fath_moth_way;
	long* pl_moth_fath_way, * pl_fath_moth_way;
	int  i_moth_fath_way_len, i_fath_moth_way_len;


	if (l_mother_cross_node_id != l_father_cross_node_id)
	{

		pc_moth_fath_way =
			pCVirtualWays->pcGetVirtualWay(l_mother_cross_node_id, l_father_cross_node_id, true);
		pc_fath_moth_way =
			pCVirtualWays->pcGetVirtualWay(l_father_cross_node_id, l_mother_cross_node_id, true);


		i_moth_fath_way_len = pc_moth_fath_way->iGetWay(&pl_moth_fath_way);
		i_fath_moth_way_len = pc_fath_moth_way->iGetWay(&pl_fath_moth_way);


	}//if  (l_mother_cross_node_id  ==  l_father_cross_node_id)
	else
	{

		i_moth_fath_way_len = 0;
		i_fath_moth_way_len = 0;

	}//else  if  (l_mother_cross_node_id  !=  l_father_cross_node_id)




	//now all we have to do is just to glue all pieces together

	long* pl_child1_way, * pl_child2_way;
	int  i_child1_way_len, i_child2_way_len;


	if (i_moth_fath_way_len > 0)
		i_child1_way_len = i_mother_crossing_node + 1
		+
		i_moth_fath_way_len - 1
		+
		i_father_way_len - i_father_crossing_node - 1;
	else
		i_child1_way_len = i_mother_crossing_node + 1
		+
		i_father_way_len - i_father_crossing_node - 1;


	pl_child1_way = new  long[i_child1_way_len];
	if (pl_child1_way == NULL)
	{
		delete  pc_child1;
		delete  pc_child2;
	}//if  (pl_child1_way  ==  NULL)




	if (i_fath_moth_way_len > 0)
		i_child2_way_len = i_father_crossing_node + 1
		+
		i_fath_moth_way_len - 1
		+
		i_mother_way_len - i_mother_crossing_node - 1;
	else
		i_child2_way_len = i_father_crossing_node + 1
		+
		i_mother_way_len - i_mother_crossing_node - 1;



	pl_child2_way = new  long[i_child2_way_len];
	if (pl_child2_way == NULL)
	{
		delete[] pl_child1_way;

		delete  pc_child1;
		delete  pc_child2;
	}//if  (pl_child2_way  ==  NULL)  



	//now we fill up the ways
	int  ii, ij, ik;
	for (ii = 0; ii < i_mother_crossing_node + 1; ii++)
		pl_child1_way[ii] = pl_mother_way[ii];

	ii--;
	for (ij = 1; ij < i_moth_fath_way_len; ij++)
		pl_child1_way[ii + ij] = pl_moth_fath_way[ij];

	ij--;
	for (ik = 1; ik < i_father_way_len - i_father_crossing_node; ik++)
		pl_child1_way[ii + ij + ik] = pl_father_way[ik + i_father_crossing_node];




	for (ii = 0; ii < i_father_crossing_node + 1; ii++)
		pl_child2_way[ii] = pl_father_way[ii];

	ii--;
	for (ij = 1; ij < i_fath_moth_way_len; ij++)
		pl_child2_way[ii + ij] = pl_fath_moth_way[ij];

	ij--;
	for (ik = 1; ik < i_mother_way_len - i_mother_crossing_node; ik++)
		pl_child2_way[ii + ij + ik] = pl_mother_way[ik + i_mother_crossing_node];




	//now we insert the ways into virtual way object
	if (pc_child1->bSetWay(pl_child1_way, i_child1_way_len) == false)
	{

		delete[] pl_child1_way;
		delete[] pl_child2_way;

		delete  pc_child1;
		delete  pc_child2;

		return(-1);

	}//if  (pc_child1->bSetWay(pl_child1_way, i_child1_way_len)  ==  false)


	if (pc_child2->bSetWay(pl_child2_way, i_child2_way_len) == false)
	{

		delete[] pl_child1_way;
		delete[] pl_child2_way;

		delete  pc_child1;
		delete  pc_child2;

		return(-1);

	}//if  (pc_child2->bSetWay(pl_child2_way, i_child2_way_len)  ==  false)



	//when the ways are inserted we delete them
	delete[] pl_child1_way;
	delete[] pl_child2_way;





	//now we try to input the virtual ways into the database
	//if there alredy is the same way we delete currently created and use the older one
	CVirtualWay* pc_the_same_way;
	int  i_insert_res;

	i_insert_res = pCVirtualWays->iInputNewVirtWay(pc_child1,
		pl_way[0], pl_way[i_way_length - 1],
		&pc_the_same_way, true);

	//if  (i_insert_res == 1) printf("JEST\n");

	//if the created way already exists
	if (i_insert_res == 2)
	{
		*pcChild1 = pc_the_same_way;
		delete  pc_child1;
	}//if  (i_insert_res  ==  2)

	if (i_insert_res == 1)  *pcChild1 = pc_child1;


	//if the operation was unsuccesful we delete everything and return false
	if (i_insert_res < 1)
	{
		delete  pc_child1;
		delete  pc_child2;

		return(-1);

	}//if  (i_insert_res  ==  2)






	//NOW SECOND CHILD
	i_insert_res = pCVirtualWays->iInputNewVirtWay(pc_child2,
		pl_way[0], pl_way[i_way_length - 1],
		&pc_the_same_way, true);

	//if the created way already exists
	if (i_insert_res == 2)
	{
		*pcChild2 = pc_the_same_way;
		delete  pc_child2;
	}//if  (i_insert_res  ==  2)

	if (i_insert_res == 1)  *pcChild2 = pc_child2;



	//if the operation was unsuccesful we delete everything and return false
	if (i_insert_res < 1)
	{
		//step back with first child
		*pcChild1 = NULL;

		if (pc_child1 != NULL)  delete  pc_child1;
		delete  pc_child2;

		return(-1);

	}//if  (i_insert_res  ==  2)


	return(1);

}//int  CVirtualWay::iCross(CVirtualWay *pcFather,  CVirtualWay *pcChild1, CVirtualWay *pcChild2)





/*
returned values:
1  -  ok
0  -  memory allocation problems
-1 -  unable to communicate wuth other objects
*/
int  CVirtualWay::iMutate
(
	CVirtualWay** pcNewWay,
	CVirtualWayDatabase* pCVirtualWays,
	CNETsimulator* pcNetSim
)
{
	CVirtualWay* pc_new_way;

	*pcNewWay = NULL;

	pc_new_way = new  CVirtualWay;
	if (pc_new_way == NULL)  return(0);


	long* pl_actual_way;
	int  i_actual_way_len;

	i_actual_way_len = iGetWay(&pl_actual_way);


	//now we find the start and finish mutation nodes
	int  i_start_mut_node, i_finish_mut_node;

	i_start_mut_node = (int)lRand((i_actual_way_len + 1) / 2);
	i_finish_mut_node = i_start_mut_node;
	while (i_start_mut_node == i_finish_mut_node)
		i_finish_mut_node = (int)lRand((i_actual_way_len + 1) / 2);


	i_start_mut_node *= 2;
	i_finish_mut_node *= 2;


	long  l_start_mut_node_id;
	long  l_finish_mut_node_id;

	l_start_mut_node_id = pl_actual_way[i_start_mut_node];
	l_finish_mut_node_id = pl_actual_way[i_finish_mut_node];




	CVirtualWay* pc_inserted_way;
	long* pl_inserted_way;
	int  i_inserted_way_len;



	pc_inserted_way =
		pCVirtualWays->pcGetVirtualWay(l_start_mut_node_id, l_finish_mut_node_id, true);

	i_inserted_way_len = pc_inserted_way->iGetWay(&pl_inserted_way);



	int  i_new_way_len;
	long* pl_new_way;

	i_new_way_len = i_start_mut_node + 1
		+
		i_inserted_way_len - 1
		+
		i_actual_way_len - i_finish_mut_node - 1;


	pl_new_way = new  long[i_new_way_len];

	if (pl_new_way == NULL)
	{
		delete  pc_new_way;
		return(0);
	}//if  (pl_new_way  ==  NULL)



	//now we fill up the ways
	int  ii, ij, ik;
	for (ii = 0; ii < i_start_mut_node + 1; ii++)
		pl_new_way[ii] = pl_actual_way[ii];

	ii--;
	for (ij = 1; ij < i_inserted_way_len; ij++)
		pl_new_way[ii + ij] = pl_inserted_way[ij];

	ij--;
	for (ik = 1; ik < i_actual_way_len - i_finish_mut_node; ik++)
		pl_new_way[ii + ij + ik] = pl_actual_way[ik + i_finish_mut_node];



	if (pc_new_way->bSetWay(pl_new_way, i_new_way_len) == false)
	{
		delete  pc_new_way;
		delete[]  pl_new_way;

		return(-1);
	}//if  (pc_new_way->bSetWay(pl_new_way,i_new_way_len)  ==  false)




	//now we cane freely delete the table with new way
	delete[]  pl_new_way;






	//now we try to input the virtual ways into the database
	//if there alredy is the same way we delete currently created and use the older one
	CVirtualWay* pc_the_same_way;
	int  i_insert_res;

	i_insert_res = pCVirtualWays->iInputNewVirtWay(pc_new_way,
		pl_way[0], pl_way[i_way_length - 1],
		&pc_the_same_way);


	//if the created way already exists
	if (i_insert_res == 2)
	{
		*pcNewWay = pc_the_same_way;
		delete  pc_new_way;
	}//if  (i_insert_res  ==  2)

	if (i_insert_res == 1)  *pcNewWay = pc_new_way;


	//if the operation was unsuccesful we delete everything and return false
	if (i_insert_res < 1)
	{
		delete  pc_new_way;
		return(i_insert_res);
	}//if  (i_insert_res  ==  2)


	return(1);

}//CVirtualWay  * CVirtualWay::pcMutate(CVirtualWayDatabase  *pCVirtualWays)


/*
returned  values:
1  -  ok
-1 -  number of ways below 0
-2 -  unexpected end of file
-3 -  memory allocation problems
-4 -  bad node number
-5 -  bad link number
-6 -  way setting unsuccessfull
*/
int  CVirtualWay::iLoadWay(FILE* pfSource, CLFLnetEvaluator* pcTranslator, bool  bTranslate)
{


	int  i_way_length_buf;



	if (feof(pfSource) == 0)
		fscanf(pfSource, "%d", &i_way_length_buf);
	else
		return(-2);


	long* pl_way_buf;

	pl_way_buf = new  long[i_way_length_buf];

	if (pl_way_buf == NULL)  return(-3);




	long  l_num;

	if (feof(pfSource) == 0)
		fscanf(pfSource, "%ld", &l_num);
	else
		return(-2);


	if (bTranslate == true)
		pl_way_buf[0] = pcTranslator->lTranslateNodeNum(l_num);
	else
		pl_way_buf[0] = l_num;




	if (pl_way_buf[0] < 0)
	{
		delete[]  pl_way_buf;
		return(-4);
	}//if  (pl_way_buf[0]  <  0)



	for (int ii = 0; ii < (i_way_length_buf - 1) / 2; ii++)
	{

		if (feof(pfSource) == 0)
			fscanf(pfSource, "%ld", &l_num);
		else
		{
			delete[]  pl_way_buf;
			return(-2);
		}//else  if  (feof(pfSource)  ==  0)


		if (bTranslate == true)
			pl_way_buf[ii * 2 + 1] = pcTranslator->lTranslateLinkNum(l_num);
		else
			pl_way_buf[ii * 2 + 1] = l_num;


		if (pl_way_buf[ii * 2 + 1] < 0)
		{
			delete[]  pl_way_buf;
			return(-5);
		}//if  (pl_way_buf[ii * 2 + 1]  <  0)  



		if (feof(pfSource) == 0)
			fscanf(pfSource, "%ld", &l_num);
		else
		{
			delete[]  pl_way_buf;
			return(-2);
		}//else  if  (feof(pfSource)  ==  0)



		if (bTranslate == true)
			pl_way_buf[ii * 2 + 2] = pcTranslator->lTranslateNodeNum(l_num);
		else
			pl_way_buf[ii * 2 + 2] = l_num;



		if (pl_way_buf[ii * 2 + 2] < 0)
		{
			delete[]  pl_way_buf;
			return(-4);
		}//if  (pl_way_buf[ii * 2 + 2]  <  0)  

	}//for  (int  ii; ii < i_way_length_buf; ii++)



	if (bSetWay(pl_way_buf, i_way_length_buf) == false)
	{
		delete[]  pl_way_buf;
		return(-6);
	}//if  (bSetWay(pl_way_buf, i_way_length_buf)  ==  false)  


	//now we must delete the buffer
	delete[]  pl_way_buf;



	return(1);

}//int  CVirtualWay::iLoadWay(FILE  *pfSource, CTopologyTranslator *pcTranslator)











void  CVirtualWay::v_remove_loops_from_way()
{

	for (int ii = 0; ii < i_way_length; ii += 2)
	{
		for (int ij = ii + 2; ij < i_way_length; ij += 2)
		{

			//if there are 2 the same nodes we cut them everything between them down
			if (pl_way[ii] == pl_way[ij])
			{

				for (int ik = 0; ij + ik < i_way_length; ik++)
					pl_way[ii + ik] = pl_way[ij + ik];

				i_way_length = i_way_length - (ij - ii);

				ij = ii + 2;

			}//if  (pl_way[ii]  ==  pl_way[ij])

		}//for  (int ij = ii + 2; ij < i_way_length;  ij+=2)

	}//for  (int ii = 0; ii < i_way_length;  ii+=2)

}//void  CVirtualWay::v_remove_loops_from_way()











bool  CVirtualWay::operator ==(CVirtualWay& pcOther)
{

	if (pcOther.i_way_length != i_way_length)  return(false);

	for (int ii = 0; ii < i_way_length; ii++)
		if (pcOther.pl_way[ii] != pl_way[ii])  return(false);


	return(true);

}//bool  CVirtualWay::operator ==(CVirtualWay  &pcOther)












void   CVirtualWay::vCreateReportFile(FILE* pfReport)
{

	fprintf(pfReport, "%d", i_way_length);

	for (int ii = 0; ii < i_way_length; ii++)
		fprintf(pfReport, " %ld", pl_way[ii]);

}//void   CVirtualWay::vCreateReportFile(FILE  *pfReport)












//-------------------------------------------------------------------------------------------
//--------------------------implementation of class CVirtualWaysSingleSet--------------------------

CVirtualWaysSingleSet::CVirtualWaysSingleSet()
{

}//CVirtualWaysSingleSet::CVirtualWaysSingleSet()







CVirtualWaysSingleSet::~CVirtualWaysSingleSet()
{

	c_virtual_ways.bFirst();

	for (long li = 0; li < c_virtual_ways.lGetCapacity(); li++)
	{

		delete  ((CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject());


		c_virtual_ways.bNext();

	}//for  (long  li = 0; li < c_virtual_ways.lGetCapacity(); li++)


	c_virtual_ways.vBYE(false);

}//CVirtualWaysSingleSet::~CVirtualWaysSingleSet()






/*
returned  values:
1  -  ok
-1 -  number of ways below 0
-2 -  unexpected end of file
-3 -  error creating the virtual way
-4 -  insertion into list unsuccessfull
-5 -  virtual way not apropriate for a given topology
*/
int  CVirtualWaysSingleSet::iLoadVirtualWays
(FILE* pfSource, CLFLnetEvaluator* pcTranslator, bool  bTranslate)
{

	long  l_number_of_ways;


	if (feof(pfSource) == 0)
		fscanf(pfSource, "%ld", &l_number_of_ways);
	else
		return(-2);


	if (l_number_of_ways < 0)  return(-1);




	CVirtualWay* pc_virt_way;

	for (long li = 0; li < l_number_of_ways; li++)
	{

		pc_virt_way = new  CVirtualWay;

		if (pc_virt_way == NULL)  return(-2);
		if (pc_virt_way->iLoadWay(pfSource, pcTranslator, bTranslate) != 1)  return(-3);


		if (iInputNewVirtWay(pc_virt_way, pcTranslator) != 1)
		{
			delete  pc_virt_way;
			return(-4);
		}//if  (iInputNewVirtWay(pc_virt_way,  pcTranslator)  !=  1)  

	}//for  (long  li = 0; li < l_number_of_ways; li++)


	return(1);

}//int  CVirtualWaysSingleSet::iLoadVirtualWays







/*
returned values:
2  -  virtual way already exists in the database ()
1  -  ok
0  -  bad way
-3 -  memory allocation problems
*/
int  CVirtualWaysSingleSet::iInputNewVirtWay
(CVirtualWay* pcNewWay, CLFLnetEvaluator* pcTranslator,
	CVirtualWay** pcTheSameWayAsNew)//**pcTheSameWayAsNew is used for returning an addres of the way that is the same in the database
{

	//first we check if the way is correct from topography simulator point of view
	long* pl_way;
	int  i_way_length;

	i_way_length = pcNewWay->iGetWay(&pl_way);


	if (pcTranslator->iCheckConnection(pl_way, i_way_length, 0, false) != 1)  return(0);



	//now we check if we don't have this way already in the topology
	if (c_virtual_ways.bFirst() == true)
	{

		for (long li = 0; li < c_virtual_ways.lGetCapacity(); li++)
		{

			if (
				*((CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject())
				==
				*pcNewWay
				)
			{

				//we return the same way only if we have a given buffer for that
				if (pcTheSameWayAsNew != NULL)
					*pcTheSameWayAsNew = (CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject();

				return(2);

			}//if

			c_virtual_ways.bNext();
		}//for  (long  li = 0; li < c_virtual_ways.lGetCapacity(); li++)


	}//if  (c_virtual_ways.bFirst()  ==  true)

	if (c_virtual_ways.bAdd(pcNewWay) == false)  return(-3);

	pcNewWay->iId = c_virtual_ways.lGetCapacity();





	return(1);

}//int  CVirtualWaysSingleSet::iInputNewVirtWay(CVirtualWay  *pcNewWay)





CVirtualWay* CVirtualWaysSingleSet::pcGetVirtualWayAtOffset(int  iOffset)
{


	if (c_virtual_ways.bSetPos(iOffset + 1) == false)
		return(NULL);

	return((CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject());


}//CVirtualWay*  CVirtualWaysSingleSet::pcGetVirtualWay()




CVirtualWay* CVirtualWaysSingleSet::pcGetVirtualWay()
{


	if (c_virtual_ways.bSetPos(lRand(c_virtual_ways.lGetCapacity()) + 1) == false)
		return(NULL);

	return((CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject());


}//CVirtualWay*  CVirtualWaysSingleSet::pcGetVirtualWay()





bool  CVirtualWaysSingleSet::bGet2VirtualWaysWithLowLevelFOM
(
	CNETsimulator* pcNetSim,
	CVirtualWay** pcMother, CVirtualWay** pcFather,
	bool  bTranslated
)
{

	double* pd_pop_fom;

	pd_pop_fom = new  double[c_virtual_ways.lGetCapacity()];
	if (pd_pop_fom == NULL)  return(false);


	//first we compute the whole "population" fom
	double  d_pop_fom, d_specie_fom;
	CVirtualWay* pc_vw_buf;


	c_virtual_ways.bFirst();
	d_pop_fom = 0;

	long  li;
	for (li = 0; li < c_virtual_ways.lGetCapacity(); li++)
	{

		pc_vw_buf = (CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject();

		d_specie_fom = pc_vw_buf->dCountFOM(pcNetSim);


		d_pop_fom += d_specie_fom;
		pd_pop_fom[li] = d_specie_fom;

		c_virtual_ways.bNext();
	}//for  (long  li = 0; li < c_virtual_ways.lGetCapacity(); li++)




	//mother
	double  d_rand = dRand();
	d_rand *= d_pop_fom;


	double  d_sum = 0;
	bool  b_found = false;

	c_virtual_ways.bFirst();
	for (li = 0; (li < c_virtual_ways.lGetCapacity()) && (b_found == false); li++)
	{
		d_sum += pd_pop_fom[li];
		if (d_sum > d_rand)
		{
			*pcMother = (CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject();
			b_found = true;
		}//if (d_sum  >  d_rand)

	}//for  (li = 0; li < c_virtual_ways.lGetCapacity(); li++)

	if (b_found == false)
	{
		c_virtual_ways.bLast();
		*pcMother = (CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject();
	}//if  (b_found  ==  false)


	if (pcFather == NULL)
	{
		c_virtual_ways.bFirst();
		delete[]  pd_pop_fom;
		return(true);
	}//if  (pcFather  ==  NULL)

	//father
	d_rand = dRand();
	d_rand *= d_pop_fom;

	d_sum = 0;
	b_found = false;

	c_virtual_ways.bFirst();
	for (li = 0; (li < c_virtual_ways.lGetCapacity()) && (b_found == false); li++)
	{
		d_sum += pd_pop_fom[li];
		if (d_sum > d_rand)
		{
			*pcFather = (CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject();
			b_found = true;
		}//if (d_sum  >  d_rand)

	}//for  (li = 0; li < c_virtual_ways.lGetCapacity(); li++)

	if (b_found == false)
	{
		c_virtual_ways.bLast();
		*pcFather = (CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject();
	}//if  (b_found  ==  false)

	c_virtual_ways.bFirst();
	delete[]  pd_pop_fom;
	return(true);
}//void  CVirtualWaysSingleSet::vGet2VirtualWaysWithLowLevelFOM







void  CVirtualWaysSingleSet::vCreateReportFile(FILE* pfReport)
{

	fprintf(pfReport, "%ld\n", c_virtual_ways.lGetCapacity());


	c_virtual_ways.bFirst();



	for (long li = 0; li < c_virtual_ways.lGetCapacity(); li++)
	{

		((CVirtualWay*)c_virtual_ways.pcGetNode()->pvGetObject())->vCreateReportFile(pfReport);

		fprintf(pfReport, "\n");

		c_virtual_ways.bNext();

	}//for  (long  li = 0; li < c_virtual_ways.lGetCapacity(); li++)


}//int  CVirtualWaysSingleSet::iCreateConnectionFile(FILE  *pfDest)



/*
returns a number of virtual ways in the set.
If plLengthSets  ==  NULL the only answer will be the above
returned values:
0 or more  -  ok
-1  -  memory allocation problems
-2  -  unexpected trajectory length (this error shouldn't occur)
*/
long  CVirtualWaysSingleSet::lGetNumberOfWays(long** plLengthSets, int* piTableLen)
{

	if (plLengthSets == NULL)  return(c_virtual_ways.lGetCapacity());


	//searching for the longest virual way
	int  i_longest_way_len = 0;
	long* pl_buf;

	c_virtual_ways.bFirst();
	for (long li = 0; li < c_virtual_ways.lGetCapacity(); li++)
	{
		if (
			((CVirtualWay*)c_virtual_ways.pvGetObject())->iGetWay(&pl_buf)
	>
			i_longest_way_len
			)
			i_longest_way_len
			=
			((CVirtualWay*)c_virtual_ways.pvGetObject())->iGetWay(&pl_buf);

		c_virtual_ways.bNext();

	}//for (long li = 0; li < c_virtual_ways.lGetCapacity(); li++)


	if (i_longest_way_len == 0)
	{
		*plLengthSets = NULL;
		*piTableLen = 0;
		return(0);
	}//if  (i_longest_way_len  ==  0)


	//now we create a proper table for statistical information
	*plLengthSets = new  long[(i_longest_way_len - 1) / 2];
	if (*plLengthSets == NULL)
	{
		*piTableLen = 0;
		return(-1);
	}//if  (*plLengthSets  ==  NULL)
	*piTableLen = (i_longest_way_len - 1) / 2;

	//now preparing the table to work
	for (long li = 0; li < (i_longest_way_len - 1) / 2; li++)
		(*plLengthSets)[li] = 0;



	//now we input the proper nubers of ways into the returned table
	int  i_len_buf;
	c_virtual_ways.bFirst();
	for (long li = 0; li < c_virtual_ways.lGetCapacity(); li++)
	{
		i_len_buf = ((CVirtualWay*)c_virtual_ways.pvGetObject())->iGetWay(&pl_buf);

		if (i_len_buf > i_longest_way_len)  return(-2);

		(*plLengthSets)[((i_len_buf - 1) / 2) - 1]++;

		c_virtual_ways.bNext();

	}//for (li = 0; li < c_virtual_ways.lGetCapacity(); li++)


	return(c_virtual_ways.lGetCapacity());


}//long  CVirtualWaysSingleSet::lGetNumberOfWays(long  **plLengthSets, int *piTableLen)









//-------------------------------------------------------------------------------------------
//--------------------------implementation of class CSingleTrajectorySet--------------------------


CSingleTrajectorySet::CSingleTrajectorySet()
{

	b_fom_lvl_actual = false;
	l_population_when_created = 0;

	d_fom_level_penalized = 0;
	d_fom_level_pure = 0;
	d_penalty_pure = 0;

	pl_start_finish_pairs = NULL;
	i_number_of_pairs = 0;
	b_capacity_extending = true;


	pc_trajectories = NULL;

	pc_fitness_counter = NULL;
}//CSingleTrajectorySet::CSingleTrajectorySet




CSingleTrajectorySet::~CSingleTrajectorySet()
{

	if (pl_start_finish_pairs != NULL)
		delete[]  pl_start_finish_pairs;


	//if (pc_net_sim != NULL)  delete  pc_net_sim;


	if (pc_trajectories != NULL)  delete[]  pc_trajectories;

}//CSingleTrajectorySet::CSingleTrajectorySet







bool  CSingleTrajectorySet::bInit
(long* plStartFinishPairs, int  iNumberOfPairs, CVirtualWayDatabase* pcWaysDatabase, CNETsimulator* pcNetSim, CFOMfunction* pcFOMcounter, long* plCapacities, long  lPenalty)
{
	pc_fitness_counter = pcFOMcounter;

	d_fom_level_penalized = 0;
	d_fom_level_pure = 0;
	d_penalty_pure = 0;

	pc_virtual_ways = pcWaysDatabase;
	if (pc_virtual_ways == NULL)  return(false);



	if (pl_start_finish_pairs != NULL)
		delete[]  pl_start_finish_pairs;

	i_number_of_pairs = 0;



	pl_start_finish_pairs = new  long[iNumberOfPairs * 2];

	if (pl_start_finish_pairs == NULL)  return(false);

	i_number_of_pairs = iNumberOfPairs;



	for (int ii = 0; ii < i_number_of_pairs * 2; ii++)
		pl_start_finish_pairs[ii] = plStartFinishPairs[ii];




	//now we init the trajectories
	if (pc_trajectories != NULL)  delete[]  pc_trajectories;
	pc_trajectories = new CVirtualWay * [i_number_of_pairs];
	if (pc_trajectories == NULL)  return(false);


	for (int ii = 0; ii < i_number_of_pairs; ii++)
	{

		pc_trajectories[ii] =
			pc_virtual_ways->pcGetVirtualWay
			(
				pl_start_finish_pairs[ii * 2],
				pl_start_finish_pairs[ii * 2 + 1]
			);

		//we do NOT break the process HERE!!! because
		//it is an init procedure...
		//if  (pc_trajectories[ii]  ==  NULL)  return(false);


	}//for  (int ii = 0; ii < i_number_of_pairs; ii++)


	//if (pc_net_sim->iCopySimulator(pcNetSim) != 1)  return(false);
	pc_net_sim = pcNetSim;

	pc_net_sim->iRemoveAllConnections();
	//if  (b_set_all_conns(plCapacities)  ==  false)  return(false);
	//we allow set all conns to return false, because it is ONLY the init
	b_set_all_conns(plCapacities);
	b_fom_lvl_actual = false;

	dCountFOM(pc_fitness_counter, plCapacities, lPenalty);

	return(true);
}//bool  CSingleTrajectorySet::bInit



int  CSingleTrajectorySet::iGetNumberOfValues(int  iPairOffset)
{
	if (iPairOffset >= i_number_of_pairs)  return(-1);
	return(pc_virtual_ways->iGetVirtualWaysNumber(pl_start_finish_pairs[iPairOffset * 2], pl_start_finish_pairs[iPairOffset * 2 + 1]));
}//int  CSingleTrajectorySet::iGetNumberOfValues(int  iPairNumber)



bool  CSingleTrajectorySet::bSetAndRateSolution(vector<int>* pvSolution, double* pdFitness, long* plCapacities, long  lPenalty)
{
	if (pvSolution->size() != i_number_of_pairs)  return(false);

	for (int ii = 0; ii < i_number_of_pairs; ii++)
	{
		if (
			pc_virtual_ways->iGetVirtualWaysNumber(pl_start_finish_pairs[ii * 2], pl_start_finish_pairs[ii * 2 + 1])
			<= pvSolution->at(ii)
			)  return(false);

		pc_trajectories[ii] =
			pc_virtual_ways->pcGetVirtualWayAtOffset
			(
				pl_start_finish_pairs[ii * 2],
				pl_start_finish_pairs[ii * 2 + 1],
				pvSolution->at(ii)
			);
	}//for  (int ii = 0; ii < i_number_of_pairs; ii++)

	pc_net_sim->iRemoveAllConnections();
	//if  (b_set_all_conns(plCapacities)  ==  false)  return(false);
	//we allow set all conns to return false, because it is ONLY the init
	b_set_all_conns(plCapacities);
	b_fom_lvl_actual = false;

	*pdFitness = dCountFOM(pc_fitness_counter, plCapacities, lPenalty);

	return(true);
}//bool  CSingleTrajectorySet::bSetAndRateSolution(vector<int>  *pvSolution, double  *pdFitness)






double  CSingleTrajectorySet::dCountFOM(CFOMfunction* pcFOMcounter, long* plCapacities, long  lPenalty)
{
	if (b_fom_lvl_actual == true)  return(d_fom_level_penalized);

	//now we ask the model about the fom value
	pc_net_sim->iRemoveAllConnections();



	b_set_all_conns(plCapacities);	//



	d_fom_level_penalized = pcFOMcounter->dCountFOM(pc_net_sim, lPenalty, &b_capacity_extending, &d_fom_level_pure, &d_penalty_pure);
	//d_fom_level_pure = d_fom_level_penalized - d_penalty_pure;


	b_fom_lvl_actual = true;
	return(d_fom_level_penalized);
}//double  CSingleTrajectorySet::dCountFOM(CTopologyTranslator  *pcTranslator)




bool  CSingleTrajectorySet::b_set_all_conns(long* plCapacities)
{
	long* pl_buf;
	int   i_buf;
	long  l_conn_set_result;

	//first we set up all connections
	b_capacity_extending = false;
	for (int ii = 0; ii < i_number_of_pairs; ii++)
	{
		if (pc_trajectories[ii] != NULL)
		{
			i_buf = pc_trajectories[ii]->iGetWay(&pl_buf);
			l_conn_set_result = pc_net_sim->lSetUpConnection(pl_buf, i_buf, plCapacities[ii]);

			if (l_conn_set_result < 1)
			{
				return(false);
			}//if  (pcTranslator->lSetUpConnetcion(pl_buf, i_buf, plCapacities[ii])  <  1)

			if (l_conn_set_result == 2)  b_capacity_extending = true;
		}//if  (pc_trajectories[ii]  !=  NULL)
		else
			return(false);

	}//for  (int ii = 0; ii < i_number_of_pairs; ii++)


	return(true);
}//bool  CSingleTrajectorySet::b_set_all_conns(long *plCapacities,  long  lPenalty)


