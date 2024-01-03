#pragma once


class  CMyNode
{
public:
	bool	bInsertObject(void *ptOBJECT);  //inserts a specified object(actually it's addres) to the node 
	bool	bDeleteObject();  //deallocates the memory of held object(deletes the object)

	void	*pvGetObject() {return(pc_object);};   //returns an addres of a held object

	CMyNode *pcGetNext() {return(pc_next);};  //returns addres of the next node
	CMyNode *pcGetPrev() {return(pc_prev);};  //returns addres of the prev node

	bool	bSetNext(CMyNode  *pcNext) {pc_next  =  pcNext; return(true);};//sets new next node addres
	bool	bSetPrev(CMyNode  *pcPrev) {pc_prev  =  pcPrev; return(true);};//sets new previous node addres

	
	//I don't know if the way you allocate the memory uses constructors and destructors
	//so i created it this way in case you just allocate and free the memory without using constructor and destructor tools
	void    vINIT();       
	void    vBYE(bool  bDeleteObject);
		
protected:
	CMyNode *pc_next;
	CMyNode *pc_prev;

	void    *pc_object;

};




class  CMyList
{
public:
	bool	bAdd();			//Adds 1 node at the en of the list
	bool    bAdd(void *);	//Adds 1 object at the end of the list

	bool    bDeleteActual(bool  bDeleteObject);  // delete's an actual node and the object it holds

	CMyNode  *pcGetNode()  {return(pc_actual_node);};   //returns an addres to an actual node
	void    *pvGetObject()  {return(pc_actual_node->pvGetObject());};
	long    lGetPos()  {return(l_position);};  //returns a position number of a current node

	long    lGetCapacity()  {return(l_capacity);}; //returns the current capacity


	bool    bFirst();  // moves the actual pointer to the first node
	bool    bLast();   // moves the actual pointer to the last node

	bool	bNext();   // moves the actual pointer to the next node
	bool    bPrev();   // moves the actual pointer to the previous node
	bool    bSetPos(long  lWantedPosition);	//moves the actual pointer to the node of a specified numer and returns true if the operation was succesful

	bool    bSendObjAddr(CMyList *Target);// this method sends all addresses in the list to the targetted list


	//I don't know if the way you allocate the memory uses constructors and destructors
	//so i created it this way in case you just allocate and free the memory without using constructor and destructor tools
	CMyList();       
	~CMyList();

	void  vBYE(bool  bDeleteObject);
	

protected:
	CMyNode  *pc_first_node;
   	CMyNode  *pc_last_node;
	CMyNode  *pc_actual_node;

	long     l_capacity;
	long	 l_position;
};




