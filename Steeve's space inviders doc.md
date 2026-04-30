# Steeve's Space Invaders 

Bienvenue dans **Steeve's Space Invaders**, un jeu d'arcade classique revisité, développé en Python avec la bibliothèque Turtle.

##  Description
Défendez la galaxie contre des vagues d'ennemis incessantes ! Pilotez votre vaisseau, détruisez les envahisseurs et récupérez des bonus pour survivre le plus longtemps possible.

##  Commandes
| Touche | Action |
| :--- | :--- |
| **Flèches Directionnelles** | Déplacer le vaisseau (Haut, Bas, Gauche, Droite) |
| **Espace** | Tirer un projectile |
| **R** | Recommencer la partie (après un Game Over) |

##  Caractéristiques du Jeu
- **Système de Vies** : Vous commencez avec 3 vies.
- **Ennemis Variés** : Plusieurs types d'ennemis avec des apparences différentes.
- **Bonus** :
  -  **Tortue verte** : Ajoute une vie supplémentaire.
  -  **Cercle jaune** : Bonus de +50 points.
- **Explosions** : Effets de particules lors de la destruction des ennemis.
- **Ambiance Sonore** : Musique de fond et bruitages d'explosions (si `pygame` est installé).

## Installation et Lancement

1. **Prérequis** :
   - Python 3 installé.
   - (Optionnel) La bibliothèque `pygame` pour les sons : `pip install pygame`.

2. **Lancer le jeu** :
   Exécutez le fichier principal :
   ```bash
   python "space_invaders eval.py"
   ```

## Structure du Projet
- `space_invaders eval.py` : Le script principal du jeu.
- `images/` : Dossier contenant les graphismes (vaisseau, ennemis, fond d'écran).
- `sounds/` : Dossier contenant les effets sonores et la musique.

---
*Bonne chance, commandant !* 
