#pragma once


//tools
#include  "atlstr.h"  //CString
#include <windows.h>


//system tools
#include  "list.h"

//vector
#include  <vector>
#include  <iostream>

using namespace std;



namespace NETsimulator
{

	//predefinition of NETway tools
	class  CNETnode;
	class  CNETlink;
	class  CNETconnection;

	//simulator interface  definition
	class  CNETsimulator
	{

	public:

		virtual  int  iGetSimulatorType()  = 0;
		virtual  int  iCopySimulator(CNETsimulator  *pcOtherSimulator)  = 0;

		virtual  bool  bAllowCapacityOverloading(bool  bAllow)  =  0;//returns the actual state

		virtual  long  lAddNewNode(long  lCapacity,  CString  sName) =  0;//returns the node id
		virtual  int   iDeleteNode(long  lNodeId)  =  0;
		virtual  int   iSetNodeCapacity(long  lNodeId, long  lNewCapacity)  =  0;


		virtual  long  lCreateLink(long  lStartNodeId, long  lFinishNodeId, long lCapacity)  =  0;
		virtual  int   iDeleteLink(long  lLinkId)  =  0;


		virtual  int   iCheckConnection
			(long  *plWay, int iWayLength, long  lCapacity, bool bCheckActualCapacity = true)  =  0;
		virtual  long  lFindLinkIdForNodes(long  lStartNodeId,  long  lFinishNodeId)  =  0;

		virtual  long  lSetUpConnection(long  *plWay, int iWayLength, long  lCapacity)  =  0;
		virtual  int   iRemoveConnection(long  lConnectionId)  =  0;
		virtual  int   iRemoveAllConnections()  =  0;

		

		virtual  long  lGetActNodeCapacity(long  lNodeId)  =  0;
		virtual  long  lGetActLinkCapacity(long  lLinkId)  =  0;
		virtual  long  lGetMaxNodeCapacity(long  lNodeId)  =  0;
		virtual  long  lGetMaxLinkCapacity(long  lLinkId)  =  0;


		virtual  double  dCountNodeLFN(long  lNodeId,  long  lPenalty,  bool  *pbCapacityExtending, double *pdFitnessPure, double *pdPenaltyPure)  =  0;
		virtual  double  dCountNodeLFL(long  lNodeId,  long  lPenalty,  bool  *pbCapacityExtending, double *pdFitnessPure, double *pdPenaltyPure)  =  0;

		virtual  long  lGetNodesNum()  =  0;
		virtual  long  lGetLinksNum()  =  0;


		CNETsimulator()  {b_check_connection_on  =  false; b_const_sat_incr_demands = false;};
		virtual  ~CNETsimulator()  {};

		void  vSetConstSatIncrDemands(bool  bConstSatIncrDemands) {b_const_sat_incr_demands = bConstSatIncrDemands;};

		virtual  int   iPresentNetwork(CString  sFileName)  =  0;
		virtual  void  vPresentNetwork(FILE  *pfDestFile,  bool  bActualState)  =  0;
		virtual  int   iCreateBasicVirtualDatabaseFile(CString  sFileName)  =  0;

		void  vTurnConnectionCheck(bool  bOnOff)  {b_check_connection_on  =  bOnOff;};

		virtual  int  iGetShortestWays(int  iShortestWaysNumber, vector <long *> *pvWays, vector <long> *pvWaysLenghts)  =  0;
		virtual  int  iGetShortestWaysForNodes(int iStartNodeId, int iFinishNodeId, int  iShortestWaysNumber, vector <long *> *pvWays, vector <long> *pvWaysLenghts)  =  0;

	protected:
		bool  b_check_connection_on;//usually set on off - checks wheather the proposed connection is not "wrong"
		bool  b_const_sat_incr_demands;


	};//class  NETsimulator











	#define  CONST_SAT_MAX_DEMAND_INCREASE  99999

