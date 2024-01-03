#include  "NETsimulator.h"

using namespace NETsimulator;


#pragma warning(disable:4996)




//--------------implemenatation of class  CNETsimulatorSimplyfied--------------------------------------------
//--------------------------------------------------------------------------------------------------------------





CNETsimulatorSimplyfied::CNETsimulatorSimplyfied()
{

	l_node_id_tool  =  0;
	pl_actual_network_state  =  NULL;
	pi_paths_per_link = NULL;
	pl_links_table_for_nodes =  NULL;

	l_number_of_links  =  0;
	pl_links_addres_table  =  NULL;

	b_allow_capacity_oveloading  =  false;

	i_minimum_allowed_demand_increase = -1;
}//CNETsimulatorSimplyfied::CNETsimulatorSimplyfied()






CNETsimulatorSimplyfied::~CNETsimulatorSimplyfied()
{

	if  (pl_actual_network_state  !=  NULL)
	{
		for  (long  li = 0; li < l_node_id_tool; li++)
			delete  []  pl_actual_network_state[li];

		delete  []  pl_actual_network_state;
	
	}//if  (pl_actual_network_state  !=  NULL)


	if  (pi_paths_per_link  !=  NULL)
	{
		for  (long  li = 0; li < l_node_id_tool; li++)
			delete  []  pi_paths_per_link[li];

		delete  []  pi_paths_per_link;
	
	}//if  (pl_actual_network_state  !=  NULL)



	if  (pl_links_table_for_nodes !=  NULL)
	{
		for  (long  li = 0; li < l_node_id_tool; li++)
			delete  []  pl_links_table_for_nodes[li];

		delete  []  pl_links_table_for_nodes;
	
	}//if  (pl_links_table_for_nodes !=  NULL)


	if  (pl_links_addres_table  !=  NULL)
		delete  []  pl_links_addres_table;
	


}//CNETsimulatorSimplyfied::~CNETsimulatorSimplyfied()






/*
WARNING: in this type of net simulator both inputted values are unimportant!
WARNING2: this operation RESETS the network state for this model
returns the node id (-1 if the operation is unsuccessfull)
*/
long  CNETsimulatorSimplyfied::lAddNewNode(long  lCapacity, CString sName)
{

	if  ( (pl_links_table_for_nodes  ==  NULL)&&(l_node_id_tool  !=  0) )  return(-1);
		
	
	long  **pl_new_table, **pl_new_actual_table;
	int  **pi_new_paths_per_link;
	long  lj;



	//first - create the new network tables
	pl_new_table  =  new  long* [l_node_id_tool + 1];
	if  (pl_new_table  ==  NULL)  return(-1);

	pl_new_actual_table  =  new  long* [l_node_id_tool + 1];
	if  (pl_new_actual_table  ==  NULL)  
	{
		delete  []  pl_new_table;
		return(-1);
	}//if  (pl_new_actual_table  ==  NULL)  


	pi_new_paths_per_link = new int* [l_node_id_tool + 1];
	if  (pi_new_paths_per_link  ==  NULL)  
	{
		delete  []  pl_new_table;
		delete  pl_new_actual_table;
		return(-1);
	}//if  (pl_new_actual_table  ==  NULL)  


	for  (long  li = 0; li < l_node_id_tool + 1; li++)
	{

		pl_new_table[li]  =  new  long[l_node_id_tool + 1];
				
		if  (pl_new_table[li]  ==  NULL)
		{

			for  (long  lj = 0; lj < li; lj++)
				delete  []  pl_new_table[lj];

			delete  []  pl_new_table;

			return(-1);
			
		}//if  (pl_new_table[li]  ==  NULL)




		pl_new_actual_table[li]  =  new  long[l_node_id_tool + 1];
				
		if  (pl_new_actual_table[li]  ==  NULL)
		{

			for  (lj = 0; lj < li; lj++)
				delete  []  pl_new_actual_table[lj];
			for  (lj = 0; lj < l_node_id_tool; lj++)
				delete  []  pl_new_table[lj];

			delete  []  pl_new_table;
			delete  []  pl_new_actual_table;

			return(-1);
			
		}//if  (pl_new_table[li]  ==  NULL)


		pi_new_paths_per_link[li] =  new  int[l_node_id_tool + 1];

	}//for  (long  li = 0; li < l_node_id_tool + 1; li++)





	//now if the old table exists we copy all of the old data into the new table
	for  (long  li = 0; li < l_node_id_tool; li++)
	{
		for  (long  lj = 0; lj < l_node_id_tool; lj++)
		{
			pl_new_table[li][lj]  =  pl_links_table_for_nodes[li][lj];
			pl_new_actual_table[li][lj]  =  pl_links_table_for_nodes[li][lj];
			pi_new_paths_per_link[li][lj] = pi_paths_per_link[li][lj];
		
		}//for  (lj = 0; lj < l_node_id_tool; lj++)

		//after copying data we can already delete the parts of table
		delete  []  pl_links_table_for_nodes[li];
		delete  []  pl_actual_network_state[li];
		delete  []  pi_paths_per_link[li];
		
	}//for  (li = 0; li < l_node_id_tool; li++)
	
	//after data copying we can delete the main table structure (the rets of it was already deleted during coping)
	if  (pl_links_table_for_nodes  !=  NULL)  delete  []  pl_links_table_for_nodes;
	if  (pl_actual_network_state  !=  NULL)  delete  []  pl_actual_network_state;
	if  (pi_paths_per_link  !=  NULL)  delete  []  pi_paths_per_link;
	
	
	
	//now just setting all the possible links between new node and the rest as 0
	for  (lj = 0; lj < l_node_id_tool + 1; lj++)
	{
		pl_new_table[l_node_id_tool][lj]  =  0;
		pl_new_actual_table[l_node_id_tool][lj]  =  0;
		pi_new_paths_per_link[l_node_id_tool][lj]  =  0;
	}//for  (lj = 0; lj < l_node_id_tool + 1; lj++)

	for  (long  li = 0; li < l_node_id_tool + 1; li++)
	{
		pl_new_table[li][l_node_id_tool]  =  0;
		pl_new_actual_table[li][l_node_id_tool]  =  0;
		pi_new_paths_per_link[li][l_node_id_tool]  =  0;
	}//for  (li = 0; li < l_node_id_tool + 1; li++)

	pl_links_table_for_nodes  =  pl_new_table;
	pl_actual_network_state  =  pl_new_actual_table;
	pi_paths_per_link  =  pi_new_paths_per_link;

	
	return(l_node_id_tool++);

}//long  CNETsimulatorSimplyfied::lAddNewNode(long  lCapacity, CString sName)





/*
WARNING: if the link already exists (value > 0) the actual state for it will be reseted
returned values (if it's below 0 it's an error):
0 or more - new link id
-1 - start node does not exist
-2 - finish node does not exist
-3 - memory allocation problem
**-4 - plug operation unsuccesfull
-5 - bad capacity inputted
** - doesn't work for this model
*/ 
long  CNETsimulatorSimplyfied::lCreateLink(long  lStartNodeId, long  lFinishNodeId, long lCapacity)
{

	if  ( (lStartNodeId < 0)||(lStartNodeId >= l_node_id_tool) )  return(-1);
	if  ( (lFinishNodeId < 0)||(lFinishNodeId >= l_node_id_tool) )  return(-1);

	if  (lCapacity  <=  0)  return(-5);

	//try to allocate the new link addres table
	long  *pl_buf;
	pl_buf  =  new  long[(l_number_of_links + 1) * 2];
	if  (pl_buf  ==  NULL)  return(-3);
	

	pl_links_table_for_nodes[lStartNodeId][lFinishNodeId]  =  lCapacity;
	pl_actual_network_state[lStartNodeId][lFinishNodeId]  =  lCapacity;
	pi_paths_per_link[lStartNodeId][lFinishNodeId]  =  0;


	//copy old link addres table into the new one
	for  (long  li = 0; li < l_number_of_links * 2; li++)
		pl_buf[li]  =  pl_links_addres_table[li];
	
	pl_buf[l_number_of_links * 2]  =  lStartNodeId;
	pl_buf[l_number_of_links * 2 + 1]  =  lFinishNodeId;


	if  (pl_links_addres_table  !=  NULL)  delete  []  pl_links_addres_table;
	pl_links_addres_table  =  pl_buf;



	return(l_number_of_links++);


}//long  CNETsimulatorSimplyfied::lCreateLink(long  lStartNodeId, long  lFinishNodeId, long lCapacity)








/*
returned values:
1  -  ok
0  -  physically ok, but capacity is too small
-1 -  bad way length
-2 -  parity error
-3 -  capacity below 0
-4 -  one of links does not exist
-5 -  one nodes does not exist or is not a begin/end of one of links
*/
int   CNETsimulatorSimplyfied::iCheckConnection
		(long  *plWay, int iWayLength, long  lCapacity, bool bCheckActualCapacity)
{

	if  (pl_links_table_for_nodes  ==  NULL)  return(-5);

	//if  (lCapacity  <  0)  return(-3);

	if  (iWayLength  <  3)  return(-1);

	//if the way length is a parit number then it is wrong
	int  ii;
	ii  =  iWayLength / 2;
	if  (ii * 2  ==  iWayLength)  return(-2);





	bool  b_capacity_ok;
	long  l_start_node_id;
	long  l_finish_node_id;
	

	b_capacity_ok  =  true;//initial step for loop
	l_finish_node_id  =  plWay[0];//initial step for loop

	for  (int ij = 0; ij < (iWayLength - 1) / 2; ij++)
	{

		l_start_node_id  =  l_finish_node_id;
		l_finish_node_id  =  plWay[ij * 2 + 2];


		
		//capacity checking only if this is still ok
		if  (b_capacity_ok  ==  true)
		{
			if  (bCheckActualCapacity  ==  true)
			{

				if  ( (l_start_node_id < 0)||(l_finish_node_id >= l_node_id_tool) )  return(-5);
				if  (pl_links_table_for_nodes[l_start_node_id][l_finish_node_id]  <=  0)  return(-4);

				if  (pl_actual_network_state[l_start_node_id][l_finish_node_id]  <  lCapacity)
					b_capacity_ok  =  false;

			}//if  (bCheckActualCapacity  ==  true)
			else
			{

				if  ( (l_start_node_id < 0)||(l_finish_node_id >= l_node_id_tool) )  return(-5);
				if  (pl_links_table_for_nodes[l_start_node_id][l_finish_node_id]  <=  0)  return(-4);

				if  (pl_links_table_for_nodes[l_start_node_id][l_finish_node_id]  <  lCapacity)
					b_capacity_ok  =  false;
			
			}//else if  (bCheckActualCapacity  ==  true)

		}//if  (b_capacity_ok  ==  true)

	}//for  (int ij = 0; ij < (iWayLength - 1) / 2; ij++)


	//if we managed to get here it means that trajectory exists
	//so the value returned depends only on capacity check...

	if  (b_capacity_ok  ==  true)
		return(1);
	else
		return(0);


	return(0);

}//int   CNETsimulatorSimplyfied::iCheckConnection



