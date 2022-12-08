# Tuodaan tarvittavat kirjastot
import pygame
import random

# Luodaan yliluokka peliobjektille, jossa asetus ja havainnointimetodit
class GameObject:
    def __init__(self, image: str):
        # Attribuutteina kuvan nimi, koordinaatit ja kuvan koko
        self._image = image
        self._x = 0
        self._y = 30
        self._height = pygame.image.load(self._image).get_height()
        self._width = pygame.image.load(self._image).get_width()

    # Funktio, jolla peliobjektin kuva saadaan näkymään ikkunassa
    def _show_object(self):
        screen.blit(pygame.image.load(self._image), (self._x, self._y))
        

    # Havainnointimetodeja konstruktorin attribuuteille, joilla saadaan kyseisen attribuutin tiedot helposti.
    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def image(self):
        return self._image
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    # Asetusmetodeja x ja y koordinaateille, jolloin koordinaatteihin lisätään haluttu luku
    @x.setter
    def x(self, value):
        self._x += value
    
    @y.setter
    def y(self, value):
        self._y += value
    

# Aliluokka koiralle, joka perii yliluokka Gameobjektin piirteitä
class Dog(GameObject):
    def __init__(self, name: str, image: str):
        # Yliluokan konstruktoriin viitataan funktiolla super(), jolla lähetetään kuvan tiedot
        super().__init__(image)

        # Koira-luokalla on lisäksi omia attribuutteja nimelle, omille pisteille, sekä liikkumissuunnille
        self._name = name
        self._points = []
        self._right = False
        self._left = False
        self._up = False
        self._down = False

    # Funktio palauttaa luokan objektin tiedot halutussa esitystavassa
    def __str__(self):
        return f"{self.name}: {len(self._points)} luuta, {self.points} pistettä."
    
    # Havainnointi metodi nimelle
    @property
    def name(self):
        return self._name
    
    # Funktio koiran liikkumiselle, joka pyörii kunnes aika on loppunut
    def _move(self):
        # Luodaan muuttuja tekstien fontille
        font = pygame.font.SysFont("Arial", 24)
        # Luodaan muuttuja alkuajalle, joka saadaan kun funktio pygame.init() kutsutaan pelin alussa.
        start = pygame.time.get_ticks()
        # Luodaan muuttujat sekunneille ja jäljellä oleville sekunneille
        seconds = 0
        remaining_secs = 10

        #Pyöritetään peliä niin kauan, kunnes ajaksi jää 0
        while remaining_secs >= 1:
            # Asetetaan sekunneiksi nyt tämän hetken ticksit-alkuaika ja jaetaan 1000, jolloin saadaan sekunnit
            seconds = (pygame.time.get_ticks()-start)/1000
            # Peliaika on 20 sekunttia, jolloin asetetaan alkuun 21, jotta alussa on näkyvissä luku 20 ja vähennetään siitä aina sen hetken saadut sekunnit
            remaining_secs = 21-seconds

            # Seurataan pelissä tapahtuvia tapahtumia
            for event in pygame.event.get():
            #Kun pelaaja painaa näppäimistöllä tietyn näppäimen, vaihdetaan sen arvoksi True, jolloin koira liikkuu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self._left = True              
                    if event.key == pygame.K_RIGHT:
                        self._right = True
                    if event.key == pygame.K_UP:
                        self._up = True
                    if event.key == pygame.K_DOWN:
                        self._down = True

                # Kun pelaaja nostaa painetun näppäimen, vaihdetaan arvoksi False, jolloin koira pysähtyy
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self._left = False
                    if event.key == pygame.K_RIGHT:
                        self._right = False
                    if event.key == pygame.K_UP:
                        self._up = False
                    if event.key == pygame.K_DOWN:
                        self._down = False

                # Mikäli pelaaja painaa rastia, suljetaan peli
                if event.type == pygame.QUIT:
                    exit()

            # Käydään koko ajan läpi: mikäli pelaaja painaa jotain nappia ja sen suunnan arvo on True, ja koira on tietyssä paikassa, liikkuu koira sen mukaan oikeaan suuntaan.
            if self._right and self._x <= 740-self._width:
                self._x += 2
            if self._left and self._x >= 0:
                self._x -= 2
            if self._up and self._y >= 30:
                self._y -= 2
            if self._down and self._y <= 580 - self._height:
                self._y += 2
                    
            # Tarkistetaan osuiko koira luuhun kutsumalla kyseistä funktiota
            self._hit_bone()
                        
            # Asetetaan taustaväri ja näytetään koira ja luut
            screen.fill((131, 238, 255))
            self._show_object()
            bone._show_object()
            bone2._show_object()
            
            # Luodaan teksti, josta näkee pisteet ja jäljellä olevan ajan, ja näytetään se ruudussa kohdassa x=200 ja y=5
            # Pisteet saadaan laskettua sum_points-funktiolla.
            text = font.render(f"{self._name}: pisteet: {self._sum_points(0)}, aikaa jäljellä: {int(remaining_secs)}", True, (0,0,0))
            # Piirretään teksti näytölle haluttuun kohtaan
            screen.blit(text, (200, 5))
            # Päivitetään näytön sisältöä
            pygame.display.flip()
            # Asetetaan kellolle arvo 60, jolloin se liikkuu sekunnissa 60 pikseliä
            clock.tick(60)
            
            
        #Kun aika loppuu, tulostetaan loppu-teksti ja koiran tiedot
        text = font.render(f"LOPPU", True, (0,0,0))
        text2 = font.render(f"{self}", True, (0,0,0))
        # Piirretään tekstit näytölle haluttuun kohtaan ja päivitetään näyttöä
        screen.blit(text, (290, 200))
        screen.blit(text2, (220, 230))
        pygame.display.flip()

    # Oma funktio tarkistamaan osuuko koira jompaankumpaan luuhun
    def _hit_bone(self):
        # Mikäli koira osuu luuhun, arvotan uusi luu uuteen paikkaan ja lisätään pisteitä koiralle.
        if bone.x-self._width <= self._x and bone.x + bone.width >= self._x and bone.y-self._height <= self._y and bone.y + bone.height >= self._y:
                        #Lisätään luun arvon verran pisteitä listalle
                        if bone.image == "bone1.png":
                            self._points.append(1)
                        elif bone.image == "bone2.png":
                            self._points.append(3)
                        elif bone.image == "bone3.png":
                            self._points.append(5)
                        
                        #Arvotaan uuden luun paikka ja vähennetään luu-laskurista 1
                        bone._random_xy()

        # Sama tarkistus toiselle luulle
        if bone2.x-self._width <= self._x and bone2.x + bone2.width >= self._x and bone2.y-self._height <= self._y and bone2.y + bone2.height >= self._y:
                        #Lisätään luun arvon verran pisteitä listalle
                        if bone2.image == "bone1.png":
                            self._points.append(1)
                        elif bone2.image == "bone2.png":
                            self._points.append(3)
                        elif bone2.image == "bone3.png":
                            self._points.append(5)
                        
                        bone2._random_xy()

    # Rekursiivinen summa laskuri luu-listan arvojen laskemiseen, johon se saa alkuarvoksi tässä pelissä aina 0
    def _sum_points(self, i: int):
        # Tarkistetaan onko listalla mitään
        if len(self._points) <= i:
            return 0
        # Jos on, palautetaan listan sen hetken luun pistemäärä ja lisätään siihen aina seuraavan luun pisteet
        return self._points[i] + self._sum_points(i + 1)

    #Havainnointimetodi pisteille, joka käyttää summa-laskuria.
    @property
    def points(self):
        return self._sum_points(0)
        
                    
