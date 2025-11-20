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
import math

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
    "life_meteor": "meteoro_vidas_v2.png",  # imagem do meteoro de vidas
    "explosion": "explosao.png"  # imagem de explosao para meteoro
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
explosion_img = load_image(ASSETS["explosion"], YELLOW, (90, 90))

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
life_meteor_list = [] 
explosoes = []

meteor_speed = 5
missil_speed = 10

score = 0
lives = 3
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()
running = True

# 🎮 Sistema de Dificuldade Progressiva
difficulty_level = 1
next_level_score = 20
growth_factor = 2
level_up_message = ""
level_up_timer = 0   # tempo que a mensagem fica na tela (em frames)
# 🎮 Sistema de Menu Principal
game_state = "MENU"  # pode ser: "MENU", "PLAYING", "PAUSED", "GAME_OVER"
menu_font_large = pygame.font.Font(None, 72)
menu_font_medium = pygame.font.Font(None, 48)
menu_font_small = pygame.font.Font(None, 32)

# Opções do menu
menu_options = ["Jogar", "Sair"]
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
# 🟢 ADDED STATISTICS (não altera lógica do jogo, só registra dados)
# ----------------------------------------------------------
total_meteors_spawned = 0
powerups_collected = 0
missiles_fired = 0
missiles_hit = 0
lives_lost = 0
start_time_ticks = None
# ----------------------------------------------------------

