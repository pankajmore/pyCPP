//**************************************
// Name: Code Example - A Recursive Function
// Description:This is some examples of basic C++ programming. Some people at school will be creating software using some of these concepts. So if someone happens to wander over here, theres some help.
//However this wont solve your problems just show you how.
// By: Jared Bruni
//
//
// Inputs:None
//
// Returns:None
//
//Assumes:None
//
//Side Effects:None
//**************************************
// jared bruni
// for planetsourcecode
/*
This is some examples of basic C++ programming. Some people at school will be creating software using some of these concepts. So if someone happens to wander over here, theres some help.
However this wont solve your problems just show you how.
*/
// C++ code example
// example how to use recursion
void recurfunc(int start,int stop,char* buff);
void main()
    {
    	cout << "enter how many times to loop: ";
    	char buff[100];
    	cin >> buff;
    	int num;
    	num = atoi(buff);
    	if(num >= 1)
        	{
        		recurfunc(0,num," this is a recursive function");
        	}
        	else
            	{
            		cout << "sorry you didnt enter valid data" << endl;
            		return;
            	}
        }
        void recurfunc(int start,int stop,char* buff)
            {
            	if(start < stop)
                	{
                		start++;
                		cout << "\n" << buff << "\n";
                		recurfunc(start,stop,buff);
                	}
                	else
                    	{
                    		return;
                    	}
                }
		
