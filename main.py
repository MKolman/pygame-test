import sys
from random import randint
import pygame
from pygame.sprite import spritecollide as sc

# Povejmo pygame naj se zažene
pygame.init()

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
                 left=pygame.K_LEFT, right=pygame.K_RIGHT, ovire=None, player=1):
        super().__init__()
        # Zapomnimo si življenje
        self.ziv = 100

        # Shranimo si vse ovire v levelu
        self.ovire = ovire

        # Shranimo vse tipke za kasnejso uporabo
        self.up = up
        self.down = down
        self.left = left
        self.right = right

        # Ustvari sliko igralca, ki je nakljucne barve
        self.image = pygame.Surface((55, 72), pygame.SRCALPHA)
        self.barva = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.rect = self.image.get_rect()

        # Shranimo si slike animacij
        if player == 1:
            self.slike = pygame.image.load("spritesheet.png")
        else:
            self.slike = pygame.image.load("spritesheet2.png")

        # Nastavimo eno sliko
        self.image.blit(self.slike, (0, 0), (5, 4, 55, 74))
                        # (55*0+5, 4, 55*(0+1), 76))
        self.stevec = {"tek": 0, "mir": 0}
        self.trajanje = 8
        self.levo = False
        # self.narisi_me()

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

    # Metoda, ki izriše našo sliko na pravilno mesto zaslona
    def narisi_me(self):
        self.image.fill((0, 0, 0, 0))
        if self.na_oviri() is False:
            self.image.blit(self.slike, (0, 0),
                            (2, 248, 52, 320))
            if self.vy > 0:
                self.image = pygame.transform.flip(self.image, False, True)
        elif abs(self.vx) > 1:
            self.stevec["tek"] += 1
            self.stevec["tek"] %= 4*self.trajanje
            st_slike = int(self.stevec["tek"] / self.trajanje)
            self.image.blit(self.slike, (0, 0),
                            (55*st_slike+5, 4, 55*(st_slike+1), 76))
        else:
            self.stevec["mir"] += 1
            self.stevec["mir"] %= 4*self.trajanje
            st_slike = int(self.stevec["mir"] / self.trajanje)
            self.image.blit(self.slike, (0, 0),
                            (56*st_slike, 169, 56*st_slike+50, 241))

        if self.levo:
            self.image = pygame.transform.flip(self.image, True, False)
        return
        # Napolnimo se z barvo
        self.image.fill(self.barva)
        # Napišimo preostanek življenja
        font = pygame.font.SysFont("comicsansms", 30)
        text = font.render(str(self.ziv), True, (0, 0, 0))
        self.image.blit(text, (5, 15))

    # Ali Igralec stoji na oviri (Tako vemo, ali lahko skoči)
    def na_oviri(self):
        if self.rect.bottom >= VISINA:
            # Lahko stoji tudi na dnu ekrana
            return True
        elif self.ovire is None:
            # Če nismo dobili ovir, potem ne more stati na njih
            return False
        else:
            # Premaknimo se za en pixel in poglejmo, če smo se zadeli ob kakšno
            # oviro
            self.rect.y += 1
            rezultat = sc(self, self.ovire, False)
            self.rect.y -= 1
            for ov in rezultat:
                # Stik z oviro velja zgolj, če sicer stojimo nad njo
                if self.rect.bottom <= ov.rect.top:
                    return True
            # Če nismo našli ovire na kateri smo, sporočimo False
            return False

    # ko uporabnik pritisne ali spusti neko tipko ustrezno popravimo hitrosti
    def oznaci_pritisk(self, smer, status):
        # Najprej si zabeležimo smer premika
        self.smeri[smer] = status

        hitrost = 6

        # Tipka dol ne naredi nič
        if self.smeri[self.down] and self.na_oviri():
            self.rect.y += 1
        # S tipko gor skočimo
        if self.smeri[self.up] and self.na_oviri():
            self.vy = -20

        # če držimo levo ali desno se premikamo levo, ali desno, sicer se ne
        self.vx = 0
        if self.smeri[self.left]:
            self.vx = -hitrost
            self.levo = True
        if self.smeri[self.right]:
            self.vx = hitrost
            self.levo = False

    # Vsak frame igre moramo premakniti igralca. To dela metoda update, ki jo
    # klicemo v vsakem prehodu
    def update(self):
        # Najprej poglejmo premik v x smeri
        self.premik(self.vx, 0)
        # Poglejmo ali smo se ob premiku v x smer kam zaleteli
        # Ta del smo zakomentirali, saj želimo, prehodne ovire v smeri x-y
        # for ov in sc(self, self.ovire, False):
        #     if self.vx > 0:
        #         self.rect.right = ov.rect.left
        #     else:
        #         self.rect.left = ov.rect.right
        #     self.vx = 0

        # Naj se zgodi gravitacija
        self.vy += 1
        # Sedaj porihtajmo premik v y smeri
        prejsnje_dno = self.rect.bottom
        self.premik(0, self.vy)
        # Če se zabijemo v kakšno oviro:
        for ov in sc(self, self.ovire, False):
            if ov.tip == 3:
                # ovira tipa 3 je CILJ
                print("Zmagal si")
                sys.exit(0)
            if self.vy > 0 and prejsnje_dno <= ov.rect.top:
                # Če smo se zabili v oviro z zgornje strani, se ustavimo
                self.rect.bottom = ov.rect.top
                self.vy = 0
            if ov.tip == 1:
                # Ovira tipa 1 nas poškoduje
                self.ziv -= 5
        if self.ziv <= 0:
            self.umri()
        self.narisi_me()

    # Pomozna funkcija, ki premakne igralca in poskrbi, da ne gre iz ekrana
    def premik(self, x, y):
        self.rect.x += x
        self.rect.y += y
        self.rect.x = max(self.rect.x, 0)
        self.rect.right = min(self.rect.right, SIRINA)
        # if self.rect.y < 0:
        #     self.rect.y = 0
        #     self.vy = 0
        # self.rect.y = max(self.rect.y, 0)
        if self.rect.bottom > VISINA:
            self.rect.bottom = VISINA
            self.vy = 0

    def umri(self):
        self.rect.left = 0
        self.rect.bottom = VISINA
        self.ziv = 100
        self.vx = 0
        self.vy = 0


