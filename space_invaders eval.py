import turtle
import time
import random
import os

# Pillow pour redimensionner les images
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("Pillow non installe. Lance : pip install pillow")

# Winsound uniquement sur Windows
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

# =============================
# CONFIGURATION
# =============================
IMAGE_DIR = "images"
RESIZED_DIR = os.path.join(IMAGE_DIR, "resized")

PLAYER_IMG_SRC  = os.path.join(IMAGE_DIR, "image.png")
# Ajout de 3 types d'ennemis différents pour le barème
ENEMY_IMGS_SRC  = [
    os.path.join(IMAGE_DIR, "enemy1.png"),
    os.path.join(IMAGE_DIR, "enemy2.png"),
    os.path.join(IMAGE_DIR, "enemy3.png"),
]
BG_IMG          = os.path.join(IMAGE_DIR, "galaxie.gif")
EXPLOSION_SOUND = "explosion.wav"

PLAYER_SIZE = (40, 40)
ENEMY_SIZE  = (32, 32)

SCREEN_WIDTH      = 800
SCREEN_HEIGHT     = 600
PLAYER_SPEED      = 20
BULLET_SPEED      = 40
ENEMY_SPEED       = 2
ENEMY_SPAWN_DELAY = 40

# =============================
# REDIMENSIONNEMENT
# =============================
def resize_image(src, dst, size):
    if not PILLOW_AVAILABLE or not os.path.exists(src):
        return None
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        img = Image.open(src).convert("RGBA")
        img = img.resize(size, Image.LANCZOS)
        img.save(dst)
        return dst
    except:
        return None

PLAYER_IMG = resize_image(PLAYER_IMG_SRC, os.path.join(RESIZED_DIR, "player.png"), PLAYER_SIZE) or PLAYER_IMG_SRC
ENEMY_IMGS = []
for i, src in enumerate(ENEMY_IMGS_SRC):
    dst = os.path.join(RESIZED_DIR, f"enemy_{i}.png")
    res = resize_image(src, dst, ENEMY_SIZE)
    ENEMY_IMGS.append(res or src)

# =============================
# FENÊTRE ET ETAT
# =============================
window = turtle.Screen()
window.title("Space Invaders Deluxe")
window.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
window.tracer(0)
window.bgcolor("black")

score = 0
lives = 3
game_over = False

# Affichage Score/Vies
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.color("white")
score_display.goto(-SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 40)

def update_score_display():
    score_display.clear()
    score_display.write(f"Score: {score}  |  Vies: {lives}", font=("Courier", 16, "bold"))

update_score_display()

# =============================
# ACTEURS
# =============================
player = turtle.Turtle()
if os.path.exists(str(PLAYER_IMG)):
    window.register_shape(PLAYER_IMG)
    player.shape(PLAYER_IMG)
else:
    player.shape("triangle")
    player.color("blue")
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

enemies = []
bonuses = []

# =============================
# FONCTIONS DE JEU
# =============================
def spawn_enemy():
    enemy = turtle.Turtle()
    idx = random.randint(0, len(ENEMY_IMGS)-1)
    img = ENEMY_IMGS[idx]
    if os.path.exists(str(img)):
        window.register_shape(img)
        enemy.shape(img)
    else:
        enemy.shape("circle")
        colors = ["red", "purple", "orange"]
        enemy.color(colors[idx % 3])
    enemy.penup()
    enemy.goto(random.randint(-350, 350), SCREEN_HEIGHT // 2)
    enemies.append(enemy)

def spawn_bonus(x, y):
    if random.random() < 0.25: # 25% de chance
        bonus = turtle.Turtle()
        b_type = random.choice(["life", "score"])
        bonus.type = b_type
        bonus.shape("diamond" if b_type == "life" else "circle")
        bonus.color("green" if b_type == "life" else "yellow")
        bonus.penup()
        bonus.goto(x, y)
        bonuses.append(bonus)

def play_sound():
    if SOUND_AVAILABLE and os.path.exists(EXPLOSION_SOUND):
        winsound.PlaySound(EXPLOSION_SOUND, winsound.SND_ASYNC)

# =============================
# CONTRÔLES (Complet : G, D, H, B)
# =============================
def move_left():  player.setx(max(-370, player.xcor() - PLAYER_SPEED))
def move_right(): player.setx(min(370, player.xcor() + PLAYER_SPEED))
def move_up():    player.sety(min(250, player.ycor() + PLAYER_SPEED))
def move_down():  player.sety(max(-270, player.ycor() - PLAYER_SPEED))

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 20)
        bullet.showturtle()

window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(move_up, "Up")
window.onkeypress(move_down, "Down")
window.onkeypress(fire_bullet, "space")

# =============================
# BOUCLE PRINCIPALE
# =============================
spawn_timer = 0

while not game_over:
    window.update()
    time.sleep(0.02)

    # Spawn ennemis
    spawn_timer += 1
    if spawn_timer > ENEMY_SPAWN_DELAY:
        spawn_enemy()
        spawn_timer = 0

    # Mouvement Bullet
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + BULLET_SPEED)
        if bullet.ycor() > SCREEN_HEIGHT // 2:
            bullet.hideturtle()
            bullet_state = "ready"

    # Gestion Ennemis
    for enemy in enemies[:]:
        enemy.sety(enemy.ycor() - ENEMY_SPEED)
        
        # Collision Tir/Ennemi
        if bullet_state == "fire" and enemy.distance(bullet) < 25:
            score += 10
            spawn_bonus(enemy.xcor(), enemy.ycor())
            play_sound()
            enemy.hideturtle()
            enemies.remove(enemy)
            bullet.hideturtle()
            bullet_state = "ready"
            update_score_display()

        # Collision Joueur/Ennemi
        elif enemy.distance(player) < 30:
            lives -= 1
            enemy.hideturtle()
            enemies.remove(enemy)
            update_score_display()
            if lives <= 0: game_over = True

        # Sortie écran
        elif enemy.ycor() < -300:
            enemy.hideturtle()
            enemies.remove(enemy)

    # Gestion Bonus (Présence d'au moins deux bonus)
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

# FIN
score_display.goto(0, 0)
score_display.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
window.update()
window.mainloop()