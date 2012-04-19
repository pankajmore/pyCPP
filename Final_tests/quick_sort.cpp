int partition(int a[],int s,int l)
{
    int b,i,temp,j;
    j = (s+l)/2;
    b = a[j];
    j = s;
    while(s < l){
        while(a[s] < b) s++;
        while(a[l] > b) l--;

        if ( s < l && a[s] != a[l] )
        {
            temp = a[s];
            a[s] = a[l];
            a[l] = temp;
        }
        else
        {
            return l;
        }
    }
    return l;
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
        quicksort(a,s,c-1);
        quicksort(a,c+1,l);
        
    }
}

int main()
{
    int *a;
    int size,b;
    print("Enter size of array - ");
    scan(size);
    a = malloc((4*size));
    int i;
    for(i=0;i<size;i++)
    {
        print("Enter the next element in array - ");
        scan(b);
        a[i]=b;
    }
    quicksort(a,0,size-1);
    for(i=0;i<size;i++)
    {
        print(a[i]);
        print(" ");
    }
    print("\n");
}
