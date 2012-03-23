class productSpecification{
   int id;
   float price;
public:
   void initializeInfo(int i,float p);
   int getItemID() {return id;}
   float getPrice() {return price;}
};
class productCatalog{
public:
   void prodInfo();
   void displayMenu();
   void searchCatalog(int v);
};
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
int main(){
   productCatalog ob;
    x = ob.prodInfo();
   return 0;
}
