import pygame
import sys
import random
import os

# Force window to center on screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Game Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
FPS = 60

# Colors
DARK_BG = (10, 10, 25)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
CYAN_GLOW = (0, 150, 150)
NEON_PINK = (255, 20, 147)
NEON_PINK_GLOW = (150, 0, 80)
HUD_BG = (20, 20, 40)
STAR_COLOR = (200, 200, 200)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.SysFont("impact", 72)
font_med = pygame.font.SysFont("impact", 48)
font_hud = pygame.font.SysFont("arial", 24, bold=True)

# Settings
settings = {
    "sound": True,
    "music": True
}

# --- Audio Setup ---
def load_sound(filename):
    try:
        return pygame.mixer.Sound(filename)
    except:
        return None

sounds = {
    "score": load_sound("assets/sounds/score.wav"),
    "level": load_sound("assets/sounds/level.wav"),
    "hit": load_sound("assets/sounds/hit.wav"),
    "menu": load_sound("assets/sounds/menu.wav")
}

def play_sound(name):
    if settings["sound"] and sounds.get(name):
        try:
            sounds[name].play()
        except:
            pass

def play_music():
    try:
        if settings["music"]:
            # Load and play if asset exists
            if os.path.exists("assets/sounds/bgm.mp3"):
                pygame.mixer.music.load("assets/sounds/bgm.mp3")
                pygame.mixer.music.play(-1)
    except:
        pass

def update_music_state():
    try:
        if settings["music"]:
            if not pygame.mixer.music.get_busy() and os.path.exists("assets/sounds/bgm.mp3"):
                pygame.mixer.music.load("assets/sounds/bgm.mp3")
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()
    except:
        pass

# Start BGM on launch
play_music()
# -------------------

# Player settings
player_width = 40
player_height = 40
player_x = float(SCREEN_WIDTH // 2 - player_width // 2)
player_y = float(SCREEN_HEIGHT - player_height - 20)
player_speed = 7.5

# Game states
game_state = "START"
score = 0
high_score = 0
level = 1

# Feedback Timers
level_up_timer = 0
score_flash_timer = 0
explosion_timer = 0
explosion_x = 0
explosion_y = 0

# Block settings
num_blocks = 4
base_speed = 4.0
blocks = []

def spawn_block_data(stagger_y=0):
    size = random.randint(30, 65)
    x = random.randint(0, SCREEN_WIDTH - size)
    current_base_speed = base_speed + (level - 1) * 1.0
    speed = random.uniform(current_base_speed, current_base_speed + 2.5)
    
    return {
        "x": float(x),
        "y": float(-size - stagger_y),
        "width": size,
        "height": size,
        "speed": speed
    }

def reset_blocks():
    blocks.clear()
    for i in range(num_blocks):
        blocks.append(spawn_block_data(stagger_y=i*160))

reset_blocks()

# Background Stars
stars = []
for _ in range(60):
    stars.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(0, SCREEN_HEIGHT),
        "speed": random.uniform(0.5, 2.0),
        "size": random.randint(1, 3)
    })

def draw_glow_rect(surface, color, glow_color, rect, border_radius=5):
    glow_rect = pygame.Rect(rect[0] - 4, rect[1] - 4, rect[2] + 8, rect[3] + 8)
    pygame.draw.rect(surface, glow_color, glow_rect, border_radius=border_radius)
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)

