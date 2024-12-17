from typing import TypedDict, List, Literal, Optional, Any


class ISubCategoriesUrl(TypedDict):
    name: str
    id_name: int


class ICategoriesUrl(TypedDict):
    muscles: List[ISubCategoriesUrl]
    category: List[ISubCategoriesUrl]
    difficulties: List[ISubCategoriesUrl]


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
