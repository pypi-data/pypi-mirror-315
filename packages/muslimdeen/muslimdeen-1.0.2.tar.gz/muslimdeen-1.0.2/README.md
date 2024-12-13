# MuslimDeenV2

## Qu'est-ce que MuslimDeenV2 ?

MuslimDeenV2 est un package Python dédié à la gestion des métadonnées des sourates du Coran, des noms d'Allah, des cinq piliers de l'Islam, des prières, des ablutions et du calcul de la zakat.  
Il a pour objectif de fournir des données structurées et précises, espérant ainsi être un bien pour la communauté musulmane et toutes les personnes souhaitant s'informer sur l'Islam.  
Je demande à Allah que ce package soit bénéfique pour toute la communauté, que nos intentions soient sincères et vouées uniquement à Lui, car tout le bien Lui appartient et tout le mal découle de nos propres actions.  
Puisse Allah nous guider, nous accorder la sincérité, et nous permettre d'avoir une bonne fin.

## Installation du package

Pour installer le package MuslimDeenV2, il est nécessaire que la version de Python soit égale ou supérieure à Python 3.6. Vous pouvez l'installer via la commande :

```python
pip install muslimDeenV2
```

## Utilisation de la classe principale MuslimDeen

La classe `MuslimDeen` prend en paramètre le chemin pour l'installation de la base de données. Il n'est pas nécessaire de créer un dossier pour la base de données, la classe `MuslimDeen` s'en charge.  
Par défaut, le paramètre est `None`, ce qui utilise le répertoire de travail courant (cwd). Il est également possible de formater le chemin souhaité avec la classe `Path` du module `pathlib`, ou de passer une chaîne de caractères représentant le chemin.

Cette classe contient toutes les autres classes du package que nous décrirons ci-dessous :

- **`Config`** : instance de configuration qui fournit les URLs des sources utilisées.
- **`MetaSurahs`** : instance des métadonnées des sourates du Coran.
- **`NameOfAllah`** : instance des 99 noms d'Allah.
- **`QuranReader`** : instance contenant le Coran avec toutes les sourates en arabe et en français.
- **`Ablutions`** : instance des étapes des ablutions (avec distinction par genre pour les images).
- **`Salat`** : instance des étapes des prières obligatoires.
- **`PillarsOfIslam`** : instance des 5 piliers de l'Islam avec une description détaillée.
- **`Zakat`** : instance fournissant des URLs vers des calculateurs de zakat (un calculateur interne est en cours de développement).

### Exemple d'utilisation de la classe MuslimDeen

```python
from muslimDeenV2 import MuslimDeen
muslimDeen = MuslimDeen()  # Initialisation sans chemin, utilise la valeur par défaut (None)
```

Ou avec `pathlib` :

```python
from muslimDeenV2 import MuslimDeen
import pathlib as plib
path = plib.Path(__file__).parent
muslimDeen = MuslimDeen(path)
```

Ou avec un chemin absolu en `str` :

```python
from muslimDeenV2 import MuslimDeen
path = "chemin/de/votre/choix"
muslimDeen = MuslimDeen(path)
```

Une fois initialisée, un dossier "database" est créé à l'emplacement spécifié.

### Les exceptions

1. **ByError**  
   La classe `ByError` lève une exception si le paramètre `by` dans la méthode `get_by` des classes contenant cette méthode utilise un nom de colonne invalide.

#### Exemple d'application :

```python
from muslimDeenV2 import ByError, MuslimDeen

muslimDeen = MuslimDeen()
metasurahs = muslimDeen.meta_surahs()  # Renvoie la classe MetaSurahs

# Effectue une recherche avec un nom de colonne invalide
try:
    response = metasurahs.get_by(by="invalid_col", value="some_value")
except ByError:
    print("Le paramètre 'by' est invalide")
```

## La classe Config

La méthode `config_url` de la classe `MuslimDeen` renvoie l'instance de configuration contenant les URLs des sources utilisées dans le projet.

#### Exemple d'utilisation :

```python
from muslimDeenV2 import MuslimDeen
muslimDeen = MuslimDeen()
config = muslimDeen.config_url()  # Renvoie l'instance de Config
```

Il est également possible d'appeler cette classe sans passer par la classe principale en l'important directement :

```python
from muslimDeenV2 import Config
config = Config()  # Instance de Config sans passer par la classe principale
```

### Méthodes de la classe Config

La classe `Config` ne contient que des méthodes statiques. Voici une liste non exhaustive :

