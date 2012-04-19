int partition(int a[],int s,int l)
{
    int b,i,temp,j;
    b = a[s];
    j =s;
    l = l-1;
    for(i=0;s<l;i++)
    {
        if(a[s]<=b)
            s=s+1;
        if(a[l]>b)
            l=l-1;
        if((a[s]>b)&&(a[l]<=b))
        {
            temp = a[s];
            a[s] = a[l];
            a[l] = temp;
            s=s+1;
            l = l-1;
        }
    }
    if(a[s]>b)
    {
        a[j] = a[s-1];
        a[s-1] = b;
        j = s-1;
        return j;
    }
    else
    {
        a[j] = a[s];
        a[s] = b;
        return s;
    }
}
void quicksort(int a[],int s,int l)
{
    int b;
    b = l-s;
    if((b==0)||(b==-1))
        return;
    else
    {
        int c,i;
        c = partition(a,s,l);
        quicksort(a,s,c);
        quicksort(a,c+1,l);
        
    }
}

int main()
{
    int *a;
    int size,b;
    print("Enter size of array : ");
    scan(size);
    a = malloc((4*size));
    int i;
    for(i=0;i<size;i++)
    {
        print("Enter the next element in array : ");
        scan(b);
        a[i]=b;
    }
    quicksort(a,0,size);
    for(i=0;i<size;i++)
    {
        print(a[i]);
        print(" ");
    }
    print("\n");
}
