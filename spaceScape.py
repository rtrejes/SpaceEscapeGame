##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.4                      ###
##############################################################
### Objetivo: desviar dos meteoros que caem.               ###
### Cada colisão tira uma vida. Sobreviva o máximo que     ###
### conseguir!                                             ###
##############################################################
### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###
##############################################################

import pygame
import random
import os

# Inicializa o PyGame
pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape")

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS (troque os arquivos de assets aqui)
# ----------------------------------------------------------
# Dica: coloque as imagens e sons na mesma pasta do arquivo .py
# e troque apenas os nomes abaixo.

ASSETS = {
    "background": "fundo_espacial.png",  # imagem de fundo
    "player": "nave001.png",  # imagem da nave
    "meteor": "meteoro001.png",  # imagem do meteoro
    "sound_point": "classic-game-action-positive-5-224402.mp3",  # som ao desviar com sucesso
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",  # som de colisão
    "sound_life": "sound_life.wav",
    "music": "distorted-future-363866.mp3",  # música de fundo. direitos: Music by Maksym Malko from Pixabay
    "missil": "missil.png",  # imagem do missil
    "life_meteor": "meteoro_vidas_v2.png"  # imagem do meteoro de vidas
}

# ----------------------------------------------------------
# 🖼️ CARREGAMENTO DE IMAGENS E SONS
# ----------------------------------------------------------
# Cores para fallback (caso os arquivos não existam)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
YELLOW = (255, 220, 0)
PINK = (255, 120, 200)

# Tela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Função auxiliar para carregar imagens de forma segura
def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    else:
        # Gera uma superfície simples colorida se a imagem não existir
        surf = pygame.Surface(size or (50, 50))
        surf.fill(fallback_color)
        return surf


# Carrega imagens
background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))
missil_img = load_image(ASSETS["missil"], YELLOW)  # tamanho original
life_meteor_img = load_image(ASSETS["life_meteor"], WHITE, (55,75))


# Sons
def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None


sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])
sound_life = load_sound(ASSETS["sound_life"])

# Música de fundo (opcional)
if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)  # loop infinito

# ----------------------------------------------------------
# 🧠 VARIÁVEIS DE JOGO
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player_speed = 7

meteor_list = []
missil_powerups = []
active_missils = []
life_meteor_list = []  # meteoro especial que dá vida

for _ in range(5):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    meteor_list.append(pygame.Rect(x, y, 40, 40))

meteor_speed = 5
missil_speed = 10

score = 0
lives = 3
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

has_missil_power = False
missil_timer = 0
missil_time_left = 0  # tempo restante do power
missil_end_time = 0  # momento em que acaba

# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Movimento do jogador ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += player_speed

    # ------------------------------------------------------
    # MOVIMENTO E LÓGICA DOS METEOROS
    # ------------------------------------------------------
    for meteor in meteor_list:
        meteor.y += meteor_speed

        # Saiu da tela → reposiciona e soma pontos
        if meteor.y > HEIGHT:
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)

            # chance de 10% de um meteoro ser powerup ou vida
            if random.random() < 0.1:
                if random.random() < 0.5:
                    # chance de 50% de ser powerup
                    px = random.randint(0, WIDTH - missil_img.get_width())
                    py = random.randint(-300, -50)
                    powerup_rect = missil_img.get_rect(topleft=(px, py))

                    missil_powerups.append(powerup_rect)
                else:
                    # chance de 50% de ser meteoro de vida
                    lx = random.randint(0, WIDTH - 40)
                    ly = random.randint(-300, -40)
                    life_meteor_list.append(pygame.Rect(lx, ly, 40, 40))

            score += 1
            if sound_point:
                sound_point.play()

        # colisão com nave
        if meteor.colliderect(player_rect):
            lives -= 1
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            if sound_hit:
                sound_hit.play()
            if lives <= 0:
                running = False

    # ------------------------------------------------------
    # MOVIMENTO DOS POWERUPS
    # ------------------------------------------------------
    for power in missil_powerups[:]:
        power.y += meteor_speed

        if power.colliderect(player_rect):
            has_missil_power = True
            missil_powerups.remove(power)

            # ❗ Ativa timer de 10 segundos
            missil_time_left = 10
            missil_end_time = pygame.time.get_ticks() + 10000

        elif power.y > HEIGHT:
            missil_powerups.remove(power)

    # ------------------------------------------------------
    # MOVIMENTO DO METEORO DE VIDA
    # ------------------------------------------------------

    for lm in life_meteor_list[:]:
        lm.y += meteor_speed

        if lm.y > HEIGHT:
            life_meteor_list.remove(lm)

        # Colisão com meteoro de vida → ganha 1 vida
        if lm.colliderect(player_rect):
            lives += 1
            if sound_life:
                sound_life.play()
            life_meteor_list.remove(lm)

    # ------------------------------------------------------
    # DISPARO AUTOMÁTICO DE MÍSSIL
    # ------------------------------------------------------
    if has_missil_power:
        missil_timer += 1
        if missil_timer > 20:  # dispara a cada 20 frames
            missil_rect = missil_img.get_rect(midbottom=player_rect.midtop)
            active_missils.append(missil_rect)
            missil_timer = 0

        # atualiza contagem regressiva
        now = pygame.time.get_ticks()
        missil_time_left = max(0, (missil_end_time - now) // 1000)

        # terminou o poder
        if missil_time_left <= 0:
            has_missil_power = False
            active_missils.clear()

    # ------------------------------------------------------
    # MOVIMENTO DOS MÍSSEIS
    # ------------------------------------------------------
    for m in active_missils[:]:
        m.y -= missil_speed

        if m.y < -30:
            active_missils.remove(m)
        else:
            for meteor in meteor_list:
                if m.colliderect(meteor):
                    meteor.y = random.randint(-100, -40)
                    meteor.x = random.randint(0, WIDTH - meteor.width)
                    active_missils.remove(m)
                    if sound_point:
                        sound_point.play()
                    break

    # ------------------------------------------------------
    # DESENHO DOS ELEMENTOS
    # ------------------------------------------------------

    # --- Desenha tudo ---
    screen.blit(player_img, player_rect)

    for meteor in meteor_list:
        screen.blit(meteor_img, meteor)

    for lm in life_meteor_list:
        screen.blit(life_meteor_img, lm)

    # --- Exibe pontuação e vidas ---
    for power in missil_powerups:
        screen.blit(missil_img, power)

    for m in active_missils:
        screen.blit(missil_img, m)

    # HUD (pontuação e vidas)
    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(text, (10, 10))

    # Timer do míssil (canto superior direito)
    if has_missil_power:
        timer_txt = font.render(f"{missil_time_left}s", True, (255, 255, 0))
        screen.blit(timer_txt, (WIDTH - 60, 10))

    pygame.display.flip()

# ----------------------------------------------------------
# 🏁 TELA DE FIM DE JOGO
# ----------------------------------------------------------
pygame.mixer.music.stop()
screen.fill((20, 20, 20))
end_text = font.render("Fim de jogo! Pressione qualquer tecla para sair.", True, WHITE)
final_score = font.render(f"Pontuação final: {score}", True, WHITE)
screen.blit(end_text, (150, 260))
screen.blit(final_score, (300, 300))
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
