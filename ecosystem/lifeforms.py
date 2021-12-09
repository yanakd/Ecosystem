from abc import ABC, abstractmethod

class lifeforms(ABC):
    def __init__(self, hp : int, dead : bool, nrj : int, form : bool, isCaca : bool):
        #variables needed by all lifeforms
        self.hp = hp #"hit points" = life points of a lifeform
        self.dead = dead #defines if a lifeform is dead if dead == true
        self.nrj = nrj #energy points of a lifeforms
        self.form = form #true if plant, false if animal
        self.isCaca = isCaca #defines if lifeform is organic waste

    #defines how a lifeform loses hp, either through damage by another lifeform or when nrj == 0 
    def damage(self):
        pass

    #defines how nrj goes up by eating ==> faut probablement enlever
    def Nrj(self):
        pass

    #changes dead to true and calls devenirCaca() if needed
    def isDead(self):
        pass

    def devenirCaca(self):
        pass