long  CNETsimulatorSimplyfied::lFindLinkIdForNodes(long  lStartNodeId,  long  lFinishNodeId)
{
	for  (int  ii = 0; ii < l_number_of_links; ii++)
		if  (
			(pl_links_addres_table[ii*2]  ==  lStartNodeId)&&
			(pl_links_addres_table[ii*2 + 1]  ==  lFinishNodeId)
			)
			return(ii);

	return(-1);

}//long  CNETsimulatorSimplyfied::lFindLinkIdForNodes(long  lStartNodeId,  long  lFinishNodeId)




bool  CNETsimulatorSimplyfied::b_is_node_visited
	(
	vector  <int>  *pvVisitedPathsTree, 
	int  iLastPathNodeIndex,
	int  iCheckedNodeId
	)
{
	int  i_current_node_index  =  iLastPathNodeIndex;
	

	while  (true)
	{
		if  (pvVisitedPathsTree->at(i_current_node_index) ==  iCheckedNodeId)  return(true);

		i_current_node_index  =  pvVisitedPathsTree->at(i_current_node_index + 1);
		if  (i_current_node_index  <  0)  return(false);	
	}//while  (b_root_found  ==  false)
	
	return(false);
}//bool  CNETsimulatorSimplyfied::b_is_node_visited(vector  <int>  vVisitedPath)




int  CNETsimulatorSimplyfied::i_expand_path_tree(vector  <int>  *pvVisitedPathTree, int iFinishNodeId)
{
	int  i_start_size;


	//VERY IMPORTANT!!! 
	//while the loop is running the tree expands, but we only check
	//for expanding the nodes which existed in the tree at the start momment
	i_start_size  =  (int) pvVisitedPathTree->size();

	//expanding loop
	for  (int ii =  0;  ii < i_start_size; ii += 3)
	{
		int  i_current_node_id;
		i_current_node_id  =  pvVisitedPathTree->at(ii);

		if  ( (pvVisitedPathTree->at(ii + 2)  ==  -1)&&(i_current_node_id  !=  iFinishNodeId) )
		{
			if  ( (i_current_node_id < 0)||(i_current_node_id >= l_node_id_tool) )  return(-5);

			int  i_child_number  =  0;
			//now we find all nodes connected to current node
			for  (int i_connected_node_id  =  0;  i_connected_node_id < l_node_id_tool;  i_connected_node_id++)
			{
				if  (
					(pl_links_table_for_nodes[i_current_node_id][i_connected_node_id]  >  0)
					&&
					(i_current_node_id  !=  i_connected_node_id)
					)
				{
					if  (b_is_node_visited(pvVisitedPathTree, ii,  i_connected_node_id)  ==  false)
					{
						pvVisitedPathTree->push_back(i_connected_node_id);
						pvVisitedPathTree->push_back(ii);
						pvVisitedPathTree->push_back(-1);

						i_child_number++;				
					}//if  (b_is_node_visited(&v_visited_path, i_connected_node)  ==  false)		
				}//if  (pl_links_table_for_nodes[i_current_node_id][i_connected_node]  >  0)

			}//for  (int i_connected_node  =  0;  i_connected_node < l_node_id_tool;  i_connected_node++)
			

			pvVisitedPathTree->at(ii + 2)  =  i_child_number;
		}//if  ( (pvVisitedPathTree->at(ii + 2)  ==  -1)&&(i_current_node_id  !=  iFinishNodeId) )

	}//for  (ii =  0;  ii < (int) pvVisitedPathTree->size(); ii += 3)

	return(1);
}//int  CNETsimulatorSimplyfied::i_expand_path_tree(vector  <int>  *pvVisitedPathTree)




int  CNETsimulatorSimplyfied::iGetShortestWaysForNodes
	(int iStartNodeId, int iFinishNodeId, int  iShortestWaysNumber, vector <long *> *pvWays, vector <long> *pvWaysLenghts)
{
	//it is a tree but it is flat
	//it contains 3s:
	//node_id, parent_index, child_num (0..n,  -1 - not checked yet!)
	vector  <int>  v_visited_path_tree;

    v_visited_path_tree.push_back(iStartNodeId);
	v_visited_path_tree.push_back(-1);
	v_visited_path_tree.push_back(-1);

	int  i_found_ways_counter  =  0;

	while  (i_found_ways_counter  <  iShortestWaysNumber)
	{
		if  (i_expand_path_tree(&v_visited_path_tree,  iFinishNodeId)  !=  1)  return(-1);

		//now we check if there is the propoer number of searched ways
		i_found_ways_counter  =  0;
		for  (int ii =  0;  ii < (int) v_visited_path_tree.size(); ii += 3)
		{
			if  (v_visited_path_tree.at(ii)  ==  iFinishNodeId)  i_found_ways_counter++;	
		}//for  (int ii =  0;  ii < (int) v_visited_path_tree.size(); ii += 3)
	}//while  (i_found_ways_counter  <  iShortestWaysNumber)

	
	//now we retrieve the ways
	long  *pl_v_way;
	vector  <int>  v_path_buffer;
	for  (int ii =  0;  ii < (int) v_visited_path_tree.size(); ii += 3)
	{
		v_path_buffer.clear();

		if  (v_visited_path_tree.at(ii)  ==  iFinishNodeId)
		{
			int  i_current_node_index  =  ii;
			v_path_buffer.push_back(v_visited_path_tree.at(i_current_node_index));

			while  (v_visited_path_tree.at(i_current_node_index + 1)  !=  -1)
			{
				i_current_node_index  =  v_visited_path_tree.at(i_current_node_index + 1);
				v_path_buffer.push_back(v_visited_path_tree.at(i_current_node_index));
				if  (i_current_node_index  <  0)  return(-1);	
			}//while  (b_root_found  ==  false)


			//now creating virtual way...
			pl_v_way  =  new  long[((int) v_path_buffer.size()) * 2 - 1];
			for  (int ij = 0; ij < (int) v_path_buffer.size(); ij++)
				pl_v_way[ij * 2]  =  v_path_buffer.at(v_path_buffer.size() - 1 - ij);
			
			for  (int ij = 1; ij < ((int) v_path_buffer.size()) * 2 - 1; ij+=2)
				pl_v_way[ij]  =  lFindLinkIdForNodes(pl_v_way[ij - 1], pl_v_way[ij + 1]);

			pvWays->push_back(pl_v_way);
			pvWaysLenghts->push_back(((int) v_path_buffer.size()) * 2 - 1);
		
		}//if  (v_visited_path_tree.at(ii)  ==  iFinishNodeId)
	}//for  (int ii =  0;  ii < (int) v_visited_path_tree.size(); ii += 3)


	return(1);    
}//int  CNETsimulatorSimplyfied::iGetShortestWaysForNodes




int  CNETsimulatorSimplyfied::iGetShortestWays(int  iShortestWaysNumber, vector <long *> *pvWays, vector <long> *pvWaysLenghts)
{
	int  i_result;
	CString  s_buf;

	for  (int  ii = 0; ii < l_node_id_tool; ii++)
	{
		for  (int  ik = 0; ik < l_node_id_tool; ik++)
		{
			if  (ii  !=  ik)
			{
				i_result  =  
					iGetShortestWaysForNodes(ii, ik, iShortestWaysNumber, pvWays, pvWaysLenghts);
				
				if  (i_result  !=  1)
				{
					for  (int  ij = 0; ij < (int) pvWays->size(); ij++)
						delete  []  pvWays->at(ij);
					return(i_result);
				}//if  (i_result  !=  1)
			}//if  (ii  !=  ik)
		}//for  (int  ii = 0; ii < l_node_id_tool; ii++)	
	}//for  (int  ii = 0; ii < l_node_id_tool; ii++)

	return(1);
}//int  CNETsimulatorSimplyfied::iGetShortestWays



/*
returned values:
2  -  capacity too small but the connection is set
1  -  ok
0  -  physically ok, but capacity is too small so the connection was NOT set
-1 -  bad way length
-2 -  parity error
-3 -  capacity below 0
-4 -  one of links does not exist
-5 -  one nodes does not exist or is not a begin/end of one of links
-6 -  mewmory allocation problem
-7 -  connection setting for nodes and links unsuccesfull
-8 -  way set in connection objerct unsuccessfull
*/
long  CNETsimulatorSimplyfied::lSetUpConnection(long  *plWay, int iWayLength, long  lCapacity)
{

	bool  b_connection_set_with_too_small_capacity  =  false;

	int i_buf;
	int i_minimum_allowed_demand_increase_on_the_way;
	
	
	//if the trajectory is ok we set up a connection
	i_minimum_allowed_demand_increase_on_the_way = -1;
	for  (int  ii = 2; ii < iWayLength;  ii+=2)
	{
		pl_actual_network_state[plWay[ii-2]][plWay[ii]]  =  
			pl_actual_network_state[plWay[ii-2]][plWay[ii]]  -  lCapacity;

		if  (b_const_sat_incr_demands = true)
		{
			if  (lCapacity > 0)
				pi_paths_per_link[plWay[ii-2]][plWay[ii]]  =  pi_paths_per_link[plWay[ii-2]][plWay[ii]] + 1;
			else
				pi_paths_per_link[plWay[ii-2]][plWay[ii]]  =  pi_paths_per_link[plWay[ii-2]][plWay[ii]] - 1;

			//computing minimum allowed capacity increase on the way
			i_buf = pl_actual_network_state[plWay[ii-2]][plWay[ii]];
			if  (i_buf > 0)
			{
				if  (pi_paths_per_link[plWay[ii-2]][plWay[ii]] == 0)
					i_buf = CONST_SAT_MAX_DEMAND_INCREASE;
				else
					i_buf = i_buf / pi_paths_per_link[plWay[ii-2]][plWay[ii]];
			}//if  (i_buf > 0)
			else
				i_buf = 0;

			if  (i_minimum_allowed_demand_increase_on_the_way < 0)  i_minimum_allowed_demand_increase_on_the_way = i_buf;
			if  (i_minimum_allowed_demand_increase_on_the_way > i_buf)  i_minimum_allowed_demand_increase_on_the_way = i_buf;
		}//if  (b_const_sat_incr_demands = true)
	}//for  (ii = 0; ii < iWayLength;  ii+=2)
		
	
	if  (b_const_sat_incr_demands = true)
	{
		if  (lCapacity > 0)
		{
			//the minimum may only decrease
			if  (i_minimum_allowed_demand_increase < 0)  i_minimum_allowed_demand_increase = i_minimum_allowed_demand_increase_on_the_way;
			if  (i_minimum_allowed_demand_increase > i_minimum_allowed_demand_increase_on_the_way)  i_minimum_allowed_demand_increase = i_minimum_allowed_demand_increase_on_the_way;		
		}//if  (lCapacity > 0)

		if  (lCapacity < 0)
		{
			//the minimum may only increase
			if  (i_minimum_allowed_demand_increase < i_minimum_allowed_demand_increase_on_the_way)  
			{
				v_recompute_minimum_allowed_demand_increase();
			}//if  (i_minimum_allowed_demand_increase < i_minimum_allowed_demand_increase_on_the_way)  
		}//if  (lCapacity < 0)		
	}//if  (b_const_sat_incr_demands = true)


	if  (b_connection_set_with_too_small_capacity  ==  true)
		return(2);
	else
		return(1);


}//long  CNETsimulatorSimplyfied::lSetUpConnection(long  *plWay, int iWayLength, long  lCapacity)




