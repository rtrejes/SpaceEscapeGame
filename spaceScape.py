##############################################################
###               S P A C E     E S C A P E                ###
###                     v0.4 - Menu                        ###
##############################################################

import pygame
import random
import os

pygame.init()

# ----------------------------------------------------------
# CONFIGURAÇÕES GERAIS
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ----------------------------------------------------------
# CORES E FONTES
# ----------------------------------------------------------
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)
BLUE = (80, 120, 255)
RED = (255, 80, 80)

font_title = pygame.font.Font(None, 74)
font_button = pygame.font.Font(None, 50)
font_info = pygame.font.Font(None, 32)

# ----------------------------------------------------------
# FUNÇÃO AUXILIAR PARA CARREGAR IMAGENS
# ----------------------------------------------------------
def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    else:
        surf = pygame.Surface(size or (50, 50))
        surf.fill(fallback_color)
        return surf

# ----------------------------------------------------------
# ASSETS
# ----------------------------------------------------------
ASSETS = {
    "background": "fundo_espacial.png",
    "player": "nave001.png",
    "meteor": "meteoro001.png",
}

background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))

# ----------------------------------------------------------
# FUNÇÃO: MENU INICIAL
# ----------------------------------------------------------
def show_menu():
    menu_running = True
    while menu_running:
        screen.fill(DARK_GRAY)
        title_text = font_title.render("🚀 Space Escape", True, WHITE)
        play_text = font_button.render("▶ Jogar", True, WHITE)
        quit_text = font_button.render("❌ Sair", True, WHITE)
        info_text = font_info.render("Use as setas para mover a nave e evite os meteoros!", True, GRAY)

        title_rect = title_text.get_rect(center=(WIDTH // 2, 180))
        play_rect = play_text.get_rect(center=(WIDTH // 2, 320))
        quit_rect = quit_text.get_rect(center=(WIDTH // 2, 400))
        info_rect = info_text.get_rect(center=(WIDTH // 2, 500))

        screen.blit(title_text, title_rect)
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)
        screen.blit(info_text, info_rect)

        # Detecta cliques do mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Destacar botão ao passar o mouse
        if play_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BLUE, play_rect.inflate(20, 10), 2)
            if mouse_click:
                menu_running = False
        elif quit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, RED, quit_rect.inflate(20, 10), 2)
            if mouse_click:
                pygame.quit()
                exit()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        clock.tick(30)

# ----------------------------------------------------------
# FUNÇÃO PRINCIPAL DO JOGO
# ----------------------------------------------------------
def run_game():
    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    player_speed = 7

    meteor_list = [pygame.Rect(random.randint(0, WIDTH - 40), random.randint(-500, -40), 40, 40) for _ in range(5)]
    meteor_speed = 5
    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimento do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect.y += player_speed

        # Movimento dos meteoros
        for meteor in meteor_list:
            meteor.y += meteor_speed
            if meteor.y > HEIGHT:
                meteor.y = random.randint(-100, -40)
                meteor.x = random.randint(0, WIDTH - meteor.width)
                score += 1
            if meteor.colliderect(player_rect):
                lives -= 1
                meteor.y = random.randint(-100, -40)
                meteor.x = random.randint(0, WIDTH - meteor.width)
                if lives <= 0:
                    running = False

        # Desenho
        screen.blit(player_img, player_rect)
        for meteor in meteor_list:
            screen.blit(meteor_img, meteor)

        # Pontos e vidas
        text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()

    # Fim de jogo
    game_over(font, score)


# ----------------------------------------------------------
# TELA DE FIM DE JOGO
# ----------------------------------------------------------
def game_over(font, score):
    screen.fill((20, 20, 20))
    end_text = font.render("Fim de jogo! Pressione qualquer tecla para voltar ao menu.", True, WHITE)
    final_score = font.render(f"Pontuação final: {score}", True, WHITE)
    screen.blit(end_text, (100, 260))
    screen.blit(final_score, (280, 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# ----------------------------------------------------------
# EXECUÇÃO
# ----------------------------------------------------------
show_menu()
run_game()
show_menu()
pygame.quit()
