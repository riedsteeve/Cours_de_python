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

# --- Chemins des images ---
IMG_PLAYER = "images/image.gif"
IMG_ENEMIES = ["images/enemy1.gif", "images/enemy2.gif", "images/enemy3.gif"]

# Initialisation de la fenêtre
window = turtle.Screen()
window.title("Space Invaders")
window.bgcolor("#000033")
window.setup(width=800, height=600)
window.tracer(0)

# Enregistrement des formes personnalisées (si elles existent)
try:
    if os.path.exists(IMG_PLAYER):
        window.register_shape(IMG_PLAYER)
    for img in IMG_ENEMIES:
        if os.path.exists(img):
            window.register_shape(img)
except:
    pass

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
    score_display.write(f"Score: {score}  Vies: {lives}", font=("Courier", 14, "normal"))

update_ui()

# Initialisation du vaisseau du joueur
player = turtle.Turtle()
player.speed(0)
if os.path.exists(IMG_PLAYER):
    player.shape(IMG_PLAYER)
else:
    player.shape("triangle")
    player.color("orange")
player.penup()
player.goto(0, -250)
player.setheading(90)

# Initialisation des projectiles
bullet = turtle.Turtle()
bullet.speed(0)
bullet.shape("square")
bullet.color("yellow")
bullet.shapesize(stretch_wid=0.2, stretch_len=0.5)
bullet.penup()
bullet.hideturtle()
bullet.setheading(90)
bullet_state = "ready"

# Liste pour stocker les ennemis
enemies = []

# Fonctions de déplacement
def move_left():
    x = player.xcor()
    if x > -380: player.setx(x - 20)

def move_right():
    x = player.xcor()
    if x < 380: player.setx(x + 20)

def move_up():
    y = player.ycor()
    if y < 0: player.sety(y + 20)

def move_down():
    y = player.ycor()
    if y > -280: player.sety(y - 20)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
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

    # Apparition des ennemis
    spawn_timer += 1
    if spawn_timer > 40:
        enemy = turtle.Turtle()
        # Choisir une image au hasard parmi la liste
        img_choice = random.choice(IMG_ENEMIES)
        if os.path.exists(img_choice):
            enemy.shape(img_choice)
        else:
            enemy.shape("circle")
            enemy.color("red")
        
        enemy.penup()
        enemy.speed(0)
        enemy.goto(random.randint(-350, 350), 280)
        enemies.append(enemy)
        spawn_timer = 0

    # Gestion des tirs
    if bullet_state == "fire":
        bullet.forward(20)
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

    # Déplacement des ennemis et collisions
    for enemy in enemies[:]:
        enemy.sety(enemy.ycor() - 3) # Vitesse de descente

        # Collision Tir / Ennemi
        if bullet_state == "fire" and enemy.distance(bullet) < 25:
            score += 10
            bullet.hideturtle()
            bullet_state = "ready"
            enemy.hideturtle()
            enemies.remove(enemy)
            update_ui()

        # Collision Joueur / Ennemi
        elif enemy.distance(player) < 30:
            lives -= 1
            enemy.hideturtle()
            enemies.remove(enemy)
            update_ui()
            
        # Ennemi qui sort par le bas
        elif enemy.ycor() < -300:
            enemy.hideturtle()
            enemies.remove(enemy)

# Fin de partie
score_display.goto(0, 0)
score_display.write("GAME OVER", align="center", font=("Courier", 24, "bold"))

window.mainloop()