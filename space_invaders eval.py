import turtle
import time
import random
import os

# ── Son multiplateforme via pygame ──────────────────────────────────────────
try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except Exception:
    SOUND_AVAILABLE = False

EXPLOSION_SOUND = "explosion.wav"

def play_sound():
    if SOUND_AVAILABLE and os.path.exists(EXPLOSION_SOUND):
        try:
            sound = pygame.mixer.Sound(EXPLOSION_SOUND)
            sound.play()
        except Exception:
            pass

# =============================
# CONFIGURATION
# =============================
IMAGE_DIR = "images"

PLAYER_IMG_SRC = os.path.join(IMAGE_DIR, "image.png")
ENEMY_IMGS_SRC = [
    os.path.join(IMAGE_DIR, "enemy1.png"),
    os.path.join(IMAGE_DIR, "enemy2.png"),
    os.path.join(IMAGE_DIR, "enemy3.png"),
]
BG_IMG = os.path.join(IMAGE_DIR, "galaxie.gif")

# Facteurs d'échelle shapesize (forme turtle de base = 20x20 px)
PLAYER_SCALE = (2.0, 2.0)
ENEMY_SCALE  = PLAYER_SCALE

SCREEN_WIDTH      = 800
SCREEN_HEIGHT     = 600
PLAYER_SPEED      = 20
BULLET_SPEED      = 40
ENEMY_SPEED       = 2
ENEMY_SPAWN_DELAY = 40

# =============================
# FENÊTRE ET ÉTAT
# =============================
window = turtle.Screen()
window.title("Space Invaders Deluxe")
window.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
window.tracer(0)
window.bgcolor("black")

score     = 0
lives     = 3
game_over = False

# Affichage Score / Vies
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.color("white")
score_display.goto(-SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 40)

def update_score_display():
    score_display.clear()
    score_display.write(
        f"Score: {score}  |  Vies: {lives}",
        font=("Courier", 16, "bold")
    )

update_score_display()

# =============================
# EXPLOSION VISUELLE
# =============================
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
    COLORS   = ["yellow", "orange", "red", "white"]
    STEPS    = 6
    DISTANCE = 5

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
            p.forward(DISTANCE)
            p.shapesize(0.4 * (1 - step / STEPS))
        window.update()
        time.sleep(0.01)

    for p in particles:
        p.hideturtle()
        _explosion_pool.append(p)

# =============================
# ACTEURS
# =============================
player = turtle.Turtle()
if os.path.exists(PLAYER_IMG_SRC):
    window.register_shape(PLAYER_IMG_SRC)
    player.shape(PLAYER_IMG_SRC)
else:
    player.shape("triangle")
    player.color("blue")
player.shapesize(*PLAYER_SCALE)
player.penup()
player.goto(0, -SCREEN_HEIGHT // 2 + 50)

bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("cyan")
bullet.shapesize(0.1, 1)
bullet.setheading(90)
bullet.penup()
bullet.hideturtle()
bullet_state = "ready"

ENEMY_SHAPES = []
for i, src in enumerate(ENEMY_IMGS_SRC):
    if os.path.exists(src):
        window.register_shape(src)
        ENEMY_SHAPES.append(src)
    else:
        ENEMY_SHAPES.append(None)

enemies = []
bonuses = []

# =============================
# FONCTIONS DE JEU
# =============================
def spawn_enemy():
    enemy = turtle.Turtle()
    idx   = random.randint(0, len(ENEMY_SHAPES) - 1)
    shape = ENEMY_SHAPES[idx]
    if shape:
        enemy.shape(shape)
    else:
        enemy.shape("circle")
        enemy.color(["red", "purple", "orange"][idx % 3])
    enemy.shapesize(*ENEMY_SCALE)
    enemy.penup()
    enemy.goto(random.randint(-350, 350), SCREEN_HEIGHT // 2)
    enemies.append(enemy)

def spawn_bonus(x, y):
    if random.random() < 0.25:
        bonus      = turtle.Turtle()
        b_type     = random.choice(["life", "score"])
        bonus.type = b_type
        bonus.shape("diamond" if b_type == "life" else "circle")
        bonus.color("green"   if b_type == "life" else "yellow")
        bonus.penup()
        bonus.goto(x, y)
        bonuses.append(bonus)

def lose_life(enemy):
    global lives, game_over
    lives -= 1
    enemy.hideturtle()
    enemies.remove(enemy)
    update_score_display()
    if lives <= 0:
        game_over = True

# =============================
# CONTRÔLES
# =============================
def move_left():  player.setx(max(-370, player.xcor() - PLAYER_SPEED))
def move_right(): player.setx(min( 370, player.xcor() + PLAYER_SPEED))
def move_up():    player.sety(min( 250, player.ycor() + PLAYER_SPEED))
def move_down():  player.sety(max(-270, player.ycor() - PLAYER_SPEED))

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 20)
        bullet.showturtle()

window.listen()
window.onkeypress(move_left,   "Left")
window.onkeypress(move_right,  "Right")
window.onkeypress(move_up,     "Up")
window.onkeypress(move_down,   "Down")
window.onkeypress(fire_bullet, "space")

# =============================
# BOUCLE PRINCIPALE
# =============================
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

        # Collision Tir / Ennemi
        if bullet_state == "fire" and enemy.distance(bullet) < 25:
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

        # Collision Joueur / Ennemi
        elif enemy.distance(player) < 30:
            lose_life(enemy)

        # Ennemi atteint la zone basse → perte de vie
        elif enemy.ycor() < -SCREEN_HEIGHT // 2 + 30:
            lose_life(enemy)

    for bonus in bonuses[:]:
        bonus.sety(bonus.ycor() - 4)
        if bonus.distance(player) < 30:
            if bonus.type == "life":
                lives += 1
            else:
                score += 50
            bonus.hideturtle()
            bonuses.remove(bonus)
            update_score_display()
        elif bonus.ycor() < -300:
            bonus.hideturtle()
            bonuses.remove(bonus)

# FIN
score_display.goto(0, 0)
score_display.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
window.update()
window.mainloop()