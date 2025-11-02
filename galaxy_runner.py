import pygame
import random
import os
import sys

pygame.init()

# --- CONFIGURACIÓN DE VENTANA ---
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("🚀 Galaxy Runner Enhanced")
RELOJ = pygame.time.Clock()
FPS = 60

# --- COLORES ---
BLANCO = (255, 255, 255)
ROJO = (255, 50, 50)
VERDE = (50, 255, 50)
AMARILLO = (255, 255, 100)

# --- RUTAS ---
ASSETS = os.path.join(os.path.dirname(__file__), "assets")

# --- FUNCIONES DE CARGA ---
def cargar_imagen(nombre, escala=None):
    ruta = os.path.join(ASSETS, nombre)
    img = pygame.image.load(ruta).convert_alpha()
    if escala:
        img = pygame.transform.scale(img, escala)
    return img

def cargar_sonido(nombre):
    ruta = os.path.join(ASSETS, nombre)
    if os.path.isfile(ruta):
        return pygame.mixer.Sound(ruta)
    return None

# --- CARGAR RECURSOS ---
BACKGROUND = cargar_imagen("background.png", (ANCHO, ALTO))
PLAYER_IMG = cargar_imagen("player.png", (60, 48))
METEOR_IMG = cargar_imagen("meteor.png", (50, 50))
STAR_IMG = cargar_imagen("star.png", (30, 30))
BULLET_IMG = cargar_imagen("bullet.png", (10, 25))

SONIDO_DISPARO = cargar_sonido("shoot.wav")
SONIDO_EXPLOSION = cargar_sonido("explosion.wav")

# --- FUENTES ---
FUENTE = pygame.font.SysFont("Arial", 28, bold=True)
FUENTE_GRANDE = pygame.font.SysFont("Arial", 50, bold=True)

# --- CLASES ---
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect(center=(ANCHO // 2, ALTO - 60))
        self.vel = 6
        self.vidas = 3
        self.cooldown = 0
        self.invulnerable = 0  # frames de invulnerabilidad

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.vel
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.vel
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.vel

        if self.cooldown > 0:
            self.cooldown -= 1
        if self.invulnerable > 0:
            self.invulnerable -= 1  # disminuye tiempo de invulnerabilidad

    def disparar(self):
        if self.cooldown == 0:
            bala = Bala(self.rect.centerx, self.rect.top)
            todas_balas.add(bala)
            if SONIDO_DISPARO:
                SONIDO_DISPARO.play()
            self.cooldown = 10

    def reaparecer(self):
        self.rect.center = (ANCHO // 2, ALTO - 60)
        self.invulnerable = 60  # 1 segundo de invulnerabilidad

class Meteorito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = METEOR_IMG
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.vel = random.randint(2, 6)

    def update(self):
        self.rect.y += self.vel
        if self.rect.top > ALTO:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, ANCHO - self.rect.width)

class Estrella(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = STAR_IMG
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-200, -40)
        self.vel = random.randint(1, 4)

    def update(self):
        self.rect.y += self.vel
        if self.rect.top > ALTO:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, ANCHO - self.rect.width)

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = BULLET_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = -10

    def update(self):
        self.rect.y += self.vel
        if self.rect.bottom < 0:
            self.kill()

# --- GRUPOS ---
jugador = Jugador()
todas_balas = pygame.sprite.Group()
meteoritos = pygame.sprite.Group()
estrellas = pygame.sprite.Group()
todos = pygame.sprite.Group(jugador)

for _ in range(5):
    m = Meteorito()
    meteoritos.add(m)
    todos.add(m)

for _ in range(3):
    e = Estrella()
    estrellas.add(e)
    todos.add(e)

puntaje = 0
mensaje_vidas = ""
mostrar_mensaje_frames = 0

# --- FUNCIONES ---
def dibujar_texto(texto, x, y, color=BLANCO, fuente=FUENTE):
    render = fuente.render(texto, True, color)
    VENTANA.blit(render, (x, y))

def game_over():
    VENTANA.blit(BACKGROUND, (0, 0))
    dibujar_texto("GAME OVER", 300, 250, ROJO, FUENTE_GRANDE)
    dibujar_texto("Presiona ENTER para reiniciar", 240, 330, BLANCO)
    pygame.display.flip()
    esperar = True
    while esperar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperar = False

# --- LOOP PRINCIPAL ---
while True:
    RELOJ.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jugador.disparar()

    # Actualizar grupos
    todos.update()
    todas_balas.update()

    # --- Colisiones bala - meteorito ---
    colisiones = pygame.sprite.groupcollide(meteoritos, todas_balas, True, True)
    for _ in colisiones:
        puntaje += 5
        if SONIDO_EXPLOSION:
            SONIDO_EXPLOSION.play()
        nuevo = Meteorito()
        meteoritos.add(nuevo)
        todos.add(nuevo)

    # --- Colisión jugador - meteorito ---
    if jugador.invulnerable == 0:
        colision = pygame.sprite.spritecollideany(jugador, meteoritos)
        if colision:
            jugador.vidas -= 1
            if SONIDO_EXPLOSION:
                SONIDO_EXPLOSION.play()
            colision.rect.y = random.randint(-100, -40)
            colision.rect.x = random.randint(0, ANCHO - colision.rect.width)

            if jugador.vidas > 0:
                jugador.reaparecer()
                mensaje_vidas = f"💥 ¡Perdiste una vida! Te quedan {jugador.vidas}."
                mostrar_mensaje_frames = 120
            else:
                game_over()
                jugador.vidas = 3
                puntaje = 0
                meteoritos.empty()
                for _ in range(5):
                    m = Meteorito()
                    meteoritos.add(m)
                    todos.add(m)
                jugador.reaparecer()

    # --- Colisión jugador - estrella ---
    recolectadas = pygame.sprite.spritecollide(jugador, estrellas, True)
    for _ in recolectadas:
        puntaje += 10
        nueva = Estrella()
        estrellas.add(nueva)
        todos.add(nueva)

    # --- DIBUJAR ---
    VENTANA.blit(BACKGROUND, (0, 0))
    estrellas.draw(VENTANA)
    meteoritos.draw(VENTANA)
    todas_balas.draw(VENTANA)
    VENTANA.blit(jugador.image, jugador.rect)

    dibujar_texto(f"Puntaje: {puntaje}", 10, 10)
    dibujar_texto(f"Vidas: {jugador.vidas}", 10, 40)

    if mostrar_mensaje_frames > 0:
        dibujar_texto(mensaje_vidas, 200, 280, AMARILLO)
        mostrar_mensaje_frames -= 1

    pygame.display.flip()
