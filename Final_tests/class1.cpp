class Student
{
    int roll;
    int marks[5];
    int sum;
    int average;
    int calc()
    {
        this.sum = this.marks[0]+this.marks[1]+this.marks[2]+this.marks[3]+this.marks[4];
        print("Sum = ");
        print(this.sum);
        print("\n");
        this.average = this.sum/5;
        print("Average = ");
        print(this.average);
        print("\n");
    }
    
};
int main()
{
    Student a;
    a.roll = 101;
    a.marks[0] = 90;
    a.marks[1] = 85;
    a.marks[2] = 90;
    a.marks[3] = 95;
    a.marks[4] = 80;
    a.calc();
}
