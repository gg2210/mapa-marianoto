import pygame
import sys
import math
import random
import os


# Configurações principais
VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 960, 540  # Resolução virtual (fixa)

# Inicializar pygame
pygame.init()

# Obter informações da tela do dispositivo
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# Calcular ratio de escala
SCALE_RATIO = min(SCREEN_WIDTH / VIRTUAL_WIDTH, SCREEN_HEIGHT / VIRTUAL_HEIGHT)
SCALED_WIDTH = int(VIRTUAL_WIDTH * SCALE_RATIO)
SCALED_HEIGHT = int(VIRTUAL_HEIGHT * SCALE_RATIO)

# Criar a tela real e a superfície virtual
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

# Ajustar posição para centralizar
OFFSET_X = (SCREEN_WIDTH - SCALED_WIDTH) // 2
OFFSET_Y = (SCREEN_HEIGHT - SCALED_HEIGHT) // 2

pygame.display.set_caption("Mapa do Marianoto")
clock = pygame.time.Clock()
FPS = 60

# ----------------------------
# CORES
GREEN = (34, 139, 34)
DARK_GREEN = (16, 90, 16)
BROWN = (139, 69, 19)
DARK_BROWN = (100, 50, 10)
YELLOW = (255, 215, 0)
GRAY = (110, 110, 110)
LIGHT_GRAY = (190, 190, 190)
RED = (220, 48, 48)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)
PURPLE = (140, 0, 200)
SAND = (237, 201, 175)
WATER = (64, 164, 223)
DARK_WATER = (35, 105, 155)
SKY_BLUE = (135, 206, 235)
BEIGE = (245, 222, 179)
WALL_COLOR = (240, 230, 210)
FLOOR_COLOR = (210, 180, 140)
ROOF_COLOR = (160, 82, 45)
LIGHT_PINK = (255, 209, 220)
DARK_PINK = (219, 112, 147)
STREET_COLOR = (100, 100, 100)
SIDEWALK_COLOR = (180, 180, 180)
LIGHT_BLUE = (173, 216, 230)
PINK = (255, 182, 193)

# ----------------------------
# FONTES
FONT_BIG = pygame.font.SysFont(None, 64)
FONT = pygame.font.SysFont(None, 34)
FONT_SM = pygame.font.SysFont(None, 24)
FONT_XS = pygame.font.SysFont(None, 18)

# ----------------------------
# VARIÁVEIS GLOBAIS
borders = []
water_zones = []
obstacles = []
enemies = []
paths = []
chest = None
keys_collected = 0
key_a_taken = False
key_b_taken = False
key_c_taken = False
puzzle_a_done = False
puzzle_b_done = False
puzzle_c_done = False
sequence_pressed = []
barrier_a = None
barrier_b = None
barrier_c = None
push_block = None
pressure_plate = None
buttons = []
sequence_needed = []
shells = []
palm_trees = []
center_zone = None
spawn_sign = None
spawn_sign_text = ""
sign_text = ""
invuln_timer = 0
enemy_speed = 1.6
current_level = 1
max_level = 4
key_a = None
key_b = None
key_c = None
attack_cooldown = 0
attack_range = 80
attack_angle = 0
player_speed = 4.0
attacking = False
moving = False
health = 5
max_health = 5
facing_right = True
last_direction = "right"

# Variáveis para controle de mensagens
msg_puzzle_a_shown = False
msg_puzzle_b_shown = False
msg_puzzle_c_shown = False

# Variáveis específicas do Capítulo 2 (Labirinto)
maze_walls = []
cards = []
cards_collected = 0
gift_hints = [
    "Para me achar, você precisa me procurar por trás da tela que mostra imagens e sons",
    "eu não estou em prateleiras nem gavetas, me aviste quando a porta fizer 'clec'",
    "convivo com facas colheres e garfos, mas não sou nenhum deles.",
    "para me encontrar você precisa olhar debaixo do lugar de onde dorme",
    "estou escondido atrás do seu reflexo",
    "fica num lugar onde guarda os sapatos",
    "fica debaixo de onde guarda os potes, pratos, comidas",
    "Fica dentro de onde assa as comidas"
]

# ----------------------------
# PLAYER / SPRITES
def load_img(path, fallback_color, size=(42, 42)):
    try:
        # No Android, as imagens estarão no diretório raiz
        from os.path import exists, join
        from android.storage import app_storage_path
        
        # Tenta carregar do diretório do app Android
        android_path = join(app_storage_path(), path)
        if exists(android_path):
            img = pygame.image.load(android_path).convert_alpha()
        elif exists(path):  # Para desenvolvimento
            img = pygame.image.load(path).convert_alpha()
        else:
            raise FileNotFoundError(f"Imagem não encontrada: {path}")
            
        return pygame.transform.scale(img, size)
    except Exception as e:
        print(f"Erro ao carregar {path}: {e}")
        # Fallback
        s = pygame.Surface(size, pygame.SRCALPHA)
        s.fill(fallback_color)
        pygame.draw.rect(s, BLACK, s.get_rect(), 2)
        return s

# Carregar imagens do jogador
player_idle = load_img("mari.png", (255, 0, 255))
player_walk_right = load_img("mari_walk.png", (0, 200, 0))
player_walk_left = pygame.transform.flip(player_walk_right, True, False)
player_walk_up = load_img("mari_up.png", (200, 200, 200))
player_walk_down = load_img("mari_down.png", (200, 200, 200))
player_attack = load_img("mari_attack.png", (255, 120, 255))
player_img = player_idle

# Carregar imagem do baú
chest_img = load_img("chest.png", (180, 120, 60), (64, 64))

player_rect = player_img.get_rect()
player_rect.center = (200, 200)

# CAMERA
cam_x, cam_y = 0, 0

# ----------------------------
# JOYSTICK VIRTUAL (HUD) - AUMENTADO para celular
joy_radius = 80  # Aumentado de 56 para 80
joy_center = (120, VIRTUAL_HEIGHT - 120)  # Ajustado para celular
joy_pos = joy_center
joy_active = False
joy_touch_id = None

# Botão de ataque - AUMENTADO para celular
attack_button = pygame.Rect(VIRTUAL_WIDTH - 140, VIRTUAL_HEIGHT - 140, 100, 100)  # Aumentado
attack_button_color = (200, 50, 50)
attack_button_active = False
attack_button_touch_id = None

# ----------------------------
# ESTADOS DO JOGO
STATE_TITLE = 0
STATE_GAME = 1
state = STATE_TITLE

# ----------------------------
# FUNÇÕES UTIL
def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def world_to_screen(rect):
    return pygame.Rect(rect.x - cam_x, rect.y - cam_y, rect.w, rect.h)