void  CNETsimulatorSimplyfied::v_recompute_minimum_allowed_demand_increase()
{

	int i_buf;
	i_minimum_allowed_demand_increase = -1;

	for  (long  li = 0; li < l_node_id_tool; li++)
	{
		for  (long  lj = 0; lj < l_node_id_tool; lj++)
		{ 
			if  (pl_links_table_for_nodes[li][lj]  >  0)
			{
				i_buf = pl_actual_network_state[li][lj];
				if  (i_buf > 0)
				{
					if  (pi_paths_per_link[li][lj] == 0)
						i_buf = CONST_SAT_MAX_DEMAND_INCREASE;
					else
						i_buf = i_buf / pi_paths_per_link[li][lj];
				}//if  (i_buf > 0)
				else
					i_buf = 0;

				if  (i_minimum_allowed_demand_increase < 0)  i_minimum_allowed_demand_increase = i_buf;
				if  (i_minimum_allowed_demand_increase > i_buf)  i_minimum_allowed_demand_increase = i_buf;
			}//if  (pl_links_table_for_nodes[li][lj]  >  0)
		}//for  (long  lj = 0; lj < l_node_id_tool; lj++)
	}//for  (long  li = 0; li < l_node_id_tool; li++)

	//CString  s_buf;
	//s_buf.Format("v_recompute_minimum_allowed_demand_increase : %d", i_minimum_allowed_demand_increase);
	//::MessageBox(NULL, s_buf, s_buf, MB_OK);
}//void  CNETsimulatorSimplyfied::v_recompute_minimum_allowed_demand()





/*
returned  values:
1  -  ok
0  -  no connections to remove
-1 -  problems occured when removing one or more connections
*/
int  CNETsimulatorSimplyfied::iRemoveAllConnections()
{

	for  (long  li = 0; li < l_node_id_tool; li++)
	{

		for  (long  lj = 0; lj < l_node_id_tool; lj++)
		{

			pl_actual_network_state[li][lj]  =  pl_links_table_for_nodes[li][lj];
			pi_paths_per_link[li][lj] = 0;
		
		}//for  (long  lj = 0; lj < l_node_id_tool; lj++)

	}//for  (long  li = 0; li < l_node_id_tool; li++)

	i_minimum_allowed_demand_increase = -1;

	return(1);

}//int  CNETsimulatorSimplyfied::iRemoveAllConnections()







/*
returned values:
any number  -  capacity
WARNING: capactiy may be below 0 in this simulator case so no error cod is returned
if any errors occur the returned value is 0
*/
long  CNETsimulatorSimplyfied::lGetActLinkCapacity(long  lLinkId)
{

	long  l_start_node_id,  l_finish_node_id;


	if  (lLinkId  <  0)  return(0);
	if  (lLinkId  >=  l_number_of_links)  return(0);

	l_start_node_id  =  pl_links_addres_table[lLinkId * 2];
	l_finish_node_id  =  pl_links_addres_table[lLinkId * 2 + 1];
	

	if  (b_const_sat_incr_demands == false)	return(pl_actual_network_state[l_start_node_id][l_finish_node_id]);

	long l_capa;
	l_capa = pl_actual_network_state[l_start_node_id][l_finish_node_id];

	if  (i_minimum_allowed_demand_increase < 0)  return(l_capa);

	l_capa = l_capa - pi_paths_per_link[l_start_node_id][l_finish_node_id] * (i_minimum_allowed_demand_increase + 1);
	return(l_capa);
}//long  CNETsimulatorSimplyfied::lGetActLinkCapacity(long  lLinkId)






/*
returned values:
any number  -  capacity
WARNING: capactiy may be below 0 in this simulator case so no error cod is returned
if any errors occur the returned value is 0
*/
long  CNETsimulatorSimplyfied::lGetMaxLinkCapacity(long  lLinkId)
{

	long  l_start_node_id,  l_finish_node_id;


	if  (lLinkId  <  0)  return(0);
	if  (lLinkId  >=  l_number_of_links)  return(0);

	l_start_node_id  =  pl_links_addres_table[lLinkId * 2];
	l_finish_node_id  =  pl_links_addres_table[lLinkId * 2 + 1];
	

	return(pl_links_table_for_nodes[l_start_node_id][l_finish_node_id]);

}//long  CNETsimulatorSimplyfied::lGetMaxLinkCapacity(long  lLinkId)







/*
returned values:
0 or more - capacity
-1  -  number too high
-2  -  number below 0
-3  -  unexpected error or node/link does not exist
*/
double  CNETsimulatorSimplyfied::dCountNodeLFN(long  lNodeId,  long  lPenalty,  bool  *pbCapacityExtending, double *pdFitnessPure, double *pdPenaltyPure)
{

	if  (lNodeId  <  0)  return(-2);
	if  (lNodeId  >=  l_node_id_tool)  return(-1);
	


	//first we compute all max capacity of links outgoing from current node
	//and all dataflow going out of the node
	double  d_max_out_capa;
	double  d_out_data_flow;
	double  d_capacity_extending;//the number of capacity units below 0 in the links outgoing from the node for penalty computing
	
	
	d_max_out_capa  =  0;
	d_out_data_flow  =  0;
	d_capacity_extending  =  0;
	for  (long li = 0; li < l_node_id_tool; li++)
	{

		d_max_out_capa  +=  pl_links_table_for_nodes[lNodeId][li];
		d_out_data_flow  +=  (pl_links_table_for_nodes[lNodeId][li] - pl_actual_network_state[lNodeId][li]);


		if  (pl_actual_network_state[lNodeId][li]  <  0)
		{
			d_capacity_extending  +=  (pl_actual_network_state[lNodeId][li])*(-1);
		}//if  (pl_actual_network_state[lNodeId][li]  <  0)

		
	}//for  (long li = 0; li < l_node_id_tool; li++)




	//now we compute LFN result
	double  d_lfn;
	double  d_buf;


	d_lfn  =  0;
	for  (long  li = 0; li < l_node_id_tool; li++)
	{

		//we care only of those links that really exists (their max capacity is above 0)
		if  (pl_links_table_for_nodes[lNodeId][li]  >  0)
		{
			d_buf  =  d_out_data_flow  -  (d_max_out_capa - pl_links_table_for_nodes[lNodeId][li]);

			if  (d_buf  <  0)  d_buf  =  0;

			d_lfn  +=  d_buf;
		}//if  (pl_links_table_for_nodes[lNodeId][li]  >  0)
	
	}//for  (li = 0; li < l_node_id_tool; li++)



	//now we have to add the capacity extending penalty
	*pbCapacityExtending  =  false;

	double  d_lfn_penalized;
	d_lfn_penalized = d_lfn;

	if  (lPenalty  >  0)
	{
		if  (d_capacity_extending  >  0)
		{
			
			d_lfn_penalized  +=  d_capacity_extending * lPenalty;
			d_lfn_penalized  =  d_lfn_penalized * d_lfn_penalized;

			*pdPenaltyPure += d_lfn_penalized - d_lfn;
			*pdFitnessPure += d_lfn;

			*pbCapacityExtending  =  true;
		}//if  (l_capacity_extending  >  0)
	}//if  (bPenalty  ==  true)






	return(d_lfn_penalized);
}//long  CNETsimulatorSimplyfied::lCountNodeLFN(long  lNodeId)




double  CNETsimulatorSimplyfied::dCountNodeLFL(long  lNodeId,  long  lPenalty,  bool  *pbCapacityExtending, double *pdFitnessPure, double *pdPenaltyPure)
{

	if  (lNodeId  <  0)  return(-2);
	if  (lNodeId  >=  l_node_id_tool)  return(-1);
	


	//first we compute all max capacity of links outgoing from current node
	//and all dataflow going out of the node
	double  d_max_out_capa, d_max_in_capa;
	double  d_out_data_flow, d_in_data_flow;
	double  d_capacity_extending;//the number of capacity units below 0 in the links outgoing from the node for penalty computing
	
	
	d_max_out_capa  =  0;
	d_out_data_flow  =  0;
	d_max_in_capa  =  0;
	d_in_data_flow  =  0;
	d_capacity_extending  =  0;
	for  (long li = 0; li < l_node_id_tool; li++)
	{

		d_max_in_capa  +=  pl_links_table_for_nodes[li][lNodeId];
		d_in_data_flow  +=  (pl_links_table_for_nodes[li][lNodeId] - pl_actual_network_state[li][lNodeId]);

		d_max_out_capa  +=  pl_links_table_for_nodes[lNodeId][li];
		d_out_data_flow  +=  (pl_links_table_for_nodes[lNodeId][li] - pl_actual_network_state[lNodeId][li]);


		if  (pl_actual_network_state[lNodeId][li]  <  0)
		{
			d_capacity_extending  +=  (pl_actual_network_state[lNodeId][li])*(-1);
		}//if  (pl_actual_network_state[lNodeId][li]  <  0)


		if  (pl_actual_network_state[li][lNodeId]  <  0)
		{
			d_capacity_extending  +=  (pl_actual_network_state[li][lNodeId])*(-1);
		}//if  (pl_actual_network_state[lNodeId][li]  <  0)

		
	}//for  (long li = 0; li < l_node_id_tool; li++)




	//now we compute LFN result
	double  d_lfl;
	double  d_buf;


	d_lfl  =  0;
	for  (long  li = 0; li < l_node_id_tool; li++)
	{

		//we care only of those links that really exists (their max capacity is above 0)
		if  (pl_links_table_for_nodes[lNodeId][li]  >  0)
		{
			d_buf  =  d_out_data_flow  -  (d_max_out_capa - pl_links_table_for_nodes[lNodeId][li]);

			if  (d_buf  <  0)  d_buf  =  0;

			d_lfl  +=  d_buf;
		}//if  (pl_links_table_for_nodes[lNodeId][li]  >  0)


		//we care only of those links that really exists (their max capacity is above 0)
		if  (pl_links_table_for_nodes[li][lNodeId]  >  0)
		{
			d_buf  =  d_in_data_flow  -  (d_max_in_capa - pl_links_table_for_nodes[li][lNodeId]);

			if  (d_buf  <  0)  d_buf  =  0;

			d_lfl  +=  d_buf;
		}//if  (pl_links_table_for_nodes[lNodeId][li]  >  0)
	
	}//for  (li = 0; li < l_node_id_tool; li++)

	d_lfl  =  d_lfl  /  2.0;

	//now we have to add the capacity extending penalty
	*pbCapacityExtending  =  false;

	double  d_lfl_penalized;
	d_lfl_penalized = d_lfl;

	if  (lPenalty  >  0)
	{
		if  (d_capacity_extending  >  0)
		{
			
			d_lfl_penalized  +=  d_capacity_extending * lPenalty;
			d_lfl_penalized  =  d_lfl_penalized * d_lfl_penalized;
			*pdPenaltyPure += d_lfl_penalized - d_lfl;
			*pdFitnessPure += d_lfl;

			*pbCapacityExtending  =  true;
		}//if  (l_capacity_extending  >  0)
	}//if  (bPenalty  ==  true)


	return(d_lfl_penalized);
}//long  CNETsimulatorSimplyfied::lCountNodeLFL(long  lNodeId,  long  lPenalty)










