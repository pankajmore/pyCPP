int sum(int a);
int sum(int a,b)
{
if (a==0)
return (a+b);
else:
return sum(a+b-1);
}

int main()
{
int q,w,e,r,t;
w=1;
e=3;
r=5;
t=10;
q=w+r+e+t;
print(q);
if (q==19)
e=(q+w);
else
e=r+t;
e=sum(1);
print(e);
}