	class  CNETsimulatorSimplyfied  :  public  CNETsimulator
	{

	public:

		int  iGetSimulatorType()  {return(2);};
		int  iCopySimulator(CNETsimulator  *pcOtherSimulator);

		bool  bAllowCapacityOverloading(bool  bAllow)
			{b_allow_capacity_oveloading = bAllow;return(bAllow);};//returns the actual state

		long  lAddNewNode(long  lCapacity,  CString  sName);//returns the node id
		int   iDeleteNode(long  lNodeId)  {return(1);};//method doesn't work for this network simulator
		int   iSetNodeCapacity(long  lNodeId, long  lNewCapacity){return(1);};//method doesn't work for this network simulator


		long  lCreateLink(long  lStartNodeId, long  lFinishNodeId, long lCapacity);
		int   iDeleteLink(long  lLinkId)  {return(1);};//method doesn't work for this network simulator


		int   iCheckConnection
			(long  *plWay, int iWayLength, long  lCapacity, bool bCheckActualCapacity = true);
		long  lFindLinkIdForNodes(long  lStartNodeId,  long  lFinishNodeId);
			//{return(lStartNodeId * l_node_id_tool  +  lFinishNodeId);};
			

		long  lSetUpConnection(long  *plWay, int iWayLength, long  lCapacity);
		//method doesn't work for this network simulator\/ but you can remove connection using lSetUpConnection with the "-" capacity and the connection checking set "off"
		int   iRemoveConnection(long  lConnectionId)  {return(-2);};
		int   iRemoveAllConnections();

		

		long  lGetActNodeCapacity(long  lNodeId)  {return(-3);};//method doesn't work for this network simulator
		long  lGetActLinkCapacity(long  lLinkId);
		long  lGetMaxNodeCapacity(long  lNodeId)  {return(-3);};//method doesn't work for this network simulator
		long  lGetMaxLinkCapacity(long  lLinkId);


		double  dCountNodeLFN(long  lNodeId,  long  lPenalty,  bool  *pbCapacityExtending, double *pdFitnessPure, double *pdPenaltyPure);
		double  dCountNodeLFL(long  lNodeId,  long  lPenalty,  bool  *pbCapacityExtending, double *pdFitnessPure, double *pdPenaltyPure);



		CNETsimulatorSimplyfied();
		~CNETsimulatorSimplyfied();

		int   iPresentNetwork(CString  sFileName);
		void  vPresentNetwork(FILE  *pfDestFile,  bool  bActualState);
		int   iCreateBasicVirtualDatabaseFile(CString  sFileName);


		//new methods for CONetAdmin
		long  lGetNodesNum()  {return(l_node_id_tool);};
		long  lGetLinksNum()  {return(l_number_of_links);};

		bool  bIsTheSame(CNETsimulatorSimplyfied  *pcOtherNetowrk);

		int  iGetShortestWays(int  iShortestWaysNumber, vector <long *> *pvWays, vector <long> *pvWaysLenghts);
		int  iGetShortestWaysForNodes(int iStartNodeId, int iFinishNodeId, int  iShortestWaysNumber, vector <long *> *pvWays, vector <long> *pvWaysLenghts);

		int  iGetMinimumAllowedDemandIncrease()  {return(i_minimum_allowed_demand_increase);};

	private:

		void  v_recompute_minimum_allowed_demand_increase();

		//tools for get shortest ways
		int  i_expand_path_tree(vector  <int>  *pvVisitedPathTree,  int iFinishNodeId);
		bool  b_is_node_visited
			(
			vector  <int>  *pvVisitedPathsTree, 
			int  iLastPathNodeIndex,
			int  iCheckedNodeId
			);


		long  **pl_links_table_for_nodes;
		long  **pl_actual_network_state;//if there are no connections inputted it's the same as pl_links_table_for_nodes
		int  **pi_paths_per_link;
		int  i_minimum_allowed_demand_increase;

