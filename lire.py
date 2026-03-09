import os
import random
'''
Entre = input("Entrez une phrase : ")

if os.path.exists("lecture.txt"):
   fichier = open("lecture.txt", "a")
   fichier.write(Entre)
else :
  with open("lecture.txt", "w") as fd:
    fd.write(Entre)
'''
'''
print("-------exo7-------") 
mdp = 'pwd' 

fichier = open("index.html", "r")
for ligne in fichier:
  if mdp in ligne:
    print(ligne)
'''


'''
print("-------exo8-------")

randnum = random.randint(1 , 50)
print (randnum)

userguess = int(input("Essayé de deviner un nombre :"))
  
MaxTry = 3 


if userguess == randnum:
    print("Et nous avons un gagnant bravo !!!") 
elif userguess <= randnum:
    print("Vous etes proches")
elif userguess >= randnum:
  print("Vous etes loin")



print("-------exo9-------")
'''



 

     
