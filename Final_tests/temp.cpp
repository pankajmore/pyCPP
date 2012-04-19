int p;
void sum(){
    p += 1;
}
int main()
{
    int i;
    for(i=0;i<10;i++)
    {
        sum();
        print(p);
    }
    
}
