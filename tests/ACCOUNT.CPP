struct account
{
int no[10];
char name[20];
long int d,b,a;
long double t;
};
void main()
{
window(27,2,53,4);
textbackground(3);
clrscr();
textcolor(0);
cprintf(" \n   BANK ACCOUNT SYSTEM");
/*menu*/
window(20,5,60,25);
textbackground(13);
clrscr();
gotoxy(2,3);
textcolor(10);
cprintf("G");
gotoxy(3,3);
textcolor(14);
cprintf("ive The Account No.");
/*name of the account holder*/
textcolor(10);
gotoxy(2,5);
cprintf("E");
textcolor(14);
gotoxy(3,5);
cprintf("nter The Name ");
/*balance*/
textcolor(10);
gotoxy(2,7);
cprintf("A");
textcolor(14);
gotoxy(3,7);
cprintf("mount");
/*amount*/
account i;
/*input*/
gotoxy(22,3);
cin>>i.no[10];
gotoxy(22,5);
cin>>i.name;
gotoxy(22,7);
cin>>i.a;
gotoxy(3,14);textcolor(11);
cout<<"Name: "<<i.name;
/*runtime calculations*/
/*******************************for deposite*******************************/
i.d=i.a+5;
gotoxy(3,16);
cout <<"The Deposite Is: "<<i.d;
/****************************Tax Deduction ***********************************/
i.t=700.8/i.d*100;
gotoxy(3,18);
cout <<"The deduced Tax is :"<<i.t;
gotoxy(15,35);
cout <<"%";
/***************************For Balance**********************************/
i.b=i.d-i.t;
/********** object of the struct account********************/
if (i.b>0 && i.a<=i.b)
{
	gotoxy(3,20);
	cout <<"WITHDRAW THE BALANCE :"<<i.b;
	}
else
     {
       gotoxy(3,20);textcolor(11);
	cprintf("Can't Withdraw Your Balance!!!");}
getch();
}