- **`url_meta_surahs_v1()`** : retourne l'une des sources pour les métadonnées des sourates.
- **`url_data_quran()`** : retourne la source du fichier JSON du Coran en arabe et traduit en français.
- **`author_quran_github()`** : retourne le profil GitHub du contributeur et auteur du fichier JSON du Coran.
- **`url_99_names_of_allah()`** : renvoie la source utilisée pour les 99 noms d'Allah.

## La classe MetaSurahs

La méthode `meta_surahs` de la classe `MuslimDeen` renvoie l'instance des métadonnées des sourates du Coran

### Méthodes de la classe MetaSurahs

Voici les méthodes disponibles dans cette classe `MetaSurahs` :

- **`df`** : retourne la DataFrame pandas des métadonnées.
- **`columns_names`** : retourne la liste des noms des colonnes présentes dans la DataFrame pandas.
- **`get_by()`** : prend les paramètres `by` (nom de la colonne) et `value` (valeurs à filtrer, qui peuvent être un tuple, une liste ou une chaîne de caractères). Le paramètre `respapi` (booléen, True ou False, par défaut True) détermine si la méthode retourne une DataFrame pandas (False) ou une liste de dictionnaires de `TypedMetaSurah` (True).
- **`get_all()`**: prend le paramètre `respapi` (boolean, True ou False). Renvoie la DataFrame complète si `respapi` est False, ou une liste de dictionnaires typés à `TypedMetaSurah` si `respapi` est True.

#### Typage des métadonnées des sourates

```python
class TypedMetaSurah(TypedDict):
    position: int
    name_arabic: str
    name_phonetic: str
    name_english: str
    name_french: str
    revelation_type: str
    number_of_ayahs: int
    sajdas_recommended: bool
    sajdas_obligatory: bool

ListMetaSurahs = List[TypedMetaSurah]
```

### Exemple d'utilisation de la classe MetaSurahs

Dans ces exemples, on va utiliser les deux méthodes (`get_by`, `get_all`) et voir les possibilités de retour.

```python
from muslimDeenV2 import MuslimDeen

muslimDeen = MuslimDeen()
metasurahs = muslimDeen.meta_surahs()  # Renvoie l'instance MetaSurahs

response_all = metasurahs.get_all(respapi=True)  # Par défaut, respapi est True

print(response_all)  # Type de variable : Union[ListMetaSurahs, DataFrame]

response_by = metasurahs.get_by(by="some_by", value="some_value", respapi=True)
response_by_2 = metasurahs.get_by(by="some_by", value=("value1", "value2", "value3"), respapi=True)

print(response_by)  # Type de variable : Union[ListMetaSurahs, DataFrame, None]
print(response_by_2)  # Type de variable : Union[ListMetaSurahs, DataFrame, None]
```

## La classe NamesOfAllah

La méthode `names_of_allah` de la classe `MuslimDeen` renvoie une instance des noms d'Allah.

### La classe NamesOfAllah a des ERREURS DONC ATTENTION (Déconseiller à l'utilisation)

### Méthodes de la classe NameOfAllah

Voici les méthodes disponibles dans cette classe `NameOfAllah` :

- **`df`** : Retourne la DataFrame pandas des noms d'Allah.
- **`columns_names`** : Retourne la liste des noms des colonnes présentes dans la DataFrame pandas.
- **`get_by()`** : Prend les paramètres `by` (nom de la colonne) et `value` (valeurs à filtrer, qui peuvent être un tuple, une liste ou une chaîne de caractères). Le paramètre `respapi` (booléen, `True` ou `False`, par défaut `True`) détermine si la méthode retourne une DataFrame pandas (`False`) ou une liste de dictionnaires de `TypedNameOfAllah` (`True`).
- **`get_all()`** : Prend le paramètre `respapi` (booléen, `True` ou `False`). Renvoie la DataFrame complète si `respapi` est `False`, ou une liste de dictionnaires typés en `TypedNameOfAllah` si `respapi` est `True`.

#### Typage des noms d'Allah

```python
class TypedNameOfAllah(TypedDict):
    number: Union[str, int]
    arabic_name_img: str
    name_phonetic: str
    name_french: str
    more_info_link: str
    description: str

ListNamesOfAllah = List[TypedNameOfAllah]
```

### Exemple d'utilisation de la classe NamesOfAllah

Dans ces exemples, on utilise les méthodes (`get_by`, `get_all`) pour voir les possibilités de retour.

```python
from muslimDeenV2 import MuslimDeen

muslimDeen = MuslimDeen()
names_of_allah = muslimDeen.names_of_allah()  # Renvoie l'instance de NamesOfAllah

response_all = names_of_allah.get_all(respapi=True)  # Par défaut, respapi est True

print(response_all)  # Type de variable : Union[List[TypedNameOfAllah], DataFrame]

response_by = names_of_allah.get_by(by="some_by", value="some_value", respapi=True)
response_by_2 = names_of_allah.get_by(by="some_by", value=("value1", "value2", "value3"), respapi=True)
print(response_by)  # Type de variable : Union[List[TypedNameOfAllah], DataFrame, None]
print(response_by_2)  # Type de variable : Union[List[TypedNameOfAllah], DataFrame, None]
```

