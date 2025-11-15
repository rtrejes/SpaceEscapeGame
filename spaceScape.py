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
import json 
from datetime import datetime    

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
BLACK = (0, 0, 0)
DARK_BLUE = (20, 20, 60)
LIGHT_BLUE = (100, 150, 255)
GREEN = (60, 255, 60)

# Sistema de Leaderboard
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    """Carrega o leaderboard do arquivo JSON"""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_leaderboard(leaderboard):
    """Salva o leaderboard no arquivo JSON"""
    with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
        json.dump(leaderboard, f, indent=2, ensure_ascii=False)

def add_score_to_leaderboard(score, player_name="Jogador"):
    """Adiciona uma pontuação ao leaderboard e retorna a posição"""
    leaderboard = load_leaderboard()
    
    new_entry = {
        "name": player_name,
        "score": score,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    
    leaderboard.append(new_entry)
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    leaderboard = leaderboard[:5]
    
    save_leaderboard(leaderboard)
    
    for i, entry in enumerate(leaderboard):
        if entry == new_entry:
            return i + 1
    return None

def is_high_score(score):
    """Verifica se a pontuação entra no Top 5"""
    leaderboard = load_leaderboard()
    return len(leaderboard) < 5 or score > leaderboard[-1]["score"]

def draw_button(surface, text, x, y, w, h, color, hover_color, mouse_pos):
    """Desenha um botão e retorna True se o mouse está sobre ele"""
    button_rect = pygame.Rect(x, y, w, h)
    
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, button_rect, border_radius=10)
        is_hover = True
    else:
        pygame.draw.rect(surface, color, button_rect, border_radius=10)
        is_hover = False
    
    pygame.draw.rect(surface, WHITE, button_rect, 3, border_radius=10)
    
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)
    
    return is_hover

