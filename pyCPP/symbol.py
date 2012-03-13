## Symbol Table 

## Environment represents a scope . So whenever you create a new scope you should create a new environment and p in the constructor 
## is the parent Environment . 
class Environment(object):
    def __init__(self,p):
        self.table = SymbolTable() 
        self.prev = p 
## First  create an object of class Symbol and then insert it in the current environment . 
    def put(self,attr):
        self.table.put(attr.name,attr)
        pass 
## get will retrun an Symbol object if symbol is found otherwise None  .
    def get(self,name):
        pass 
    
## Symbol table is implemented as a simple python dictionary .
class SymbolTable(object):
    def __init__(self):
        self.symbols = {}
    def put(self,name,symbol):
        pass 
    def get(self,name,symbol):
        pass 

## This class represts a symbol , its type and associated attributes . 
class Symbol(object):
    def __init__(self,name):
        self.name = name 
        self.keyword = False 
        self.type = None 
        self.attrs = {} 



def test():
    ## When new scope begins 
    env = Environment(None) ## For the first scope since no parent so None 
    i = Symbol("i")
    i.type = "Int"
    i.attrs["foo"] = "bar"
    env.put(i)
    print("Done")
    