class Plato(pygame.sprite.Sprite):
    """ Ravna podlaga po kateri lahko igralci skacejo.
    Obstaja več tipov platojev
        0: Navaden plato skozi katerega lahko gremo od spodaj,
        1: Plato, ki nas poskoduje,
        2: Plato skozi katerega nikakor ne moremo,
        3: Cilj,
    """
    # Vse kar potrebujemo so položaj (x, y) in dimenzije (w, h)
    def __init__(self, x=100, y=300, w=200, h=10, tip=0):
        super().__init__()
        self.image = pygame.Surface((w, h))
        if tip == 0:
            self.image.fill((0, 255, 0))
        elif tip == 1:
            self.image.fill((255, 0, 0))
        elif tip == 3:
            self.image.fill((255, 255, 0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tip = tip


# Naredimo nekaj odskočišč za igralce in jih poimenujemo "level"
level = pygame.sprite.Group()
# Cilj
level.add(Plato(10, 10, 50, 50, 3))
# Nevarnosti
level.add(Plato(200, 395, 400, 10, 1))
level.add(Plato(200, 300, 50, 10, 1))
# Odskocisca
level.add(Plato(250, 300, 50, 10))
level.add(Plato(500, 200, 50, 10))
level.add(Plato(300, 100, 50, 10))
level.add(Plato(10, 100, 100, 10))
level.add(Plato(10, 160, 100, 10))
# Spodaj dodamo še: level.draw(ekran)

# Ustvarimo dva igralca, vsakega s svojim setom ukaznih tipk
igralec = Igralec(pygame.K_w, pygame.K_s,
                  pygame.K_a, pygame.K_d, ovire=level, player=1)
igralec2 = Igralec(ovire=level, player=2)
igralec.rect.bottom = VISINA
igralec2.rect.bottom = VISINA

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
