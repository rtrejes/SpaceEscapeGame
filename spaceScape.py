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
missil_powerup_img = load_image(ASSETS["missil"], YELLOW, (40,40))
missil_shot_img = load_image(ASSETS["missil"], YELLOW, (30, 40))
life_meteor_img = load_image(ASSETS["life_meteor"], PINK, (55, 75))

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
life_meteor_list = []   # meteoro especial que dá vida

meteor_speed = 5
missil_speed = 10

score = 0
lives = 3
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

# 🎮 Sistema de Menu Principal
game_state = "MENU"  # pode ser: "MENU", "PLAYING", "PAUSED", "GAME_OVER"
menu_font_large = pygame.font.Font(None, 72)
menu_font_medium = pygame.font.Font(None, 48)
menu_font_small = pygame.font.Font(None, 32)

# Opções do menu
menu_options = ["Jogar", "Controles", "Sair"]
selected_option = 0

# Cores do menu
MENU_WHITE = (255, 255, 255)
MENU_YELLOW = (255, 220, 0)
MENU_GRAY = (150, 150, 150)

has_missil_power = False
missil_timer = 0
missil_time_left = 0          # tempo restante do power
missil_end_time = 0           # momento em que acaba

# ----------------------------------------------------------
# 🎮 FUNÇÕES DO MENU
# ----------------------------------------------------------
# 🎮 Função para desenhar o menu principal
def draw_menu(screen, selected):
    screen.blit(background, (0, 0))
    
    # Título do jogo
    title = menu_font_large.render("SPACE ESCAPE", True, MENU_YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title, title_rect)
    
    # Subtítulo
    subtitle = menu_font_small.render("Desvie dos meteoros!", True, MENU_WHITE)
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 160))
    screen.blit(subtitle, subtitle_rect)
    
    # Opções do menu
    for i, option in enumerate(menu_options):
        if i == selected:
            color = MENU_YELLOW
            text = menu_font_medium.render(f"> {option} <", True, color)
        else:
            color = MENU_GRAY
            text = menu_font_medium.render(option, True, color)
        
        text_rect = text.get_rect(center=(WIDTH // 2, 280 + i * 70))
        screen.blit(text, text_rect)
    
    # Instruções na parte inferior
    instructions = menu_font_small.render("Use ↑↓ para navegar | ENTER para selecionar", True, MENU_WHITE)
    instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(instructions, instructions_rect)

# 🎮 Função para desenhar tela de controles
def draw_controls(screen):
    screen.blit(background, (0, 0))
    
    # Título
    title = menu_font_large.render("CONTROLES", True, MENU_YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title, title_rect)
    
    # Controles
    controls_text = [
        "← → ↑ ↓  -  Mover a nave",
        "",
        "OBJETIVO:",
        "Desvie dos meteoros vermelhos",
        "Colete power-ups amarelos",
        "Colete meteoros de vida (rosa)",
        "",
        "DICAS:",
        "• Power-ups dão disparo automático por 10s",
        "• A dificuldade aumenta com o tempo",
        "• Cada colisão tira uma vida"
    ]
    
    y_position = 180
    for line in controls_text:
        if line == "":
            y_position += 20
        else:
            if line in ["OBJETIVO:", "DICAS:"]:
                text = menu_font_medium.render(line, True, MENU_YELLOW)
            else:
                text = menu_font_small.render(line, True, MENU_WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, y_position))
            screen.blit(text, text_rect)
            y_position += 40
    
    # Voltar
    back_text = menu_font_small.render("Pressione ESC para voltar", True, MENU_YELLOW)
    back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(back_text, back_rect)

# 🎮 Função para resetar o jogo
def reset_game():
    global score, lives, meteor_list, missil_powerups, active_missils, life_meteor_list
    global has_missil_power, missil_timer, missil_time_left, missil_end_time
    global player_rect, meteor_speed
    
    # Reseta variáveis
    score = 0
    lives = 3
    meteor_speed = 5
    
    # Reseta posição do jogador
    player_rect.center = (WIDTH // 2, HEIGHT - 60)
    
    # Limpa listas
    meteor_list.clear()
    missil_powerups.clear()
    active_missils.clear()
    life_meteor_list.clear()
    
    # Recria meteoros iniciais
    for _ in range(5):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-500, -40)
        meteor_list.append(pygame.Rect(x, y, 40, 40))
    
    # Reseta power-ups
    has_missil_power = False
    missil_timer = 0
    missil_time_left = 0
    missil_end_time = 0
    
   # Reinicia música
    if os.path.exists(ASSETS["music"]):
        pygame.mixer.music.play(-1)
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
    
    # 🎮 EVENTOS DO MENU
        if game_state == "MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Jogar
                        reset_game()
                        game_state = "PLAYING"
                    elif selected_option == 1:  # Controles
                        game_state = "CONTROLS"
                    elif selected_option == 2:  # Sair
                        running = False
    
    # 🎮 EVENTOS DURANTE O JOGO
        elif game_state == "PLAYING":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "PAUSED"
        
    # 🎮 EVENTOS DO PAUSE
        elif game_state == "PAUSED":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "PLAYING"
                elif event.key == pygame.K_m:
                    game_state = "MENU"
        
    # 🎮 EVENTOS DO GAME OVER
        elif game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = "PLAYING"
                elif event.key == pygame.K_m:
                    game_state = "MENU"
    # ========================================
    # 🎮 RENDERIZAÇÃO BASEADA NO ESTADO
    # ========================================
    
    if game_state == "MENU":
        draw_menu(screen, selected_option)
    
    elif game_state == "CONTROLS":
        draw_controls(screen)
    
    elif game_state == "PAUSED":
        # Desenha o jogo congelado
        screen.blit(background, (0, 0))
        screen.blit(player_img, player_rect)
        for meteor in meteor_list:
            screen.blit(meteor_img, meteor)
        for lm in life_meteor_list:
            screen.blit(life_meteor_img, lm)
        for power in missil_powerups:
            screen.blit(missil_powerup_img, power)
        for m in active_missils:
            screen.blit(missil_shot_img, m)
        
        # HUD durante pause
        text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
        screen.blit(text, (10, 10))
        if has_missil_power:
            timer_txt = font.render(f"{missil_time_left}s", True, (255, 255, 0))
            screen.blit(timer_txt, (WIDTH - 60, 10))
        
        # Overlay de pausa
        pause_overlay = pygame.Surface((WIDTH, HEIGHT))
        pause_overlay.set_alpha(128)
        pause_overlay.fill((0, 0, 0))
        screen.blit(pause_overlay, (0, 0))
        
        pause_text = menu_font_large.render("PAUSADO", True, MENU_YELLOW)
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(pause_text, pause_rect)
        
        resume_text = menu_font_small.render("ESC - Continuar | M - Menu", True, MENU_WHITE)
        resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(resume_text, resume_rect)
    
    elif game_state == "GAME_OVER":
        screen.fill((20, 20, 20))
        
        game_over_text = menu_font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(game_over_text, game_over_rect)
        
        final_score_text = menu_font_medium.render(f"Pontuação: {score}", True, MENU_WHITE)
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(final_score_text, final_score_rect)
        
        restart_text = menu_font_small.render("ENTER - Jogar Novamente | M - Menu", True, MENU_YELLOW)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        screen.blit(restart_text, restart_rect)
    
    elif game_state == "PLAYING":
        screen.blit(background, (0, 0))    

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
                    px = random.randint(0, WIDTH - missil_powerup_img.get_width())
                    py = random.randint(-300, -50)
                    powerup_rect = missil_powerup_img.get_rect(topleft=(px, py))

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
        if missil_timer > 10:  # dispara a cada 20 frames
            missil_rect = missil_shot_img.get_rect(midbottom=player_rect.midtop)
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
        screen.blit(missil_powerup_img, power)

    for m in active_missils:
        screen.blit(missil_shot_img, m)

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