def draw_player(surface, x, y, width, height):
    flame_height = random.randint(10, 20)
    flame_points = [
        (x + width // 4, y + height),
        (x + 3 * width // 4, y + height),
        (x + width // 2, y + height + flame_height)
    ]
    pygame.draw.polygon(surface, YELLOW, flame_points)
    
    body_points = [
        (x + width // 2, y),
        (x + width, y + height),
        (x + width // 2, y + 3 * height // 4),
        (x, y + height)
    ]
    pygame.draw.polygon(surface, CYAN_GLOW, body_points)
    
    core_points = [
        (x + width // 2, y + 5),
        (x + 3 * width // 4 - 2, y + height - 5),
        (x + width // 2, y + 3 * height // 4 + 2),
        (x + width // 4 + 2, y + height - 5)
    ]
    pygame.draw.polygon(surface, CYAN, core_points)

# Main game loop
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if game_state == "START":
                if event.key == pygame.K_RETURN:
                    play_sound("menu")
                    game_state = "PLAYING"
                    score = 0
                    level = 1
                    level_up_timer = 0
                    player_x = float(SCREEN_WIDTH // 2 - player_width // 2)
                    reset_blocks()
                elif event.key == pygame.K_s:
                    play_sound("menu")
                    game_state = "SETTINGS"

            elif game_state == "SETTINGS":
                if event.key == pygame.K_m:
                    play_sound("menu")
                    game_state = "START"
                elif event.key == pygame.K_1:
                    play_sound("menu")
                    settings["sound"] = not settings["sound"]
                elif event.key == pygame.K_2:
                    play_sound("menu")
                    settings["music"] = not settings["music"]
                    update_music_state()

            elif game_state == "PLAYING":
                if event.key == pygame.K_p:
                    play_sound("menu")
                    game_state = "PAUSED"

            elif game_state == "PAUSED":
                if event.key == pygame.K_p:
                    play_sound("menu")
                    game_state = "PLAYING"
                elif event.key == pygame.K_m:
                    play_sound("menu")
                    game_state = "START"

            elif game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    play_sound("menu")
                    game_state = "PLAYING"
                    score = 0
                    level = 1
                    level_up_timer = 0
                    explosion_timer = 0
                    player_x = float(SCREEN_WIDTH // 2 - player_width // 2)
                    reset_blocks()
                elif event.key == pygame.K_m:
                    play_sound("menu")
                    game_state = "START"

    keys = pygame.key.get_pressed()

    # 2. Update Game State
    if game_state == "PLAYING":
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        if player_x < 0:
            player_x = 0
        elif player_x > SCREEN_WIDTH - player_width:
            player_x = SCREEN_WIDTH - player_width

        player_rect = pygame.Rect(int(player_x), int(player_y), player_width, player_height)

        for star in stars:
            star["y"] += star["speed"]
            if star["y"] > SCREEN_HEIGHT:
                star["y"] = 0
                star["x"] = random.randint(0, SCREEN_WIDTH)

        for block in blocks:
            block["y"] += block["speed"]

            if block["y"] > SCREEN_HEIGHT:
                score += 1
                play_sound("score")
                score_flash_timer = 15 # Flash score text for 15 frames
                
                if score > high_score:
                    high_score = score
                
                new_level = (score // 10) + 1
                if new_level > level:
                    level = new_level
                    level_up_timer = 90
                    play_sound("level")
                
                new_block_data = spawn_block_data(stagger_y=random.randint(0, 100))
                block["x"] = new_block_data["x"]
                block["y"] = new_block_data["y"]
                block["width"] = new_block_data["width"]
                block["height"] = new_block_data["height"]
                block["speed"] = new_block_data["speed"]

            block_rect = pygame.Rect(int(block["x"]), int(block["y"]), block["width"], block["height"])
            
            if player_rect.colliderect(block_rect):
                game_state = "GAME_OVER"
                play_sound("hit")
                explosion_timer = 40
                explosion_x = int(player_x + player_width // 2)
                explosion_y = int(player_y + player_height // 2)

    # 3. Draw Everything
    screen.fill(DARK_BG)

    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, (int(star["x"]), int(star["y"])), star["size"])

    if game_state in ["PLAYING", "PAUSED", "GAME_OVER"]:
        # Draw Player unless they just exploded
        if not (game_state == "GAME_OVER" and explosion_timer > 0):
            draw_player(screen, int(player_x), int(player_y), player_width, player_height)
            
        # Draw explosion feedback
        if game_state == "GAME_OVER" and explosion_timer > 0:
            explosion_timer -= 1
            rad1 = (40 - explosion_timer) * 3
            rad2 = (40 - explosion_timer) * 4
            pygame.draw.circle(screen, ORANGE, (explosion_x, explosion_y), rad1, 5)
            pygame.draw.circle(screen, NEON_PINK, (explosion_x, explosion_y), rad2, 2)

        # Draw Blocks
        for block in blocks:
            rect = (int(block["x"]), int(block["y"]), block["width"], block["height"])
            draw_glow_rect(screen, NEON_PINK, NEON_PINK_GLOW, rect, border_radius=8)
            
        if game_state == "PLAYING" and level_up_timer > 0:
            level_up_timer -= 1
            if (level_up_timer // 15) % 2 == 0:
                lvl_up_surf = font_large.render("LEVEL UP!", True, YELLOW)
                screen.blit(lvl_up_surf, (SCREEN_WIDTH // 2 - lvl_up_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

        # Top HUD Area
        pygame.draw.rect(screen, HUD_BG, (0, 0, SCREEN_WIDTH, 40))
        pygame.draw.line(screen, CYAN_GLOW, (0, 40), (SCREEN_WIDTH, 40), 2)
        
        # Visual feedback for score
        score_color = YELLOW if score_flash_timer > 0 else WHITE
        if score_flash_timer > 0:
            score_flash_timer -= 1
            
        score_surf = font_hud.render(f"SCORE: {score}", True, score_color)
        high_score_surf = font_hud.render(f"HIGH SCORE: {high_score}", True, WHITE)
        level_surf = font_hud.render(f"LEVEL: {level}", True, WHITE)

        screen.blit(score_surf, (20, 8))
        screen.blit(high_score_surf, (SCREEN_WIDTH // 2 - high_score_surf.get_width() // 2, 8))
        screen.blit(level_surf, (SCREEN_WIDTH - level_surf.get_width() - 20, 8))

    # Overlays
    if game_state == "START":
        title_text = font_large.render("DODGE THE FALLING BLOCKS", True, CYAN)
        desc_text = font_hud.render("Avoid the falling blocks and survive as long as possible.", True, WHITE)
        
        start_text = font_med.render("Press ENTER to Start", True, YELLOW)
        settings_text = font_hud.render("Press S for Settings", True, WHITE)
        quit_text = font_hud.render("Press ESC to Quit", True, STAR_COLOR)
        
        ctrl_title = font_hud.render("Controls:", True, CYAN_GLOW)
        ctrl_move = font_hud.render("A / D or Arrow Keys = Move", True, WHITE)
        ctrl_pause = font_hud.render("P = Pause", True, WHITE)
        ctrl_quit = font_hud.render("ESC = Quit", True, WHITE)
        
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 80))
        screen.blit(desc_text, (SCREEN_WIDTH // 2 - desc_text.get_width() // 2, 160))
        
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 240))
        screen.blit(settings_text, (SCREEN_WIDTH // 2 - settings_text.get_width() // 2, 310))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 360))
        
        screen.blit(ctrl_title, (SCREEN_WIDTH // 2 - ctrl_title.get_width() // 2, 440))
        screen.blit(ctrl_move, (SCREEN_WIDTH // 2 - ctrl_move.get_width() // 2, 480))
        screen.blit(ctrl_pause, (SCREEN_WIDTH // 2 - ctrl_pause.get_width() // 2, 520))
        screen.blit(ctrl_quit, (SCREEN_WIDTH // 2 - ctrl_quit.get_width() // 2, 560))

    elif game_state == "SETTINGS":
        title_text = font_large.render("SETTINGS", True, CYAN)
        
        snd_val = "ON" if settings["sound"] else "OFF"
        mus_val = "ON" if settings["music"] else "OFF"
        
        sound_text = font_med.render(f"1. Sound: {snd_val}", True, WHITE)
        music_text = font_med.render(f"2. Music: {mus_val}", True, WHITE)
        
        back_text = font_hud.render("Press M for Main Menu", True, CYAN_GLOW)
        
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(sound_text, (SCREEN_WIDTH // 2 - sound_text.get_width() // 2, 250))
        screen.blit(music_text, (SCREEN_WIDTH // 2 - music_text.get_width() // 2, 320))
        screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 500))

    elif game_state == "PAUSED":
        paused_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        paused_bg.fill((0, 0, 0, 150))
        screen.blit(paused_bg, (0, 0))
        
        paused_title = font_large.render("PAUSED", True, CYAN)
        resume_text = font_hud.render("Press P to Resume", True, WHITE)
        menu_text = font_hud.render("Press M for Main Menu", True, WHITE)
        esc_text = font_hud.render("Press ESC to Quit", True, STAR_COLOR)
        
        screen.blit(paused_title, (SCREEN_WIDTH // 2 - paused_title.get_width() // 2, 150))
        screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, 300))
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 350))
        screen.blit(esc_text, (SCREEN_WIDTH // 2 - esc_text.get_width() // 2, 400))

    elif game_state == "GAME_OVER":
        paused_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        paused_bg.fill((0, 0, 0, 150))
        screen.blit(paused_bg, (0, 0))

        go_title = font_large.render("GAME OVER", True, NEON_PINK)
        go_score = font_med.render(f"Score: {score}", True, WHITE)
        go_high = font_med.render(f"High Score: {high_score}", True, YELLOW)

        restart_text = font_hud.render("Press R to Restart", True, CYAN)
        menu_text = font_hud.render("Press M for Main Menu", True, WHITE)
        esc_text = font_hud.render("Press ESC to Quit", True, STAR_COLOR)
        
        screen.blit(go_title, (SCREEN_WIDTH // 2 - go_title.get_width() // 2, 100))
        screen.blit(go_score, (SCREEN_WIDTH // 2 - go_score.get_width() // 2, 220))
        screen.blit(go_high, (SCREEN_WIDTH // 2 - go_high.get_width() // 2, 290))

        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 420))
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 470))
        screen.blit(esc_text, (SCREEN_WIDTH // 2 - esc_text.get_width() // 2, 520))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame properly
pygame.quit()
sys.exit()
