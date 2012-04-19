int main()
{
    int a,b,c;
    float x,y,z;
    x = 3.14159;
    print("Enter a element\n");
    scan(a);
    if (x > a){
    y = x + a;
    c = (int) x + a;
    }
    else {
    y = 4 * x * x;
    c = (int) x / a ;
    }
    print(y);
    print("\n");
    print(c);
}