def menu_principal():
    """Menu principal do jogo"""
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)
    
    title_font = pygame.font.Font(None, 80)
    subtitle_font = pygame.font.Font(None, 30)
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(50)]
    
    while True:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        screen.fill(DARK_BLUE)
        for i, (x, y) in enumerate(stars):
            stars[i] = (x, (y + 1) % HEIGHT)
            size = random.randint(1, 3)
            pygame.draw.circle(screen, WHITE, (x, y), size)
        
        title = title_font.render("SPACE ESCAPE", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        subtitle = subtitle_font.render("Desvie dos meteoros e sobreviva!", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 160))
        screen.blit(subtitle, subtitle_rect)
        
        play_hover = draw_button(screen, "JOGAR", WIDTH//2 - 150, 250, 300, 60, BLUE, LIGHT_BLUE, mouse_pos)
        leaderboard_hover = draw_button(screen, "LEADERBOARD", WIDTH//2 - 150, 330, 300, 60, GREEN, (100, 255, 100), mouse_pos)
        quit_hover = draw_button(screen, "SAIR", WIDTH//2 - 150, 410, 300, 60, RED, (255, 100, 100), mouse_pos)
        
        controls_font = pygame.font.Font(None, 24)
        controls = controls_font.render("Use as SETAS para mover a nave", True, WHITE)
        controls_rect = controls.get_rect(center=(WIDTH // 2, 520))
        screen.blit(controls, controls_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_hover:
                    return "play"
                elif leaderboard_hover:
                    return "leaderboard"
                elif quit_hover:
                    return "quit"
        
        pygame.display.flip()

def tela_leaderboard():
    """Tela do leaderboard"""
    clock = pygame.time.Clock()
    leaderboard = load_leaderboard()
    
    title_font = pygame.font.Font(None, 70)
    entry_font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    while True:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        screen.blit(background, (0, 0))
        
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        title = title_font.render("🏆 TOP 5 🏆", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 60))
        screen.blit(title, title_rect)
        
        if leaderboard:
            y_start = 150
            for i, entry in enumerate(leaderboard):
                rank = i + 1
                color = YELLOW if rank == 1 else WHITE
                
                rank_text = entry_font.render(f"{rank}º", True, color)
                screen.blit(rank_text, (100, y_start + i * 70))
                
                name_text = entry_font.render(entry["name"], True, color)
                screen.blit(name_text, (180, y_start + i * 70))
                
                score_text = entry_font.render(f"{entry['score']} pts", True, color)
                screen.blit(score_text, (450, y_start + i * 70))
                
                date_text = small_font.render(entry["date"], True, color)
                screen.blit(date_text, (180, y_start + i * 70 + 35))
        else:
            no_scores = entry_font.render("Nenhuma pontuação registrada!", True, WHITE)
            no_scores_rect = no_scores.get_rect(center=(WIDTH // 2, 300))
            screen.blit(no_scores, no_scores_rect)
        
        back_hover = draw_button(screen, "VOLTAR", WIDTH//2 - 100, 500, 200, 50, BLUE, LIGHT_BLUE, mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_hover:
                    return "menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
        
        pygame.display.flip()

def tela_final(score):
    """Tela final com input de nome"""
    pygame.mixer.music.stop()
    
    clock = pygame.time.Clock()
    input_font = pygame.font.Font(None, 50)
    title_font = pygame.font.Font(None, 70)
    text_font = pygame.font.Font(None, 36)
    
    player_name = ""
    input_active = True
    ranking_position = None
    is_top5 = is_high_score(score)
    
    while True:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        screen.fill(DARK_BLUE)
        
        title = title_font.render("FIM DE JOGO!", True, RED if not is_top5 else YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        score_text = text_font.render(f"Pontuação: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 160))
        screen.blit(score_text, score_rect)
        
        if is_top5 and ranking_position is None:
            prompt = text_font.render("🎉 NOVO RECORDE! Digite seu nome:", True, GREEN)
            prompt_rect = prompt.get_rect(center=(WIDTH // 2, 240))
            screen.blit(prompt, prompt_rect)
            
            input_box = pygame.Rect(WIDTH // 2 - 200, 300, 400, 60)
            pygame.draw.rect(screen, WHITE, input_box, 3, border_radius=5)
            
            name_surface = input_font.render(player_name + "|" if input_active else player_name, True, WHITE)
            screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))
            
            hint = text_font.render("Pressione ENTER para salvar", True, LIGHT_BLUE)
            hint_rect = hint.get_rect(center=(WIDTH // 2, 390))
            screen.blit(hint, hint_rect)
        
        elif ranking_position:
            congrats = text_font.render(f"Você ficou em {ranking_position}º lugar!", True, YELLOW)
            congrats_rect = congrats.get_rect(center=(WIDTH // 2, 250))
            screen.blit(congrats, congrats_rect)
        
        y_buttons = 450 if ranking_position or not is_top5 else 500
        play_hover = draw_button(screen, "JOGAR NOVAMENTE", WIDTH//2 - 200, y_buttons, 180, 50, GREEN, (100, 255, 100), mouse_pos)
        menu_hover = draw_button(screen, "MENU", WIDTH//2 + 30, y_buttons, 180, 50, BLUE, LIGHT_BLUE, mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN:
                if is_top5 and ranking_position is None:
                    if event.key == pygame.K_RETURN and len(player_name) > 0:
                        ranking_position = add_score_to_leaderboard(score, player_name)
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif len(player_name) < 15 and event.unicode.isprintable():
                        player_name += event.unicode
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_hover and (ranking_position or not is_top5):
                    return "play"
                elif menu_hover and (ranking_position or not is_top5):
                    return "menu"
        
        pygame.display.flip()


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
missil_time_left = 0          # tempo restante do power
missil_end_time = 0           # momento em que acaba

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
# 🚀 SISTEMA DE NAVEGAÇÃO ENTRE TELAS
# ----------------------------------------------------------
def executar_jogo():
    """Executa o loop principal do jogo e retorna (próxima_tela, pontuação)"""
    # 🆕 Esta função ENCAPSULA todo o loop do jogo que já existe
    # MAS NÃO MUDA NADA da lógica interna!
    
    # Reinicia as variáveis locais do jogo
    local_player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    local_player_speed = 7
    
    local_meteor_list = []
    local_missil_powerups = []
    local_active_missils = []
    local_life_meteor_list = []
    
    for _ in range(5):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-500, -40)
        local_meteor_list.append(pygame.Rect(x, y, 40, 40))
    
    local_meteor_speed = 5
    local_missil_speed = 10
    
    local_score = 0
    local_lives = 3
    local_font = pygame.font.Font(None, 36)
    local_clock = pygame.time.Clock()
    local_running = True
    
    local_has_missil_power = False
    local_missil_timer = 0
    local_missil_time_left = 0
    local_missil_end_time = 0
    
    pygame.mixer.music.play(-1)
    
    # Loop do jogo (EXATAMENTE igual ao original)
    while local_running:
        local_clock.tick(FPS)
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", local_score
            # 🆕 Adiciona ESC para voltar ao menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu", local_score
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and local_player_rect.left > 0:
            local_player_rect.x -= local_player_speed
        if keys[pygame.K_RIGHT] and local_player_rect.right < WIDTH:
            local_player_rect.x += local_player_speed
        if keys[pygame.K_UP] and local_player_rect.top > 0:
            local_player_rect.y -= local_player_speed
        if keys[pygame.K_DOWN] and local_player_rect.bottom < HEIGHT:
            local_player_rect.y += local_player_speed
        
        for meteor in local_meteor_list:
            meteor.y += local_meteor_speed
            
            if meteor.y > HEIGHT:
                meteor.y = random.randint(-100, -40)
                meteor.x = random.randint(0, WIDTH - meteor.width)
                
                if random.random() < 0.1:
                    if random.random() < 0.5:
                        px = random.randint(0, WIDTH - missil_powerup_img.get_width())
                        py = random.randint(-300, -50)
                        powerup_rect = missil_powerup_img.get_rect(topleft=(px, py))
                        local_missil_powerups.append(powerup_rect)
                    else:
                        lx = random.randint(0, WIDTH - 40)
                        ly = random.randint(-300, -40)
                        local_life_meteor_list.append(pygame.Rect(lx, ly, 40, 40))
                
                local_score += 1
                if sound_point:
                    sound_point.play()
            
            if meteor.colliderect(local_player_rect):
                local_lives -= 1
                meteor.y = random.randint(-100, -40)
                meteor.x = random.randint(0, WIDTH - meteor.width)
                if sound_hit:
                    sound_hit.play()
                if local_lives <= 0:
                    local_running = False
        
        for power in local_missil_powerups[:]:
            power.y += local_meteor_speed
            
            if power.colliderect(local_player_rect):
                local_has_missil_power = True
                local_missil_powerups.remove(power)
                local_missil_time_left = 10
                local_missil_end_time = pygame.time.get_ticks() + 10000
            elif power.y > HEIGHT:
                local_missil_powerups.remove(power)
        
        for lm in local_life_meteor_list[:]:
            lm.y += local_meteor_speed
            
            if lm.y > HEIGHT:
                local_life_meteor_list.remove(lm)
            
            if lm.colliderect(local_player_rect):
                local_lives += 1
                if sound_life:
                    sound_life.play()
                local_life_meteor_list.remove(lm)
        
        if local_has_missil_power:
            local_missil_timer += 1
            if local_missil_timer > 10:
                missil_rect = missil_shot_img.get_rect(midbottom=local_player_rect.midtop)
                local_active_missils.append(missil_rect)
                local_missil_timer = 0
            
            now = pygame.time.get_ticks()
            local_missil_time_left = max(0, (local_missil_end_time - now) // 1000)
            
            if local_missil_time_left <= 0:
                local_has_missil_power = False
                local_active_missils.clear()
        
        for m in local_active_missils[:]:
            m.y -= local_missil_speed
            
            if m.y < -30:
                local_active_missils.remove(m)
            else:
                for meteor in local_meteor_list:
                    if m.colliderect(meteor):
                        meteor.y = random.randint(-100, -40)
                        meteor.x = random.randint(0, WIDTH - meteor.width)
                        local_active_missils.remove(m)
                        if sound_point:
                            sound_point.play()
                        break
        
        screen.blit(player_img, local_player_rect)
        
        for meteor in local_meteor_list:
            screen.blit(meteor_img, meteor)
        
        for lm in local_life_meteor_list:
            screen.blit(life_meteor_img, lm)
        
        for power in local_missil_powerups:
            screen.blit(missil_powerup_img, power)
        
        for m in local_active_missils:
            screen.blit(missil_shot_img, m)
        
        text = local_font.render(f"Pontos: {local_score}   Vidas: {local_lives}", True, WHITE)
        screen.blit(text, (10, 10))
        
        if local_has_missil_power:
            timer_txt = local_font.render(f"{local_missil_time_left}s", True, (255, 255, 0))
            screen.blit(timer_txt, (WIDTH - 60, 10))
        
        pygame.display.flip()
    
    return "gameover", local_score

# ----------------------------------------------------------
# 🎮 LOOP PRINCIPAL DE NAVEGAÇÃO
# ----------------------------------------------------------
def main():
    """Controla a navegação entre todas as telas"""
    current_screen = "menu"
    last_score = 0
    
    while True:
        if current_screen == "menu":
            current_screen = menu_principal()
        
        elif current_screen == "play":
            current_screen, last_score = executar_jogo()
        
        elif current_screen == "gameover":
            current_screen = tela_final(last_score)
        
        elif current_screen == "leaderboard":
            current_screen = tela_leaderboard()
        
        elif current_screen == "quit":
            break
    
    pygame.quit()

# Inicia o programa
if __name__ == "__main__":
    main()
