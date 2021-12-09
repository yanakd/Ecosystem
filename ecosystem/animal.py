import lifeforms

class Animals(lifeforms):
    def __init__(self, gender : bool, isViande : bool):
        super().__init__(10, False, 10, True, False)
        self.gender = __gender
        self.isViande = __isViande

    def bouffe(self):
        pass

    def roam(self):
        pass

    @abstractmethod
    def reproduction(self):
        pass

    def devenirMiams(self):
        pass

    def faireCaca(self):
        pass

    def infligerDegats(self):
        pass