/*
retruned values:
1  -  ok
0  -  file creation impossible
*/
int   CNETsimulatorSimplyfied::iPresentNetwork(CString  sFileName)
{

	FILE  *pf_report;

	
	pf_report  =  fopen( (LPCSTR) sFileName, "w+");
	if  (pf_report  ==  NULL)  return(0);

	vPresentNetwork(pf_report,false);

	fclose(pf_report);
	return(1);

}//int   CNETsimulatorSimplyfied::iPresentNetwork(CString  sFileName)







void   CNETsimulatorSimplyfied::vPresentNetwork(FILE  *pfDestFile,  bool  bActualState)
{

	
	fprintf(pfDestFile,"Number of nodes:%ld\n", l_node_id_tool);
	fprintf(pfDestFile,"Number of links:%ld\n\n\n", l_number_of_links);

	fprintf(pfDestFile,"  \t");
	for  (long  li = 0; li < l_node_id_tool; li++)
		fprintf(pfDestFile,"%ld  \t", li);
	fprintf(pfDestFile,"\n");

	for  (long  li = 0; li < l_node_id_tool; li++)
	{
		fprintf(pfDestFile,"%ld  \t", li);

		for  (long  lj = 0; lj < l_node_id_tool; lj++)
		{
			if  (pl_links_table_for_nodes[li][lj]  ==  0)
				fprintf(pfDestFile,"*  \t");
			else
				if  (bActualState  ==  true)
					fprintf(pfDestFile,"%ld  \t",  pl_actual_network_state[li][lj]);
				else
					fprintf(pfDestFile,"%ld  \t",  pl_links_table_for_nodes[li][lj]);
		}//for  (long  lj = 0; lj < l_node_id_tool; lj++)
		
		fprintf(pfDestFile,"\n");
	}//for  (long  li = 0; li < l_node_id_tool; li++)



	fprintf(pfDestFile,"\n\n\n\nCapacity incr:\n\n");

	for  (long  li = 0; li < l_node_id_tool; li++)
	{
		fprintf(pfDestFile,"%ld  \t", li);

		for  (long  lj = 0; lj < l_node_id_tool; lj++)
		{
			if  (pl_links_table_for_nodes[li][lj]  ==  0)
				fprintf(pfDestFile,"*  \t");
			else
			{
				if  (pi_paths_per_link[li][lj] == 0)
					fprintf(pfDestFile,"(%ld)  \t",  pl_actual_network_state[li][lj]);
				else
					fprintf(pfDestFile,"%ld  \t",  pl_actual_network_state[li][lj]/pi_paths_per_link[li][lj]);
			}//else
		}//for  (long  lj = 0; lj < l_node_id_tool; lj++)
		
		fprintf(pfDestFile,"\n");
	}//for  (long  li = 0; li < l_node_id_tool; li++)
	

	fprintf(pfDestFile,"\n\n\n\nWays per link:\n\n");

	for  (long  li = 0; li < l_node_id_tool; li++)
	{
		fprintf(pfDestFile,"%ld  \t", li);

		for  (long  lj = 0; lj < l_node_id_tool; lj++)
		{
			if  (pl_links_table_for_nodes[li][lj]  ==  0)
				fprintf(pfDestFile,"*  \t");
			else
				fprintf(pfDestFile,"%d  \t",  pi_paths_per_link[li][lj]);
		}//for  (long  lj = 0; lj < l_node_id_tool; lj++)
		
		fprintf(pfDestFile,"\n");
	}//for  (long  li = 0; li < l_node_id_tool; li++)


	if  (b_const_sat_incr_demands == true)  fprintf(pfDestFile,"\n\n i_minimum_allowed_demand_increase: %d\n\n\n\n\n\n", i_minimum_allowed_demand_increase); 

	v_recompute_minimum_allowed_demand_increase();

	if  (b_const_sat_incr_demands == true)  fprintf(pfDestFile,"\n\n i_minimum_allowed_demand_increase: %d\n\n\n\n\n\n", i_minimum_allowed_demand_increase); 
	

}//int   CNETsimulatorSimplyfied::iPresentNetwork(CString  sFileName)










/*
retruned values:
1  -  ok
0  -  file creation impossible
*/
int   CNETsimulatorSimplyfied::iCreateBasicVirtualDatabaseFile(CString  sFileName)
{


	FILE  *pf_report;

	
	pf_report  =  fopen( (LPCSTR) sFileName, "w+");
	if  (pf_report  ==  NULL)  return(0);


	fprintf(pf_report,"%ld\n\n",  l_number_of_links);


	for  (long  li = 0; li < l_number_of_links; li++)
	{

		fprintf(pf_report,"%ld\n", pl_links_addres_table[li * 2] );
		fprintf(pf_report,"%ld\n", pl_links_addres_table[li * 2 + 1]);
		fprintf(pf_report,"1\n");
		fprintf(pf_report,"3 %ld %ld %ld\n", pl_links_addres_table[li * 2], li, pl_links_addres_table[li * 2 + 1]);
		fprintf(pf_report,"\n");

	}//for  (long  li = 0; li < c_list_of_links.lGetCapacity(); li++)

	
	fclose(pf_report);

	return(1);


}//int   CNETsimulatorSimplyfied::iCreateBasicVirtualDatabaseFile(CString  sFileName)


/*
1 - ok
0 - failed due to unknwon problem
-1 - simulator types different
*/
int  CNETsimulatorSimplyfied::iCopySimulator(CNETsimulator  *pcOtherSimulator)
{
	if  (iGetSimulatorType()  !=  pcOtherSimulator->iGetSimulatorType())
		return(-1);

	b_const_sat_incr_demands = ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->b_const_sat_incr_demands;
	i_minimum_allowed_demand_increase = ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->i_minimum_allowed_demand_increase;

	if  (l_node_id_tool  !=  ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->l_node_id_tool)
	{
		if  (pl_actual_network_state  !=  NULL)
		{
			for  (long  li = 0; li < l_node_id_tool; li++)
				delete  []  pl_actual_network_state[li];

			delete  []  pl_actual_network_state;		
		}//if  (pl_actual_network_state  !=  NULL)
		pl_actual_network_state  =  NULL;


		if  (pi_paths_per_link  !=  NULL)
		{
			for  (long  li = 0; li < l_node_id_tool; li++)
				delete  []  pi_paths_per_link[li];

			delete  []  pi_paths_per_link;		
		}//if  (pl_actual_network_state  !=  NULL)
		pi_paths_per_link  =  NULL;



		if  (pl_links_table_for_nodes !=  NULL)
		{
			for  (long  li = 0; li < l_node_id_tool; li++)
				delete  []  pl_links_table_for_nodes[li];

			delete  []  pl_links_table_for_nodes;		
		}//if  (pl_links_table_for_nodes !=  NULL)
		pl_links_table_for_nodes  =  NULL;


		if  (pl_links_addres_table  !=  NULL)
			delete  []  pl_links_addres_table;
		pl_links_addres_table  =  NULL;


		l_node_id_tool  =  ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->l_node_id_tool;

		pl_links_table_for_nodes  =  new  long*[l_node_id_tool];
		pl_actual_network_state  =  new  long*[l_node_id_tool];
		pi_paths_per_link  =  new  int*[l_node_id_tool];
		for  (int  ii = 0; ii < l_node_id_tool; ii++)
		{
			pl_links_table_for_nodes[ii]  =  new  long[l_node_id_tool];
			pl_actual_network_state[ii]  =  new  long[l_node_id_tool];		
			pi_paths_per_link[ii]  =  new  int[l_node_id_tool];
		}//for  (int  ii = 0; ii < l_node_id_tool; ii++)


		l_number_of_links  =  ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->l_number_of_links;
		pl_links_addres_table  =  new  long[l_number_of_links  *  2];
	}//if  (l_node_id_tool  !=  pcOtherNetowrk->l_node_id_tool)



	if  (l_number_of_links  !=  ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->l_number_of_links)
	{
		l_number_of_links  =  ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->l_number_of_links;
		pl_links_addres_table  =  new  long[l_number_of_links * 2];
	}//if  (l_number_of_links  !=  pcOtherNetowrk->l_number_of_links)



	for  (int  ii = 0; ii < l_node_id_tool;  ii++)
	{
		for  (int  ij = 0; ij < l_node_id_tool;  ij++)
		{
			pl_links_table_for_nodes[ii][ij]  =  ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->pl_links_table_for_nodes[ii][ij];
			pl_actual_network_state[ii][ij]  =  ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->pl_actual_network_state[ii][ij];
			pi_paths_per_link[ii][ij]  =  ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->pi_paths_per_link[ii][ij];
		}//for  (int  ij = 0; ij < l_node_id_tool;  ij++)
	}//for  (int  ii = 0; ii < l_node_id_tool;  ii++)


	for  (int  ii = 0; ii < l_number_of_links;  ii++)
	{
		pl_links_addres_table[ii * 2]  =  ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->pl_links_addres_table[ii * 2];
		pl_links_addres_table[ii * 2 + 1]  =  ((CNETsimulatorSimplyfied *)  pcOtherSimulator)->pl_links_addres_table[ii * 2 + 1];	
	}//for  (int  ii = 0; ii < l_number_of_links;  ii++)
			

	return(1);
}//int  CNETsimulatorSimplyfied::iCopySimulator()


bool  CNETsimulatorSimplyfied::bIsTheSame(CNETsimulatorSimplyfied  *pcOtherNetowrk)
{
	if  (l_node_id_tool  !=  pcOtherNetowrk->l_node_id_tool)  return(false);
	if  (l_number_of_links  !=  pcOtherNetowrk->l_number_of_links)  return(false);

	for  (int  ii = 0; ii < l_node_id_tool;  ii++)
		for  (int  ij = 0; ij < l_node_id_tool;  ij++)
			if  (
					pl_links_table_for_nodes[ii][ij]
					!=
					pcOtherNetowrk->pl_links_table_for_nodes[ii][ij]
				)
				return(false);

	return(true);

}//bool  CNETsimulatorSimplyfied::bIsTheSame(CNETsimulatorSimplyfied  *pcOtherNetowrk)







//----------------------end of implementation of CNETsimulatorSimplyfied--------------------------------------------

















//--------------implemenatation of class  CNETsimulatorComplex--------------------------------------------
//--------------------------------------------------------------------------------------------------------------

CNETsimulatorComplex::CNETsimulatorComplex()
{

	l_node_id_tool  =  0;//used as counter of ids of nodes
	l_link_id_tool  =  0;//used as counter of ids of nodes
	l_connection_id_tool  =  1;//used as counter of ids of nodes


	//acces optimalization tools
	pc_nodes_table  =  NULL;
	pc_links_table  =  NULL;
//	pc_connections_table  =  NULL;


}//CNETsimulatorComplex::CNETsimulatorComplex()