# ----------------------------------------------------------
# 🎮 FUNÇÕES DO MENU
# ----------------------------------------------------------
# 🎮 Função para desenhar o menu principal
def draw_menu(screen, selected):
    screen.blit(background, (0, 0))
    
    # Título do jogo
    title = menu_font_large.render("SPACE ESCAPE", True, MENU_YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 150))
    screen.blit(title, title_rect)
    
    # Subtítulo
    subtitle = menu_font_small.render("Desvie dos meteoros!", True, MENU_WHITE)
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 220))
    screen.blit(subtitle, subtitle_rect)
    
    # Opções do menu
    for i, option in enumerate(menu_options):
        if i == selected:
            color = MENU_YELLOW
            text = menu_font_medium.render(f"> {option} <", True, color)
        else:
            color = MENU_GRAY
            text = menu_font_medium.render(option, True, color)
        
        text_rect = text.get_rect(center=(WIDTH // 2, 320 + i * 70))
        screen.blit(text, text_rect)
    
    # Instruções na parte inferior
    instructions = menu_font_small.render("Use as setas para navegar | ENTER para selecionar", True, MENU_WHITE)
    instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(instructions, instructions_rect)

# 🎮 Função para resetar o jogo
def reset_game():
    global score, lives, meteor_list, missil_powerups, active_missils, life_meteor_list, explosoes
    global has_missil_power, missil_timer, missil_time_left, missil_end_time
    global player_rect, meteor_speed, difficulty_level, next_level_score, level_up_message, level_up_timer, growth_factor
    global total_meteors_spawned, powerups_collected, missiles_fired, missiles_hit, lives_lost, start_time_ticks

    # Reseta variáveis
    score = 0
    lives = 3
    meteor_speed = 5
    difficulty_level = 1
    next_level_score = 20
    growth_factor = 2
    level_up_message = ""
    level_up_timer = 0
    
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
        total_meteors_spawned += 1  # ADDED: conta meteoros gerados inicialmente
    
    # Reseta power-ups
    has_missil_power = False
    missil_timer = 0
    missil_time_left = 0
    missil_end_time = 0
    
    # Reseta estatísticas
    powerups_collected = 0
    missiles_fired = 0
    missiles_hit = 0
    lives_lost = 0
    # marca tempo de início
    start_time_ticks = pygame.time.get_ticks()
    
   # Reinicia música
    if os.path.exists(ASSETS["music"]):
        pygame.mixer.music.play(-1)
# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
jogo_rodando = True  # ← MUDANÇA: Loop externo para permitir reiniciar

while jogo_rodando:  # ← MUDANÇA: while jogo_rodando
    
    # ← MUDANÇA: Reseta o jogo
    reset_game()
    
    running = True  # ← MUDANÇA: running dentro do loop externo
    
    while running:
        clock.tick(FPS)

        # --- Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                jogo_rodando = False  # ← MUDANÇA: Sai dos dois loops
            
            # 🎮 ADIÇÃO: Eventos do Menu
            if game_state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Jogar
                            # NÃO cria meteoros aqui - reset_game() já fez isso!
                            game_state = "PLAYING"
                            # marca tempo de início quando começar a jogar
                            start_time_ticks = pygame.time.get_ticks()
                        elif selected_option == 1:  # Sair
                            running = False
                            jogo_rodando = False  # ← MUDANÇA: Sai dos dois loops
        
        # 🎮 ADIÇÃO: Renderiza Menu
        if game_state == "MENU":
            draw_menu(screen, selected_option)
            pygame.display.flip()
            continue

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
                # ADDED: score reflete meteoros evitados (mantido)
                if sound_point:
                    sound_point.play()
                
                # 🎮 Sistema de Dificuldade Progressiva
                if score >= next_level_score:
                    difficulty_level += 1
                    meteor_speed += 0.75  # aumenta velocidade dos meteoros
                    level_up_message = f"Subiu de Nível: {difficulty_level}!"
                    level_up_timer = 120  # deixa mensagem por 120 frames (~2 segundos)
                    next_level_score = int(next_level_score * growth_factor)
                    if difficulty_level % 2 == 0:
                        new_meteor_x = random.randint(0, WIDTH - 40)
                        new_meteor_y = random.randint(-300, -40)
                        meteor_list.append(pygame.Rect(new_meteor_x, new_meteor_y, 40, 40))
                        total_meteors_spawned += 1  # ADDED: conta meteoros criados por level-up


            # colisão com nave
            if meteor.colliderect(player_rect):
                lives -= 1
                lives_lost += 1  # ADDED: conta vidas perdidas
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

                powerups_collected += 1  # ADDED: conta powerups coletados

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
                missiles_fired += 1  # ADDED: conta mísseis disparados

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
                        explosoes.append({
                            "img": explosion_img,
                            "rect": explosion_img.get_rect(center=meteor.center),
                            "timer": 5
                        })
                        meteor.y = random.randint(-100, -40)
                        meteor.x = random.randint(0, WIDTH - meteor.width)
                        active_missils.remove(m)
                        missiles_hit += 1  # ADDED: conta acertos de mísseis
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
        
        # Mostra o nível atual
        level_text = font.render(f"Nível: {difficulty_level}", True, WHITE)
        screen.blit(level_text, (10, 50))

        # Timer do míssil (canto superior direito)
        if has_missil_power:
            timer_txt = font.render(f"{missil_time_left}s", True, (255, 255, 0))
            screen.blit(timer_txt, (WIDTH - 60, 10))

        # Mensagem de Level Up
        if level_up_timer > 0:
            msg = font.render(level_up_message, True, (255, 255, 0))
            msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            screen.blit(msg, msg_rect)
            level_up_timer -= 1

        # Explosões temporárias
        for ex in explosoes[:]:
            screen.blit(ex["img"], ex["rect"])
            ex["timer"] -= 1
            if ex["timer"] <= 0:
                explosoes.remove(ex)

        pygame.display.flip()

    # ----------------------------------------------------------
    # 🏁 TELA DE FIM DE JOGO (AGORA COM ESTATÍSTICAS E REINICIAR)
    # ----------------------------------------------------------
    if jogo_rodando:  # ← MUDANÇA: Só mostra se não fechou a janela
        pygame.mixer.music.stop()
        
        # Calcula tempo de jogo
        if start_time_ticks is None:
            play_seconds = 0
        else:
            play_seconds = max(0, (pygame.time.get_ticks() - start_time_ticks) // 1000)
        
        selected_button = 0
        tela_final_ativa = True
        
        while tela_final_ativa:
            screen.blit(background, (0, 0))
            
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # GAME OVER
            game_over_text = menu_font_large.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, 60))
            screen.blit(game_over_text, game_over_rect)
            
            # Score e nível
            score_text = menu_font_medium.render(f"Score: {score}", True, YELLOW)
            score_rect = score_text.get_rect(center=(WIDTH // 2, 130))
            screen.blit(score_text, score_rect)
            
            level_text = menu_font_small.render(f"Nível: {difficulty_level}", True, WHITE)
            level_rect = level_text.get_rect(center=(WIDTH // 2, 170))
            screen.blit(level_text, level_rect)
            
            # Estatísticas
            stats_y = 210
            stat_lines = [
                f"--- Estatísticas ---",
                f"Meteoros gerados: {total_meteors_spawned}",
                f"Power-ups coletados: {powerups_collected}",
                f"Mísseis disparados: {missiles_fired}",
                f"Mísseis acertados: {missiles_hit}",
                f"Vidas perdidas: {lives_lost}",
                f"Tempo: {play_seconds}s"
            ]
            for i, line in enumerate(stat_lines):
                txt = small_font.render(line, True, WHITE)
                txt_rect = txt.get_rect(center=(WIDTH // 2, stats_y + i * 22))
                screen.blit(txt, txt_rect)
            
            # Botões
            button_y_start = 420
            
            if selected_button == 0:
                restart_text = menu_font_medium.render("> REINICIAR <", True, YELLOW)
            else:
                restart_text = menu_font_medium.render("REINICIAR", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, button_y_start))
            screen.blit(restart_text, restart_rect)
            
            if selected_button == 1:
                exit_text = menu_font_medium.render("> SAIR <", True, YELLOW)
            else:
                exit_text = menu_font_medium.render("SAIR", True, WHITE)
            exit_rect = exit_text.get_rect(center=(WIDTH // 2, button_y_start + 60))
            screen.blit(exit_text, exit_rect)
               
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tela_final_ativa = False
                    jogo_rodando = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_button = (selected_button - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        selected_button = (selected_button + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if selected_button == 0:  # Reiniciar
                            tela_final_ativa = False
                            game_state = "PLAYING"  # Começa o jogo direto!
                            
                        elif selected_button == 1:  # Sair
                            tela_final_ativa = False
                            jogo_rodando = False
            
            clock.tick(FPS)

pygame.quit()