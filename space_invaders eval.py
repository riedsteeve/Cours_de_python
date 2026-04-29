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

# --- Gestion du Son (Pygame) ---
try:
    import pygame
    pygame.mixer.init()
    SOUND_AVAILABLE = True
except Exception:
    SOUND_AVAILABLE = False

EXPLOSION_SOUND = os.path.join("sounds", "explosion.wav")

def play_sound():
    if SOUND_AVAILABLE and os.path.exists(EXPLOSION_SOUND):
        try:
            sound = pygame.mixer.Sound(EXPLOSION_SOUND)
            sound.play()
        except Exception:
            pass

# --- Configuration et Chemins ---
IMAGE_DIR = "images"
PLAYER_IMG_SRC = os.path.join(IMAGE_DIR, "image.gif")
ENEMY_IMGS_SRC = [
    os.path.join(IMAGE_DIR, "enemy1.gif"),
    os.path.join(IMAGE_DIR, "enemy2.gif"),
    os.path.join(IMAGE_DIR, "enemy3.gif"),
]
BG_IMG = os.path.join(IMAGE_DIR, "galaxie.gif")

# Initialisation de la fenêtre
window = turtle.Screen()
window.title("Space Invaders Deluxe")
window.bgcolor("#000033")
window.setup(width=800, height=600)
window.tracer(0)

if os.path.exists(BG_IMG):
    window.bgpic(BG_IMG)

# Affichage du score et des vies
score = 0
lives = 3
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-380, 260)

def update_ui():
    score_display.clear()
    score_display.write(f"Score: {score}  Vies: {lives}", font=("Courier", 14, "bold"))

update_ui()

# Initialisation du vaisseau du joueur
player = turtle.Turtle()
if os.path.exists(PLAYER_IMG_SRC):
    window.register_shape(PLAYER_IMG_SRC)
    player.shape(PLAYER_IMG_SRC)
else:
    player.shape("triangle")
    player.color("orange")
player.penup()
player.goto(0, -250)
player.setheading(90)

# Initialisation des projectiles
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("cyan")
bullet.shapesize(stretch_wid=0.1, stretch_len=1)
bullet.penup()
bullet.hideturtle()
bullet.setheading(90)
bullet_state = "ready"

# Initialisation des ennemis et bonus
ENEMY_SHAPES = []
for src in ENEMY_IMGS_SRC:
    if os.path.exists(src):
        window.register_shape(src)
        ENEMY_SHAPES.append(src)

enemies = []
bonuses = []
_explosion_pool = []

# --- Système d'explosion ---
def _get_particle():
    if _explosion_pool:
        return _explosion_pool.pop()
    t = turtle.Turtle()
    t.penup()
    t.hideturtle()
    return t

def show_explosion(x, y):
    colors = ["yellow", "orange", "red", "white"]
    particles = []
    for angle in range(0, 360, 45):
        p = _get_particle()
        p.shape("circle")
        p.shapesize(0.4, 0.4)
        p.color(random.choice(colors))
        p.goto(x, y)
        p.setheading(angle)
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

# Fonctions de déplacement
def move_left():
    x = player.xcor()
    if x > -370: player.setx(x - 20)

def move_right():
    x = player.xcor()
    if x < 370: player.setx(x + 20)

def move_up():
    y = player.ycor()
    if y < 250: player.sety(y + 20)

def move_down():
    y = player.ycor()
    if y > -270: player.sety(y - 20)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 20)
        bullet.showturtle()

# Écoute des touches
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(move_up, "Up")
window.onkeypress(move_down, "Down")
window.onkeypress(fire_bullet, "space")

# Boucle de jeu
spawn_timer = 0
while lives > 0:
    window.update()
    time.sleep(0.02)

    # Initialisation / Apparition des ennemis
    spawn_timer += 1
    if spawn_timer > 40:
        enemy = turtle.Turtle()
        enemy.penup()
        if ENEMY_SHAPES:
            enemy.shape(random.choice(ENEMY_SHAPES))
        else:
            enemy.shape("circle")
            enemy.color("red")
        enemy.goto(random.randint(-350, 350), 300)
        enemies.append(enemy)
        spawn_timer = 0

    # Gestion des tirs
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + 40)
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

    # Déplacement des ennemis
    for enemy in enemies[:]:
        enemy.sety(enemy.ycor() - 2)

        # Détection des collisions (Tir / Ennemi)
        if bullet_state == "fire" and enemy.distance(bullet) < 25:
            ex, ey = enemy.xcor(), enemy.ycor()
            score += 10
            # Bonus aléatoire
            if random.random() < 0.25:
                bonus = turtle.Turtle()
                bonus.penup()
                bonus.type = random.choice(["life", "score"])
                bonus.shape("turtle" if bonus.type == "life" else "circle")
                bonus.color("green" if bonus.type == "life" else "yellow")
                bonus.goto(ex, ey)
                bonuses.append(bonus)
            
            enemy.hideturtle()
            enemies.remove(enemy)
            bullet.hideturtle()
            bullet_state = "ready"
            play_sound()
            show_explosion(ex, ey)
            update_ui()

        # Détection des collisions (Ennemi / Joueur)
        elif enemy.distance(player) < 30 or enemy.ycor() < -280:
            lives -= 1
            enemy.hideturtle()
            if enemy in enemies: enemies.remove(enemy)
            update_ui()

    # Gestion des bonus
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

# Affichage de l'écran de fin
score_display.goto(0, 0)
if lives <= 0:
    score_display.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
else:
    score_display.write("GG WP !", align="center", font=("Courier", 36, "bold"))

window.update()
window.mainloop()