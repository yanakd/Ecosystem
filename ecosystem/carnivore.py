from animal import Animals

class Carnivore(Animals):
    def __init__(self):
        super().__init__(True, False)

    def chasser(self):
        pass

    def reproduction(self):
        pass