CNETsimulatorComplex::~CNETsimulatorComplex()
{

	long  l_max;
	long  li;


	c_list_of_nodes.bFirst();
	l_max  =  c_list_of_nodes.lGetCapacity();

	for  (li = 0; li < l_max; li++)
	{
		delete (CNETnode *) c_list_of_nodes.pcGetNode()->pvGetObject();
		c_list_of_nodes.bNext();
	}//for  (li = 0; li < l_max; li++)



	c_list_of_links.bFirst();
	l_max  =  c_list_of_links.lGetCapacity();

	for  (li = 0; li < l_max; li++)
	{
		delete (CNETlink *) c_list_of_links.pcGetNode()->pvGetObject();
		c_list_of_links.bNext();
	}//for  (li = 0; li < l_max; li++)



	c_list_of_connections.bFirst();
	l_max  =  c_list_of_connections.lGetCapacity();

	for  (li = 0; li < l_max; li++)
	{
		delete (CNETconnection *) c_list_of_connections.pcGetNode()->pvGetObject();
		c_list_of_connections.bNext();
	}//for  (li = 0; li < l_max; li++)
	


	
	

	c_list_of_nodes.vBYE(false);
	c_list_of_links.vBYE(false);
	c_list_of_connections.vBYE(false);


	if  (pc_nodes_table  !=  NULL)  delete  pc_nodes_table;
	if  (pc_links_table  !=  NULL)  delete  pc_links_table;
//	if  (pc_connections_table  !=  NULL)  delete  pc_connections_table;

}//CNETsimulatorComplex::~CNETsimulatorComplex()










//returns the node id (-1 if the operation is unsuccessfull)
long  CNETsimulatorComplex::lAddNewNode(long  lCapacity,  CString  sName)
{

	CNETnode  *pc_new_node;
	long      l_new_node_id;
	CNETnode  **pc_new_nodes_table;


	pc_new_node  =  new  CNETnode;

	
	
	if  (pc_new_node  ==  NULL)  return(-1);// we return error if the operation is unsuccessfull

	
	if  (pc_new_node->bSetCapacity(lCapacity)  ==  false)  return(-2);

	
	
	if  (c_list_of_nodes.bAdd(pc_new_node)  ==  false)
	{
		delete  pc_new_node;
		return(-1);
	}//if  (c_list_of_nodes.bAdd()  ==  false)




	//first we check wheather there's no free places in current table
	l_new_node_id  =  -1;
	if  (pc_nodes_table  !=  NULL)
	{

		for  (long  li = 0;(li < l_node_id_tool)&&(l_new_node_id == -1); li++)
		{

			if  (pc_nodes_table[li]  ==  NULL)  l_new_node_id  =  li;
		
		}//for  (long  li = 0;li < l_node_id_tool; li++)
	
	}//if  (pc_nodes_table  !=  NULL)





	//if we have found a free id in the table we set it as new node's id and finish
	if  (l_new_node_id  !=  -1)
	{

		pc_new_node->b_change_id(l_new_node_id);
		pc_nodes_table[l_new_node_id]  =  pc_new_node;

		return(l_new_node_id);
			
	}//if  (l_new_node_id  !=  -1)




	//if there's no free id in the table we have to create a new one and rewrite the values from previous
	l_node_id_tool++;
	pc_new_nodes_table  =  new   CNETnode*  [l_node_id_tool];

	//if the error occurs
	if  (pc_new_nodes_table  ==  NULL)
	{

		l_node_id_tool--;
		delete  (CNETnode*)  (c_list_of_nodes.pcGetNode()->pvGetObject());
		c_list_of_nodes.bDeleteActual(false);
		return(-1);
	
	}//if  (pc_new_nodes_table  ==  NULL)




	//if everything is ok we copy the data and destroy the previous table 
	//and put the new one instead
	for  (long lj = 0; lj < l_node_id_tool - 1;lj++)
		pc_new_nodes_table[lj]  =  pc_nodes_table[lj];


	pc_new_node->b_change_id(l_node_id_tool - 1);
	pc_new_nodes_table[l_node_id_tool - 1]  =  pc_new_node;


	delete  []  pc_nodes_table;
	pc_nodes_table  =  pc_new_nodes_table;



	return(l_node_id_tool - 1);



}//long  CNETsimulatorComplex::lAddNewNode(long  lCapacity,  CString  sName)






/*
returned values:
0  -  operation successfull
-1 - node id below 0
-2 - node id above upper border
-3 - node does not exist
-4 - node undeletable!
-5 - fatal error!!! node id was not found in the main list!!!
*/  
int  CNETsimulatorComplex::iDeleteNode(long  lNodeId)
{

	//first error communication
	if  (lNodeId  <  0)  return(-1);
	if  (lNodeId  >= l_node_id_tool)  return(-2);

	if  (pc_nodes_table[lNodeId]  ==  NULL)  return(-3);

	if  (pc_nodes_table[lNodeId]->bIsDeletable()  ==  false)  return(-4);


	//first we must search for the node in the main list
	c_list_of_nodes.bFirst();

	long  l_max  =  c_list_of_nodes.lGetCapacity();
	bool  b_finished  =  false;

	for  (long  li = 0; (li < l_max)&&(b_finished == false) ; li++)
	{

		if  (
			((CNETnode*)  c_list_of_nodes.pcGetNode()->pvGetObject())->lGetId()
			==
			lNodeId
			)
		{

			b_finished  =  true;
			delete  (CNETnode*)  (c_list_of_nodes.pcGetNode()->pvGetObject());
			c_list_of_nodes.bDeleteActual(false);
		
		}//if

		c_list_of_nodes.bNext();
	
	}//for  (long  li = 0; (li < l_max)&&(b_finished == false) ; li++)

	
	if  (b_finished  ==  false)  return(-5);

	pc_nodes_table[lNodeId]  =  NULL;


	return(0);//all ok!



}//bool  CNETsimulatorComplex::bDeleteNode(long  lNodeId)










/*
returned values:
1  -  ok
0  -  node not found
-1 -  operation unsuccessfull

*/
int   CNETsimulatorComplex::iSetNodeCapacity(long  lNodeId, long  lNewCapacity)
{

	if  (pc_nodes_table  ==  NULL)  return(0);
	if  (l_node_id_tool  <=  lNodeId)  return(0);
	if  (pc_nodes_table[lNodeId]  ==  NULL)  return(0);

	if  (pc_nodes_table[lNodeId]->bSetCapacity(lNewCapacity)  ==  true)
		return(1);
	else
		return(-1);

}//int   CNETsimulatorComplex::iSetNodeCapacity(long  lNodeId, lNewCapacity)










/*
returned values (if it's below 0 it's an error):
0 or more - new link id
-1 - start node does not exist
-2 - finish node does not exist
-3 - memory allocation problem
-4 - plug operation unsuccesfull
-5 - bad capacity inputted
*/ 
long  CNETsimulatorComplex::lCreateLink(long  lStartNodeId, long  lFinishNodeId,  long lCapacity)
{

	if  (pc_nodes_table  ==  NULL)  return(-1);
	if  (pc_nodes_table[lStartNodeId]  ==  NULL)  return(-1);

	if  (pc_nodes_table[lFinishNodeId]  ==  NULL)  return(-2);

	
	CNETlink  *pc_new_link;
	long      l_new_link_id;
	CNETlink  **pc_new_links_table;


	pc_new_link  =  new  CNETlink;
	if  (pc_new_link->bSetCapacity(lCapacity)  ==  false)  return(-5);

	if  (
		pc_new_link->bPlugFinishStart(false,lStartNodeId,pc_nodes_table[lStartNodeId])
		==
		false
		)
	{
		delete  pc_new_link;
		return(-4);
	}//if



	if  (
		pc_new_link->bPlugFinishStart(true,lFinishNodeId,pc_nodes_table[lFinishNodeId])
		==
		false
		)
	{
		delete  pc_new_link;
		return(-4);
	}//if


	
	

	
	if  (pc_new_link  ==  NULL)  return(-3);// we return error if the operation is unsuccessfull

	
	
	if  (c_list_of_links.bAdd(pc_new_link)  ==  false)
	{
		delete  pc_new_link;
		return(-3);
	}//if  (c_list_of_nodes.bAdd()  ==  false)




	//first we check wheather there's no free places in current table
	l_new_link_id  =  -1;
	if  (pc_links_table  !=  NULL)
	{

		for  (long  li = 0;(li < l_link_id_tool)&&(l_new_link_id == -1); li++)
		{

			if  (pc_links_table[li]  ==  NULL)  l_new_link_id  =  li;
		
		}//for  (long  li = 0;li < l_node_id_tool; li++)
	
	}//if  (pc_nodes_table  !=  NULL)





	//if we have found a free id in the table we set it as new node's id and finish
	if  (l_new_link_id  !=  -1)
	{

		pc_new_link->b_change_id(l_new_link_id);
		pc_links_table[l_new_link_id]  =  pc_new_link;

		return(l_new_link_id);
			
	}//if  (l_new_node_id  !=  -1)




	//if there's no free id in the table we have to create a new one and rewrite the values from previous
	l_link_id_tool++;
	pc_new_links_table  =  new   CNETlink*  [l_link_id_tool];

	//if the error occurs
	if  (pc_new_links_table  ==  NULL)
	{

		l_link_id_tool--;
		delete  (CNETlink *) (c_list_of_links.pcGetNode()->pvGetObject());
		c_list_of_links.bDeleteActual(false);
		return(-1);
	
	}//if  (pc_new_nodes_table  ==  NULL)




	//if everything is ok we copy the data and destroy the previous table 
	//and put the new one instead
	for  (long lj = 0; lj < l_link_id_tool - 1;lj++)
		pc_new_links_table[lj]  =  pc_links_table[lj];


	pc_new_link->b_change_id(l_link_id_tool - 1);
	pc_new_links_table[l_link_id_tool - 1]  =  pc_new_link;


	delete  []  pc_links_table;
	pc_links_table  =  pc_new_links_table;



	return(l_link_id_tool - 1);



}//long  CNETsimulatorComplex::lCreteLink(long  lStartNodeId, long  lFinishNodeId)









/*
returned values:
0  -  operation successfull
-1 - link id below 0
-2 - link id above upper border
-3 - link does not exist
-4 - link undeletable!
-5 - fatal error!!! link id was not found in the main list!!!
*/  
int   CNETsimulatorComplex::iDeleteLink(long  lLinkId)
{

	//first error communication
	if  (lLinkId  <  0)  return(-1);
	if  (lLinkId  >= l_link_id_tool)  return(-2);

	if  (pc_links_table[lLinkId]  ==  NULL)  return(-3);

	if  (pc_links_table[lLinkId]->bIsDeletable()  ==  false)  return(-4);


	//first we must search for the node in the main list
	c_list_of_links.bFirst();

	long  l_max  =  c_list_of_links.lGetCapacity();
	bool  b_finished  =  false;

	for  (long  li = 0; (li < l_max)&&(b_finished == false) ; li++)
	{

		if  (
			((CNETlink*)  c_list_of_links.pcGetNode()->pvGetObject())->lGetId()
			==
			lLinkId
			)
		{

			b_finished  =  true;
			delete  (CNETlink *) (c_list_of_links.pcGetNode()->pvGetObject());
			c_list_of_links.bDeleteActual(false);
		
		}//if

		c_list_of_links.bNext();
	
	}//for  (long  li = 0; (li < l_max)&&(b_finished == false) ; li++)

	
	if  (b_finished  ==  false)  return(-5);

	pc_links_table[lLinkId]  =  NULL;


	return(0);//all ok!


}//int   CNETsimulatorComplex::iDeleteLink(long  lLinkId)






