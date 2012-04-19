int main()
{
int **a;
int b,c;
int i,j;
print("Enter size of 2d matrix\n");
scan(b);
a = malloc((4 * b));
for(i=0;i<b;i++)
    a[i] = malloc((4*b));

for(i=0;i<b;i++)
    for(j=0;j<b;j++)
        a[i][j]=i+j;
for(i=0;i<b;i++)
{for(j=0;j<b;j++)
    {   print(a[i][j]);
        print(" ");
    }
    print("\n");
}
}
