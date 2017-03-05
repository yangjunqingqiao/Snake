
import pygame
import random
import queue

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
RED = (255, 0, 0)


class ImprovedQueue(queue.Queue):

    def to_list(self):
        with self.mutex:
            return list(self.queue)

    def __repr__(self):
        self.repr = ""
        for segment in self.to_list():
            self.repr += ''.join(segment.as_string())
        return self.repr


class Snake:

    def __init__(self):
        # how many segments the snake has
        self.size = 1
        # iterable queue of snake parts
        self.snakeParts = ImprovedQueue()
        self.snakeParts.put(Segment(0, 0))
        # space between each part
        self.gap = 5
        # first part of snake starts at the upper left of screen
        self.tail = (0, 0)
        self.head = (0, 0)
        # constants for updating and adding new parts to the snake
        self.updateGap = Segment.get_height() + self.gap
        self.LEFT = (-self.updateGap, 0)
        self.RIGHT = (self.updateGap, 0)
        self.UP = (0, -self.updateGap)
        self.DOWN = (0, self.updateGap)
        self.currentDirection = self.RIGHT
        print(self.snakeParts)

    def grow(self):
        self.snakeParts.put(Segment(self.tail[0], self.tail[1]))

    def update_direction(self, key_pressed):
        if key_pressed == pygame.K_LEFT and self.currentDirection is not self.RIGHT:
            print("LEFT")
            self.currentDirection = self.LEFT
        elif key_pressed == pygame.K_RIGHT and self.currentDirection is not self.LEFT:
            print("RIGHT")
            self.currentDirection = self.RIGHT
        elif key_pressed == pygame.K_UP and self.currentDirection is not self.DOWN:
            print("UP")
            self.currentDirection = self.UP
        elif key_pressed == pygame.K_DOWN and self.currentDirection is not self.UP:
            print("DOWN")
            self.currentDirection = self.DOWN

    def update(self, food):
        print(self.snakeParts)
        self.tail = self.snakeParts.get().get_coordinates()
        self.head = (self.head[0] + self.currentDirection[0], self.head[1] + self.currentDirection[1])
        self.snakeParts.put(Segment(self.head[0], self.head[1]))
        if pygame.sprite.spritecollide(food, self.snakeParts.to_list(), False):
            self.grow()
            food.spawn()

    def get_segments(self):
        return self.snakeParts

    def __repr__(self):
        return self.snakeParts


class Segment(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.width = 15
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def get_coordinates(self):
        return self.rect.x, self.rect.y

    @staticmethod
    def get_width():
        return 15

    @staticmethod
    def get_height():
        return 15

    def as_string(self):
        return str((self.rect.x, self.rect.y))

    def __repr__(self):
        return str((self.rect.x, self.rect.y))


class Food(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.width = 15
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(0, 800)

    def get_coordinates(self):
        return self.rect.x, self.rect.y

    def spawn(self):
        self.rect.x = random.randint(0, 800)
        self.rect.y = random.randint(0, 800)

    def __repr__(self):
        return str((self.rect.x, self.rect.y))


class Game:
    def __init__(self):
        pygame.init()
        self.size = [800, 800]
        self.screen = pygame.display.set_mode(self.size)
        self.snake = Snake()
        self.food = Food()
        self.running = True
        self.snakeSprites = pygame.sprite.Group()
        self.foodSprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

    def start_game(self):
        while self.running:
            self.snakeSprites.empty()
            for segment in self.snake.get_segments().to_list():
                self.snakeSprites.add(segment)
            self.foodSprites.add(self.food)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.snake.update_direction(event.key)
            self.snake.update(self.food)
            self.screen.fill(BLACK)
            self.snakeSprites.draw(self.screen)
            self.foodSprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(5)
        pygame.quit()

if __name__ == "__main__":
    Game().start_game()
