# Snake Tutorial Python

import random
import pygame
import tkinter as tk
from tkinter import messagebox

global largura, rows, snake, snack


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnX = 1
        self.dirnY = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnX = dirnx
        self.dirnY = dirny
        self.pos = (self.pos[0] + self.dirnX, self.pos[1] + self.dirnY)

    def draw(self, surface, eyes=False):
        size = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        # pygame.draw.circle(surface, self.color, self.pos, size - 3)
        pygame.draw.rect(surface, self.color, (i * size + 1, j * size + 1, size - 2, size - 2))
        if eyes:
            centre = size // 2
            radius = 3
            circleMiddle = (i * size + centre - radius, j * size + 8)
            circleMiddle2 = (i * size + size - radius * 2, j * size + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)
            

class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        # Direção que a cobra se movimenta em X e Y
        self.dirnX = 0
        self.dirnY = 1

    def move(self):
        # analisa qual a tecla esta sendo pressionada
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            # movimenta para cima
            if keys[pygame.K_UP]:
                self.dirnX = 0
                self.dirnY = -1
                self.turns[self.head.pos[:]] = [self.dirnX, self.dirnY]
            # movimenta para baixo
            elif keys[pygame.K_DOWN]:
                self.dirnX = 0
                self.dirnY = 1
                self.turns[self.head.pos[:]] = [self.dirnX, self.dirnY]
            # movimenta para esquerda
            elif keys[pygame.K_LEFT]:
                self.dirnX = -1
                self.dirnY = 0
                self.turns[self.head.pos[:]] = [self.dirnX, self.dirnY]
            # movimenta para direita
            elif keys[pygame.K_RIGHT]:
                self.dirnX = 1
                self.dirnY = 0
                self.turns[self.head.pos[:]] = [self.dirnX, self.dirnY]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnX == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnX == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirnY == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirnY == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnX, c.dirnY)

    def reset(self, pos):
        self.body = []
        self.turns = {}
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnX = 0
        self.dirnY = 1

    def add_cube(self):
        final = self.body[-1]
        dx, dy = final.dirnX, final.dirnY

        if dx == 1 and dy == 0:
            self.body.append(Cube((final.pos[0] - 1, final.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((final.pos[0] + 1, final.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((final.pos[0], final.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((final.pos[0], final.pos[1] + 1)))

        self.body[-1].dirnX = dx
        self.body[-1].dirnY = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(largura, rows, surface):
    # tamanho da lacuna entre as linhas
    size = largura // rows

    # possição na tela
    x = 0
    y = 0

    for i in range(rows):
        x = x + size
        y = y + size

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, largura))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (largura, y))


# redesenha toda a tela do jogo
def redraw_window(surface):
    global rows, largura, snake, snack
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    draw_grid(largura, rows, surface)
    pygame.display.update()


# adiciona as frutinhas da cobra
# verifica se a posição está ocupada pela cobra antes
def random_snack(item):
    global rows
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def message_box(subject, content):
    pass


def main():
    global largura, rows, snake, snack
    pygame.init()
    # altura e largura da tela
    largura = 500
    # quantidade de linhas
    rows = 20
    win = pygame.display.set_mode((largura, largura))

    snake = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(snake), color=(0, 245, 3))
    flag = True

    # tempo de movimentação da cobrinha
    clock = pygame.time.Clock()

    while flag:
        # controle do tempo de movimento da cobrinha, pra ela não ser tão rápida ou devagar
        # se quiser aumentar a velocidade tem que aumentar o tick, ou diminuir o delay
        pygame.time.delay(30)
        clock.tick(10)
        snake.move()
        if snake.body[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(random_snack(snake), color=(0, 245, 3))

        for x in range(len(snake.body)):
            if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                print('Score: ', len(snake.body))
                snake.reset((10, 10))
                break

        redraw_window(win)


main()
