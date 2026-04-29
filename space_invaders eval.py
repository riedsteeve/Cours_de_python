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

# ── Démarrage de la musique de fond ─────────────────────────────────────────
start_music()

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
player.speed(0)
if os.path.exists(IMG_PLAYER):
    player.shape(IMG_PLAYER)
else:
    player.shape("triangle")
    player.color("blue")
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

ENEMY_SHAPES = []
for src in ENEMY_IMGS_SRC:
    if os.path.exists(src):
        window.register_shape(src)
        ENEMY_SHAPES.append(src)
    else:
        ENEMY_SHAPES.append(None)

enemies = []

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
    enemy.penup()
    enemy.goto(random.randint(-350, 350), SCREEN_HEIGHT // 2)
    enemies.append(enemy)

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

        if bullet_state == "fire" and enemy.distance(bullet) < 25:
            score += 10
            bullet.hideturtle()
            bullet_state = "ready"
            update_score_display()
            play_explosion()
            show_explosion(ex, ey)

        elif enemy.distance(player) < 30:
            lives -= 1
            enemy.hideturtle()
            enemies.remove(enemy)
            update_ui()
            
        # Ennemi qui sort par le bas
        elif enemy.ycor() < -300:
            enemy.hideturtle()
            enemies.remove(enemy)

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
if SOUND_AVAILABLE:
    pygame.mixer.music.stop()
score_display.goto(0, 0)
score_display.write("GAME OVER", align="center", font=("Courier", 24, "bold"))

window.mainloop()