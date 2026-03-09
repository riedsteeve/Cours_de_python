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

# Initialisation de la fenêtre
window = turtle.Screen()
window.title("Space Invaders")
window.bgcolor("#000033")
window.setup(width=800, height=600)
window.tracer(0)  # Désactive l'animation automatique pour un rendu fluide

# Affichage du score et des vies
score = 0
lives = 3
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-380, 260)
score_display.write(f"Score: {score}  Vies: {lives}", font=("Courier", 14, "normal"))

# Initialisation du vaisseau du joueur

img_path = "images/vaisseau.gif"
img_path2 = "images/vaisseau.png"
img_path3 = "images/eneny.png"



window.register_shape(img_path)
window.register_shape(img_path2)
window.register_shape(img_path3)

player = turtle.Turtle()
player.speed(0)
player.shape(img_path2)
player.penup()
player.goto(0, -250)
player.setheading(90)

# Initialisation des projectiles
bullet = turtle.Turtle()
bullet.speed(0)
bullet.shape("square")
bullet.color("red")
bullet.shapesize(stretch_wid=1, stretch_len=1)
bullet.penup()
bullet.hideturtle()
bullet_state = "ready"




# Initialisation des ennemis
ennemies = []
for i in range(5):
    enemy = turtle.Turtle()
    enemy.speed(0)
    enemy.shape("square")
    enemy.color("yellow")
    enemy.penup()
    enemy.goto(-200 + i * 100, 250)
    ennemies.append(enemy)


# Fonctions de déplacement
def move_left():
    x = player.xcor()
    if x > -380:
        player.setx(x - 20)

def move_right():
    x = player.xcor()
    if x < 380:
        player.setx(x + 20)
        
    
    
def fire_bullet():
        global bullet_state 
        if bullet_state == "ready":
            bullet_state = "fire"
            bullet.showturtle()
            bullet.setposition(player.xcor(), player.ycor() + 10)
       
enemy_speed = 20      
            
def move_enemies():
    global enemy_speed
    for enemy in ennemies:
        x = enemy.xcor()
        x += enemy_speed  
        enemy.setx(x)
        
        # Changement de direction et descente
        if x > 380 or x < -380:
            enemy_speed *= -1
            
            for e in ennemies:
                y = e.ycor()
                y -= 40  # Descente des ennemis
                e.sety(y)
            break  # Sort de la boucle pour éviter les problèmes de modification de liste
        
        
  

# Écoute des touches
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(fire_bullet, "space")


# Boucle de jeu
while lives > 0:
    window.update()
    time.sleep(0.05)  # Ralentit la boucle
    move_enemies()

    # Gestion des tirs
    if bullet_state == "fire":
        y = bullet.ycor()
        bullet.sety(y + 70)
        
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = "ready"
        
            
    
    # Déplacement des ennemis
    for enemy in ennemies:
        if enemy.distance(player) < 20:
            lives -= 1
            score_display.clear()
            score_display.write(f"Score: {score}  Vies: {lives}", font=("Courier", 14, "normal"))
            enemy.goto(-200 + ennemies.index(enemy) * 100, 250)  # Réinitialise la position de l'ennemi
            
        if bullet_state == "fire" and enemy.distance(bullet) < 20:
            score += 10
            score_display.clear()
            score_display.write(f"Score: {score}  Vies: {lives}", font=("Courier", 14, "normal"))
            bullet.hideturtle()
            bullet_state = "ready"
            enemy.goto(-200 + ennemies.index(enemy) * 100, 250)  # Réinitialise la position de l'ennemi
    

    # Détection des collisions
   

# Affichage de l'écran de victoire
if lives == 0:
    score_display.goto(0, 0)
    score_display.write("GAME OVER", align="center", font=("Courier", 24, "normal"))
else:
    score_display.goto(0, 0)
    score_display.write("GG WP !", align="center", font=("Courier", 24, "normal"))

window.mainloop()
