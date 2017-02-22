from random import randint
import pygame
from pygame.sprite import spritecollide as sc

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
                 left=pygame.K_LEFT, right=pygame.K_RIGHT, ovire=None):
        super().__init__()
        # Shranimo si vse ovire v levelu
        self.ovire = ovire

        # Shranimo vse tipke za kasnejso uporabo
        self.up = up
        self.down = down
        self.left = left
        self.right = right

        # Ustvari sliko igralca, ki je nakljucne barve
        self.image = pygame.Surface((50, 50))
        self.image.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
        self.rect = self.image.get_rect()

        # hitrosti igralca
        self.vx = 0
        self.vy = 0

        # Predpostavimo, da so vse tipke spuscene ob zacetku igre
        self.smeri = {
            self.up: False,
            self.down: False,
            self.right: False,
            self.left: False,
        }

    # Ali Igralec stoji na oviri (Tako vemo, ali lahko skoči)
    def na_oviri(self):
        if self.rect.bottom >= VISINA:
            # Lahko stoji tudi na dnu ekrana
            return True
        elif self.ovire is None:
            # Če nismo dobili ovir, potem ne more stati na njih
            return False
        else:
            self.rect.y += 1
            rezultat = sc(self, self.ovire, False)
            self.rect.y -= 1
            return rezultat

    # ko uporabnik pritisne ali spusti neko tipko ustrezno popravimo hitrosti
    def oznaci_pritisk(self, smer, status):
        # Najprej si zabeležimo smer premika
        self.smeri[smer] = status

        hitrost = 10

        # Tipka dol ne naredi nič
        if self.smeri[self.down]:
            pass
        # S tipko gor skočimo
        if self.smeri[self.up] and self.na_oviri():
            self.vy = -20

        # če držimo levo ali desno se premikamo levo, ali desno, sicer se ne
        self.vx = 0
        if self.smeri[self.left]:
            self.vx = -hitrost
        if self.smeri[self.right]:
            self.vx = hitrost

    # Vsak frame igre moramo premakniti igralca. To dela metoda update, ki jo
    # klicemo v vsakem prehodu
    def update(self):
        # Najprej poglejmo premik v x smeri
        self.premik(self.vx, 0)
        # Poglejmo ali smo se ob premiku v x smer kam zaleteli
        for ov in sc(self, self.ovire, False):
            if self.vx > 0:
                self.rect.right = ov.rect.left
            else:
                self.rect.left = ov.rect.right
            self.vx = 0

        # Naj se zgodi gravitacija
        self.vy += 1
        # Sedaj porihtajmo še premik v y smeri
        self.premik(0, self.vy)
        # Če se zabijemo v kakšno oviro se ustavimo
        for ov in sc(self, self.ovire, False):
            if self.vy > 0:
                self.rect.bottom = ov.rect.top
            else:
                self.rect.top = ov.rect.bottom
            self.vy = 0

    # Pomozna funkcija, ki premakne igralca in poskrbi, da ne gre iz ekrana
    def premik(self, x, y):
        self.rect.x += x
        self.rect.y += y
        self.rect.x = max(self.rect.x, 0)
        self.rect.right = min(self.rect.right, SIRINA)
        if self.rect.y < 0:
            self.rect.y = 0
            self.vy = 0
        if self.rect.bottom > VISINA:
            self.rect.bottom = VISINA
            self.vy = 0


class Plato(pygame.sprite.Sprite):
    """ Ravna podlaga po kateri lahko igralci skacejo. """

    # Vse kar potrebujemo so položaj (x, y) in dimenzije (w, h)
    def __init__(self, x=100, y=300, w=200, h=10):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Naredimo nekaj odskočišč za igralce in jih poimenujemo "level"
level = pygame.sprite.Group()
level.add(Plato(50, 200, 100, 10))
level.add(Plato(200, 300, 100, 10))
# Spodaj dodamo še: level.draw(ekran)

# Ustvarimo dva igralca, vsakega s svojim setom ukaznih tipk
igralec = Igralec(pygame.K_w, pygame.K_s,
                  pygame.K_a, pygame.K_d, ovire=level)
igralec2 = Igralec(ovire=level)

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
    # Na ekran narisi igralce in level
    level.draw(ekran)
    igra_skupina.draw(ekran)
    # Poskrbi, da se vse skupaj izrise na monitor
    pygame.display.flip()

# Zapri okno pygame
pygame.quit()
