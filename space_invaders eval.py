import turtle
import time
import random
import os

# --- INITIALISATION SONORE ---
try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except Exception:
    SOUND_AVAILABLE = False

EXPLOSION_SOUND = os.path.join("sounds", "explosion.wav")
MUSIC_BACKGROUND = os.path.join("sounds", "background_sound.mp3")

def play_sound():
    if SOUND_AVAILABLE and os.path.exists(EXPLOSION_SOUND):
        try:
            sound = pygame.mixer.Sound(EXPLOSION_SOUND)
            sound = pygame.mixer.Sound(MUSIC_BACKGROUND)
            sound.play()
        except Exception:
            pass

# --- CONFIGURATION GRAPHIQUE ---
IMAGE_DIR = "images"
PLAYER_IMG_SRC = os.path.join(IMAGE_DIR, "image.gif")
ENEMY_IMGS_SRC = [
    os.path.join(IMAGE_DIR, "enemy1.gif"),
    os.path.join(IMAGE_DIR, "enemy2.gif"),
    os.path.join(IMAGE_DIR, "enemy3.gif"),
]
BG_IMG = os.path.join(IMAGE_DIR, "galaxie.gif")

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED  = 70
BULLET_SPEED  = 60
ENEMY_SPEED   = 2
ENEMY_SPAWN_DELAY = 40

 
window = turtle.Screen()
window.title("Steeve's Space Invaders")
window.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
window.tracer(0)
window.bgcolor("black")

if os.path.exists(BG_IMG):
    window.bgpic(BG_IMG)

# --- VARIABLES GLOBALES ---
score = 0
lives = 3
game_over = False
enemies = []
bonuses = []
bullet_state = "ready"

score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.color("white")

def update_score_display():
    score_display.clear()
    score_display.goto(-SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 40)
    score_display.write(f"Score: {score}  |  Vies: {lives}", font=("Courier", 16, "bold"))

# --- SYSTÈME DE PARTICULES ---
_explosion_pool = []

def _get_particle():
    if _explosion_pool:
        t = _explosion_pool.pop()
    else:
        t = turtle.Turtle()
        t.penup()
        t.hideturtle()
    return t

def show_explosion(x, y):
    COLORS = ["yellow", "orange", "red", "white"]
    STEPS = 6
    particles = []
    for angle in [i * 45 for i in range(8)]:
        p = _get_particle()
        p.shape("circle")
        p.shapesize(0.4, 0.4)
        p.color(random.choice(COLORS))
        p.goto(x, y)
        p.setheading(angle)
        p.showturtle()
        particles.append(p)

    for step in range(STEPS):
        for p in particles:
            p.forward(5)
            p.shapesize(0.4 * (1 - step / STEPS))
        window.update()
        time.sleep(0.01)

    for p in particles:
        p.hideturtle()
        _explosion_pool.append(p)

# --- JOUEUR ET TIR ---
player = turtle.Turtle()
if os.path.exists(PLAYER_IMG_SRC):
    window.register_shape(PLAYER_IMG_SRC)
    player.shape(PLAYER_IMG_SRC)
else:
    player.shape("triangle")
    player.color("orange")
player.penup()

bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("cyan")
bullet.shapesize(0.1, 0.8)
bullet.setheading(90)
bullet.penup()
bullet.hideturtle()

# --- ENNEMIS ---
ENEMY_SHAPES = []
for src in ENEMY_IMGS_SRC:
    if os.path.exists(src):
        window.register_shape(src)
        ENEMY_SHAPES.append(src)
    else:
        ENEMY_SHAPES.append(None)

def spawn_enemy():
    enemy = turtle.Turtle()
    idx = random.randint(0, len(ENEMY_SHAPES) - 1)
    shape = ENEMY_SHAPES[idx]
    enemy.shape(shape if shape else "circle")
    if not shape: enemy.color("red")
    enemy.penup()
    enemy.goto(random.randint(-350, 350), SCREEN_HEIGHT // 2)
    enemies.append(enemy)

def spawn_bonus(x, y):
    if random.random() < 0.2:
        bonus = turtle.Turtle()
        b_type = random.choice(["life", "score"])
        bonus.type = b_type
        bonus.shape("turtle" if b_type == "life" else "circle")
        bonus.color("green" if b_type == "life" else "yellow")
        bonus.penup()
        bonus.goto(x, y)
        bonuses.append(bonus)

# --- COMMANDES ---
def move_left():
    player.setx(max(-370, player.xcor() - PLAYER_SPEED))
def move_right():
    player.setx(min( 370, player.xcor() + PLAYER_SPEED))
def move_up():
    player.sety(min( 250, player.ycor() + PLAYER_SPEED))
def move_down():
    player.sety(max(-270, player.ycor() - PLAYER_SPEED))

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 20)
        bullet.showturtle()

# --- LOGIQUE DE RESTART ---
def restart_game():
    global score, lives, game_over, enemies, bonuses, bullet_state
    if game_over: # Ne redémarre que si on a perdu
        score = 0
        lives = 3
        game_over = False
        bullet_state = "ready"
        
        for e in enemies: e.hideturtle()
        for b in bonuses: b.hideturtle()
        enemies.clear()
        bonuses.clear()
        bullet.hideturtle()
        
        player.goto(0, -SCREEN_HEIGHT // 2 + 50)
        update_score_display()
        play_game()

window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(move_up, "Up")
window.onkeypress(move_down, "Down")
window.onkeypress(fire_bullet, "space")
window.onkeypress(restart_game, "r")

# --- BOUCLE PRINCIPALE ---
def play_game():
    global score, lives, game_over, bullet_state
    spawn_timer = 0
    
    while not game_over:
        window.update()
        time.sleep(0.02)

        spawn_timer += 1
        if spawn_timer > ENEMY_SPAWN_DELAY:
            spawn_enemy()
            spawn_timer = 0

        if bullet_state == "fire":
            bullet.sety(bullet.ycor() + BULLET_SPEED)
            if bullet.ycor() > SCREEN_HEIGHT // 2:
                bullet.hideturtle()
                bullet_state = "ready"

        for enemy in enemies[:]:
            enemy.sety(enemy.ycor() - ENEMY_SPEED)

            if bullet_state == "fire" and enemy.distance(bullet) < 30:
                ex, ey = enemy.xcor(), enemy.ycor()
                score += 10
                spawn_bonus(ex, ey)
                enemy.hideturtle()
                enemies.remove(enemy)
                bullet.hideturtle()
                bullet_state = "ready"
                update_score_display()
                play_sound()
                show_explosion(ex, ey)

            elif enemy.distance(player) < 30 or enemy.ycor() < -SCREEN_HEIGHT // 2 + 30:
                lives -= 1
                enemy.hideturtle()
                if enemy in enemies: enemies.remove(enemy)
                update_score_display()
                if lives <= 0: game_over = True

        for bonus in bonuses[:]:
            bonus.sety(bonus.ycor() - 4)
            if bonus.distance(player) < 30:
                if bonus.type == "life": lives += 1
                else: score += 50
                bonus.hideturtle()
                bonuses.remove(bonus)
                update_score_display()
            elif bonus.ycor() < -300:
                bonus.hideturtle()
                bonuses.remove(bonus)

    # Fin de partie
    score_display.goto(0, 0)
    score_display.write("GAME OVER\nAppuyez sur 'R' pour rejouer", align="center", font=("Courier", 24, "bold"))
    window.update()

player.goto(0, -SCREEN_HEIGHT // 2 + 50)
update_score_display()
play_game()
window.mainloop()