/*
returned values:
1  -  ok
0  -  physically ok, but capacity is too small
-1 -  bad way length
-2 -  parity error
-3 -  capacity below 0
-4 -  one of links does not exist
-5 -  one nodes does not exist or is not a begin/end of one of links
*/
int   CNETsimulatorComplex::iCheckConnection
	(long  *plWay, int iWayLength, long  lCapacity, bool bCheckActualCapacity)
{

	if  (pc_nodes_table  ==  NULL)  return(-5);

	if  (lCapacity  <  0)  return(-3);

	if  (iWayLength  <  3)  return(-1);

	//if the way length is a parit number then it is wrong
	int  ii;
	ii  =  iWayLength / 2;
	if  (ii * 2  ==  iWayLength)  return(-2);



	bool  b_capacity_ok;
	long  l_start_node_id;
	long  l_finish_node_id;
	long  l_link_id;


	b_capacity_ok  =  true;//initial step for loop
	l_finish_node_id  =  plWay[0];//initial step for loop

	for  (int ij = 0; ij < (iWayLength - 1) / 2; ij++)
	{

		l_start_node_id  =  l_finish_node_id;
		l_link_id  =  plWay[ij * 2 + 1];
		l_finish_node_id  =  plWay[ij * 2 + 2];


		if  (pc_links_table  ==  NULL)  return(-4);
		if  (pc_links_table[l_link_id]  ==  NULL)  return(-4);
		if  (pc_links_table[l_link_id]->lGetStartNodeId()  !=  l_start_node_id)  return(-5);
		if  (pc_links_table[l_link_id]->lGetFinishNodeId()  !=  l_finish_node_id)  return(-5);


		//capacity checking only if this is still ok
		if  (b_capacity_ok  ==  true)
		{
			if  (bCheckActualCapacity  ==  true)
			{

				if  (pc_nodes_table[l_start_node_id]->lGetActualCapacity()  <  lCapacity)
					b_capacity_ok  =  false;

				if  (pc_links_table[l_link_id]->lGetActualCapacity()  <  lCapacity)
					b_capacity_ok  =  false;

			}//if  (bCheckActualCapacity  ==  true)
			else
			{

				if  (pc_nodes_table[l_start_node_id]->lGetMaxCapacity()  <  lCapacity)
					b_capacity_ok  =  false;

				if  (pc_links_table[l_link_id]->lGetMaxCapacity()  <  lCapacity)
					b_capacity_ok  =  false;
			
			}//else if  (bCheckActualCapacity  ==  true)

		}//if  (b_capacity_ok  ==  true)

	}//for  (int ij = 0; ij < (iWayLength - 1) / 2; ij++)


	//the post step of trajectory checking algorithm
	//capacity checking only if this is still ok
	if  (b_capacity_ok  ==  true)
	{
		if  (bCheckActualCapacity  ==  true)
		{

			if  (pc_nodes_table[l_finish_node_id]->lGetActualCapacity()  <  lCapacity)
				b_capacity_ok  =  false;

		}//if  (bCheckActualCapacity  ==  true)
		else
		{

			if  (pc_nodes_table[l_finish_node_id]->lGetMaxCapacity()  <  lCapacity)
				b_capacity_ok  =  false;

		}//else if  (bCheckActualCapacity  ==  true)

	}//if  (b_capacity_ok  ==  true)

	

	//if we managed to get here it means that trajectory exists
	//so the value returned depends only on capacity check...

	if  (b_capacity_ok  ==  true)
		return(1);
	else
		return(0);


	return(0);

}//int   CNETsimulatorComplex::iCheckConnection(long  *plWay, int iWayLength)







/*
returned values:
0 or more - link id
-1  -  link not found
-2  -  link table empty
*/
long  CNETsimulatorComplex::lFindLinkIdForNodes(long  lStartNode,  long  lFinishNode)
{

	//if the links table does not exist we return an error message
	if  ( (pc_links_table  ==  NULL)&&(l_link_id_tool  <  0) )  return(-2);

	for  (long  li = 0; li < l_link_id_tool; li++)
	{

		if  (pc_links_table[li]  !=  NULL)
		{
			if  (
				(pc_links_table[li]->lGetStartNodeId()  ==  lStartNode)
				&&
				(pc_links_table[li]->lGetFinishNodeId()  ==  lFinishNode)
				)
				return(li);//when we find the proper link we just return it and finish whole procedure
							
		
		}//if  (pc_links_table[li]  !=  NULL)
	
	}//for  (long  li = 0; (b_found == false)&&(li < l_link_id_tool) ; li++)


	return(-1);

}//long  CNETsimulatorComplex::lFindLinkIdForNodes(long  lStartNode,  long  lFinishNode)









/*
returned values:
1 or more  -  ok
0  -  physically ok, but capacity is too small
-1 -  bad way length
-2 -  parity error
-3 -  capacity below 0
-4 -  one of links does not exist
-5 -  one nodes does not exist or is not a begin/end of one of links
-6 -  mewmory allocation problem
-7 -  connection setting for nodes and links unsuccesfull
-8 -  way set in connection objerct unsuccessfull
*/
long  CNETsimulatorComplex::lSetUpConnection(long  *plWay, int iWayLength, long  lCapacity)
{

	int  i_check_trajectory_result;



	if  (b_check_connection_on  ==  false)
		i_check_trajectory_result  =  1;
	else
		i_check_trajectory_result  =  iCheckConnection(plWay, iWayLength, lCapacity);


	if  (i_check_trajectory_result  !=  1)  return(i_check_trajectory_result);

	
	//if the trajectory is ok we set up a connection


	CNETconnection  *pc_new_connection;

	pc_new_connection  =  new  CNETconnection;
	pc_new_connection->bSetCapacity(lCapacity);
	if  (pc_new_connection  ==  NULL)  return(-6);


	
	
	if  (c_list_of_connections.bAdd(pc_new_connection)  ==  false)
	{
		delete  pc_new_connection;
		return(-6);
	}//if  (c_list_of_nodes.bAdd()  ==  false)



	//we give the connection an id...
	pc_new_connection->b_change_id(l_connection_id_tool++);



	//now we have to set up connection for all the nodes and links on the connection way
	if  (
		b_set_connection_for_nodes_and_links(plWay, iWayLength, pc_new_connection, lCapacity)  
		==
		false
		)
	{

		delete  ((CNETconnection *) c_list_of_connections.pcGetNode()->pvGetObject());
		c_list_of_connections.bDeleteActual(false);

		return(-7);
			
	}//if



	//now we put the connection way into the connection object
	if  (pc_new_connection->bSetConnectionWay(plWay, iWayLength)  ==  false )
	{

		b_remove_connection_on_the_way(plWay, iWayLength, l_connection_id_tool);
		return(-8);
	}//if  (pc_new_connection->bSetConnectionWay(plWay, iWayLength)  ==  false )
	




	return(l_connection_id_tool - 1);


}//int   CNETsimulatorComplex::iSetUpConnection(long  *plWay, int iWayLength, long  lCapacity)








bool  CNETsimulatorComplex::b_set_connection_for_nodes_and_links
	(long  *plWay, int iWayLength,  
	 CNETconnection *pcNewConnection, long  lConnectionCapacity)
{


	if  (
		pc_nodes_table[plWay[0]]->bSetUpConnection (pcNewConnection, lConnectionCapacity)
		==
		false
		)
		return(false);


	for  (int  ii = 1;  ii <  iWayLength;  ii += 2)
	{

		if  (
			pc_links_table[plWay[ii]]->bSetUpConnection (pcNewConnection, lConnectionCapacity)
			==
			false
			)
		{

			long  l_conn_id;
			l_conn_id  =  pcNewConnection->lGetId();

			for  (int  ij = ii;  ij > 0; ij = ij - 2)
			{

				pc_links_table[ij]->iRemoveConnection(l_conn_id);
				pc_nodes_table[ij - 1]->iRemoveConnection(l_conn_id);
			
			}//for  (int  ij = ii;  ij > 0; ij = ij - 2)


			return(false);
		
		}//if



		if  (
			pc_nodes_table[plWay[ii+1]]->bSetUpConnection (pcNewConnection, lConnectionCapacity)
			==
			false
			)
		{

			long  l_conn_id;
			l_conn_id  =  pcNewConnection->lGetId();

			for  (int  ij = ii;  ij > 0; ij = ij - 2)
			{

				pc_nodes_table[ij]->iRemoveConnection(l_conn_id);

				if  (ij - 1 >= 0)
					pc_links_table[ij - 1]->iRemoveConnection(l_conn_id);
			
			}//for  (int  ij = ii;  ij > 0; ij = ij - 2)


			return(false);

		}//if
	
	}//for  (int  ii = 1;  ii <  iWayLength;  ii += 2)




	return(true);
	

	

}//bool  CNETsimulatorComplex::b_set_connection_for_nodes_and_links







/*
returned values:
1  -  ok
0  -  operarion done, but some of nodes/links returned unsuccessfull result after removal
-1 -  connection not found
*/
int   CNETsimulatorComplex::iRemoveConnection(long  lConnectionId)
{

	CNETconnection  *pc_searched_conn;

	//first we find connection and connection way
	if  (c_list_of_connections.bLast()  ==  false)  return(-1);


	long  l_max;
	bool  b_finished  =  false;
	l_max  =  c_list_of_connections.lGetCapacity();

	for  (long  li = 0; (li < l_max)&&(b_finished == false); li++)
	{

		if  (
			((CNETconnection *)  c_list_of_connections.pcGetNode()->pvGetObject())->lGetId()
			==
			lConnectionId
			)
		{

			b_finished  =  true;
			pc_searched_conn  =  (CNETconnection *) c_list_of_connections.pcGetNode()->pvGetObject();
			
			c_list_of_connections.bDeleteActual(false);
		
		}//if


		c_list_of_connections.bPrev();
	
	}//for  (long  li = 0; li < l_max; li++)



	//if we didn't find a proper id in the list
	if  (b_finished  ==  false)  return(-2);







	//now we get the way
	long  *pl_way;
	int  i_way_length;
	

	i_way_length  =  pc_searched_conn->iGetConnectionWay(&pl_way);


	
	if  (b_remove_connection_on_the_way(pl_way, i_way_length, lConnectionId)  ==  true)
	{
		delete  pc_searched_conn;
		return(1);
	}//if  (b_remove_connection_on_the_way(pl_way, i_way_length, lConnectionId)  ==  true)
	else
	{
		delete  pc_searched_conn;
		return(0);
	}//else  if  (b_remove_connection_on_the_way(pl_way, i_way_length, lConnectionId)  ==  true)


}//int   CNETsimulatorComplex::iRemoveConnection(long  lConnectionId)








