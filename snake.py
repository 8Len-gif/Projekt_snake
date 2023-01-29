from pathlib import Path
import pyglet
import random

tile_size = 64
width = height = tile_size * 10
window = pyglet.window.Window(width, height)

label = pyglet.text.Label("Game Over!",
                font_name="Arial",
                font_size = 36,
                x=window.width//2, y=window.height//2,
                anchor_x="center", anchor_y="center")

apple = pyglet.image.load("apple.png")
fruit = pyglet.sprite.Sprite(apple)

TILES_DIRECTORY = Path("snake-tiles")
snake_tiles = {}
for path in TILES_DIRECTORY.glob('*.png'):
    snake_tiles[path.stem] = pyglet.image.load(path)

picture = snake_tiles["tail-head"] #dle klíče si vyhledám ve slovníku potřebný obrázek
green_square = pyglet.sprite.Sprite(picture)

class Game:
    def __init__(self):
        self.snake = [(1, 2), (2,2)]
        self.direction = "d" or "s" or "w" or "a"
        self.width = 10
        self.height = 10
        self.fruit = []
        self.new_fruit()
        self.status = "alive"

    def move(self, t):
        #pohyb hada dle vybrané klávesnice
        (x, y) = self.snake[-1]
        if self.direction == "d":
            x += 1
        elif self.direction == "s":
            y += -1
        elif self.direction == "w":
            y += 1
        elif self.direction == "a":
            x += -1
        
        #zamezení pohybu mimo herní pole
        if x < 0:
            self.status = "dead"
            pyglet.clock.unschedule(game.move)
            return
        if y < 0:
            self.status = "dead"
            pyglet.clock.unschedule(game.move)
            return
        if x > (self.width - 1):
            self.status = "dead"
            pyglet.clock.unschedule(game.move)
            return
        if y > (self.height - 1):
            self.status = "dead"
            pyglet.clock.unschedule(game.move)
            return

        #náraz do sebe samého
        if (x, y) in self.snake:
            pyglet.clock.unschedule(game.move)
            self.status = "dead"
            return

        self.snake.append((x, y))

        #pokud je pozice na pozici jídla, dojde ke zvětšení hada, a někde se objeví další jídlo
        if (x, y) in self.fruit:
            new_position = x, y
            self.fruit.remove(new_position)
            self.new_fruit() 
        else:
            del self.snake[0]

    def new_fruit(self):
        for number in range(100):
            fruit_x = random.randrange(self.width)
            fruit_y = random.randrange(self.height)
            new_fruit = fruit_x, fruit_y
            if (new_fruit not in self.snake) and (new_fruit not in self.fruit):
                self.fruit.append(new_fruit) 
                return 
        
def draw():
    window.clear()
    for (x, y) in game.snake:
        green_square.x = x * 64
        green_square.y = y * 64
        green_square.draw()

    #vložení jídla na hrací plochu
    for (x, y) in game.fruit:
        fruit.x = x * 64
        fruit.y = y * 64
        fruit.draw()

    if game.status == "dead":
        label.draw()
    
def direction(text):
    if text == "s":
        game.direction = "s"
        green_square.y += -1
    elif text == "d":
        game.direction = "d"
        green_square.x += 1
    elif text == "w":
        game.direction = "w"
        green_square.y += 1
    elif text == "a":
        game.direction = "a"
        green_square.x += -1

window.push_handlers(
    on_draw=draw,
    on_text=direction
)

game = Game()

pyglet.clock.schedule_interval(game.move, 1/6)

pyglet.app.run()