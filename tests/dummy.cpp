int sum(int a,int b);
int sum(int a, int b)
{
if (a==0)
return (a+b);
else
return a-1+b;
}

int main()
{
int q,w,e,r,t;
w=0;
e=0;
r=5;
t=10;
q=w+r+e+t;
print(q);
e=sum(r,t);
print(e);
}
