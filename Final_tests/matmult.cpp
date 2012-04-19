
void matrixmult(int a[][2],int b[][2],int temp[][2],int c)
{

    int i,j,k,x,y;
    for(x=0;x<c;x++)
    {       
        for(y=0;y<c;y++)
        {
            print(a[x][y]);
            print(" ");
        }
        print("\n");
    }
    for(i=0;i<c;i++)
        for(j=0;j<c;j++)
        { 
            temp[i][j] =0;
            for(k=0;k<c;k++)
            { 
            temp[i][j] +=  a[i][k] * b[k][j];
            }
        }
}

int main()
{
    int a[2][2],b[2][2],temp[2][2];
    int x,y;
    int c=2;


    a[0][0]=1;a[0][1]=2;
    a[1][0]=3;a[1][1]=4;
    b[0][0]=1;b[0][1]=2;
    b[1][0]=3;b[1][1]=4;
    matrixmult(a,b,temp,c);
    for(x=0;x<c;x++)
    {       
        for(y=0;y<c;y++)
        {
            print(temp[x][y]);
            print(" ");
        }
        print("\n");
    }

}

