import os, random, time
from dataclasses import dataclass

MAP = """
###############
#.............#
#........#..G.#
#....#...#....#
#.####........#
#..........#..#
#.....#....####
#.S...#.......#
#.............#
###############
"""

START_SYMBOL = 'S'
END_SYMBOL = 'G'
ROUTE_SYMBOL = '+'

# Per iteration
NO_OF_ROUTES = 3
# Chance of mutation while following a route
ROUTE_RANDOM = 0.2
MAX_ROUTE_LENGTH = 30

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(
            self.x + other.x, self.y + other.y
        )

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def direction_to(self, other):
        return Point(other.x - self.x, other.y - self.y)

UP = Point(0,-1)
DOWN = Point(0,1)
LEFT = Point(1,0)
RIGHT = Point(-1,0)

class Game:

    def __init__(self, path=None):
        if path:
            # TODO; load from file
            pass
        else:
            rows = MAP.strip().split('\n')

        self.start = None
        self.end = None
        self.level = []
        for x, row in enumerate(rows):
            self.level.append([])
            for y, cell in enumerate(row):
                if cell == START_SYMBOL:
                    self.start = Point(x, y)
                    self.level[-1].append('.')
                elif cell == END_SYMBOL:
                    self.end = Point(x, y)
                    self.level[-1].append('.')
                else:
                    self.level[-1].append(cell)

    def print_route(self, route=[], clear=False):
        temp = [row[:] for row in self.level]

        for p in route:
            temp[p.x][p.y] = ROUTE_SYMBOL
        # Draw start and end point on top
        temp[self.start.x][self.start.y] = START_SYMBOL
        temp[self.end.x][self.end.y] = END_SYMBOL

        if clear:
            cls()
        for row in temp:
            print(' '.join(row))

    def animate_route(self, route=[]):
        for i in range(len(route)):
            self.print_route(route[:i], clear=True)
            time.sleep(0.2)

    def get_random_direction(self):
        return random.choice([UP, DOWN, LEFT, RIGHT])

    def valid_space(self, pos):
        if self.level[pos.x][pos.y] != '.':
            return False
        else:
            return True
        
    def get_direction(self, pos):
        """ Get a random direction that is valid from the given position """
        direction = self.get_random_direction()
        while not self.valid_space(pos + direction):
            direction = self.get_random_direction()
        return direction

    def get_random_route(self):
        """
        Get a random route of directions that either reaches the end or is
        MAX_ROUTE_LENGTH long
        """
        route = []
        pos = self.start
        # TODO; do not allow to go over own path
        # Will need to check do not trap self
        while pos != self.end and len(route) < MAX_ROUTE_LENGTH:
            pos += self.get_direction(pos)
            route.append(pos)

        return route

    def mutate_route(self, route):
        """
        Follow the directions given in a route but according to the ROUTE_RANDOM
        chance mutate the direction
        """
        new_route = []
        route.insert(0, self.start)
        pos = self.start
        count = 0
        while pos != self.end and len(new_route) < MAX_ROUTE_LENGTH:
            route_direction = route[count].direction_to(route[count+1])
            # If we hit that random chance or the current route is not valid
            if random.random() < ROUTE_RANDOM or not self.valid_space(pos + route_direction):
                pos += self.get_direction(pos)
                new_route.append(pos)
            else:
                pos += route_direction
                new_route.append(pos)
            count += 1

        return new_route

    def score(self, route):
        """
        Score the route
        Lowest score wins
        """
        # TODO; implement path finding to score more accurately

        # Super simple measure
        diff = abs(self.end.x - route[-1].x) + abs(self.end.y - route[-1].y)
        return diff + len(route)

    def won(self, route):
        if route and route[-1] == self.end:
            return True
        return False
        

def run():
    game = Game()
    route = None
    score = 1000
    iterations = 0
    # TODO; continue until optimal
    while not game.won(route):
        new_routes = []
        # Generate routes
        for _ in range(NO_OF_ROUTES):
            if route:
                new_route = game.mutate_route(route)
            else:
                new_route = game.get_random_route()
            score = game.score(new_route)

            new_routes.append((score, new_route))

        # Pick the best one to continue with
        score, route = sorted(new_routes, key=lambda x: x[0])[0]
        iterations += 1

    game.animate_route(route)
    print(f'Took {iterations} iterations.')

if __name__ == "__main__":
    run()

