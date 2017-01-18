import pygame


class Igralec(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect()
        self.smeri = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_RIGHT: False,
            pygame.K_LEFT: False,
        }

    def oznaci_pritisk(self, smer, status):
        self.smeri[smer] = status

    def update(self):
        if self.smeri[pygame.K_DOWN]:
            igralec.premik(0, 5)
        if self.smeri[pygame.K_UP]:
            igralec.premik(0, -5)
        if self.smeri[pygame.K_LEFT]:
            igralec.premik(-5, 0)
        if self.smeri[pygame.K_RIGHT]:
            igralec.premik(5, 0)

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
            igralec.oznaci_pritisk(
                dogodek.key, True)
        elif dogodek.type == pygame.KEYUP:
            igralec.oznaci_pritisk(
                dogodek.key, False)

    igra_skupina.update()
    ekran.fill((200, 200, 255))
    igra_skupina.draw(ekran)
    pygame.display.flip()

pygame.quit()