/*
returned  values:
1  -  ok
0  -  no connections to remove
-1 -  problems occured when removing one or more connections
*/
int  CNETsimulatorComplex::iRemoveAllConnections()
{


	if  (c_list_of_connections.bFirst()  ==  false)  return(0);


	CNETconnection  *pc_conn_buff;
	long  *pl_way;
	int   i_way_length;
	bool  b_all_removed_correct  =  true;




	for  (long  li = 0; c_list_of_connections.bFirst()  ==  true; li++)
	{

		pc_conn_buff  =  (CNETconnection *) c_list_of_connections.pcGetNode()->pvGetObject();
		c_list_of_connections.bDeleteActual(false);

		i_way_length  =  pc_conn_buff->iGetConnectionWay(&pl_way);


		if  (b_remove_connection_on_the_way(pl_way, i_way_length, pc_conn_buff->lGetId())  ==  true)
			delete  pc_conn_buff;
		else
		{
			delete  pc_conn_buff;
			b_all_removed_correct  =  false;
		}//else  if  (b_remove_connection_on_the_way(pl_way, i_way_length, pc_conn_buff->lGetId())  ==  true)
		
	}//for  (long  li = 0; li <  c_list_of_connections.lGetCapacity(); li++)


	if  (b_all_removed_correct  ==  true)
		return(1);
	else
		return(-1);

}//int  CNETsimulatorComplex::iRemoveAllConnections()









bool  CNETsimulatorComplex::b_remove_connection_on_the_way(long  *plWay, int iWayLength, long  lConnectionId)
{

	bool  b_all_op_ok = true;// needed to remember that something was wrong during removal



	if  (iWayLength  >  0)
	{

		if  (pc_nodes_table[plWay[0]]->iRemoveConnection(lConnectionId)  !=  1)
			b_all_op_ok  =  false;


		for  (int  ii = 1; ii < iWayLength;  ii+=2)
		{

			if  (pc_links_table[plWay[ii]]->iRemoveConnection(lConnectionId)  !=  1)
				b_all_op_ok  =  false;


			if  (pc_nodes_table[plWay[ii + 1]]->iRemoveConnection(lConnectionId)  !=  1)
				b_all_op_ok  =  false;
		
		}//for  (int  ii = 1; ii < i_way_length;  ii+=2)

	
	}//if  (i_way_length  >  0)



	if  (b_all_op_ok  ==  true)
		return(1);
	else
		return(0);




}//bool  CNETsimulatorComplex::b_remove_connection_on_the_way(long  *plWay, int iWayLength)










/*
returned values:
0 or more - capacity
-1  -  number too high
-2  -  number below 0
-3  -  unexpected error or node/link does not exist
*/
long  CNETsimulatorComplex::lGetActNodeCapacity(long  lNodeId)
{

	if  (lNodeId  <  0)  return(-2);
	if  (lNodeId  >=  l_node_id_tool)  return(-1);
	if  (pc_nodes_table[lNodeId]  ==  NULL)  return(-3);

	return(pc_nodes_table[lNodeId]->lGetActualCapacity());

}//long  CNETsimulatorComplex::lGetActNodeCapacity(long  lNodeNum)




/*
returned values:
0 or more - capacity
-1  -  number too high
-2  -  number below 0
-3  -  unexpected error or node/link does not exist
*/
long  CNETsimulatorComplex::lGetActLinkCapacity(long  lLinkId)
{

	if  (lLinkId  <  0)  return(-2);
	if  (lLinkId  >=  l_link_id_tool)  return(-1);
	if  (pc_links_table[lLinkId]  ==  NULL)  return(-3);

	return(pc_links_table[lLinkId]->lGetActualCapacity());

}//long  CNETsimulatorComplex::lGetActLinkCapacity(long  lLinkId)





/*
returned values:
0 or more - capacity
-1  -  number too high
-2  -  number below 0
-3  -  unexpected error or node/link does not exist
*/
long  CNETsimulatorComplex::lGetMaxNodeCapacity(long  lNodeId)
{

	if  (lNodeId  <  0)  return(-2);
	if  (lNodeId  >=  l_node_id_tool)  return(-1);
	if  (pc_nodes_table[lNodeId]  ==  NULL)  return(-3);

	return(pc_nodes_table[lNodeId]->lGetMaxCapacity());

}//long  CNETsimulatorComplex::lGetMaxNodeCapacity(long  lNodeId)






/*
returned values:
0 or more - capacity
-1  -  number too high
-2  -  number below 0
-3  -  unexpected error or node/link does not exist
*/
long  CNETsimulatorComplex::lGetMaxLinkCapacity(long  lLinkId)
{

	if  (lLinkId  <  0)  return(-2);
	if  (lLinkId  >=  l_link_id_tool)  return(-1);
	if  (pc_links_table[lLinkId]  ==  NULL)  return(-3);

	return(pc_links_table[lLinkId]->lGetActualCapacity());


}//long  CNETsimulatorComplex::lGetMaxLinkCapacity(long  lLinkId);






/*
returned values:
0 or more - capacity
-1  -  number too high
-2  -  number below 0
-3  -  unexpected error or node/link does not exist
*/
double    CNETsimulatorComplex::dCountNodeLFN(long  lNodeId,  long  lPenalty,  bool  *pbCapacityExtending, double *pdPenaltyPure)
{

	if  (lNodeId  <  0)  return(-2);
	if  (lNodeId  >=  l_node_id_tool)  return(-1);
	if  (pc_nodes_table[lNodeId]  ==  NULL)  return(-3);


	return(pc_nodes_table[lNodeId]->lCountLFN());


}//double  CNETsimulatorComplex::dCountNodeLFN(long  lNodeId)











/*
retruned values:
1  -  ok
0  -  file creation impossible
*/
int   CNETsimulatorComplex::iPresentNetwork(CString  sFileName)
{

	FILE  *pf_report;

	
	pf_report  =  fopen( (LPCSTR) sFileName, "w+");
	if  (pf_report  ==  NULL)  return(0);



	c_list_of_nodes.bFirst();
	for  (long  li = 0; li < c_list_of_nodes.lGetCapacity(); li++)
	{

		((CNETnode *)  c_list_of_nodes.pcGetNode()->pvGetObject())->vPresent(pf_report);

		c_list_of_nodes.bNext();

	}//for  (long  li = 0; li < c_list_of_nodes.lGetCapacity; li++)




	fclose(pf_report);

	return(1);


}//void  CNETsimulatorComplex::vPresentNetwork(CString  sFileName)








/*
retruned values:
1  -  ok
0  -  file creation impossible
*/
int   CNETsimulatorComplex::iCreateBasicVirtualDatabaseFile(CString  sFileName)
{


	FILE  *pf_report;

	
	pf_report  =  fopen( (LPCSTR) sFileName, "w+");
	if  (pf_report  ==  NULL)  return(0);


	fprintf(pf_report,"%ld\n\n",  c_list_of_links.lGetCapacity());


	c_list_of_links.bFirst();
	for  (long  li = 0; li < c_list_of_links.lGetCapacity(); li++)
	{

		((CNETlink *)  c_list_of_links.pcGetNode()->pvGetObject())->vCreateBasiCVirtualWay(pf_report);

		c_list_of_links.bNext();

	}//for  (long  li = 0; li < c_list_of_links.lGetCapacity(); li++)



	fclose(pf_report);

	return(1);


}//int   CNETsimulatorComplex::iCreateBasicVirtualDatabaseFile(CStringsFileName)



//----------------------end of implementation of CNETsimulatorComplex--------------------------------------------








//--------------implemenatation of class  CNETnode--------------------------------------------
//--------------------------------------------------------------------------------------------------------------

CNETnode::CNETnode()
{

	l_id  = -1;//"unset" value assigned

	s_name  =  "no name";

		
	l_max_capacity  =  0;//no capacity
	l_actual_capacity  =  0;

}//CNETnode::CNETnode()





CNETnode::~CNETnode()
{

	c_list_net_links_out.vBYE(false);//just delete list components without deleting carried objects
	c_list_net_links_in.vBYE(false);//just delete list components without deleting carried objects
	c_list_of_net_connections.vBYE(false);

}//CNETnode::~CNETnode()





bool  CNETnode::b_change_id(long  lNewId)
{

	if  (lNewId  <  0)  return(false);

	l_id  =  lNewId;

	return(true);

}//bool  CNETnode::b_change_id(long  lNewId)









bool  CNETnode::bSetCapacity(long  lNewCapacity)
{

	if  (l_max_capacity  -  l_actual_capacity  >  lNewCapacity)
		return(false);


	l_actual_capacity  =  lNewCapacity  -  (l_max_capacity  -  l_actual_capacity);
	l_max_capacity  =  lNewCapacity;



	return(true);
	

}//bool  CNETnode::bSetCapacity(long  lNewCapacity)






//if the node is attracted to any connection or link then it is undeletable
bool  CNETnode::bIsDeletable()
{

	//if the lists are not empty we can not delete the node
	if  (c_list_net_links_in.bFirst()  ==  true)  return(false);
	if  (c_list_net_links_out.bFirst()  ==  true)  return(false);
	if  (c_list_of_net_connections.bFirst()  ==  true)  return(false);

	return(true);

}//bool  CNETnode::bIsDeletable()







bool  CNETnode::bAddNewLink(bool  bInOut, CNETlink  *pcNewLink)
{

	CMyList  *pc_list_for_adding;


	if  (bInOut  ==  true)
		pc_list_for_adding  =  &c_list_net_links_in;
	else
		pc_list_for_adding  =  &c_list_net_links_out;


	if  (pc_list_for_adding->bAdd(pcNewLink)  ==  true)
		return(true);
	else
		return(false);


}//bool  CNETnode::bAddNewLink(bool  bInOut, CNETlink  *pcNewLink)








bool  CNETnode::bRemoveLink(bool  bInOut, CNETlink  *pcRemovedLink)
{

	CMyList  *pc_list_for_removal;


	if  (bInOut  ==  true)
		pc_list_for_removal  =  &c_list_net_links_in;
	else
		pc_list_for_removal  =  &c_list_net_links_out;


	//now we are looking for the specified link
	if  (pc_list_for_removal->bFirst()  ==  false)  return(false);


	long  l_max;
	l_max  =  pc_list_for_removal->lGetCapacity();
	bool  b_finish;
	b_finish  =  false;


	for  (long  li = 0; (li < l_max)&&(b_finish == false); li++)
	{
		if  (
			(CNETlink*) (pc_list_for_removal->pcGetNode()->pvGetObject())
			==
			pcRemovedLink
			)
		{
			b_finish  =  true;
			pc_list_for_removal->bDeleteActual(false);
		}//if
	}//for  (long  li = 0; (li < l_max)&&(b_finish == false); li++)


	return(b_finish);

	

}//bool  CNETnode::bRemoveLink(bool  bInOut, CNETlink  *pcRemovedLink)








bool  CNETnode::bSetUpConnection(CNETconnection  *pcNewConnection, long  lConnectionCapacity)
{

	//if it's impossible to set the connection
	if  (l_actual_capacity  <  lConnectionCapacity)  return(false);

	//if the capacity is ok we set up the connection
	if  (c_list_of_net_connections.bAdd(pcNewConnection)  ==  false)  return(false);

	//now we decrease the actual capacity information
	l_actual_capacity  =  l_actual_capacity  -  lConnectionCapacity;


	return(true);
	

}//bool  CNETnode::bSetUpConnection(CNETconnection  *pcNewConnection, long  lConnectionCapacity)







