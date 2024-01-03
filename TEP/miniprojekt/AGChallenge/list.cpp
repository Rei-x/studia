#include  "list.h"
#include  "atlstr.h"  //CString
#include  <math.h>
#include  <time.h>

#include <windows.h>




//----------implentation of CMyNode---------------------

bool   CMyNode::bInsertObject(void *ptOBJECT)
{
	if  (pc_object != NULL) return (false);
  

	pc_object  =  ptOBJECT;
	return (true);
}



bool   CMyNode::bDeleteObject()
{
   if  (pc_object ==  NULL)  return (false);
   delete  pc_object;
   pc_object  =  NULL;
   return(true);
}


void  CMyNode::vINIT()
{
	pc_next  =  NULL;
	pc_prev  =  NULL;
	
	pc_object  =  NULL;
}



void  CMyNode::vBYE(bool  bDelObject)
{
	if  (bDelObject  ==  true)
	{
		if  (pc_object != NULL)
		{
			bDeleteObject();
		}//if  (pc_object != NULL)

	}//if  (bDelObject  ==  true)
}




//---------implementatio of CMyList---------------------

bool  CMyList::bAdd()
{
	CMyNode  *pc_new_node  =  NULL;


	pc_new_node  =  new  CMyNode;

	if  (pc_new_node == NULL)  return(false);//failed to allocate memory for a new node
	pc_new_node->vINIT();  //init of the object (because we most probably don't use the constructors)

	//if the allocate operation was succesful we start to change List settings, so
	// the node is really added and remebered at the end of the list
	l_capacity++; //we increase the actual number of objects
	
	if  (pc_first_node == NULL ) //we are adding first node to the list
	{
	    pc_first_node  =  pc_new_node;
		pc_last_node   =  pc_new_node;
	
		pc_actual_node  =  pc_last_node;
		l_position  =  l_capacity; // posiotion set to the last node
		
		return(true);
	}//if  (pc_first_node == pc_last_node == NULL) 
	else  //we are not adding the first node
	{
		pc_last_node->bSetNext(pc_new_node);
		pc_new_node->bSetPrev(pc_last_node);  //inserting the pc_new_node at the end of the chain of nodes
		
		pc_last_node  =  pc_new_node; //we are always adding at the end of the list

		pc_actual_node  =  pc_last_node;
		l_position  =  l_capacity; // posiotion set to the last node
				
		return(true);
	}//else of if (pc_first_node == pc_last_node == NULL) 
   return(true);

}




bool    CMyList::bAdd(void  *pvNewObject)
{
	if  (bAdd()  ==   false)  return(false);

	if  (pc_actual_node->bInsertObject(pvNewObject)  ==  false)  
	{
		bDeleteActual(false);
		return(false);
	}//if  (pc_actual_node->bInsertObject(pvNewObject)  ==  false)  


	return(true);
}



bool   CMyList::bSetPos(long  lWantedPosition)
{
	long  l_counter;
	
	if  (lWantedPosition  >  l_capacity)  return  (false);
	if  (lWantedPosition  <= 0 )  return  (false);

	l_counter  =  1;
	pc_actual_node  =  pc_first_node;


	while (l_counter < lWantedPosition)
	{
		pc_actual_node  =  pc_actual_node->pcGetNext();
		l_counter++;
	}//while (l_counter < lWantedPosition)
                       
	return(true);

}




bool  CMyList::bSendObjAddr(CMyList  *Target)
{
	long  li;
	
	bFirst();

	for (li = 0; li < l_capacity; li++)
	{
		if  ( Target->bAdd() ==  false )  return(false) ;
		if  ( Target->pcGetNode()->bInsertObject(  pcGetNode()->pvGetObject() )  ==  false )  return(false);

		bNext();
	}


	return(true);
}





//if bDeleteObject is true the hold object will be deleted, if not only the node will be destroyed!
bool   CMyList::bDeleteActual(bool   bDeleteObject)
{
	CMyNode  *pc_node_to_delete;

	if (l_capacity == 0)  return(false);

	pc_node_to_delete  =  pc_actual_node;

	//first we have to remove the node from the node chain...
	//...by setting next node->prevNode (if the next node exist's)...
	if  (pc_node_to_delete->pcGetNext() != NULL)
		pc_node_to_delete->pcGetNext()->bSetPrev(pc_node_to_delete->pcGetPrev());
	//...and by setting previous node->nextNode (if the previous node exist's)...
	if  (pc_node_to_delete->pcGetPrev() != NULL)
		pc_node_to_delete->pcGetPrev()->bSetNext(pc_node_to_delete->pcGetNext());

		
	//if pc_node_to_delete is the first node we must set it...
	if  (pc_node_to_delete == pc_first_node)
		pc_first_node  =  pc_node_to_delete->pcGetNext();


	//if pc_node_to_delete is the last node we must set it...
	if  (pc_node_to_delete == pc_last_node)
		pc_last_node  =  pc_node_to_delete->pcGetPrev();


	//...now we clean up after the node to delete...
	pc_node_to_delete->vBYE(bDeleteObject);


	//...and delete him finally!
	delete  pc_node_to_delete;

	//DONT FORGET WE HAVE 1 OBJECT LESS
	l_capacity--;

	//and  about setting a new actual position (we will always set it to the begining)
	pc_actual_node  =  pc_first_node;
	if  (pc_actual_node  ==  NULL)
		l_position  =  0;
	else
		l_position  =  1;
   
	return(true);
}



bool  CMyList::bFirst()
{
	if  (pc_first_node != NULL)  
	{
		pc_actual_node  =  pc_first_node;
		l_position  =  1;
		return(true);
	}
	else
		return(false);

}



bool   CMyList::bLast()
{
	if  (pc_last_node != NULL)  
	{
		pc_actual_node  =  pc_last_node;
		l_position  =  l_capacity;
		return(true);
	}
	else
		return(false);
}




bool  CMyList::bNext()
{
	//if the list is empty we cannot move
	if  (pc_first_node  ==  NULL)
		return  (false);

	//if we are at the end of the list we also cannot move
	if  (pc_actual_node  ==  pc_last_node)
		return(false);

	//if we get into here it means we can move
	pc_actual_node  =  pc_actual_node->pcGetNext();
	l_position++;
	return(true);

}



bool   CMyList::bPrev()
{

    //if the list is empty we cannot move
	if  (pc_first_node  ==  NULL)
		return  (false);

	//if we are at the beginning of the list we also cannot move
	if  (pc_actual_node  ==  pc_first_node)
		return(false);

	//if we get into here it means we can move
	pc_actual_node  =  pc_actual_node->pcGetPrev();
	l_position--;
	return(true);


}





CMyList::CMyList()
{
	pc_first_node   =  NULL;
	pc_last_node    =  NULL;
	pc_actual_node  =  NULL;
	
	l_capacity  =  0;
	l_position  =  0;

}


CMyList::~CMyList()
{
	vBYE(false);
}

void  CMyList::vBYE(bool  bDeleteObject)
{
	//sets on the beginning and then deletes all the nodes
	if  (bFirst()  ==  true)
		while(bDeleteActual(bDeleteObject) == true) ;

}





