int fibonacci(int x)
{
int y;
y=x;

if (y==0)
return 1;

else if(y==1)
return 1;

else
return fibonacci(y-1) + fibonacci(y-2);
}
int main()
{

int x;
int i;
for(i=0;i<=15;i++)
{
	x=fibonacci(i);
	print(x);
	print("\n");
}
}