/*
returned values:
1  -  ok
0  -  connection was not found
-1 -  removal of found connection unsuccessfull
*/
int   CNETnode::iRemoveConnection(long  lConnectionId)
{

	//if the list is emopty...
	if  (c_list_of_net_connections.bLast()  ==  false)  return(0);


	long  l_list_capacity;
	
	l_list_capacity  =  c_list_of_net_connections.lGetCapacity();

	
	
	for  (long  li = 0; (li < l_list_capacity); li++)
	{

		if  (
			((CNETconnection *) c_list_of_net_connections.pcGetNode()->pvGetObject())->lGetId()
			==
			lConnectionId
			)
		{

			l_actual_capacity  +=
			(
			(CNETconnection *) c_list_of_net_connections.pcGetNode()->pvGetObject()
			)->lGetCapacity();
			
				
			//not likely to happen but you never know...
			if  (c_list_of_net_connections.bDeleteActual(false)  ==  false) 
			{
				l_actual_capacity  =  l_actual_capacity  -
				(
				(CNETconnection *) c_list_of_net_connections.pcGetNode()->pvGetObject()
				)->lGetCapacity();
				
				return(-1);
			}//if  (c_list_of_net_connections.bDeleteActual(false)  ==  false) 

			return(1);
		}//if


		c_list_of_net_connections.bPrev();
	
	}//for  (long  li = 0; li < l_list_capacity; li++)


	return(0);

}//int   CNETnode::iRemoveConnection(long  lConnectionId)








long  CNETnode::lCountLFN()
{

	//first we compute all max capacity of links outgoing from current node
	//and all dataflow going out of the node
	long  l_max_out_capa;
	long  l_out_data_flow;
	CNETlink  *pc_buf_link;


	if  (c_list_net_links_out.bFirst()  !=  true)  return(0);


	l_max_out_capa  =  0;
	l_out_data_flow  =  0;
	for  (long li = 0; li < c_list_net_links_out.lGetCapacity(); li++)
	{

		pc_buf_link  =  (CNETlink *)  c_list_net_links_out.pcGetNode()->pvGetObject();


		l_max_out_capa  +=  pc_buf_link->lGetMaxCapacity();	
		l_out_data_flow  +=  (pc_buf_link->lGetMaxCapacity() - pc_buf_link->lGetActualCapacity());

		c_list_net_links_out.bNext();

	}//for  (long li = 0; li < c_list_net_links_out.lGetCapacity; li++)




	//now we compute LFN result
	long  l_lfn;
	long  l_buf;


	c_list_net_links_out.bFirst();
	l_lfn  =  0;
	for  (long  li = 0; li < c_list_net_links_out.lGetCapacity(); li++)
	{

		pc_buf_link  =  (CNETlink *)  c_list_net_links_out.pcGetNode()->pvGetObject();

		l_buf  =  l_out_data_flow  -  (l_max_out_capa - pc_buf_link->lGetMaxCapacity());

		if  (l_buf  <  0)  l_buf  =  0;

		l_lfn  +=  l_buf;

		c_list_net_links_out.bNext();
	
	}//for  (li = 0; li < c_list_net_links_out.lGetCapacity; li++)



	return(l_lfn);


}//double  CNETnode::dCountLFN()








void  CNETnode::vPresent(FILE  *pfReportFile)
{

	fprintf(pfReportFile,"\n\n");

	fprintf(pfReportFile,"node number:%ld\n", l_id);
	fprintf(pfReportFile,"node capacity:%ld\n", l_max_capacity);
	fprintf(pfReportFile,"node actual capacity:%ld\n", l_actual_capacity);

	fprintf(pfReportFile,"Number of outgoing links:%ld\n", c_list_net_links_out.lGetCapacity());
	fprintf(pfReportFile,"Number of incoming links:%ld\n", c_list_net_links_in.lGetCapacity());



}//void  CNETnode::vPresent(FILE  pfReportFile)




//----------------------end of implementation of CNETnode--------------------------------------------
















//--------------implemenatation of class  CNETlink--------------------------------------------
//--------------------------------------------------------------------------------------------------------------

CNETlink::CNETlink()
{

	l_id  = -1;//"unset" value assigned

	s_name  =  "no name";

		
	l_max_capacity  =  0;//no capacity
	l_actual_capacity  =  0;


	l_start_node_id  =  -1;//impossible id;
	l_finish_node_id  =  -1;//impossible id;

	pc_start_node  =  NULL;
	pc_finish_node  =  NULL;


	

}//CNETlink::CNETlink()





CNETlink::~CNETlink()
{

	if  (l_start_node_id >= 0)
	{

		if  (pc_start_node  !=  NULL)
			pc_start_node->bRemoveLink(false,this);
	
	}//if  (l_start_node_id >= 0)


	if  (l_finish_node_id >= 0)
	{

		if  (pc_finish_node  !=  NULL)
			pc_finish_node->bRemoveLink(true,this);
	
	}//if  (l_start_node_id >= 0)



	c_list_of_net_connections.vBYE(false);

}//CNETlink::~CNETlink()







bool  CNETlink::b_change_id(long  lNewId)
{

	if  (lNewId  <  0)  return(false);

	l_id  =  lNewId;

	return(true);

}//bool  CNETlink::b_change_id(long  lNewId)










bool  CNETlink::bSetCapacity(long  lNewCapacity)
{


	if  (l_max_capacity  -  l_actual_capacity  >  lNewCapacity)
		return(false);


	l_actual_capacity  =  lNewCapacity  -  (l_max_capacity  -  l_actual_capacity);
	l_max_capacity  =  lNewCapacity;



	return(true);
	

}//bool  CNETlink::bSetCapacity(long  lNewCapacity)












//if the link is attracted to any connection then it is undeletable
bool  CNETlink::bIsDeletable()
{

	//if the lists are not empty we can not delete the node
	if  (c_list_of_net_connections.bFirst()  ==  true)  return(false);

	return(true);

}//bool  CNETnode::bIsDeletable()









bool  CNETlink::bPlugFinishStart(bool  bFinishStart, long lNodeId, CNETnode *pcNode)
{


	if  (bFinishStart  ==  TRUE)
	{

		l_finish_node_id  =  lNodeId;
		pc_finish_node  =  pcNode;
	
	}//if  (bFinishStart  ==  TRUE)
	else
	{

		l_start_node_id  =  lNodeId;
		pc_start_node  =  pcNode;
	
	}//else  if  (bFinishStart  ==  TRUE)



	return(pcNode->bAddNewLink(bFinishStart,this));



}//bool  CNETlink::bPlugInOut(bool  bInOut, long LNodeId, CNETnode *pcNode)






bool  CNETlink::bSetUpConnection(CNETconnection  *pcNewConnection, long  lConnectionCapacity)
{

	//if it's impossible to set the connection
	if  (l_actual_capacity  <  lConnectionCapacity)  return(false);

	//if the capacity is ok we set up the connection
	if  (c_list_of_net_connections.bAdd(pcNewConnection)  ==  false)  return(false);

	//now we decrease the actual capacity information
	l_actual_capacity  =  l_actual_capacity  -  lConnectionCapacity;


	return(true);
	

}//bool  CNETlink::bSetUpConnection(CNETconnection  *pcNewConnection, long  lConnectionCapacity)






/*
returned values:
1  -  ok
0  -  connection was not found
-1 -  removal of found connection unsuccessfull
*/
int  CNETlink::iRemoveConnection(long  lConnectionId)
{

	//if the list is emopty...
	if  (c_list_of_net_connections.bLast()  ==  false)  return(0);


	long  l_list_capacity;
	
	l_list_capacity  =  c_list_of_net_connections.lGetCapacity();

	
	
	for  (long  li = 0; (li < l_list_capacity); li++)
	{

		if  (
			((CNETconnection *) c_list_of_net_connections.pcGetNode()->pvGetObject())->lGetId()
			==
			lConnectionId
			)
		{

			l_actual_capacity  +=
			(
			(CNETconnection *) c_list_of_net_connections.pcGetNode()->pvGetObject()
			)->lGetCapacity();
			
				
			//not likely to happen but you never know...
			if  (c_list_of_net_connections.bDeleteActual(false)  ==  false) 
			{
				l_actual_capacity  =  l_actual_capacity  -
				(
				(CNETconnection *) c_list_of_net_connections.pcGetNode()->pvGetObject()
				)->lGetCapacity();
				
				return(-1);
			}//if  (c_list_of_net_connections.bDeleteActual(false)  ==  false) 

			return(1);
		}//if



		c_list_of_net_connections.bPrev();
	
	}//for  (long  li = 0; li < l_list_capacity; li++)


	return(0);

}//bool  CNETlink::bRemoveConnection(long  lConnectionId)







void  CNETlink::vCreateBasiCVirtualWay(FILE  *pfReportFile)
{

	fprintf(pfReportFile,"%ld\n",lGetStartNodeId());
	fprintf(pfReportFile,"%ld\n",lGetFinishNodeId());
	fprintf(pfReportFile,"1\n");
	fprintf(pfReportFile,"3 %ld %ld %ld\n", lGetStartNodeId(), l_id, lGetFinishNodeId());
	fprintf(pfReportFile,"\n");

}//void  CNETlink::vCreateBasiCVirtualWay(FILE  *pfReportFile)



//----------------------end of implementation of CNETlink--------------------------------------------





















//--------------implemenatation of class  CNETconnection--------------------------------------------
//--------------------------------------------------------------------------------------------------------------


CNETconnection::CNETconnection()
{

	l_id  = -1;//"unset" value assigned

	s_name  =  "no name";


	l_capacity  =  0;//no weight

	pl_way  =  NULL;
	i_way_length = 0;


}//CNETconnection::CNETconnection()




CNETconnection::~CNETconnection()
{

	if  (pl_way  !=  NULL)  delete [] pl_way;
	

}//CNETconnection::~CNETconnection






bool  CNETconnection::b_change_id(long  lNewId)
{

	if  (lNewId  <  0)  return(false);

	l_id  =  lNewId;

	return(true);

}//bool  CNETconnection::b_change_id(long  lNewId)






bool  CNETconnection::bSetCapacity(long  lNewCapacity)
{

	if  (lNewCapacity  <  0)  return(false);


	l_capacity  =  lNewCapacity;
	
	return(true);

}//bool  CNETconnection::bSetCapacity(long  lNewCapacity)







bool  CNETconnection::bSetConnectionWay(long  *plNewWay,  int  iWayLength)
{


	if  (pl_way  !=  NULL)  delete  []  pl_way;

	i_way_length = 0;

	
	pl_way  =  NULL;
	pl_way  =  new  long[iWayLength];

	if  (pl_way  ==  NULL)  return(false);


	for  (int  ii = 0; ii < iWayLength; ii++)
		pl_way[ii]  =  plNewWay[ii];


	i_way_length  =  iWayLength;

	return(true);


}//bool  CNETconnection::bSetConnectionWay(long  plNewWay,  int  iWayLength)











int  CNETconnection::iGetConnectionWay(long  **plWay)
{

	*plWay  =  pl_way;

	return(i_way_length);

}//int  CNETconnection::iGetConnectionWay(long  *plWay)









//----------------------end of implementation of CNETconnection--------------------------------------------