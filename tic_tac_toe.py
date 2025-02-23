import pygame

pygame.init()
pygame.display.set_caption('Крестики-нолики')

coords = dict()
ban_list = []
sign = True


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, window):
        move_x = self.left
        move_y = self.top
        begin_corner = self.left
        end_corner = self.cell_size
        for (n_y, row) in enumerate(self.board):
            for (n_x, cell) in enumerate(row):
                coords[(move_x, self.cell_size + move_x, move_y, self.cell_size + move_y)] = (n_x, n_y)
                pygame.draw.rect(window, (255, 255, 255), (move_x, move_y, self.cell_size, self.cell_size),
                                 width=1)
                move_x += self.cell_size
                begin_corner += self.cell_size
                end_corner += self.cell_size
            move_x = self.left
            move_y += self.cell_size

    def get_values(self):
        return [self.cell_size, self.left, self.top]


size = list(map(int, input('Введите размер клеточного поля: ').split()))
board = Board(size[0], size[1])
board.set_view(25, 15, 29)
screen = pygame.display.set_mode(((board.get_values()[1] * 2) + (size[0] * board.get_values()[0]),
                                  (board.get_values()[2] * 2) + (size[1] * board.get_values()[0])))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_x = pygame.mouse.get_pos()[0]
            pos_y = pygame.mouse.get_pos()[1]
            flag = False
            for coord in coords:
                if coords[coord] not in ban_list:
                    if (pos_x >= coord[0]) and (pos_x <= coord[1]) and (pos_y >= coord[2]) and (
                            pos_y <= coord[3]):
                        if sign:
                            pygame.draw.line(screen, (255, 255, 255), (coord[0], coord[2]), (coord[1], coord[3]), 2)
                            pygame.draw.line(screen, (255, 255, 255), (coord[0], coord[3]),
                                             (coord[0] + board.get_values()[0], coord[2]), 2)
                            ban_list.append(coords[coord])
                            flag = True
                            sign = False
                        else:
                            pygame.draw.circle(screen, (255, 255, 255),
                                               (coord[0] + board.get_values()[0] // 2,
                                                coord[2] + board.get_values()[0] // 2),
                                               board.get_values()[0] // 2, 2)
                            ban_list.append(coords[coord])
                            flag = True
                            sign = True
            if not flag:
                print('Тут уже нельзя рисовать.', end='\n\n')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                ban_list = []
                sign = True
                screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
