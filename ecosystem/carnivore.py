from animal import Animals

class Carnivore(Animals):
    def __init__(self):
        super().__init__(True, False)

    def chasser(self):
        pass

    def reproduction(self):
        pass

    def draw():
        pygame.draw.polygon(surface=screen, color=(255, 255, 255), points=[x, y, z])