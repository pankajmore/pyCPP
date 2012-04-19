int main()
{
int i;
char ch[10];
for(i=0;i<8;i++)
{
ch[i]=(char)(9+'0');
}

int loop;
int num=0;
for(loop=0;loop<8;loop++)
{
char tmp;
tmp = ch[loop]-'0';
num=num*10+tmp;
}

num+=1;
print(num);
print("\n");
}
