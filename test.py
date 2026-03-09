
'''num1 = 20

num2 = 3

num3 = num1 * num2

num4 = num1 / num2

result = round(num4 + num3 - 11.111 , 2)

print(num1)
print(num2)
print(num3)
print(num4)
print (result)


print("--------------------Les chaines de caractères---------------------")


hello = "Hello Steeve !"
print(hello[:]) #Pour afficher toute la chaine de caractere

print(hello[2:]) #j'affiche la chaine a partir du deuxieme index

print(hello[-2:]) #Ca marche aussi avec les indexes négatifs


print(hello[-1: -8]) #Ici rien ne s'affiche

print(hello[4:10]) #dAffiche les nombre de l'index 4 a 10

print(hello[::2]) #Pour afficher un caractere surn deux ainsi de suite


name = "Steeve"
age = 94

 
#Trois maniere de formater des chaines de caractère
print(F"Bonjour je suis {name} et j'ai {age} ans")

ma_liste = [name, age, num1, 5656.65656, [[[[]]]], "Hello world"]


ma_liste.append("Chien")#Pour ajouter
ma_liste.remove("Hello world") #Pour supprimer un élémen,t de la liste
ma_liste.clear()#Pour vider la liste

print(ma_liste)






Liste_de_nom = ["Steevey", "Jeffrey", "Randy", "Anna", "Montana"]
Liste_de_nom.sort()
print(Liste_de_nom)

#Le tuple est un liste qu'on ne peu pas modifier 
un_tuple = (1,2,3)

print(un_tuple)
print(un_tuple[2])

#Unset est un conteneur ordoné modfiabkle mais non indexable
un_set = {1,2,3}
un_set.add(10)
un_set.add(20)
un_set.add(30)
un_set.remove(10)

print(un_set)


#Un dictionnaire
un_dico = {'key': 'value', 'nom' : 'Titi' , 'ville' : 'Nantes', 'code_postal': 44566}
print(un_dico['nom'])
print(un_dico.keys())
print(un_dico.values())




print("--------------------Les conditions---------------------")



age = 10

if age == 0:
  print("Félicitation ! vous etes nés !")
elif age <= 7:
  print("Vous etes jeune")
elif age == 16:
  print("Vous pouvez passer le code")
elif age >= 18:
  print("Félicitation vous etes majeur")
  if(age) in(20 , 50 , 46 , 78 , 100):
    print("Félicitation pour cette nouvelle décénie")
else:
  print("Age invalide")
  

str = "Vous etes majeurs !" if age >= 18 else "Vous etes mineurs"
print(str)
  
  
  
  
print("--------------------Les boucles---------------------")

Liste_de_nom = ["Steevey", "Jeffrey", "Randy", "Anna", "Montana"]

#les boucles whiles
i = 0
while i < 0:
  print(i)
  i += 1
  
#La boucle for
i = 0
for i in Liste_de_nom:
  print(i)
  
#La boucle for ... range

for i in range(5, 10):
  print(i)


print("--------------------Les entrées---------------------")

value = input("Entrez qqch :")
print(value)



print("--------------------Exercice---------------------")


val1 = int(input("Entrez une longeur : "))

val2 = int(input("Entrez une largeur : "))

calcAire = val1 * val2

print ("Ce resctangle a pour aire" , calcAire)


perim = 2* val1 + 2*val2
print("Le périmetre du rectangle est " , perim)

print("--------------------Affichage de votre rectangle---------------------")

print("Carré", val1, "X", val2)

for i in range(val2):
  print (" -" * val1)
  


print("--------------------Les fonctions---------------------")

#La fonction input() permet de lire 

#Fonction basique
def direBonjour():
  print("bonjour")
  
#Fonction qui prend deux parametre

def deux(a , b):
  print(1 , 3)
  
res = direBonjour()
print
#Une fonction qui retourne plusieurs parametre
'''

'''
print("--------------------Exos 4---------------------")
  
val1 = int(input("Entrez une longeur : "))

val2 = int(input("Entrez une largeur : "))
  
  
def calcAire(val1, val2):
  print("Ce resctangle a pour aire", val1 * val2)

def perim(val1, val2):
  print("Le périmetre du carré est :", 2*val1 + 2*val2)
    
def AfficherForme(*args):
  for i in range(val2):
    print(" -" * val2)
  
  
aire = calcAire(val1, val2)
permi = perim(val1, val2)
forme = AfficherForme()
'''

print("--------------------Exos 5---------------------")
'''
entre = input("Entrez votre phrase : ")

def compterNbCara(entre):
  print("Votre phrase a ", len(entre), "caractère")
  return 

retour = compterNbCara(entre)
'''

'''
def count_char(sentence):
  if sentence == '':
    return 0
  return 1 + count_char(sentence[1:])
''' 
'''
# Etape 2 
sentence = input("Votre phrase : ")

def palindrom(sentence):
  if sentence == '' or len(sentence) == 1:
    print("La phrase ", sentence , "est un palindrome")
    return True
  elif sentence[0] != sentence[-1]:
    print("Cette phrase", sentence, "n'est pas un palindrome")
    return False
palindrom(sentence[1: -1])
  

'''
import os

with open("fichier.txt", "w") as fd:
  fd.write("Ca manipule des bites")
  