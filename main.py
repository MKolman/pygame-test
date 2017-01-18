import pygame


class Igralec(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect()

    def premik(self, x, y):
        self.rect.x += x
        self.rect.y += y


igralec = Igralec()
igra_skupina = pygame.sprite.Group()
igra_skupina.add(igralec)

ekran = pygame.display.set_mode([600, 400])
ura = pygame.time.Clock()

igramo = True
while igramo:
    ura.tick(60)
    for dogodek in pygame.event.get():
        if dogodek.type == pygame.QUIT:
            igramo = False
        elif dogodek.type == pygame.KEYDOWN:
            if dogodek.key == pygame.K_DOWN:
                igralec.premik(0, 10)
            elif dogodek.key == pygame.K_UP:
                igralec.premik(0, -10)
            elif dogodek.key == pygame.K_LEFT:
                igralec.premik(-10, 0)
            elif dogodek.key == pygame.K_RIGHT:
                igralec.premik(10, 0)

    ekran.fill((200, 200, 255))
    igra_skupina.draw(ekran)
    pygame.display.flip()

pygame.quit()
