#include<iostream>
#include<string>
class productSpecification{
   int id;
   float price;
   string description;
public:
   void initializeInfo(int i,float p, string d);
   int getItemID() {return id;}
   float getPrice() {return price;}
   string getDescription() {return description;}
};
void productSpecification::initializeInfo(int i, float p, string d){
   id=i;
   price=p;
   description=d;
}
   
class productCatalog{
public:
   void prodInfo();
   void displayMenu();
   void searchCatalog(int v);
};
void productCatalog::prodInfo(){
   productSpecification obj[3];
   int n;
   
   obj[0].initializeInfo(100, 24.95, "Enter the Dragon DVD");
   obj[1].initializeInfo(200, 22.95, "Gladiator DVD");
   
   cout<<"Id: "<<obj[0].getItemID()<<endl;
   cout<<"Price: "<<obj[0].getPrice()<<endl; 
   cout<<"Description: "<<obj[0].getDescription()<<endl;   
   cout<<'\n';
   cout<<"Id: "<<obj[1].getItemID()<<endl;
   cout<<"Price: "<<obj[1].getPrice()<<endl;
   cout<<"Description: "<<obj[1].getDescription()<<endl; 
}
void productCatalog::displayMenu(int choice){
   
int main(){
   productCatalog ob;
   ob.prodInfo();
   return 0;
}
