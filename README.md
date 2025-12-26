# Stochastic Procedural Texture Generation

Implémentation d'un algorithme de génération procédurale stochastique de textures basé sur la méthode décrite dans le papier de Deliot & Heitz. Cet algorithme permet de générer des textures procédurales à partir d'une texture d'entrée en utilisant un pavage hexagonal et des transformations statistiques.

## Description

Ce projet implémente une méthode de génération de textures procédurales qui transforme une texture d'entrée en une texture de sortie plus grande en utilisant :

- Une transformation statistique basée sur une distribution gaussienne
- Un pavage hexagonal pour la génération procédurale
- Une fonction de hachage pour le bruit stochastique
- Une interpolation barycentrique pour le mélange des valeurs

L'algorithme génère une texture de sortie deux fois plus grande que la texture d'entrée en préservant les caractéristiques statistiques de l'image originale.

## Prérequis

- Python 3.x
- NumPy
- SciPy
- Pillow (PIL)

## Installation

Installez les dépendances nécessaires :

```bash
pip install numpy scipy pillow
```

Ou créez un fichier `requirements.txt` avec le contenu suivant :

```
numpy
scipy
pillow
```

Puis installez avec :

```bash
pip install -r requirements.txt
```

## Utilisation

1. Placez votre texture d'entrée dans le répertoire du projet et nommez-la `texture.jpg`

2. Exécutez le script :

```bash
python app.py
```

3. La texture générée sera sauvegardée sous le nom `output.jpg` dans le même répertoire

## Paramètres

Le script contient plusieurs paramètres configurables en haut du fichier `app.py` :

- `GAUSSIAN_AVERAGE` : Moyenne de la distribution gaussienne (par défaut : 0.5)
- `GAUSSIAN_STD` : Écart-type de la distribution gaussienne (par défaut : 1/6)
- `LUT_LENGTH` : Longueur de la table de correspondance (par défaut : 256)
- `OUTPUT_SCALE_FACTOR` : Facteur d'échelle de la texture de sortie (par défaut : 2)

## Fonctionnement

L'algorithme fonctionne en plusieurs étapes :

1. **Transformation T** : Convertit les valeurs de pixels de chaque canal (R, G, B) en valeurs suivant une distribution gaussienne en triant les pixels par intensité et en les mappant à des quantiles gaussiens.

2. **Transformation inverse Tinv** : Crée une table de correspondance (LUT) qui permet de convertir les valeurs gaussiennes en valeurs d'intensité d'origine.

3. **Pavage hexagonal** : Utilise un pavage hexagonal pour déterminer les coordonnées barycentriques et les sommets des triangles pour chaque pixel de sortie.

4. **Fonction de hachage** : Génère des valeurs stochastiques à partir des coordonnées des sommets pour créer de la variation dans la texture.

5. **Interpolation et reconstruction** : Mélange les valeurs gaussiennes des trois sommets en utilisant les poids barycentriques, puis convertit le résultat en valeur d'intensité finale via la LUT.

## Structure du projet

```
stochastic-procedural-texture-gen/
├── app.py                 # Script principal
├── texture.jpg            # Texture d'entrée (à fournir)
├── output.jpg             # Texture de sortie (générée)
└── results/               # Dossier contenant des exemples de résultats
    ├── texture-*.jpg      # Textures d'entrée d'exemple
    └── output-*.jpg       # Textures de sortie correspondantes
```

## Notes techniques

- La texture d'entrée doit être au format JPEG et nommée `texture.jpg`
- La texture de sortie est générée avec un facteur d'échelle de 2 (largeur et hauteur doublées)
- L'algorithme traite chaque canal de couleur (R, G, B) indépendamment
- La longueur minimale de la LUT est de 256 pour correspondre aux niveaux d'intensité 8 bits (0-255)

## Références

Cet algorithme est basé sur les travaux de Deliot & Heitz concernant la génération procédurale stochastique de textures.

## Licence

Ce projet est fourni tel quel, sans garantie d'aucune sorte.

