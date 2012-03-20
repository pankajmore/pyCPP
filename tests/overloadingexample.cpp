//**************************************
// Name: Code Example - function overloading / polymorphisim
// Description:A concept we went over today in class.
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
/* example of function overloading/polymorphisim
written by Jared Bruni
www.LostSideDead.com
*/
void func1(char* str);
void func1(int val);
int main()
    {
    	func1("character string passed\n");
    	func1(123);
    	return (system("pause"));
}
void func1(char* str)
    {
    	cout << "string value := " << str << endl;
}
void func1(int val)
    {
    	cout << "integer value := " << val << endl;
}
		
