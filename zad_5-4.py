from anytree import Node, RenderTree
from faker import Faker
import random
import datetime

fake = Faker('pl_PL')

class Movies:
    def __init__(self, title, year):
        self.title, self.year = title, year
 
    def play(self, views, view = 1):
        views += view
        self.views = views
    
    def genres(self, genre):
        self.genre = genre

    def __str__(self):
        return f'"{self.title.title()}" ({self.year}), Kategoria: {self.genre}, Oglądalność: {self.views}'

class Series(Movies):
    def __init__(self, season_number, episode_number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.season_number, self.episode_number = season_number, episode_number

    @property
    def ep_sum(self):
        eps = random.randrange(12, 24, 2)
        self.eps = eps
        return self.eps * ((self.season_number) - 1) + self.episode_number

    def __str__(self):
        return f'"{self.title.title()}" ({self.year}), Kategoria: {self.genre}, Odcinek: {self.title.title()} S{self.season_number:02}E{self.episode_number:02}, Oglądalność: {self.views}'

library = []
for i in range(10):
    library.append(Movies(title = fake.word(), year = fake.year()))
    library.append(Series(title = fake.word(), year = fake.year(), season_number = fake.random_digit_not_null(), episode_number = fake.random_int(1,20)))

for x in library:
    views = 0
    x.play(views)
    genre = ['Komedia', 'Dramat', 'Akcja', 'Horror']
    x.genres(random.choice(genre))

def call_generate_views(func):
    def multiple():  
        for i in range(10):
            func()
    return multiple()

@call_generate_views    
def generate_views():
    random.shuffle(library)
    library[0].views += random.randrange(1, 100)

def search(x):
    for i in range(len(library)):
        if library[i] == x:
            print(f"Wynik wyszykiwania dla: '{x.title.upper()}'", x, sep = '\n')

main = Node("\nBiblioteka filmów i seriali\n")
films = Node("Filmy", parent = main)
series = Node("Seriale", parent = main)

def get_movies():
    library[:] = sorted(library, key = lambda x: x.title)
    for x in library:
        if x.__class__.__name__ == 'Movies':          
            film = Node(f"{x}", parent = films)
get_movies()

def get_series():
    library[:] = sorted(library, key = lambda x: x.title)
    for x in library:
        if x.__class__.__name__ == 'Series':
            serie = Node(f"{x}", parent = series)
            ep_sum = Node(f"W sumie: sezonów - {x.season_number:01}, odcinków - {x.ep_sum}", parent = serie)
get_series()

def top_titles(num):
    library[:] = sorted(library, key = lambda x: x.views, reverse=True)
    print("Najpopularniejsze filmy i seriale dnia", datetime.date.today())
    print(*library[:num], sep = '\n')
    
for pre, fill, node in RenderTree(main):
    print(f"{pre}{node.name}")

print()
search(x)
print()
top_titles(3)
print()