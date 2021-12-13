from animal import Animals

class Herbivore(Animals):
    def __init__(self):
        super().__init__(True, False)

    def chasserHerbe(self):
        pass

    def reproduction(self):
        pass

    def fuite(self):
        pass