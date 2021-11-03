import sys
import random
import time
import pygame

WINDOW_SIZE = (600, 600)
FIELD_SIZE = (30, 30)

pygame.init()
pygame.display.set_caption('Snake')
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

class Snake:
    def __init__(self) -> None:
        self.x = 10
        self.y = 10
        self.color = (1, 50, 32)
        self.points = [(10,10)]
        self.direction = 'right'
    def make_step(self):
        match self.direction:
            case 'right':
                self.x += 1
            case 'left':
                self.x -= 1
            case 'up':
                self.y -= 1
            case 'down':
                self.y += 1
        snake.points.append((self.x, self.y))
        snake.points.pop(0)
    def draw_point(self, screen, x ,y):
        pygame.draw.rect(screen, self.color, ((x-1)*20, (y-1)*20, 20, 20))
    def draw(self, screen):
        for point in self.points:
            self.draw_point(screen, point[0], point[1])
    def handle_input(self, input):
        match input:
            case pygame.K_w:
                self.direction = 'up'
            case pygame.K_s:
                self.direction = 'down'
            case pygame.K_a:
                self.direction = 'left'
            case pygame.K_d:
                self.direction = 'right'
class Grid:
    def __init__(self) -> None:
        self.bg_color = (0,0,0)
        # self.bg_color = (255,0,100)
    def draw(self):
        pixel_side = WINDOW_SIZE[0]/FIELD_SIZE[0]
        screen.fill(self.bg_color)
        for i in range(FIELD_SIZE[0]):
            pygame.draw.line(screen, (255, 255, 255), (i*pixel_side,0), (i*pixel_side, 600))
            pygame.draw.line(screen, (255, 255, 255), (0, i*pixel_side), (600, i*pixel_side))

class GameObject:
    def __init__(self, screen) -> None:
        self.x = random.randint(1, 30)
        self.y = random.randint(1, 30)
        self.screen = screen
        self.color = (255, 0, 0)
    def spawn(self):
        pygame.draw.rect(self.screen, self.color, ((self.x-1)*20, (self.y-1)*20, 20, 20))
snake = Snake()
grid = Grid()
apple = GameObject(screen)

while True:
    clock.tick(15)
    grid.draw()
    snake.draw(screen)
    apple.spawn()
    snake.make_step()
    if snake.x == apple.x and snake.y == apple.y:
        snake.points.append((snake.x, snake.y))
        apple = GameObject(screen)
        print(apple.x, apple.y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            snake.handle_input(event.key)
    pygame.display.flip()
