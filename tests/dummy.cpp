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
int i,j,k,l,m;
i=1;
j=2;
k=3;
l=4;
m=i+j+k+l;
print(m);
int e;
e=sum(15);
print(e);
}
