import pygame

class GameEngine:
    def __init__(self, width=800, height=600):
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("AI Text RPG")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))  # czarne tło
            pygame.display.flip()
            self.clock.tick(60)
