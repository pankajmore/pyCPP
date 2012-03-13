## Symbol Table 

## Environment represents a scope . So whenever you create a new scope you should create a new environment and p in the constructor 
## is the parent Environment . 
class Environment(object):
    def __init__(self,p):
        self.table = SymbolTable() 
        self.prev = p 
## First  create an object of class Symbol and then insert it in the current environment . 
## returns True if put was successful .In case of duplicate entry returns False . 
    def put(self,attr):
        return self.table.put(attr.name,attr)
## get will retrun an Symbol object if symbol is found otherwise None  .
    def get(self,name):
        env = self
        symbol = None 
        while(symbol is None and env is not None):
            symbol = env.table.get(name)
            env = env.prev 
        return symbol 
    
## Symbol table is implemented as a simple python dictionary .
class SymbolTable(object):
    def __init__(self):
        self.symbols = {}
    def put(self,name,symbol):
        if name in self.symbols:
            return False 
        self.symbols[name]=symbol
        return True 
    def get(self,name):
        if name in self.symbols:
            return self.symbols[name]
        else :
            return None 
        

## This class represts a symbol , its type and associated attributes . 
class Symbol(object):
    def __init__(self,name):
        self.name = name 
        self.keyword = False 
        self.type = None 
        self.attrs = {} 
    def __repr__(self):
        return ("name : " + str(self.name) + " || type : " + str(self.type) + " || keyword : " + str(self.keyword))



def test():
    ## When new scope begins 
    env = Environment(None) ## For the first scope since no parent so None 
    i = Symbol("i")
    i.type = "Int"
    i.attrs["foo"] = "bar"
    env.put(i)

    j = Symbol("j")
    j.type = "Int"
    j.attrs["foo"] = "bar"
    env.put(j)

    env2 = Environment(env)
    i = Symbol("i")
    i.type = "Float"
    i.attrs["foo2"] = "bar2"
    env2.put(i)

    print(env.get("i"))
    print(env2.get("i"))
    print(env2.get("j"))

if __name__ == "__main__":
    test()
    