#Ali-luokka luulle, joka perii GameObjektin piirteitä
class Bone(GameObject):
    def __init__(self, images: list):
        #Viitataan yliluokan konstruktoriin ja annetaan kuvan arvoksi arpomalla joku luu listalta
        super().__init__(random.choice(images))

        #arvotaan arvot luun koordinaateille
        self._x = random.randint(0,700)
        self._y = random.randint(40, 520)
        # Lisäksi lista luista
        self._images = images
    
    # Funktio, jolla arvotaan luu uuteen paikkaan eri värisenä
    def _random_xy(self):
        self._x = random.randint(0, 700)
        self._y = random.randint(0, 520)
        self._image = random.choice(self._images)
    
# Käynnistetään ohjelma
pygame.init()
# Asetetaan ohjelmalle nimi
pygame.display.set_caption("Bone Hunt")
# Asetetaan näytölle koko
screen = pygame.display.set_mode((740,580))
# Määritellään kello, jolla säädetään animaation nopeutta
clock = pygame.time.Clock()

# Luodaan koirille kuvat ja luodaan tyhjä koiraolio
dogpic = pygame.image.load("dog1.png")
dogpic2 = pygame.image.load("dog2.png")
dog = None

# Luodaan muuttuja luiden kuville ja luodaan kaksi luu-oliota
bones = ["bone1.png", "bone2.png", "bone3.png"]
bone = Bone(bones)
bone2 = Bone(bones)

# Luodaan alkuun koordinaatit koirien kuville, joista valitaan kummalla koiralla haluaa pelata
x = 250
y = 200
x2 = 400
y2 = 200

# Täytetään näyttö sinisellä värillä
screen.fill((131, 238, 255))
font = pygame.font.SysFont("Arial", 24)
text = font.render(f"Valitse pelaaja:", True, (0,0,0))

# Piirretään koirien kuvat näytölle haluttuun koordinaattiin
screen.blit(text, (300, 150))
screen.blit(dogpic, (x,y))
screen.blit(dogpic2, (x2, y2))
# Päivitetään ikkunan sisältöä
pygame.display.flip()


while True:
    for event in pygame.event.get():

        # Pelaaja valitsee koiran itselleen hiirellä, jolloin se valitaan koordinaattien perusteella
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] >= x and event.pos[0] <= x+dogpic.get_width() and event.pos[1] >= y and event.pos[1] <= y+dogpic.get_height():

                # Luodaan uusi koira ja laitetaan se liikkumaan
                dog = Dog("Bluey", "dog1.png")
                dog._move()
                
            
            elif event.pos[0] >= x2 and event.pos[0] <= x2+dogpic2.get_width() and event.pos[1] >= y2 and event.pos[1] <= y2+dogpic2.get_height():
                dog = Dog("Bingo", "dog2.png")
                dog._move()

        # Mikäli pelaaja painaa rastia, peli päättyy
        if event.type == pygame.QUIT:
                            exit()
           