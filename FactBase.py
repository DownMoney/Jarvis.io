from Modules import utilities


class FactBase:
    """stores unary and binary relational facts"""
    
    factBase = {}    

    def __init__(self):
        self.triggerProb = 0.5
        self.factBase = {}
        self.addFacts(utilities.GetCurrentLocation()['AdditionalData'])        

    def addFacts(self, data):
        self.factBase = dict(self.factBase.items() + data.items())       

    def getFactBase(self):
        return self.factBase

 


