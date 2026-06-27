from dataclasses import dataclass


@dataclass
class Costructor:
    constructorId:int
    constructorRef:str
    name:str
    nationality:str
    url:str
    risultati:dict=None

    def __hash__(self):
        return hash(self.constructorId)
    def __eq__(self, other):
        return self.constructorId == other.constructorId
    def __str__(self):
        return f"{self.constructorId}"