def draw_text_center(text, y, font=FONT, color=WHITE):
    surf = font.render(text, True, color)
    virtual_surface.blit(surf, (VIRTUAL_WIDTH // 2 - surf.get_width() // 2, y))

def draw_button(rect, label, color=YELLOW):
    pygame.draw.rect(virtual_surface, color, rect, border_radius=10)
    pygame.draw.rect(virtual_surface, BLACK, rect, 2, border_radius=10)
    txt = FONT.render(label, True, BLACK)
    virtual_surface.blit(txt, (rect.centerx - txt.get_width() // 2,
                      rect.centery - txt.get_height() // 2))

def draw_joystick():
    pygame.draw.circle(virtual_surface, (100, 100, 100, 150), joy_center, joy_radius)
    pygame.draw.circle(virtual_surface, (200, 200, 200, 200), joy_pos, 30)  # Aumentado
    pygame.draw.circle(virtual_surface, BLACK, joy_pos, 30, 2)  # Aumentado

def draw_attack_button():
    pygame.draw.circle(virtual_surface, attack_button_color, attack_button.center,
                       attack_button.width // 2)
    pygame.draw.circle(virtual_surface, BLACK, attack_button.center,
                       attack_button.width // 2, 2)
    atk_text = FONT_SM.render("ATK", True, WHITE)
    virtual_surface.blit(atk_text, (attack_button.centerx - atk_text.get_width() // 2,
                           attack_button.centery - atk_text.get_height() // 2))

def draw_hearts():
    for i in range(max_health):
        x = 16 + i * 28
        y = 12
        color = RED if i < health else GRAY
        pygame.draw.circle(virtual_surface, color, (x + 8, y + 10), 8)
        pygame.draw.circle(virtual_surface, color, (x + 20, y + 10), 8)
        points = [(x, y + 14), (x + 28, y + 14), (x + 14, y + 30)]
        pygame.draw.polygon(virtual_surface, color, points)
        pygame.draw.polygon(virtual_surface, BLACK, points, 1)

def draw_keys_ui():
    if current_level == 4:  # Capítulo 2 - mostrar contador de cartas
        card_text = FONT_SM.render(f"Cartas: {cards_collected}/8", True, WHITE)
        virtual_surface.blit(card_text, (VIRTUAL_WIDTH - card_text.get_width() - 16, 12))
    else:  # Outros níveis - mostrar contador de chaves
        keys_needed = 3 if current_level == 3 else 2
        ktxt = FONT_SM.render(f"Chaves: {int(keys_collected)}/{keys_needed}", True,
                              WHITE)
        virtual_surface.blit(ktxt, (VIRTUAL_WIDTH - ktxt.get_width() - 16, 12))

def block_collision_move(mover, dx, dy, solids):
    # Colisão em X
    mover.x += dx
    for s in solids:
        if mover.colliderect(s):
            if dx > 0:
                mover.right = s.left
            elif dx < 0:
                mover.left = s.right

    # Colisão em Y
    mover.y += dy
    for s in solids:
        if mover.colliderect(s):
            if dy > 0:
                mover.bottom = s.top
                return True  # Indica que está no chão
            elif dy < 0:
                mover.top = s.bottom
    return False  # Não está no chão

def show_message(text_lines, callback=None):
    overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    btn = pygame.Rect(VIRTUAL_WIDTH // 2 - 120, VIRTUAL_HEIGHT // 2 + 90, 240, 56)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Converter coordenadas da tela para coordenadas virtuais
                mx = (mx - OFFSET_X) / SCALE_RATIO
                my = (my - OFFSET_Y) / SCALE_RATIO
                if btn.collidepoint(mx, my):
                    if callback:
                        callback()
                    return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE or e.key == pygame.K_ESCAPE:
                    if callback:
                        callback()
                    return

        # Desenhar na superfície virtual
        virtual_surface.blit(overlay, (0, 0))
        pygame.draw.rect(virtual_surface,
                         LIGHT_GRAY,
                         (VIRTUAL_WIDTH // 2 - 320, VIRTUAL_HEIGHT // 2 - 140, 640, 300),
                         border_radius=14)
        pygame.draw.rect(virtual_surface,
                         WHITE,
                         (VIRTUAL_WIDTH // 2 - 320, VIRTUAL_HEIGHT // 2 - 140, 640, 300),
                         3,
                         border_radius=14)
        for i, line in enumerate(text_lines):
            draw_text_center(line, VIRTUAL_HEIGHT // 2 - 110 + i * 36, FONT, BLACK)

        cont_text = "CONTINUAR" if current_level != 4 or cards_collected < 8 else "VOLTAR AO MENU"
        pygame.draw.rect(virtual_surface, YELLOW, btn, border_radius=10)
        pygame.draw.rect(virtual_surface, BLACK, btn, 2, border_radius=10)
        txt = FONT.render(cont_text, True, BLACK)
        virtual_surface.blit(txt, (btn.centerx - txt.get_width() // 2,
                          btn.centery - txt.get_height() // 2))

        # Atualizar a tela real
        screen.blit(pygame.transform.scale(virtual_surface, (SCALED_WIDTH, SCALED_HEIGHT)), (OFFSET_X, OFFSET_Y))
        pygame.display.update()
        clock.tick(FPS)

# ----------------------------
# TELA DE TÍTULO
def title_screen():
    global state, current_level

    chapter1_btn = pygame.Rect(VIRTUAL_WIDTH // 2 - 140, VIRTUAL_HEIGHT // 2 - 20, 280, 64)
    chapter2_btn = pygame.Rect(VIRTUAL_WIDTH // 2 - 140, VIRTUAL_HEIGHT // 2 + 60, 280, 64)
    chapter2_locked = current_level < 4  # Desbloqueado após completar Capítulo 1

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Converter coordenadas da tela para coordenadas virtuais
                mx = (mx - OFFSET_X) / SCALE_RATIO
                my = (my - OFFSET_Y) / SCALE_RATIO

                if chapter1_btn.collidepoint(mx, my):
                    current_level = 1
                    setup_level(current_level)
                    state = STATE_GAME
                    running = False
                if not chapter2_locked and chapter2_btn.collidepoint(mx, my):
                    current_level = 4
                    setup_level(current_level)
                    state = STATE_GAME
                    running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    current_level = 1
                    setup_level(current_level)
                    state = STATE_GAME
                    running = False
                elif e.key == pygame.K_2 and not chapter2_locked:
                    current_level = 4
                    setup_level(current_level)
                    state = STATE_GAME
                    running = False

        virtual_surface.fill(DARK_GREEN)
        draw_text_center("Mapa do Marianoto", 60, FONT_BIG, WHITE)

        # Capítulo 1
        draw_text_center("Capítulo 1: Aventura na Natureza", 150, FONT,
                         (0, 255, 120))
        draw_button(chapter1_btn, "JOGAR CAPÍTULO 1")

        # Capítulo 2
        draw_text_center("Capítulo 2: O Labirinto de Cartas", 230, FONT,
                         (0, 200, 255) if not chapter2_locked else GRAY)
        if chapter2_locked:
            pygame.draw.rect(virtual_surface, (100, 100, 100, 150),
                             chapter2_btn,
                             border_radius=10)
            pygame.draw.rect(virtual_surface, BLACK, chapter2_btn, 2, border_radius=10)
            lock_text = FONT.render("BLOQUEADO", True, BLACK)
            virtual_surface.blit(lock_text,
                        (chapter2_btn.centerx - lock_text.get_width() // 2,
                         chapter2_btn.centery - lock_text.get_height() // 2))
        else:
            draw_button(chapter2_btn, "JOGAR CAPÍTULO 2")

        draw_text_center("Pressione 1 ou 2 para selecionar a fase", 400,
                         FONT_SM, WHITE)

        # Atualizar a tela real
        screen.blit(pygame.transform.scale(virtual_surface, (SCALED_WIDTH, SCALED_HEIGHT)), (OFFSET_X, OFFSET_Y))
        pygame.display.update()
        clock.tick(FPS)

# ----------------------------
# CONFIGURAÇÃO DOS NÍVEIS
def setup_level(level):
    global borders, obstacles, center_zone, chest, keys_collected
    global key_a_taken, key_b_taken, key_c_taken, push_block, pressure_plate
    global puzzle_a_done, puzzle_b_done, puzzle_c_done, sequence_pressed, enemies, paths
    global spawn_sign, spawn_sign_text, sign_text, water_zones, palm_trees
    global shells, enemy_speed, player_rect, health, invuln_timer
    global key_a, key_b, key_c, barrier_a, barrier_b, barrier_c
    global msg_puzzle_a_shown, msg_puzzle_b_shown, msg_puzzle_c_shown
    global buttons, sequence_needed, current_level, WORLD_W, WORLD_H
    global maze_walls, cards, cards_collected

    # Resetar variáveis
    keys_collected = 0
    key_a_taken = False
    key_b_taken = False
    key_c_taken = False
    puzzle_a_done = False
    puzzle_b_done = False
    puzzle_c_done = False
    sequence_pressed = []
    health = max_health
    invuln_timer = 0
    msg_puzzle_a_shown = False
    msg_puzzle_b_shown = False
    msg_puzzle_c_shown = False
    cards_collected = 0
    maze_walls = []
    cards = []

    if level == 1:
        # FASE 1: FLORESTA
        WORLD_W, WORLD_H = 2400, 1800
        borders = [
            pygame.Rect(0, 0, WORLD_W, 24),
            pygame.Rect(0, WORLD_H - 24, WORLD_W, 24),
            pygame.Rect(0, 0, 24, WORLD_H),
            pygame.Rect(WORLD_W - 24, 0, 24, WORLD_H),
        ]

        water_zones = []
        obstacles = []
        palm_trees = []
        shells = []

        # Árvores
        random.seed(7)
        for _ in range(80):
            x = random.randrange(100, WORLD_W - 150)
            y = random.randrange(100, WORLD_H - 150)
            w = random.choice([42, 48, 56])
            h = random.choice([42, 48, 56])
            obstacles.append(pygame.Rect(x, y, w, h))

        # Centro
        center_zone = pygame.Rect(WORLD_W // 2 - 260, WORLD_H // 2 - 200, 520,
                                  400)
        obstacles = [
            r for r in obstacles
            if not r.colliderect(center_zone.inflate(-40, -40))
        ]

        # Baú
        chest = pygame.Rect(WORLD_W // 2 - 32, WORLD_H // 2 - 32, 64, 64)
        sign_text = "Precisa de 2 chaves."
        spawn_sign = pygame.Rect(120, 140, 160, 40)
        spawn_sign_text = "Centro → Baú com Dica"

        # Chaves
        key_a = pygame.Rect(WORLD_W // 2 - 520, WORLD_H // 2 - 160, 28, 28)
        key_b = pygame.Rect(WORLD_W // 2 + 520, WORLD_H // 2 + 160, 28, 28)

        # Puzzle A (empurrar bloco)
        push_block = pygame.Rect(WORLD_W // 2 - 760, WORLD_H // 2 - 160, 64,
                                 64)
        pressure_plate = pygame.Rect(WORLD_W // 2 - 640, WORLD_H // 2 - 160,
                                     50, 50)
        barrier_a = pygame.Rect(WORLD_W // 2 - 580, WORLD_H // 2 - 220, 20,
                                180)

        # Puzzle B (sequência) - BOTÕES MAIORES
        buttons = [
            {
                "rect": pygame.Rect(WORLD_W // 2 + 420, WORLD_H // 2 + 120, 80,
                                    80),
                "id": 1
            },
            {
                "rect": pygame.Rect(WORLD_W // 2 + 480, WORLD_H // 2 + 220, 80,
                                    80),
                "id": 2
            },
            {
                "rect": pygame.Rect(WORLD_W // 2 + 540, WORLD_H // 2 + 140, 80,
                                    80),
                "id": 3
            },
            {
                "rect": pygame.Rect(WORLD_W // 2 + 600, WORLD_H // 2 + 180, 80,
                                    80),
                "id": 4
            },
        ]
        sequence_needed = [1, 3, 2, 4]
        barrier_b = pygame.Rect(WORLD_W // 2 + 460, WORLD_H // 2 + 100, 180,
                                20)

        # Inimigos
        enemy_speed = 2.0
        enemies = []
        paths = [
            [(WORLD_W // 2 - 100, WORLD_H // 2 - 320),
             (WORLD_W // 2 + 100, WORLD_H // 2 - 320)],
            [(WORLD_W // 2 - 360, WORLD_H // 2 + 60),
             (WORLD_W // 2 - 160, WORLD_H // 2 + 60)],
            [(WORLD_W // 2 + 320, WORLD_H // 2 - 40),
             (WORLD_W // 2 + 320, WORLD_H // 2 + 160)],
        ]
        for p in paths:
            r = pygame.Rect(p[0][0], p[0][1], 38, 38)
            enemies.append({
                "rect": r,
                "path": p,
                "dir": 1,
                "speed": enemy_speed,
                "health": 2
            })

        # Posicionar jogador
        player_rect.center = (300, 300)

    elif level == 2:
        # FASE 2: PRAIA
        WORLD_W, WORLD_H = 2400, 1800
        borders = [
            pygame.Rect(0, 0, WORLD_W, 24),
            pygame.Rect(0, WORLD_H - 24, WORLD_W, 24),
            pygame.Rect(0, 0, 24, WORLD_H),
            pygame.Rect(WORLD_W - 24, 0, 24, WORLD_H),
        ]

        # Zonas de água
        water_zones = [
            pygame.Rect(400, 400, 600, 500),
            pygame.Rect(1600, 500, 500, 700),
            pygame.Rect(900, 1300, 600, 400)
        ]

        obstacles = []
        palm_trees = []

        # Palmeiras
        random.seed(8)
        for _ in range(40):
            x = random.randrange(100, WORLD_W - 150)
            y = random.randrange(100, WORLD_H - 150)
            # Não colocar palmeiras na água
            tree_rect = pygame.Rect(x, y, 56, 56)
            if not any(water.colliderect(tree_rect) for water in water_zones):
                obstacles.append(tree_rect)
                palm_trees.append(tree_rect)

        # Centro
        center_zone = pygame.Rect(WORLD_W // 2 - 260, WORLD_H // 2 - 200, 520,
                                  400)
        obstacles = [
            r for r in obstacles
            if not r.colliderect(center_zone.inflate(-40, -40))
        ]

        # Baú
        chest = pygame.Rect(WORLD_W // 2 - 32, WORLD_H // 2 - 32, 64, 64)
        sign_text = "Precisa de 2 chaves."
        spawn_sign = pygame.Rect(120, 140, 160, 40)
        spawn_sign_text = "Centro → Baú com Dica"

        # Chaves
        key_a = pygame.Rect(WORLD_W // 2 - 520, WORLD_H // 2 - 160, 28, 28)
        key_b = pygame.Rect(WORLD_W // 2 + 520, WORLD_H // 2 + 160, 28, 28)

        # Puzzle A - Encontrar e levar conchas para um altar
        shells = [
            pygame.Rect(WORLD_W // 2 - 700, WORLD_H // 2 - 300, 24, 24),
            pygame.Rect(WORLD_W // 2 - 650, WORLD_H // 2 + 200, 24, 24),
            pygame.Rect(WORLD_W // 2 + 600, WORLD_H // 2 - 250, 24, 24)
        ]

        barrier_a = pygame.Rect(WORLD_W // 2 - 580, WORLD_H // 2 - 220, 20,
                                180)

        # Puzzle B - Ativar totens na ordem correta
        buttons = [
            {
                "rect": pygame.Rect(WORLD_W // 2 + 400, WORLD_H // 2 - 100, 80,
                                    80),
                "id": 1
            },
            {
                "rect": pygame.Rect(WORLD_W // 2 + 480, WORLD_H // 2 + 50, 80,
                                    80),
                "id": 2
            },
            {
                "rect": pygame.Rect(WORLD_W // 2 + 560, WORLD_H // 2 - 50, 80,
                                    80),
                "id": 3
            },
        ]
        sequence_needed = [1, 3, 2]
        barrier_b = pygame.Rect(WORLD_W // 2 + 460, WORLD_H // 2 + 100, 180,
                                20)

        # Inimigos (caranguejos)
        enemy_speed = 1.5
        enemies = []
        paths = [
            [(WORLD_W // 2 - 100, WORLD_H // 2 - 320),
             (WORLD_W // 2 + 100, WORLD_H // 2 - 320)],
            [(WORLD_W // 2 - 360, WORLD_H // 2 + 60),
             (WORLD_W // 2 - 160, WORLD_H // 2 + 60)],
            [(WORLD_W // 2 + 320, WORLD_H // 2 - 40),
             (WORLD_W // 2 + 320, WORLD_H // 2 + 160)],
        ]
        for p in paths:
            r = pygame.Rect(p[0][0], p[0][1], 38, 38)
            enemies.append({
                "rect": r,
                "path": p,
                "dir": 1,
                "speed": enemy_speed,
                "health": 3
            })

        # Posicionar jogador
        player_rect.center = (300, 300)

    elif level == 3:
        # FASE 3: VILA ABANDONADA
        WORLD_W, WORLD_H = 2400, 1800
        borders = [
            pygame.Rect(0, 0, WORLD_W, 24),
            pygame.Rect(0, WORLD_H - 24, WORLD_W, 24),
            pygame.Rect(0, 0, 24, WORLD_H),
            pygame.Rect(WORLD_W - 24, 0, 24, WORLD_H),
        ]

        water_zones = []
        obstacles = []

        # Casas abandonadas
        random.seed(9)
        for _ in range(15):
            x = random.randrange(100, WORLD_W - 200)
            y = random.randrange(100, WORLD_H - 200)
            w = random.choice([120, 150, 180])
            h = random.choice([100, 120, 140])
            obstacles.append(pygame.Rect(x, y, w, h))

        # Cercas e muros
        for i in range(10):
            obstacles.append(pygame.Rect(i * 200 + 50, 300, 20, 100))
            obstacles.append(pygame.Rect(1800, i * 150 + 100, 100, 20))

        # Centro
        center_zone = pygame.Rect(WORLD_W // 2 - 260, WORLD_H // 2 - 200, 520,
                                  400)
        obstacles = [
            r for r in obstacles
            if not r.colliderect(center_zone.inflate(-40, -40))
        ]

        # Baú
        chest = pygame.Rect(WORLD_W // 2 - 32, WORLD_H // 2 - 32, 64, 64)
        sign_text = "Precisa de 3 chaves."

        # Chaves
        key_a = pygame.Rect(WORLD_W // 2 - 520, WORLD_H // 2 - 160, 28, 28)
        key_b = pygame.Rect(WORLD_W // 2 + 520, WORLD_H // 2 + 160, 28, 28)
        key_c = pygame.Rect(WORLD_W // 2, WORLD_H // 2 - 300, 28, 68)

        # Puzzle A (empurrar bloco)
        push_block = pygame.Rect(WORLD_W // 2 - 760, WORLD_H // 2 - 160, 64,
                                 64)
        pressure_plate = pygame.Rect(WORLD_W // 2 - 640, WORLD_H // 2 - 160,
                                     50, 50)
        barrier_a = pygame.Rect(WORLD_W // 2 - 580, WORLD_H // 2 - 220, 20,
                                180)

        # Puzzle B (sequência)
        buttons = [
            {
                "rect": pygame.Rect(WORLD_W // 2 + 420, WORLD_H // 2 + 120, 80,
                                    80),
                "id": 1
            },
            {
                "rect": pygame.Rect(WORLD_W // 2 + 480, WORLD_H // 2 + 220, 80,
                                    80),
                "id": 2
            },
            {
                "rect": pygame.Rect(WORLD_W // 2 + 540, WORLD_H // 2 + 140, 80,
                                    80),
                "id": 3
            },
        ]
        sequence_needed = [1, 3, 2]
        barrier_b = pygame.Rect(WORLD_W // 2 + 460, WORLD_H // 2 + 100, 180,
                                20)

        # Puzzle C (coletar itens)
        shells = [
            pygame.Rect(WORLD_W // 2 - 300, WORLD_H // 2 + 300, 24, 24),
            pygame.Rect(WORLD_W // 2 + 200, WORLD_H // 2 - 200, 24, 24),
            pygame.Rect(WORLD_W // 2 + 350, WORLD_H // 2 + 450, 24, 24)
        ]
        barrier_c = pygame.Rect(WORLD_W // 2, WORLD_H // 2 - 400, 20, 200)

        # Inimigos
        enemy_speed = 1.8
        enemies = []
        paths = [
            [(WORLD_W // 2 - 100, WORLD_H // 2 - 320),
             (WORLD_W // 2 + 100, WORLD_H // 2 - 320)],
            [(WORLD_W // 2 - 360, WORLD_H // 2 + 60),
             (WORLD_W // 2 - 160, WORLD_H // 2 + 60)],
            [(WORLD_W // 2 + 320, WORLD_H // 2 - 40),
             (WORLD_W // 2 + 320, WORLD_H // 2 + 160)],
        ]
        for p in paths:
            r = pygame.Rect(p[0][0], p[0][1], 32, 32)
            enemies.append({
                "rect": r,
                "path": p,
                "dir": 1,
                "speed": enemy_speed,
                "health": 2
            })

        # Posicionar jogador
        player_rect.center = (300, 300)

    elif level == 4:  # CAPÍTULO 2 - LABIRINTO
        WORLD_W, WORLD_H = 4800, 3600  # Mapa maior para o labirinto

        borders = [
            pygame.Rect(0, 0, WORLD_W, 24),
            pygame.Rect(0, WORLD_H - 24, WORLD_W, 24),
            pygame.Rect(0, 0, 24, WORLD_H),
            pygame.Rect(WORLD_W - 24, 0, 24, WORLD_H),
        ]

        # Limpar obstáculos anteriores e configurar labirinto
        obstacles = []
        water_zones = []
        enemies = []
        maze_walls = []
        cards = []

        # CONSTRUIR LABIRINTO
        cell_size = 120
        cols = WORLD_W // cell_size
        rows = WORLD_H // cell_size

        # Inicializar todas as células como paredes
        grid = [[1 for _ in range(cols)] for _ in range(rows)]

        # Função para gerar labirinto usando DFS
        def generate_maze(x, y):
            grid[y][x] = 0  # Marcar célula como caminho

            # Direções: cima, direita, baixo, esquerda
            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 1:
                    grid[ny][nx] = 0  # Marcar nova célula como caminho
                    grid[y + dy//2][x + dx//2] = 0  # Remover parede entre as células
                    generate_maze(nx, ny)

        # Começar a gerar a partir de uma posição aleatória
        start_x, start_y = random.randrange(1, cols-1, 2), random.randrange(1, rows-1, 2)
        generate_maze(start_x, start_y)

        # Garantir uma saída no canto inferior direito
        grid[rows-2][cols-2] = 0
        grid[rows-3][cols-2] = 0
        grid[rows-2][cols-3] = 0

        # Converter grid para paredes reais
        for y in range(rows):
            for x in range(cols):
                if grid[y][x] == 1:
                    maze_walls.append(pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

        # Posicionar jogador no início do labirinto (canto superior esquerdo)
        player_rect.x = cell_size * 1.5
        player_rect.y = cell_size * 1.5

        # Criar cartas em posições acessíveis no labirinto
        path_cells = []
        for y in range(rows):
            for x in range(cols):
                if grid[y][x] == 0:
                    path_cells.append((x, y))

        # Embaralhar células de caminho e selecionar 8 para colocar cartas
        random.shuffle(path_cells)
        for i in range(min(8, len(path_cells))):
            x, y = path_cells[i]
            card_x = x * cell_size + cell_size // 4
            card_y = y * cell_size + cell_size // 4

            cards.append({
                "rect": pygame.Rect(card_x, card_y, 30, 40),
                "hint": gift_hints[i],
                "collected": False
            })

        current_level = 4

# ----------------------------
# LÓGICA DE INIMIGOS / DANO
def move_enemies():
    global health, invuln_timer, player_rect

    for e in enemies:
        rect = e["rect"]
        p = e["path"]
        d = e["dir"]
        speed = e["speed"]

        # Movimento em direção ao player se estiver perto
        dist_to_player = math.hypot(player_rect.centerx - rect.centerx,
                                    player_rect.centery - rect.centery)
        if dist_to_player < 200:
            # Perseguir o jogador
            vx = player_rect.centerx - rect.centerx
            vy = player_rect.centery - rect.centery
            dist = math.hypot(vx, vy)
            if dist > 0:
                rect.x += int(vx / dist * speed * 1.2)
                rect.y += int(vy / dist * speed * 1.2)
        else:
            # Patrulha normal
            tx, ty = p[d]
            vx, vy = tx - rect.x, ty - rect.y
            dist = math.hypot(vx, vy)
            if dist > 0:
                rect.x += int(vx / dist * speed)
                rect.y += int(vy / dist * speed)
            if abs(rect.x - tx) < 4 and abs(rect.y - ty) < 4:
                e["dir"] = 1 - d

        # Dano por contato
        if invuln_timer <= 0 and rect.colliderect(player_rect):
            health -= 1
            invuln_timer = 60
            # knockback simples
            kb = pygame.Vector2(player_rect.center) - pygame.Vector2(
                rect.center)
            if kb.length() == 0: kb = pygame.Vector2(1, 0)
            kb = kb.normalize() * 28
            player_rect.centerx = clamp(player_rect.centerx + int(kb.x),
                                        24 + 20, WORLD_W - 24 - 20)
            player_rect.centery = clamp(player_rect.centery + int(kb.y),
                                        24 + 20, WORLD_H - 24 - 20)

# ----------------------------
# SISTEMA DE ATAQUE
def handle_attack():
    global attacking, attack_cooldown, attack_angle, enemies

    if attack_cooldown > 0:
        attack_cooldown -= 1
        return

    if attacking:
        # Calcular ângulo de ataque
        if facing_right:
            attack_angle = 0
        else:
            attack_angle = 180

        # Área de ataque
        attack_pos = pygame.Vector2(player_rect.centerx, player_rect.centery)

        # Verificar colisão com inimigos
        for e in enemies[:]:
            enemy_pos = pygame.Vector2(e["rect"].centerx, e["rect"].centery)
            dist = attack_pos.distance_to(enemy_pos)

            if dist < attack_range:
                angle_to_enemy = math.degrees(
                    math.atan2(enemy_pos.y - attack_pos.y,
                               enemy_pos.x - attack_pos.x))
                angle_diff = abs((angle_to_enemy - attack_angle + 180) % 360 -
                                 180)
                if angle_diff < 90:
                    e["health"] -= 1

                    # knockback
                    knockback_dir = pygame.Vector2(enemy_pos.x - attack_pos.x,
                                                   enemy_pos.y - attack_pos.y)
                    if knockback_dir.length() > 0:
                        knockback_dir = knockback_dir.normalize() * 30
                        e["rect"].x += int(knockback_dir.x)
                        e["rect"].y += int(knockback_dir.y)

                    if e["health"] <= 0:
                        enemies.remove(e)

        attack_cooldown = 20
        attacking = False

# ----------------------------
# PUZZLE A
def update_puzzle_a(solids):
    global puzzle_a_done, barrier_a, keys_collected, key_a_taken, msg_puzzle_a_shown

    if current_level == 1 or current_level == 3:
        # Floresta e Vila: Empurrar bloco
        if player_rect.colliderect(push_block):
            move_vec = pygame.Vector2(player_move_dx, player_move_dy)
            if move_vec.length() > 0.2:
                mv = move_vec.normalize() * 2.0
                block_collision_move(push_block, int(mv.x), int(mv.y), solids)

        if push_block.colliderect(pressure_plate) and not puzzle_a_done:
            puzzle_a_done = True
            if not msg_puzzle_a_shown:
                show_message(
                    ["Bloco posicionado corretamente! Barreira removida."])
                msg_puzzle_a_shown = True

    elif current_level == 2:
        # Praia: Coletar conchas
        shells_to_remove = []
        for shell in shells:
            if player_rect.colliderect(shell):
                shells_to_remove.append(shell)

        for shell in shells_to_remove:
            shells.remove(shell)

        if len(shells) == 0 and not puzzle_a_done:
            puzzle_a_done = True
            if not msg_puzzle_a_shown:
                show_message(
                    ["Todas as conchas coletadas! Barreira removida."])
                msg_puzzle_a_shown = True

    if puzzle_a_done and barrier_a:
        barrier_a.width = 0
        barrier_a.height = 0

# ----------------------------
# PUZZLE B
def update_puzzle_b():
    global sequence_pressed, puzzle_b_done, barrier_b, keys_collected, key_b_taken, msg_puzzle_b_shown
    global buttons

    if puzzle_b_done:
        return

    hit_id = None
    for b in buttons:
        # VERIFIQUE SE A COLISÃO ESTÁ OCORRENDO
        if player_rect.colliderect(b["rect"]):
            hit_id = b["id"]
            break  # Importante: sair do loop após encontrar um botão

    if hit_id is not None and (not sequence_pressed
                               or sequence_pressed[-1] != hit_id):
        sequence_pressed.append(hit_id)

        if len(sequence_pressed) > len(sequence_needed):
            sequence_pressed = []
            if not msg_puzzle_b_shown:
                show_message(["Sequência errada! Tente novamente."])
                msg_puzzle_b_shown = True
        else:
            for i in range(len(sequence_pressed)):
                if sequence_pressed[i] != sequence_needed[i]:
                    sequence_pressed = []
                    if not msg_puzzle_b_shown:
                        show_message(["Sequência errada! Tente novamente."])
                        msg_puzzle_b_shown = True
                    break

            if sequence_pressed == sequence_needed and not puzzle_b_done:
                puzzle_b_done = True
                if not msg_puzzle_b_shown:
                    show_message(["Sequência correta! Barreira removida."])
                    msg_puzzle_b_shown = True

    if puzzle_b_done and barrier_b:
        barrier_b.width = 0
        barrier_b.height = 0

# ----------------------------
# PUZZLE C
def update_puzzle_c():
    global puzzle_c_done, barrier_c, keys_collected, key_c_taken, msg_puzzle_c_shown

    if current_level == 3 and not puzzle_c_done:
        shells_to_remove = []
        for shell in shells:
            if player_rect.colliderect(shell):
                shells_to_remove.append(shell)

        for shell in shells_to_remove:
            shells.remove(shell)

        if len(shells) == 0 and not puzzle_c_done:
            puzzle_c_done = True
            if not msg_puzzle_c_shown:
                show_message(["Todos os itens coletados! Barreira removida."])
                msg_puzzle_c_shown = True

    if puzzle_c_done and barrier_c:
        barrier_c.width = 0
        barrier_c.height = 0

# ----------------------------
def check_keys_and_chest():
    global keys_collected, key_a_taken, key_b_taken, key_c_taken, current_level
    global cards_collected

    if current_level == 4:  # CAPÍTULO 2 - Coletar cartas
        for card in cards:
            if not card["collected"] and player_rect.colliderect(card["rect"]):
                card["collected"] = True
                cards_collected += 1
                show_message([f"Carta {cards_collected}/8 encontrada!", "", f"Dica: {card['hint']}"])

                if cards_collected >= 8:
                    show_message(["Parabéns!", "Você coletou todas as cartas!", 
                                 "Agora você tem 8 dicas de presentes!",
                                 "Voltando ao menu principal..."], 
                                lambda: [globals().update(state=STATE_TITLE), title_screen()])
        return

    if not key_a_taken and key_a and player_rect.colliderect(key_a):
        if puzzle_a_done:
            key_a_taken = True
            keys_collected += 1
            show_message(["Chave A encontrada!"])

    if not key_b_taken and key_b and player_rect.colliderect(key_b):
        if puzzle_b_done:
            key_b_taken = True
            keys_collected += 1
            show_message(["Chave B encontrada!"])

    if current_level == 3 and not key_c_taken and key_c and player_rect.colliderect(key_c):
        if puzzle_c_done:
            key_c_taken = True
            keys_collected += 1
            show_message(["Chave C encontrada!"])

    if player_rect.colliderect(chest):
        keys_needed = 3 if current_level == 3 else 2
        if keys_collected >= keys_needed:
            if current_level == 1:
                show_message([
                    "Você abriu o baú e encontrou a Dica 1:",
                    "",
                    "\"Está dentro de alguma coisa\"",
                    "",
                    "Fase 2 desbloqueada!"
                ], lambda: open_level(2))
            elif current_level == 2:
                show_message([
                    "Você abriu o baú e encontrou a Dica 2:",
                    "",
                    "\"Está dentro de uma coisa que fica achatada quando é utilizada\"",
                    "",
                    "Fase 3 desbloqueada!"
                ], lambda: open_level(3))
            else:
                show_message([
                    "Você abriu o baú e encontrou a Dica 3:",
                    "",
                    "\"sem mim seu travesseiro fica nu\"",
                    "",
                    "Parabéns! Você completou o Capítulo 1!",
                    "Capítulo 2 desbloqueado!"
                ], open_cap2)
        else:
            show_message([
                "Baú trancado.",
                f"Reúna as {keys_needed} chaves! ({keys_collected}/{keys_needed})"
            ])

def open_cap2():
    global state
    show_message([
        "Parabéns! Você completou o Capítulo 1!",
        "Iniciando Capítulo 2: O Labirinto de Cartas",
        "Encontre todas as 8 cartas com dicas de presentes!"
    ])
    setup_level(4)

def open_level(level):
    global current_level
    current_level = level
    setup_level(current_level)

# ----------------------------
# DESENHO DO MUNDO - FASE 1 (FLORESTA)
def draw_world_ch1():
    # Fundo
    tile = 64
    base = DARK_GREEN
    virtual_surface.fill(base)

    for x in range(int(cam_x // tile) * tile - cam_x % tile, VIRTUAL_WIDTH, tile):
        pygame.draw.line(virtual_surface, (14, 70, 14), (x, 0), (x, VIRTUAL_HEIGHT))
    for y in range(int(cam_y // tile) * tile - cam_y % tile, VIRTUAL_HEIGHT, tile):
        pygame.draw.line(virtual_surface, (14, 70, 14), (0, y), (VIRTUAL_WIDTH, y))

    for b in borders:
        pygame.draw.rect(virtual_surface, DARK_BROWN, world_to_screen(b))

    pygame.draw.rect(virtual_surface, (60, 120, 60), world_to_screen(center_zone), 2)

    virtual_surface.blit(chest_img, world_to_screen(chest))

    text = FONT_SM.render(sign_text, True, WHITE)
    virtual_surface.blit(text, (world_to_screen(chest).centerx - text.get_width() // 2,
                       world_to_screen(chest).top - 22))

    for r in obstacles:
        obstacle_rect = world_to_screen(r)
        pygame.draw.rect(virtual_surface, (20, 100, 20), obstacle_rect)
        pygame.draw.rect(virtual_surface, (10, 60, 10), obstacle_rect, 2)

    if barrier_a and barrier_a.width > 0:
        pygame.draw.rect(virtual_surface, PURPLE, world_to_screen(barrier_a))

    if push_block:
        pygame.draw.rect(virtual_surface, (200, 120, 40), world_to_screen(push_block))

    if pressure_plate:
        pygame.draw.rect(
            virtual_surface, YELLOW if push_block
            and push_block.colliderect(pressure_plate) else LIGHT_GRAY,
            world_to_screen(pressure_plate))

        pa = FONT_SM.render("Empurre o bloco até a placa", True, WHITE)
        virtual_surface.blit(
            pa, (world_to_screen(pressure_plate).centerx - pa.get_width() // 2,
                 world_to_screen(pressure_plate).top - 22))

    if barrier_b and barrier_b.width > 0:
        pygame.draw.rect(virtual_surface, PURPLE, world_to_screen(barrier_b))

    for b in buttons:
        col = BLUE if (b["id"] in sequence_pressed) else LIGHT_GRAY
        pygame.draw.rect(virtual_surface, col, world_to_screen(b["rect"]))
        num = FONT_SM.render(str(b["id"]), True, BLACK)
        br = world_to_screen(b["rect"])
        virtual_surface.blit(num, (br.centerx - num.get_width() // 2,
                          br.centery - num.get_height() // 2))

    if buttons:
        pb = FONT_SM.render("Ative na ordem: 1, 3, 2, 4", True, WHITE)
        virtual_surface.blit(
            pb,
            (world_to_screen(buttons[0]["rect"]).centerx - pb.get_width() // 2,
             world_to_screen(buttons[0]["rect"]).top - 24))

    if puzzle_a_done and not key_a_taken and key_a:
        pygame.draw.rect(virtual_surface, YELLOW, world_to_screen(key_a))
        pygame.draw.circle(virtual_surface, YELLOW, world_to_screen(key_a).center, 14)

    if puzzle_b_done and not key_b_taken and key_b:
        pygame.draw.rect(virtual_surface, YELLOW, world_to_screen(key_b))
        pygame.draw.circle(virtual_surface, YELLOW, world_to_screen(key_b).center, 14)

    for e in enemies:
        rr = world_to_screen(e["rect"])
        pygame.draw.rect(virtual_surface, RED, rr)
        health_percent = e["health"] / 2
        pygame.draw.rect(virtual_surface, GREEN,
                         (rr.x, rr.y - 5, rr.width * health_percent, 4))
        pygame.draw.rect(virtual_surface, BLACK, (rr.x, rr.y - 5, rr.width, 4), 1)

    # Desenhar player com sprite correto
    rr = world_to_screen(player_rect)
    virtual_surface.blit(player_img, rr)

    if attacking and attack_cooldown > 15:
        attack_pos = (rr.centerx, rr.centery)
        if facing_right:
            pygame.draw.arc(virtual_surface, (255, 200, 50),
                            (attack_pos[0], attack_pos[1] - attack_range // 2,
                             attack_range, attack_range), math.radians(-45),
                            math.radians(45), 5)
        else:
            pygame.draw.arc(virtual_surface, (255, 200, 50),
                            (attack_pos[0] - attack_range, attack_pos[1] -
                             attack_range // 2, attack_range, attack_range),
                            math.radians(135), math.radians(225), 5)

# ----------------------------
# DESENHO DO MUNDO - FASE 2 (PRAIA)
def draw_world_ch2():
    virtual_surface.fill(SKY_BLUE)

    for water in water_zones:
        wr = world_to_screen(water)
        pygame.draw.rect(virtual_surface, WATER, wr)
        for i in range(0, wr.width, 40):
            offset = math.sin(pygame.time.get_ticks() / 500 + i / 40) * 5
            pygame.draw.arc(virtual_surface, DARK_WATER,
                            (wr.x + i, wr.y + offset, 40, 20), 0, math.pi, 3)

    for x in range(0, WORLD_W, 64):
        for y in range(0, WORLD_H, 64):
            sand_rect = pygame.Rect(x, y, 64, 64)
            if not any(water.colliderect(sand_rect) for water in water_zones):
                sr = world_to_screen(sand_rect)
                pygame.draw.rect(virtual_surface, SAND, sr)
                for i in range(3):
                    px = random.randint(sr.x, sr.x + sr.width)
                    py = random.randint(sr.y, sr.y + sr.height)
                    pygame.draw.circle(virtual_surface, (220, 190, 160), (px, py), 1)

    for b in borders:
        pygame.draw.rect(virtual_surface, BEIGE, world_to_screen(b))

    virtual_surface.blit(chest_img, world_to_screen(chest))

    text = FONT_SM.render(sign_text, True, WHITE)
    virtual_surface.blit(text, (world_to_screen(chest).centerx - text.get_width() // 2,
                       world_to_screen(chest).top - 22))

    for r in palm_trees:
        rr = world_to_screen(r)
        pygame.draw.rect(virtual_surface, (101, 67, 33),
                         (rr.x + rr.width // 3, rr.y + rr.height // 2,
                          rr.width // 3, rr.height // 2))
        pygame.draw.circle(virtual_surface, (34, 139, 34),
                           (rr.x + rr.width // 2, rr.y + rr.height // 3),
                           rr.width // 2)

    for shell in shells:
        sr = world_to_screen(shell)
        pygame.draw.ellipse(virtual_surface, (255, 230, 200), sr)
        pygame.draw.ellipse(virtual_surface, (200, 170, 150), sr, 2)

    if barrier_a and barrier_a.width > 0:
        pygame.draw.rect(virtual_surface, PURPLE, world_to_screen(barrier_a))

    if barrier_b and barrier_b.width > 0:
        pygame.draw.rect(virtual_surface, PURPLE, world_to_screen(barrier_b))

    for b in buttons:
        col = BLUE if (b["id"] in sequence_pressed) else LIGHT_GRAY
        pygame.draw.rect(virtual_surface, col, world_to_screen(b["rect"]))
        num = FONT_SM.render(str(b["id"]), True, BLACK)
        br = world_to_screen(b["rect"])
        virtual_surface.blit(num, (br.centerx - num.get_width() // 2,
                          br.centery - num.get_height() // 2))

    if buttons:
        pb = FONT_SM.render("Ative na ordem: 1, 3, 2", True, WHITE)
        virtual_surface.blit(
            pb,
            (world_to_screen(buttons[0]["rect"]).centerx - pb.get_width() // 2,
             world_to_screen(buttons[0]["rect"]).top - 24))

    if puzzle_a_done and not key_a_taken and key_a:
        pygame.draw.rect(virtual_surface, YELLOW, world_to_screen(key_a))
        pygame.draw.circle(virtual_surface, YELLOW, world_to_screen(key_a).center, 14)

    if puzzle_b_done and not key_b_taken and key_b:
        pygame.draw.rect(virtual_surface, YELLOW, world_to_screen(key_b))
        pygame.draw.circle(virtual_surface, YELLOW, world_to_screen(key_b).center, 14)

    for e in enemies:
        rr = world_to_screen(e["rect"])
        pygame.draw.ellipse(virtual_surface, (200, 50, 50), rr)
        for i in range(4):
            angle = i * math.pi / 2 + pygame.time.get_ticks() / 200
            leg_len = 15 + math.sin(pygame.time.get_ticks() / 100 + i) * 5
            end_x = rr.centerx + math.cos(angle) * leg_len
            end_y = rr.centery + math.sin(angle) * leg_len
            pygame.draw.line(virtual_surface, (200, 50, 50), (rr.centerx, rr.centery),
                             (end_x, end_y), 3)
        pygame.draw.circle(virtual_surface, BLACK, (rr.centerx - 5, rr.top + 8), 3)
        pygame.draw.circle(virtual_surface, BLACK, (rr.centerx + 5, rr.top + 8), 3)
        health_percent = e["health"] / 3
        pygame.draw.rect(virtual_surface, GREEN,
                         (rr.x, rr.y - 5, rr.width * health_percent, 4))
        pygame.draw.rect(virtual_surface, BLACK, (rr.x, rr.y - 5, rr.width, 4), 1)

    # Desenhar player com sprite correto
    rr = world_to_screen(player_rect)
    virtual_surface.blit(player_img, rr)

    if attacking and attack_cooldown > 15:
        attack_pos = (rr.centerx, rr.centery)
        if facing_right:
            pygame.draw.arc(virtual_surface, (255, 200, 50),
                            (attack_pos[0], attack_pos[1] - attack_range // 2,
                             attack_range, attack_range), math.radians(-45),
                            math.radians(45), 5)
        else:
            pygame.draw.arc(virtual_surface, (255, 200, 50),
                            (attack_pos[0] - attack_range, attack_pos[1] -
                             attack_range // 2, attack_range, attack_range),
                            math.radians(135), math.radians(225), 5)

# ----------------------------
# DESENHO DO MUNDO - FASE 3 (VILA ABANDONADA)
def draw_world_ch3():
    # Fundo
    virtual_surface.fill((180, 180, 180))  # Cor de terra abandonada

    for x in range(0, WORLD_W, 64):
        for y in range(0, WORLD_H, 64):
            tile_rect = pygame.Rect(x, y, 64, 64)
            tr = world_to_screen(tile_rect)
            pygame.draw.rect(virtual_surface, (160, 160, 160), tr)
            pygame.draw.rect(virtual_surface, (140, 140, 140), tr, 1)

    for b in borders:
        pygame.draw.rect(virtual_surface, DARK_BROWN, world_to_screen(b))

    pygame.draw.rect(virtual_surface, (80, 80, 80), world_to_screen(center_zone), 2)

    virtual_surface.blit(chest_img, world_to_screen(chest))

    text = FONT_SM.render(sign_text, True, WHITE)
    virtual_surface.blit(text, (world_to_screen(chest).centerx - text.get_width() // 2,
                       world_to_screen(chest).top - 22))

    for r in obstacles:
        obstacle_rect = world_to_screen(r)
        pygame.draw.rect(virtual_surface, (100, 80, 60),
                         obstacle_rect)  # Cor de casa abandonada
        pygame.draw.rect(virtual_surface, (80, 60, 40), obstacle_rect, 2)
        # Janelas quebradas
        pygame.draw.rect(virtual_surface, (50, 50, 50),
                         (obstacle_rect.x + 10, obstacle_rect.y + 15, 20, 25))
        pygame.draw.rect(virtual_surface, (50, 50, 50),
                         (obstacle_rect.x + obstacle_rect.width - 30,
                          obstacle_rect.y + 15, 20, 25))

    if barrier_a and barrier_a.width > 0:
        pygame.draw.rect(virtual_surface, PURPLE, world_to_screen(barrier_a))

    if push_block:
        pygame.draw.rect(virtual_surface, (200, 120, 40), world_to_screen(push_block))

    if pressure_plate:
        pygame.draw.rect(
            virtual_surface, YELLOW if push_block
            and push_block.colliderect(pressure_plate) else LIGHT_GRAY,
            world_to_screen(pressure_plate))

        pa = FONT_SM.render("Empurre o bloco até a placa", True, WHITE)
        virtual_surface.blit(
            pa, (world_to_screen(pressure_plate).centerx - pa.get_width() // 2,
                 world_to_screen(pressure_plate).top - 22))

    if barrier_b and barrier_b.width > 0:
        pygame.draw.rect(virtual_surface, PURPLE, world_to_screen(barrier_b))

    if barrier_c and barrier_c.width > 0:
        pygame.draw.rect(virtual_surface, PURPLE, world_to_screen(barrier_c))

    for b in buttons:
        col = BLUE if (b["id"] in sequence_pressed) else LIGHT_GRAY
        pygame.draw.rect(virtual_surface, col, world_to_screen(b["rect"]))
        num = FONT_SM.render(str(b["id"]), True, BLACK)
        br = world_to_screen(b["rect"])
        virtual_surface.blit(num, (br.centerx - num.get_width() // 2,
                          br.centery - num.get_height() // 2))

    if buttons:
        pb = FONT_SM.render("Ative na ordem: 1, 3, 2", True, WHITE)
        virtual_surface.blit(
            pb,
            (world_to_screen(buttons[0]["rect"]).centerx - pb.get_width() // 2,
             world_to_screen(buttons[0]["rect"]).top - 24))

    for shell in shells:
        sr = world_to_screen(shell)
        pygame.draw.ellipse(virtual_surface, (150, 150, 200),
                            sr)  # Itens azuis para diferenciar
        pygame.draw.ellipse(virtual_surface, (100, 100, 150), sr, 2)

    if puzzle_a_done and not key_a_taken and key_a:
        pygame.draw.rect(virtual_surface, YELLOW, world_to_screen(key_a))
        pygame.draw.circle(virtual_surface, YELLOW, world_to_screen(key_a).center, 14)

    if puzzle_b_done and not key_b_taken and key_b:
        pygame.draw.rect(virtual_surface, YELLOW, world_to_screen(key_b))
        pygame.draw.circle(virtual_surface, YELLOW, world_to_screen(key_b).center, 14)

    if puzzle_c_done and not key_c_taken and key_c:
        pygame.draw.rect(virtual_surface, YELLOW, world_to_screen(key_c))
        pygame.draw.circle(virtual_surface, YELLOW, world_to_screen(key_c).center, 14)

    for e in enemies:
        rr = world_to_screen(e["rect"])
        pygame.draw.rect(virtual_surface, (80, 80, 80), rr)  # Inimigos cinzas
        health_percent = e["health"] / 2
        pygame.draw.rect(virtual_surface, GREEN,
                         (rr.x, rr.y - 5, rr.width * health_percent, 4))
        pygame.draw.rect(virtual_surface, BLACK, (rr.x, rr.y - 5, rr.width, 4), 1)

    # Desenhar player com sprite correto
    rr = world_to_screen(player_rect)
    virtual_surface.blit(player_img, rr)

    if attacking and attack_cooldown > 15:
        attack_pos = (rr.centerx, rr.centery)
        if facing_right:
            pygame.draw.arc(virtual_surface, (255, 200, 50),
                            (attack_pos[0], attack_pos[1] - attack_range // 2,
                             attack_range, attack_range), math.radians(-45),
                            math.radians(45), 5)
        else:
            pygame.draw.arc(virtual_surface, (255, 200, 50),
                            (attack_pos[0] - attack_range, attack_pos[1] -
                             attack_range // 2, attack_range, attack_range),
                            math.radians(135), math.radians(225), 5)

# ----------------------------
# DESENHO DO MUNDO - CAPÍTULO 2 (LABIRINTO)
def draw_world_cap2():
    # Fundo
    virtual_surface.fill(DARK_GREEN)

    # Desenhar chão do labirinto
    for wall in maze_walls:
        area_around_wall = pygame.Rect(wall.x - 20, wall.y - 20, wall.width + 40, wall.height + 40)
        if area_around_wall.colliderect(pygame.Rect(cam_x, cam_y, VIRTUAL_WIDTH, VIRTUAL_HEIGHT)):
            pygame.draw.rect(virtual_surface, (50, 120, 50), world_to_screen(wall.inflate(40, 40)))

    # Desenhar paredes do labirinto
    for wall in maze_walls:
        if wall.colliderect(pygame.Rect(cam_x, cam_y, VIRTUAL_WIDTH, VIRTUAL_HEIGHT)):
            pygame.draw.rect(virtual_surface, DARK_BROWN, world_to_screen(wall))
            pygame.draw.rect(virtual_surface, BLACK, world_to_screen(wall), 2)

    # Desenhar cartas
    for card in cards:
        if not card["collected"] and card["rect"].colliderect(pygame.Rect(cam_x, cam_y, VIRTUAL_WIDTH, VIRTUAL_HEIGHT)):
            card_rect = world_to_screen(card["rect"])
            pygame.draw.rect(virtual_surface, LIGHT_BLUE, card_rect, border_radius=5)
            pygame.draw.rect(virtual_surface, BLUE, card_rect, 2, border_radius=5)

            # Desenhar símbolo de carta
            pygame.draw.rect(virtual_surface, WHITE, (card_rect.x + 5, card_rect.y + 10, 20, 15))
            pygame.draw.polygon(virtual_surface, WHITE, [
                (card_rect.x + 5, card_rect.y + 10),
                (card_rect.x + 15, card_rect.y + 5),
                (card_rect.x + 25, card_rect.y + 10)
            ])

    # Desenhar jogador
    rr = world_to_screen(player_rect)
    virtual_surface.blit(player_img, rr)

def draw_world():
    if current_level == 1:
        draw_world_ch1()
    elif current_level == 2:
        draw_world_ch2()
    elif current_level == 3:
        draw_world_ch3()
    elif current_level == 4:  # CAPÍTULO 2
        draw_world_cap2()

# ----------------------------
# LOOP PRINCIPAL DO JOGO
def run_game():
    global cam_x, cam_y, attacking, moving, player_img
    global invuln_timer, health, player_move_dx, player_move_dy
    global joy_active, joy_pos, joy_touch_id, attack_button_active, attack_button_touch_id
    global facing_right, last_direction

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        player_move_dx = 0
        player_move_dy = 0
        attacking = False

        # INPUT TECLADO
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_move_dx -= player_speed
            facing_right = False
            last_direction = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_move_dx += player_speed
            facing_right = True
            last_direction = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_move_dy -= player_speed
            last_direction = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_move_dy += player_speed
            last_direction = "down"
        if keys[pygame.K_SPACE] or keys[pygame.K_j]:
            attacking = True

        # Verifica se está na água (fase 2)
        in_water = False
        if current_level == 2:
            for water in water_zones:
                if player_rect.colliderect(water):
                    in_water = True
                    player_move_dx *= 0.6
                    player_move_dy *= 0.6
                    break

        # EVENTOS
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.FINGERDOWN:
                x, y = e.x * SCREEN_WIDTH, e.y * SCREEN_HEIGHT

                # Converter coordenadas da tela para coordenadas virtuais
                x = (x - OFFSET_X) / SCALE_RATIO
                y = (y - OFFSET_Y) / SCALE_RATIO

                # Verificar se tocou no joystick (área circular)
                dx = x - joy_center[0]
                dy = y - joy_center[1]
                if dx*dx + dy*dy <= joy_radius*joy_radius:
                    joy_active = True
                    joy_touch_id = e.finger_id
                    joy_pos = (x, y)

                # Verificar se tocou no botão de ataque (área circular)
                dx = x - attack_button.centerx
                dy = y - attack_button.centery
                if dx*dx + dy*dy <= (attack_button.width//2)*(attack_button.width//2):
                    attack_button_active = True
                    attack_button_touch_id = e.finger_id
                    attacking = True

                if current_level != 4:  # Não há baú no Capítulo 2
                    sr = world_to_screen(chest)
                    if sr.collidepoint(x, y):
                        check_keys_and_chest()

            if e.type == pygame.FINGERUP:
                if e.finger_id == joy_touch_id:
                    joy_active = False
                    joy_pos = joy_center
                    joy_touch_id = None
                if e.finger_id == attack_button_touch_id:
                    attack_button_active = False
                    attack_button_touch_id = None

            if e.type == pygame.FINGERMOTION:
                if joy_active and e.finger_id == joy_touch_id:
                    x, y = e.x * SCREEN_WIDTH, e.y * SCREEN_HEIGHT
                    # Converter coordenadas da tela para coordenadas virtuais
                    x = (x - OFFSET_X) / SCALE_RATIO
                    y = (y - OFFSET_Y) / SCALE_RATIO

                    dx = x - joy_center[0]
                    dy = y - joy_center[1]
                    dist = math.hypot(dx, dy)
                    if dist > joy_radius:
                        dx = dx / dist * joy_radius
                        dy = dy / dist * joy_radius
                    joy_pos = (joy_center[0] + dx, joy_center[1] + dy)
                    speed = player_speed * (0.6 if in_water else 1.0)
                    player_move_dx = dx / joy_radius * speed
                    player_move_dy = dy / joy_radius * speed

                    if dx > 0:
                        facing_right = True
                        last_direction = "right"
                    elif dx < 0:
                        facing_right = False
                        last_direction = "left"
                    elif dy < 0:
                        last_direction = "up"
                    elif dy > 0:
                        last_direction = "down"

        # MOVIMENTO / COLISÃO
        solids = borders + obstacles
        if current_level == 4:  # Capítulo 2 - incluir paredes do labirinto
            solids += maze_walls
        if barrier_a and barrier_a.width > 0: solids.append(barrier_a)
        if barrier_b and barrier_b.width > 0: solids.append(barrier_b)
        if barrier_c and barrier_c.width > 0: solids.append(barrier_c)

        moving = abs(player_move_dx) > 0.05 or abs(player_move_dy) > 0.05

        # Atualizar sprite do jogador baseado na direção
        if attacking:
            player_img = player_attack
        elif moving:
            if last_direction == "right":
                player_img = player_walk_right
            elif last_direction == "left":
                player_img = player_walk_left
            elif last_direction == "up":
                player_img = player_walk_up
            elif last_direction == "down":
                player_img = player_walk_down
        else:
            player_img = player_idle

        # Movimento horizontal
        block_collision_move(player_rect, int(player_move_dx), 0, solids)
        # Movimento vertical
        block_collision_move(player_rect, 0, int(player_move_dy), solids)

        # CÂMERA
        cam_x = clamp(player_rect.centerx - VIRTUAL_WIDTH // 2, 0, WORLD_W - VIRTUAL_WIDTH)
        cam_y = clamp(player_rect.centery - VIRTUAL_HEIGHT // 2, 0, WORLD_H - VIRTUAL_HEIGHT)

        # PUZZLES (apenas para os primeiros 3 níveis)
        if current_level < 4:
            update_puzzle_a(solids)
            update_puzzle_b()
            if current_level == 3:
                update_puzzle_c()

        # CHAVES & BAÚ ou CARTAS
        check_keys_and_chest()

        # INIMIGOS (apenas para os primeiros 3 níveis)
        if current_level < 4:
            move_enemies()
        if invuln_timer > 0:
            invuln_timer -= 1

        # ATAQUE (apenas para os primeiros 3 níveis)
        if current_level < 4:
            handle_attack()

        # MORREU?
        if health <= 0:
            show_message(["Você desmaiou!", "Voltando ao início da fase..."],
                         lambda: setup_level(current_level))
            return

        # DESENHO
        draw_world()

        # HUD
        draw_hearts()
        draw_keys_ui()
        draw_joystick()
        draw_attack_button()

        # Informações da fase
        info = ""
        if current_level == 1:
            info = "Fase 1: Floresta - Objetivo: Abra o baú com 2 chaves"
        elif current_level == 2:
            info = "Fase 2: Praia - Objetivo: Abra o baú com 2 chaves"
        elif current_level == 3:
            info = "Fase 3: Vila Abandonada - Objetivo: Abra o baú com 3 chaves"
        elif current_level == 4:
            info = "Capítulo 2: Labirinto - Objetivo: Encontre todas as 8 cartas"

        info_surf = FONT_SM.render(info, True, WHITE)
        virtual_surface.blit(info_surf,
                    (VIRTUAL_WIDTH // 2 - info_surf.get_width() // 2, VIRTUAL_HEIGHT - 28))

        # Indicador de água
        if in_water:
            water_ind = FONT_SM.render("Nadando...", True, BLUE)
            virtual_surface.blit(water_ind,
                        (VIRTUAL_WIDTH // 2 - water_ind.get_width() // 2, 50))

        # Atualizar a tela real
        screen.blit(pygame.transform.scale(virtual_surface, (SCALED_WIDTH, SCALED_HEIGHT)), (OFFSET_X, OFFSET_Y))
        pygame.display.update()

# ----------------------------
# MAIN LOOP
def main():
    global state
    while True:
        if state == STATE_TITLE:
            title_screen()
        elif state == STATE_GAME:
            run_game()

if __name__ == "__main__":
    main()
