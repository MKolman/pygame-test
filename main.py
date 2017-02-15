from random import randint
import pygame

# Velikost okna
SIRINA = 600
VISINA = 400


class Igralec(pygame.sprite.Sprite):
    """ Razred, ki opisuje enega igralca. Notri so njegove dimenzije, njegova
    barva, katere tipke uporablja za premikanje,...
    """

    # Metoda __init__ je funkcija, ki se zazene ob kreairanju novega igralca.
    # V njej nastavimo vse osnovne lastnosti igralca
    def __init__(self, up=pygame.K_UP, down=pygame.K_DOWN,
                 left=pygame.K_LEFT, right=pygame.K_RIGHT):
        super().__init__()
        # Shranimo vse tipke za kasnejso uporabo
        self.up = up
        self.down = down
        self.left = left
        self.right = right

        # Ustvari sliko igralca, ki je nakljucne barve
        self.image = pygame.Surface((50, 50))
        self.image.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
        self.rect = self.image.get_rect()

        # Predpostavimo, da so vse tipke spuscene ob zacetku igre
        self.smeri = {
            self.up: False,
            self.down: False,
            self.right: False,
            self.left: False,
        }

    # ko uporabnik pritisne ali spusti neko tipko, si to oznacimo
    def oznaci_pritisk(self, smer, status):
        self.smeri[smer] = status

    # Vsak frame igre moramo premakniti igralca. To dela metoda update, ki jo
    # klicemo v vsakem prehodu
    def update(self):
        if self.smeri[self.down]:
            self.premik(0, 5)
        if self.smeri[self.up]:
            self.premik(0, -5)
        if self.smeri[self.left]:
            self.premik(-5, 0)
        if self.smeri[self.right]:
            self.premik(5, 0)

    # Pomozna funkcija, ki premakne igralca in poskrbi, da ne gre iz ekrana
    def premik(self, x, y):
        self.rect.x += x
        self.rect.y += y
        self.rect.x = max(self.rect.x, 0)
        self.rect.y = max(self.rect.y, 0)
        self.rect.right = min(self.rect.right, SIRINA)
        self.rect.bottom = min(self.rect.bottom, VISINA)

# Ustvarimo dva igralca, vsakega s svojim setom ukaznih tipk
igralec = Igralec(pygame.K_w, pygame.K_s,
                  pygame.K_a, pygame.K_d)
igralec2 = Igralec()

# Oba igralca dodamo v skupino, da ju lazje skupaj risemo in posodabljamo
igra_skupina = pygame.sprite.Group()
igra_skupina.add(igralec)
igra_skupina.add(igralec2)

# Ustvarimo prazno okno definirane sirine in visine
ekran = pygame.display.set_mode([SIRINA, VISINA])
# Ura bo poskrbela, da se bo nasa igra predvajala pri 60 slikah na sekundo
ura = pygame.time.Clock()

# Definiramo spemenljivko s katero bomo spremljali, ali se vedno igramo igro
igramo = True
while igramo:
    # Poskrbimo, da igra tece pri 60 slikah na sekundo
    ura.tick(60)

    # Preverimo vse dogodke, ki so se zgodili v tem 1/60s
    # To so vsi pritiski tipk na tipkovnici in miski
    for dogodek in pygame.event.get():
        if dogodek.type == pygame.QUIT:
            # Ce uporabnik zapre okno nehajmo igrati
            igramo = False
        elif dogodek.type == pygame.KEYDOWN:
            # Ce uporabnik pritisne katerokoli tipko si to oznacimo
            igralec.oznaci_pritisk(dogodek.key, True)
            igralec2.oznaci_pritisk(dogodek.key, True)
        elif dogodek.type == pygame.KEYUP:
            # Ce uporabnik spusti katerokoli tipko si to oznacimo
            igralec.oznaci_pritisk(dogodek.key, False)
            igralec2.oznaci_pritisk(dogodek.key, False)

    # Premakni oba igralca
    igra_skupina.update()

    # Cel ekran prebarvaj z ozadjem
    ekran.fill((200, 200, 255))
    # Na ekran narisi igralce
    igra_skupina.draw(ekran)
    # Poskrbi, da se vse izrise na monitor
    pygame.display.flip()

# Zapri okno pygame
pygame.quit()