		long  l_node_id_tool;//used as counter of ids of nodes
		
		long  l_number_of_links;
		long  *pl_links_addres_table;//store way: (linkId * 2)-start node (linkId * 2+1)-finish node

		bool  b_allow_capacity_oveloading;
		
	};//class  CNETsimulatorSimplyfied  :  public  CNETsimulator















	class  CNETsimulatorComplex  :  public  CNETsimulator
	{

	public:

		int  iGetSimulatorType()  {return(2);};
		int  iCopySimulator(CNETsimulator  *pcOtherSimulator)  {return(0);};

		bool  bAllowCapacityOverloading(bool  bAllow){return(false);};//method doesn't work for this network simulator

		long  lAddNewNode(long  lCapacity,  CString  sName);//returns the node id
		int   iDeleteNode(long  lNodeId);
		int   iSetNodeCapacity(long  lNodeId, long  lNewCapacity);


		long  lCreateLink(long  lStartNodeId, long  lFinishNodeId, long lCapacity);
		int   iDeleteLink(long  lLinkId);


		int   iCheckConnection
			(long  *plWay, int iWayLength, long  lCapacity, bool bCheckActualCapacity = true);
		long  lFindLinkIdForNodes(long  lStartNodeId,  long  lFinishNodeId);

		long  lSetUpConnection(long  *plWay, int iWayLength, long  lCapacity);
		int   iRemoveConnection(long  lConnectionId);
		int   iRemoveAllConnections();

		

		long  lGetActNodeCapacity(long  lNodeId);
		long  lGetActLinkCapacity(long  lLinkId);
		long  lGetMaxNodeCapacity(long  lNodeId);
		long  lGetMaxLinkCapacity(long  lLinkId);


		double  dCountNodeLFN(long  lNodeId,  long  lPenalty,  bool  *pbCapacityExtending, double *pdPenaltyPure);
		double  dCountNodeLFL(long  lNodeId,  long  lPenalty,  bool  *pbCapacityExtending, double *pdPenaltyPure)  {return(0);};

		//new methods for CONetAdmin
		long  lGetNodesNum()  {return(c_list_of_nodes.lGetCapacity());};
		long  lGetLinksNum()  {return(c_list_of_links.lGetCapacity());};



		CNETsimulatorComplex();
		~CNETsimulatorComplex();

		int   iPresentNetwork(CString  sFileName);
		void  vPresentNetwork(FILE  *pfDestFile,  bool  bActualState) {return;};//method doesn't work for this network simulator
		int   iCreateBasicVirtualDatabaseFile(CString  sFileName);

		int  iGetShortestWays(int  iShortestWaysNumber, vector <long *> *pvWays, vector <long> *pvWaysLenghts)  {return(-1);};
		int  iGetShortestWaysForNodes(int iStartNodeId, int iFinishNodeId, int  iShortestWaysNumber, vector <long *> *pvWays, vector <long> *pvWaysLenghts)  {return(-1);};


	private:

		//similar to iCheckConnection, but it really sets the connection information for nodes abd links!
		bool  b_set_connection_for_nodes_and_links
				(long  *plWay, int iWayLength,  
				CNETconnection *pcNewConnection, long  lConnectionCapacity);

		bool  b_remove_connection_on_the_way(long  *plWay, int iWayLength,  long  lConnectionId);



		CMyList  c_list_of_nodes;
		CMyList  c_list_of_links;
		CMyList  c_list_of_connections;


		long  l_node_id_tool;//used as counter of ids of nodes
		long  l_link_id_tool;//used as counter of ids of nodes
		long  l_connection_id_tool;//used as counter of ids of nodes


		
		//acces optimalization tools
		CNETnode		**pc_nodes_table;
		CNETlink		**pc_links_table;
	//	CNETconnection  **pc_connections_table;


	};//class  CNETsimulatorComplex  :  public  CNETsimulator