## La classe QuranReader

La méthode `quran_reader` de la classe `MuslimDeen` renvoie une instance du Coran en arabe et de sa traduction en français.

### Méthodes de la classe QuranReader

Voici les méthodes disponibles dans cette classe `QuranReader` :

- **`revelation_type_enum()`** : Retourne l'énumération des types de révélations (Médinoise ou Mecquoise).
- **`quran`** : Retourne les données complètes du Coran, typé en `QuranData`.
- **`sourate_by_number`** : Retourne un dictionnaire des sourates indexées par leur numéro de position, typé en `Dict[int, QuranSourateData]`.
- **`sourate_by_name_fr`** : Retourne un dictionnaire des sourates indexées par leur nom en français, typé en `Dict[str, QuranSourateData]`.
- **`sourate_by_name_arabic`** : Retourne un dictionnaire des sourates indexées par leur nom en arabe, typé en `Dict[str, QuranSourateData]`.

- **`search_by_number()`** : Prend en paramètre le numéro de la sourate. Retourne `None` si la sourate n'est pas trouvée, sinon retourne `QuranSourateData`.

- **`search_by_name_fr()`** : Prend en paramètre le nom de la sourate en français. Retourne `None` si la sourate n'est pas trouvée, sinon retourne `QuranSourateData`.

- **`search_by_name_arabic()`** : Prend en paramètre le nom de la sourate en arabe. Retourne `None` si la sourate n'est pas trouvée, sinon retourne `QuranSourateData`.

- **`get_all_by_type_revelation()`** : Prend en paramètre soit une des valeurs de l'énumération `RevelationType` soit un `Literal` de 'Médinoise' ou 'Mecquoise'. Retourne une liste des sourates en fonction du type de révélation, typée en `List[QuranSourateData]`.

#### Typage du Coran

```python
class QuranVersetData(TypedDict):
    position: int
    text: str
    position_ds_sourate: int
    juz: int
    manzil: int
    page: int
    ruku: int
    hizbQuarter: int
    sajda: bool
    text_arabe: str

class QuranSourateData(TypedDict):
    position: int
    nom: str
    nom_phonetique: str
    englishNameTranslation: str
    revelation: str
    versets: List[QuranVersetData]
    nom_sourate: str

class QuranData(TypedDict):
    sourates: List[QuranSourateData]


class RevelationType(Enum):
    MEDINOIS = "Medinois"
    MECQUOISE = "Mecquoise"
```

### Exemple d'utilisation de la classe QuranReader

Dans ces exemples, on utilisera quelques méthodes disponibles pour voir les possibilités de retour.

```python
from muslimDeenV2 import MuslimDeen

muslimDeen = MuslimDeen()
quranReader = muslimDeen.quran_reader()

get_revelation_type = quranReader.get_all_by_type_revelation('Mecquoise')
print(get_revelation_type)  # Retourne une liste de toutes les sourates révélées à la Mecque

resp_name_fr = quranReader.search_by_name_fr('Les hommes')
print(resp_name_fr)  # Retourne le dictionnaire typé QuranSourateData, la sourate existe donc pas de None.

resp_error_position = quranReader.search_by_number(115)
print(resp_error_position)  # Retourne None car aucune sourate n'existe avec la position 115
```

## La classe Ablutions

La méthode `ablutions` de la classe `MuslimDeen` renvoie une instance de la classe Ablutions pour les ablutions selon le genre (homme ou femme). Le paramètre `gender` accepte deux valeurs possibles : `'man'` ou `'women'`. Par défaut, le paramètre est défini sur `'man'`.

### Méthodes de la classe Ablutions

Voici les méthodes disponibles dans cette classe `Ablutions` :

- **`df`** : Retourne la DataFrame pandas des ablutions.
- **`data()`** : Prend le paramètre `respapi` (booléen, `True` ou `False`). Renvoie la DataFrame complète si `respapi` est `False`, ou une liste de dictionnaires typés en `TypedAblution` si `respapi` est `True`.

#### Typage des ablutions

```python
class TypedAblution(TypedDict):
    step: str
    description: str
    nb_repetition: int
    references: str
    img: str

ListTypedAblutions = List[TypedAblution]
```

### Exemple d'utilisation de la classe Ablutions

Dans ces exemples, on utilisera la méthode `data()` pour voir les possibilités de retour.

