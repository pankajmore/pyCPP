
void swap(int *a, int*b)
{
int tmp;
tmp=*a;
*a=*b;
*b=tmp;
}
int main()
{
int a,b;
a=5;
b=10;

print("Values Before Swap \n");
print(a);
print("\n");
print(b);
print("\n\n");

swap(&a,&b);

print("Values After Swap \n");
print(a);
print("\n");
print(b);
print("\n");
}