	class  CNETnode
	{
	friend  class  CNETsimulatorComplex;

	public:

		long  lGetId()  {return(l_id);};

		long  lGetActualCapacity()  {return(l_actual_capacity);};
		long  lGetMaxCapacity()  {return(l_max_capacity);};
		bool  bSetCapacity(long  lNewCapacity);




		bool  bAddNewLink(bool  bInOut, CNETlink  *pcNewLink);
		bool  bRemoveLink(bool  bInOut, CNETlink  *pcRemovedLink);


		bool  bSetUpConnection(CNETconnection  *pcNewConnection, long  lConnectionCapacity);
		int   iRemoveConnection(long  lConnectionId);


		bool  bIsDeletable();//if the node is attracted to any connection or link then it is undeletable
		void  vSetName(CString  sNewName)  {s_name  =  sNewName;};
		


		CNETnode();
		~CNETnode();


		long  lCountLFN();

		void  vPresent(FILE  *pfReportFile);

	private:

		bool  b_change_id(long  lNewId);





	//inforamtion part

		long  l_id;//identification number of this node (given from outside)

		CString  s_name;//set by user (unimportant from system point of view)

			
		long  l_max_capacity;
		long  l_actual_capacity;


		CMyList  c_list_net_links_out;//list of links going from the node to the other ones
		CMyList  c_list_net_links_in;//list of links going to the node to the other ones
		CMyList  c_list_of_net_connections;//list of connections going through the node


	};//class  CNETnode









	class  CNETlink
	{
	friend  class  CNETsimulatorComplex;

	public:

		long  lGetId()  {return(l_id);};

		long  lGetActualCapacity()  {return(l_actual_capacity);};
		long  lGetMaxCapacity()  {return(l_max_capacity);};
		bool  bSetCapacity(long  lNewCapacity);


		bool  bPlugFinishStart(bool  bFinishStart, long lNodeId, CNETnode *pcNode);

		long  lGetStartNodeId()  {return(l_start_node_id);};
		long  lGetFinishNodeId()  {return(l_finish_node_id);};


		bool  bSetUpConnection(CNETconnection  *pcNewConnection, long  lConnectionCapacity);
		int   iRemoveConnection(long  lConnectionId);

		
		bool  bIsDeletable();//if the link is attracted to any connection then it is undeletable
		void  vSetName(CString  sNewName)  {s_name  =  sNewName;};




		void  vCreateBasiCVirtualWay(FILE  *pfReportFile);

		CNETlink();
		~CNETlink();



	private:


		bool  b_change_id(long  lNewId);
		



	//data part


		long  l_id;//identification number of this link  (given from outside)

		CString  s_name;//set by user (unimportant from system point of view)



		long  l_max_capacity;
		long  l_actual_capacity;



		//start and finish node information
		long  l_start_node_id;
		CNETnode  *pc_start_node;

		long  l_finish_node_id;
		CNETnode  *pc_finish_node;



		CMyList  c_list_of_net_connections;//list of connections going through the link
		


	};//class  CNETlink










	class  CNETconnection
	{
	friend  class  CNETsimulatorComplex;

	public:
		
		
		long  lGetId()  {return(l_id);};

		long  lGetCapacity()  {return(l_capacity);};
		

		bool  bSetConnectionWay(long  *plNewWay,  int  iWayLength);
		int   iGetConnectionWay(long  **plWay);

		

		bool  bSetCapacity(long  lNewCapacity);
		void  vSetName(CString  sNewName)  {s_name  =  sNewName;};


		CNETconnection();
		~CNETconnection();
		

	private:

		bool  b_change_id(long  lNewId);


		long  l_id;

		CString  s_name;//set by user (unimportant from system point of view)



		long  l_capacity;//how much capacity it takes

		long  *pl_way;
		int   i_way_length;

	};//class  CNETconnection

};//namespace NETsimulator





