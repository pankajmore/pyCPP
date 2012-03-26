from lexer import *
from copy import *
## Symbol Table 

## Environment represents a scope . So whenever you create a new scope you should create a new environment and p in the constructor 
## is the parent Environment . 
class Environment(object):
    def __init__(self,p):
        self.table = SymbolTable() 
        self.prev = p
    def __repr__(self):
        return str(self.table)
       
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
        for key in keywords :
            symbol = Symbol(key)
            symbol.keyword = True
            symbol.type = 'Keyword'
            self.put(key,symbol)
            
    def put(self,name,symbol):
        if name in self.symbols:
            return False 
        symbol.table = self;
        self.symbols[name]=symbol
        return True 
    def get(self,name):
        if name in self.symbols:
            if self.symbols[name].error :
                print ("Error : ambiguous reference to " + str(self.symbols[name]))
                return None 
            return self.symbols[name]
        else :
            return None 
    ## If symbol with given key exists then delete it and returns the symbol else returns None . 
    def delete(self,name):
        return self.symbols.pop(name,None)
    def __repr__(self):
        return str(self.symbols)
    ## Note : changes the current symbol table 
    def combine(self,other):
        if isinstance(other,SymbolTable):
            for k in other.symbols:
                i = deepcopy(other.symbols[k])
                if k in  self.symbols:
                    i.error = True 
                self.symbols[k] = i



        

## This class represts a symbol , its type and associated attributes . 
class Symbol(object):
    def __init__(self,name):
        self.name = name 
        self.keyword = False 
        self.type = None 
        self.error = False 
        self.attr = {}
        self.table = None
    def __repr__(self):
        if not self.keyword:
            return ("name : " + str(self.name) + " || type : " + str(self.type) + " || keyword : " + str(self.keyword) + " || attributes : " + str(self.attr))
        else :
            return ''
        



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

    j = Symbol("k")
    j.type = "Int"
    j.attrs["foo"] = "bar"
    env.put(j)

    env2 = Environment(env)
    i = Symbol("i")
    i.type = "Float"
    i.attrs["foo2"] = "bar2"
    env2.put(i)

    ## Duplicate entry test 
    
    j = Symbol("j")
    j.type = "Float"
    j.attrs["foo2"] = "bar2"
    ## Env put should fail as j already exist 
    if not env.put(j):
        print "failure"
    ## Env2 put should succeed as no local variable with id j 
    if not env2.put(j):
        print "failure"
    env3 = copy(env2);
    env3.prev = None 

    print(env.get("i"))
    print(env2.get("i"))
    print(env2.get("j"))
    print(env2.get("k"))
    print(env3.get("i"))
    print(env3.get("j"))
    print(env3.get("k"))
    print(env2.prev)
    print(env3.prev)


if __name__ == "__main__":
    test()
    




