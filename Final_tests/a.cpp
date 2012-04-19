void matrixmult(int **a,int **b,int **temp,int c)
{
    int i,j,k,x,y;
    print("\nMatrix A -\n\n");
    for(x=0;x<c;x++)
    {       
        for(y=0;y<c;y++)
        {
		int p;
		p=**(a+x*2+y);
            print(p);
            print(" ");
        }
        print("\n");
    }
    print("\nMatrix B -\n\n");
    for(x=0;x<c;x++)
    {       
        for(y=0;y<c;y++)
        {
		int p;
		p=**(b+x*2+y);
            print(p);
            print(" ");
        }
        print("\n");
    }
    for(i=0;i<c;i++)
        for(j=0;j<c;j++)
        { 
            **(temp+i*2+j)=0;
            for(k=0;k<c;k++)
            { 
            **(temp+i*2+j) = **(temp+i*2+j)+  **(a+i*2+k) * **(b+2*k+j);
            }
        }
    print("\nProduct Matrix -\n\n");
}

int main()
{
    int a[2][2],b[2][2],temp[2][2];
    int x,y;
    int c=2;

    for(x=0;x<c;x++)
        for(y=0;y<c;y++)
         {a[x][y]=1;
          b[x][y]=1;
         }
    a[0][0]=1;a[0][1]=2;
    a[1][0]=3;a[1][1]=4;
    b[0][0]=1;b[0][1]=2;
    b[1][0]=3;b[1][1]=4;


    matrixmult(a,b,temp,c);

    for(x=0;x<c;x++)
    {       
        for(y=0;y<c;y++)
        {
	    int p;
            print(temp[x][y]);
            print(" ");
        }
        print("\n");
    }
    print("\n");

}
