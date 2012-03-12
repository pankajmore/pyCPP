//**************************************
// Name: Code Example - generating random numbers
// Description:Today in class we went over a few different concepts. I wrote my own
examples of these C++ concepts.
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
//This code is copyrighted and has limited warranties.
//**************************************
/* random number example
written by Jared Bruni
www.LostSideDead.com
*/
#include<iostream>
#include<time.h>
using namespace std;
int main()
    {
    	srand(time(NULL)); // seed randomization
    	// now generate and display 10 random numbers 0-10
    	for(int i = 0; i < 10; i++)
        	{
        		cout << "random number: " << rand()%10 << endl;
        	}
        	return system("pause");
    }
		
