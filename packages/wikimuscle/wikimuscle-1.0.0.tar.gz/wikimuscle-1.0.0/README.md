# WikiMuscle API

## Qu'est-ce que WikiMuscle API ?

WikiMuscle API est un package Python (non officiel) permettant de récupérer des exercices en fonction des muscles, équipements ou difficultés ciblés.

## Installation du package

Pour installer le package WikiMuscle, il est nécessaire d'utiliser Python à partir de la version 3.6. Vous pouvez l'installer via la commande suivante :

```
pip install wikimuscle
```

## Utilisation de la classe principale `Wiki`

La classe `Wiki` prend en paramètre le chemin pour l'installation de la base de données. Il n'est pas nécessaire de créer un dossier pour la base de données, car la classe `Wiki` s'en charge automatiquement.

Par défaut, le paramètre est `None`, ce qui utilise le répertoire de travail courant (cwd). Il est également possible de formater le chemin souhaité avec la classe `Path` du module `pathlib`, ou de passer une chaîne de caractères `PathLike` représentant le chemin.

La classe `Wiki` hérite de la classe `ApiWiki`, qui gère principalement la logique pour l'interaction avec l'API.

### Méthodes disponibles via la classe `Wiki` :

- **`get`** : Interagit directement avec l'API.

  - Paramètres :
    - `muscles` : Optional[List[MusclesCategory]]
    - `equipments` : Optional[List[EquipmentsCategory]]
    - `difficulties` : Optional[List[DifficultiesCategory]]
    - `path_json` : str
    - `create_dir` : bool
    - `dir_exercises` : Optional[Union[str, PathLike, Path]] = None
  - Retourne : Un tuple composé d'un dictionnaire (key = nom de l'exercice, value = IResponseExercise) et d'une liste (List[IResponseExercise]).

- **`create_dir_exercise`** : Crée un répertoire pour un exercice unique (vidéo de l'exercice et fichier texte avec les étapes).

  - Paramètres :
    - `base_path` : Optional[Union[str, PathLike, Path]]
    - `element` : Optional[IResponseExercise]
  - Retourne : `None`.

- **`create_dir`** : Crée un répertoire complet des exercices récupérés à l'aide de la méthode `get`.
  - Paramètres :
    - `base_path` : Optional[Union[str, PathLike, Path]]
    - `data` : Optional[List[IResponseExercise]]
  - Retourne : `None`.

### Exemple d'utilisation de la classe `Wiki`

```python
from wikimuscle import Wiki

# Initialisation sans chemin, utilise la valeur par défaut
wiki = Wiki()
```

Une fois initialisée, un dossier **"database"** est créé à l'emplacement spécifié.

### La méthode `get` de la classe `Wiki`

```python
from wikimuscle import Wiki

wiki = Wiki()

# Récupère les exercices et crée un dossier "exercises" contenant les données
response_dict, response_list = wiki.get(
    muscles=["Biceps"],
    equipments=["Poids corporel"],
    difficulties=["Débutant"],
    create_dir=True,
    dir_exercises="exercises"
)
```

### La méthode `create_dir_exercise` de la classe `Wiki`

```python
from wikimuscle import Wiki

wiki = Wiki()

# Récupération des exercices
response_dict, response_list = wiki.get(
    muscles=["Biceps"],
    equipments=["Poids corporel"],
    difficulties=["Débutant"]
)

# Crée un dossier contenant les données d'un exercice unique
element = response_list[0]
wiki.create_dir_exercise("exemple", element)
```

### La méthode `create_dir` de la classe `Wiki`

```python
from wikimuscle import Wiki

wiki = Wiki()

# Récupération des exercices
response_dict, response_list = wiki.get(
    muscles=["Biceps"],
    equipments=["Poids corporel"],
    difficulties=["Débutant"]
)

# Crée un répertoire "exemples" contenant tous les exercices
wiki.create_dir("exemples", response_list)
```

### Les interfaces

Voici les interfaces et sous interfaces :

```python
MusclesCategory = Literal['Biceps', 'Biceps Longue Portion', 'Biceps court', 'Traps (milieu du dos)', 'Bas du dos', 'Abdominaux', "Bas de l'abdomen", 'Abdominaux Supérieurs', 'Mollets', 'Tibialis', 'Soleus', 'Gastrocnémien', 'Avant-bras', 'Extenseurs du Poignet', 'Fléchisseurs du Poignet', 'Fessiers', 'Gluteus Medius', 'Grand Fessier', 'Ischio-jambiers', 'Ischio-jambiers médiaux', 'Ischio-jambiers latéraux', 'Grands dorsaux', 'Épaules',
                          'Deltoides Latéraux', 'Deltoïde Antérieur', 'Deltoïde Postérieur', 'Triceps', 'Triceps Longue Portion', 'Triceps Latéral', 'Triceps - Tête Médiane', 'Trapèzes', 'Trapèzes Supérieurs', 'Traps inférieurs', 'Quadriceps', 'Cuisse Intérieure', 'Quadriceps Internes', 'Quadriceps Externe', 'Rectus Femoris', 'Poitrine', 'Grand Pectoral', 'Milieu et Bas de la Poitrine', 'Obliques', 'Mains', 'Pieds', 'Épaules Avant', 'Épaules Arrière', 'Cou Nack', 'Aine']

EquipmentsCategory = Literal['Barre', 'Haltères', 'Poids corporel', 'Machine', 'Ballon de Médecine', 'Haltères Kettlebell',
                             'Étirements', 'Câbles', 'Groupe', 'Assiette', 'TRX', 'Yoga', 'Ballon Bosu', 'Vitruvian', 'Cardio', 'Smith-Machine', 'Récupération']

DifficultiesCategory = Literal['Débutant', 'Intermédiaire', 'Avancé', 'Novice']


class _IMuscles(TypedDict):
    id: int
    name: str
    name_en_us: str
    scientific_name: None
    url_name: str
    description: str
    description_us: str


class _IGrips(TypedDict):
    id: int
    name: str
    name_en_us: str
    description: str
    description_en_us: str
    url_name: str


class _ICategory(TypedDict):
    id: int
    name: str
    name_en_us: str


class _IDifficulty(TypedDict):
    id: int
    name: str
    name_en_us: str


class _IForce(TypedDict):
    id: int
    name: str
    url_name: str
    name_en_us: str
    description: str
    description_en_us: str


class _IMechanic(TypedDict):
    id: int
    name: str
    url_name: str
    name_en_us: str
    description: str
    description_en_us: str


class _IImage(TypedDict):
    id: int
    order: int
    src: Optional[str]
    og_image: Optional[str]
    original_video: Optional[str]
    unbranded_video: Optional[str]
    branded_video: Optional[str]
    gender: int
    exercise: int


class _IStep(TypedDict):
    id: int
    order: int
    text: str
    text_en_us: str
    exercise: int


class _ITargetURL(TypedDict):
    male: str
    female: str


class IResponseExercise(TypedDict):
    muscles: List[_IMuscles]
    muscles_primary: Optional[List[_IMuscles]]
    muscles_secondary: Optional[List[_IMuscles]]
    muscles_tertiary: Optional[List[_IMuscles]]
    grips: List[_IGrips]
    category: _ICategory
    additional_categories: List[_ICategory]
    difficulty: _IDifficulty
    force: _IForce
    mechanic: _IMechanic
    images: List[_IImage]
    correct_steps: List[_IStep]
    target_url: _ITargetURL
    male_images: List[_IImage]
    female_images: List[_IImage]
    name: str
    slug: str
```
