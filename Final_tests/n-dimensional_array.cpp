int main()
{
int a[4][4][4][4];
int i,j,k,l;
int p=0;
for (i=0;i<4;i++)
{
for(j=0;j<4;j++)
{
for(k=0;k<4;k++)
{
for(l=0;l<4;l++)
{
a[i][j][k][l]=p;
p+=1;
}
}
}
}


for (i=0;i<4;i++)
{
for(j=0;j<4;j++)
{
for(k=0;k<4;k++)
{
for(l=0;l<4;l++)
{
print(a[i][j][k][l]);
print(" ");
}
}
print("\n");
}
}
print("\n");

}
