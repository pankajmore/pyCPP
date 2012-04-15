int sum(int a);
int sum(int a)
{
if (a==0 || a==1)
return 1;
else 
return sum(a-1)+sum(a-2);
}

int main()
{

int e;
e=sum(5);
print(e);
}
