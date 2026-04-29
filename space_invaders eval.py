'''
Bonjour à tous !

Votre objectif aujourd'hui, que vous l'acceptiez ou non, va être de terminer 
ce Space Invaders en utilisant la bibliothèque Turtle avec Python.

Vous avez déjà un début de code permettant d'initialiser la fenêtre et le 
joueur. Il vous donc rajouter les fonctionnalités suivantes :
- l'initialisation des ennemis
- le déplacement des ennemis vers le bas de l'écran ou sur les côtés
- la capacité de pouvoir tirer pour le joueur
- la gestion des collisions
- plus tout autre bonus que vous jugerez adéquat !

Bon courage !
'''

import turtle
import time
import random
import os
import sys

# --- Gestion des ressources (PyInstaller / Chemins) ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Gestion du Son (Pygame) ---
try:
    import pygame
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    SOUND_AVAILABLE = True
    print("[SON] pygame.mixer initialisé avec succès")
except Exception as e:
    SOUND_AVAILABLE = False
    print(f"[SON] Echec init pygame : {e}")

EXPLOSION_SOUND = resource_path(os.path.join("sounds", "explosion.wav"))

def play_sound():
    if SOUND_AVAILABLE and os.path.exists(EXPLOSION_SOUND):
        try:
            pygame.mixer.Sound(EXPLOSION_SOUND).play()
        except: pass

# =============================
# CONFIGURATION ET FENÊTRE
# =============================
window = turtle.Screen()
window.title("Space Invaders Deluxe")
window.bgcolor("#000033")
window.setup(width=800, height=600)
window.tracer(0)

IMAGE_DIR = "images"
BG_IMG = resource_path(os.path.join(IMAGE_DIR, "galaxie.gif"))
if os.path.exists(BG_IMG):
    window.bgpic(BG_IMG)

score = 0
lives = 3
game_over = False

# Affichage UI
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-380, 260)

def update_ui():
    score_display.clear()
    score_display.write(f"Score: {score}  |  Vies: {lives}", font=("Courier", 16, "bold"))

update_ui()

# =============================
# ACTEURS (Joueur, Projectile, Ennemis)
# =============================

# Configuration images
PLAYER_IMG = resource_path(os.path.join(IMAGE_DIR, "image.gif"))
ENEMY_IMGS = [
    resource_path(os.path.join(IMAGE_DIR, "enemy1.gif")),
    resource_path(os.path.join(IMAGE_DIR, "enemy2.gif")),
    resource_path(os.path.join(IMAGE_DIR, "enemy3.gif")),
]

# Initialisation Joueur
player = turtle.Turtle()
if os.path.exists(PLAYER_IMG):
    window.register_shape(PLAYER_IMG)
    player.shape(PLAYER_IMG)
else:
    player.shape("triangle")
    player.color("orange")
player.penup()
player.goto(0, -250)
player.setheading(90)

# Initialisation Projectile
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("cyan")
bullet.shapesize(0.1, 1)
bullet.penup()
bullet.hideturtle()
bullet.setheading(90)
bullet_state = "ready"

# Préparation Ennemis
ENEMY_SHAPES = []
for src in ENEMY_IMGS:
    if os.path.exists(src):
        window.register_shape(src)
        ENEMY_SHAPES.append(src)

enemies = []
bonuses = []
_explosion_pool = []

# =============================
# LOGIQUE DES PARTICULES
# =============================
def show_explosion(x, y):
    particles = []
    for _ in range(8):
        p = _explosion_pool.pop() if _explosion_pool else turtle.Turtle()
        p.penup()
        p.shape("circle")
        p.shapesize(0.4, 0.4)
        p.color(random.choice(["yellow", "orange", "red", "white"]))
        p.goto(x, y)
        p.setheading(random.randint(0, 360))
        p.showturtle()
        particles.append(p)

    for _ in range(6):
        for p in particles:
            p.forward(5)
        window.update()
        time.sleep(0.01)
    for p in particles:
        p.hideturtle()
        _explosion_pool.append(p)

# =============================
# FONCTIONS DE JEU
# =============================
def spawn_enemy():
    enemy = turtle.Turtle()
    enemy.penup()
    if ENEMY_SHAPES:
        enemy.shape(random.choice(ENEMY_SHAPES))
    else:
        enemy.shape("circle")
        enemy.color("red")
    enemy.goto(random.randint(-350, 350), 300)
    enemies.append(enemy)

def spawn_bonus(x, y):
    if random.random() < 0.25:
        bonus = turtle.Turtle()
        bonus.penup()
        bonus.type = random.choice(["life", "score"])
        bonus.shape("turtle" if bonus.type == "life" else "circle")
        bonus.color("green" if bonus.type == "life" else "yellow")
        bonus.goto(x, y)
        bonuses.append(bonus)

def lose_life(enemy):
    global lives, game_over
    lives -= 1
    enemy.hideturtle()
    if enemy in enemies: enemies.remove(enemy)
    update_ui()
    if lives <= 0: game_over = True

# Contrôles
def move_left():  player.setx(max(-370, player.xcor() - 20))
def move_right(): player.setx(min(370, player.xcor() + 20))
def move_up():    player.sety(min(250, player.ycor() + 20))
def move_down():  player.sety(max(-270, player.ycor() - 20))

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
    if spawn_timer > 40:
        spawn_enemy()
        spawn_timer = 0

    # Mouvement Bullet
    if bullet_state == "fire":
        bullet.forward(40)
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

    # Mouvement Ennemis
    for enemy in enemies[:]:
        enemy.sety(enemy.ycor() - 2)

        # Collision Bullet / Enemy
        if bullet_state == "fire" and enemy.distance(bullet) < 25:
            ex, ey = enemy.xcor(), enemy.ycor()
            score += 10
            spawn_bonus(ex, ey)
            enemy.hideturtle()
            enemies.remove(enemy)
            bullet.hideturtle()
            bullet_state = "ready"
            update_ui()
            play_sound()
            show_explosion(ex, ey)

        # Collision Player / Enemy
        elif enemy.distance(player) < 30 or enemy.ycor() < -280:
            lose_life(enemy)

    # Mouvement Bonus
    for bonus in bonuses[:]:
        bonus.sety(bonus.ycor() - 4)
        if bonus.distance(player) < 30:
            if bonus.type == "life": lives += 1
            else: score += 50
            bonus.hideturtle()
            bonuses.remove(bonus)
            update_ui()
        elif bonus.ycor() < -300:
            bonus.hideturtle()
            bonuses.remove(bonus)

# FIN DE PARTIE
score_display.goto(0, 0)
score_display.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
window.update()
window.mainloop()