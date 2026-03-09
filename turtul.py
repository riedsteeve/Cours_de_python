import turtle
import time

#Initialisation du cadre
windows = turtle.Screen()
windows.title("Ma premiere fenetre")
windows.bgcolor("blue")
windows.setup(600, 400)
#Création d'un curseur "Turtle"

t = turtle.Turtle("turtle")
t.color("red")
t.speed(1)
#t.backward(600)


for i in range(4):
  t.forward(200)
  t.left(90)
  
  
t.penup()
t.goto(100 , 100)
#Pour abaisser le curseur
t.pendown()

t.pencolor("orange")
t.fillcolor("yellow")

t.circle(60)

#def moveForward():
  
  
def moveBackward():
  print("Gauche")
  t.backward(50)
  
def turnLeft():
  print("Gauche")
  t.left(50)
  
def turnRight():
  t.right(50)


while True:
  windows.listen()
  windows.onkeypress(moveForward, "Right")
  windows.onkeypress(moveBackward, "Left")
  windows.onkeypress(turnLeft, "Up")
  windows.update()
  time.sleep(1)



turtle.done()