```python
from muslimDeenV2 import MuslimDeen

muslimDeen = MuslimDeen()
ablutions_man = muslimDeen.ablutions(gender='man')
ablutions_women = muslimDeen.ablutions(gender='women')
data_man = ablutions_man.data(respapi=True)
data_women = ablutions_women.data(respapi=True)

print(data_man)  # Retourne une liste de dictionnaires typés TypedAblution

print(data_women)  # Retourne une liste de dictionnaires typés TypedAblution
```

## La classe Salat

La méthode `salat` de la classe `MuslimDeen` renvoie une instance des étapes de toutes les prières obligatoires en Islam (les 5 prières quotidiennes).

### Méthodes de la classe Salat

Voici les méthodes disponibles dans la classe `Salat` :

- **`df`** : Retourne la DataFrame avec les informations essentielles des prières obligatoires.
- **`fajr`** : Retourne les étapes détaillées de la prière `Fajr`, typage de retour `TypedSalat`.
- **`dohr`** : Retourne les étapes détaillées de la prière `Dohr`, typage de retour `TypedSalat`.
- **`asr`** : Retourne les étapes détaillées de la prière `Asr`, typage de retour `TypedSalat`.
- **`maghrib`** : Retourne les étapes détaillées de la prière `Maghrib`, typage de retour `TypedSalat`.
- **`isha`** : Retourne les étapes détaillées de la prière `Isha`, typage de retour `TypedSalat`.

#### Typage des étapes de la prière

```python
class TypedInfosSalat(TypedDict):
    number: int
    name: str
    nb_rakat: int
    description_salat: str
    link_video: str

ListTypedInfosSalat = List[TypedInfosSalat]
```

### Exemple d'utilisation de la classe Salat

Dans cet exemple, on utilise la méthode `fajr`. L'utilisation est valable pour toutes les autres méthodes également.

```python
from muslimDeenV2 import MuslimDeen

muslimDeen = MuslimDeen()
salat = muslimDeen.salat()

pray_fajr = salat.fajr

print(pray_fajr)  # Typage variable : TypedSalat
```

## La classe PillarsOfIslam

La méthode `pillars_of_islam` de la classe `MuslimDeen` renvoie une instance de la classe PillarsOfIslam pour les 5 piliers de l'Islam avec une description détaillée pour chaque pilier.

### Méthodes de la classe PillarsOfIslam

Voici les méthodes disponibles dans cette classe `PillarsOfIslam` :

- **`shahada`** : Retourne un dictionnaire contenant les données du pilier de l'attestation de foi, typage de retour `TypedPillarOfIslam`.
- **`salat`** : Retourne un dictionnaire contenant les données du pilier de la prière, typage de retour `TypedPillarOfIslam`.
- **`zakat`** : Retourne un dictionnaire contenant les données du pilier de la zakat, typage de retour `TypedPillarOfIslam`.
- **`sawm`** : Retourne un dictionnaire contenant les données du pilier du jeûne, typage de retour `TypedPillarOfIslam`.
- **`hajj`** : Retourne un dictionnaire contenant les données du pilier du pèlerinage à la Mecque, typage de retour `TypedPillarOfIslam`.

#### Typage des piliers de l'Islam

```python
class TypedPillarOfIslam(TypedDict):
    number: Union[int, str]
    name: str
    description: str
    sources: List[str]
    more_infos: List[str]
```

### Exemple d'utilisation de la classe PillarsOfIslam

Dans cet exemple, on utilise la méthode `shahada`. L'utilisation est valable pour toutes les autres méthodes également.

```python
from muslimDeenV2 import MuslimDeen

muslimDeen = MuslimDeen()
pillars_of_islam = muslimDeen.pillars_of_islam()

pillar_shahada = pillars_of_islam.shahada

print(pillar_shahada)  # Typage variable : TypedPillarOfIslam
```

## La classe Zakat

La méthode `zakat` de la classe `MuslimDeen` renvoie une instance de la Zakat, qui (pour l'instant) renvoie des liens vers des sites fiables pour calculer sa zakat.

### Méthodes de la classe Zakat

Voici les méthodes disponibles dans la classe `Zakat` :

- **`link_zakat()`** : Renvoie des URLs pour calculer sa zakat.

### En cours de développement

La classe `Zakat` est en cours de développement afin de créer notre propre calculateur de zakat.

#### Exemple d'utilisation de la classe Zakat

Dans cet exemple, on utilise la méthode `link_zakat()`.

```python
from muslimDeenV2 import MuslimDeen

muslimDeen = MuslimDeen()
zakat = muslimDeen.zakat()
link_zakat = zakat.link_zakat()

print(link_zakat)  # Typage variable : List[str]
```
