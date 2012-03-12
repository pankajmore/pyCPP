//**************************************
//     
// Name: Code Example - how to use names
//     paces
// Description:Simple example showing ho
//     w to use namespaces.
// By: Jared Bruni
//
//This code is copyrighted and has// limited warranties.
//**************************************
//     
/* Namespaces example
written by Jared Bruni
www.LostSideDead.com
*/
#include<iostream.h>
#include <stdlib.h>
namespace master 
    {
    	int variable = 100;
    	void test1();
    	void test2();
}
void master::test1()
    {
    	cout << " calling function #1 " << endl;
}
void master::test2()
    {
    	cout << " calling function #2 " << endl;
    	cout << " the variable holds the value of : " << variable << endl;
}
using namespace master;
int main()
    {
    	test1();
    	test2();
    	system("pause");
    	return (0);
}
