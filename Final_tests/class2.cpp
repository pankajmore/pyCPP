class A
{
    int a,b;
    int sum;
    int update(int c,int d)
    {
        this.a+=c;
        this.b+=d;
        this.sum=this.a+this.b;
        print("Sum = ");
        print(this.sum);
        print("\n");
    }
};
class B
{
    int c,d;
    int init(int a,int b)
    {
        this.c = a;
        this.d = b;
        print(this.c);
        print(" ");
        print(this.d);
        print("\n");
    }
};
int main()
{
    A a1,a2;
    B b1,b2;
    a1.a = 10;
    a1.b = 20;
    a1.update(0,0);
    a2.a = 30;
    a2.b = 40;
    a2.update(0,0);
    b1.init(25,35);
    b2.init(45,55);
    a1.update(20,10);
    a2.update(15,25);
    b1.c = 55;
    b2.d = 90;
    print("a1 : ");
    print(a1.a);
    print(" ");
    print(a1.b);
    print(" ");
    print(a1.sum);
    print("\n");
    print("b1 : ");
    print(b1.c);
    print(" ");
    print(b1.d);
    print("\n");
}
