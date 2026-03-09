import turtle 
import time
import random

du = 0.1
s = 0
ms = 0
name = input("Entrez votre prénom")

windows = turtle.Screen()

windows.title("Snake game")
windows.bgcolor("Black")
windows.setup(600, 400)
windows.title("Bienvenue " + name + " la partie peut commencer")
windows.update()

t = turtle.Turtle()

t.shape("square")
t.color("yellow")
t.speed(0) 
t.penup() 
t.direction = "stop"

b = turtle.Turtle()
b.shape(random.choice(['square', 'triangle', 'circle']))
b.color(random.choice(['red', 'green', 'black']))
b.penup()
b.goto(0, 100)

m = turtle.Turtle()
m.speed(0)
m.shape("square")
m.color("green")
m.penup()
m.hideturtle()
m.goto(0, 250)
m.write("Score : 0 Meilleur score : 0", align="center",
        font=("cambria" ,24, "bold"))


def agauche(): 
  t.direction = "left"
  print("Gauche")

def adroite():
  t.direction = "right" 
  print("Droite")
  
def haut():
  t.direction = "up"
  print("Haut")
  
def bas():
  t.direction = "down"
  print("Bas")


def move():
  if t.direction == "left":
    t.setx(t.xcor() -20)
  if t.direction == "right":
    t.setx(t.xcor() + 20)
  if t.direction == "up":
    t.sety(t.ycor() + 20)
  if t.direction == "down":
    t.sety(t.ycor() - 20)
  
  
  
windows.listen()
windows.onkeypress(haut, "Up")
windows.onkeypress(bas, "Down")
windows.onkeypress(agauche, "Left")
windows.onkeypress(adroite, "Right")
 
while True:
    windows.update()
    move()
    
    if t.distance(b) < 20:
      b.goto(random.randint(-200, 200), random.randint(-200, 200))
    
    seg = []
    nseg = turtle.Turtle()
    nseg.speed(0)
    nseg.shape("square")
    nseg.setposition(t.xcor(), t.ycor())
    nseg.color("yellow")
    nseg.penup()
    seg.append(nseg)
    du -= 0.001
    s += 10
    if s > ms:
      ms = s
    m.clear()
    m.write(f"score : {s} Meilleur Score : {ms}" ,align="center",
        font=("cambria" ,24, "bold" ))
    
    
    time.sleep(0.15)
    

 
 
  
    