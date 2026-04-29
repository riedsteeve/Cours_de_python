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
import winsound

# Initialisation de la fenêtre
window = turtle.Screen()
window.title("Space Invaders")
window.bgcolor("#000033")
window.setup(width=800, height=600)
window.tracer(0)

# Affichage du score et des vies
score = 0
lives = 3
level = 1
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-380, 260)
score_display.write(f"Score: {score}  Vies: {lives}  Niveau: {level}", font=("Courier", 14, "normal"))

# Définition des formes
img_player = "images/image.gif"
img_enemy = "images/enemy_classic.gif"
window.register_shape(img_player)
window.register_shape(img_enemy)
window.register_shape("laser", ((-1,-10), (1,-10), (1,10), (-1,10)))

# Initialisation du vaisseau du joueur
player = turtle.Turtle()
player.speed(0)
player.shape(img_player) 
player.penup()
player.goto(0, -250)
player.setheading(90)

# Initialisation des projectiles
bullet = turtle.Turtle()
bullet.speed(0)
bullet.shape("laser")
bullet.color("white")
bullet.penup()
bullet.hideturtle()
bullet_state = "ready"

# Initialisation des ennemis
ennemies = []
enemy_speed = 20      

# Fonctions de déplacement
player_dx = 0
player_dy = 0

def move_left():
    global player_dx
    player_dx = -15

def move_right():
    global player_dx
    player_dx = 15

def move_up():
    global player_dy
    player_dy = 15

def move_down():
    global player_dy
    player_dy = -15
    
def stop_move_x():
    global player_dx
    player_dx = 0

def stop_move_y():
    global player_dy
    player_dy = 0
    
def fire_bullet():
    global bullet_state 
    if bullet_state == "ready":
        winsound.PlaySound("sounds/shoot.wav", winsound.SND_ASYNC)
        bullet_state = "fire"
        bullet.showturtle()
        bullet.setposition(player.xcor(), player.ycor() + 10)

def move_enemies():
    global enemy_speed
    for enemy in ennemies:
        x = enemy.xcor()
        x += enemy_speed  
        enemy.setx(x)
        
        if x > 380 or x < -380:
            enemy_speed *= -1
            for e in ennemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            break 

# Écoute des touches
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(move_up, "Up")
window.onkeypress(move_down, "Down")
window.onkeyrelease(stop_move_x, "Left")
window.onkeyrelease(stop_move_x, "Right")
window.onkeyrelease(stop_move_y, "Up")
window.onkeyrelease(stop_move_y, "Down")
window.onkeypress(fire_bullet, "space")

def restart_game():
    global score, lives, level, bullet_state, ennemies, enemy_speed, player_dx, player_dy
    score = 0
    lives = 3
    level = 1
    bullet_state = "ready"
    player_dx = 0
    player_dy = 0
    setup_level()

def setup_level():
    global ennemies, level, enemy_speed
    score_display.clear()
    score_display.goto(-380, 260)
    score_display.write(f"Score: {score}  Vies: {lives}  Niveau: {level}", font=("Courier", 14, "normal"))
    
    player.goto(0, -250)
    bullet.hideturtle()
    
    num_enemies = 5 + (level - 1)
    enemy_speed = 8 + (level * 2)
    
    for enemy in ennemies:
        enemy.hideturtle()
    ennemies.clear()
    
    for i in range(num_enemies):
        enemy = turtle.Turtle()
        enemy.speed(0)
        enemy.shape(img_enemy)
        enemy.penup()
        x = -350 + (i % 8) * 90
        y = 250 - (i // 8) * 50
        enemy.goto(x, y)
        ennemies.append(enemy)
    run_game_loop()

def run_game_loop():
    global lives, score, level, bullet_state, enemy_speed
    while lives > 0:
        window.update()
        time.sleep(0.02)
        
        new_x = player.xcor() + player_dx
        new_y = player.ycor() + player_dy
        
        if -380 < new_x < 380:
            player.setx(new_x)
        if -280 < new_y < 0:
            player.sety(new_y)
            
        move_enemies()

        if bullet_state == "fire":
            y = bullet.ycor()
            bullet.sety(y + 20)
            
        if bullet.ycor() > 280:
            bullet.hideturtle()
            bullet_state = "ready"
            
        for enemy in ennemies[:]:
            if enemy.distance(player) < 30:
                lives = 0
                break
                
            if bullet_state == "fire" and enemy.distance(bullet) < 30:
                winsound.PlaySound("sounds/explosion.wav", winsound.SND_ASYNC)
                score += 10
                score_display.clear()
                score_display.write(f"Score: {score}  Vies: {lives}  Niveau: {level}", font=("Courier", 14, "normal"))
                bullet.hideturtle()
                bullet_state = "ready"
                bullet.sety(-1000)
                enemy.hideturtle()
                ennemies.remove(enemy)
                
        if len(ennemies) == 0:
            level += 1
            setup_level()
            return

    # Fin de partie
    score_display.goto(0, 0)
    score_display.write(f"GAME OVER\nScore: {score}  Niveau: {level}\nAppuyez sur 'R' pour recommencer", align="center", font=("Courier", 20, "normal"))

# Écoute de la touche R pour redémarrer
window.onkeypress(restart_game, "r")
window.onkeypress(restart_game, "R")

restart_game()
window.mainloop()
