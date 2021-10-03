import pygame


class Player:
    def __init__(self, start_position=(50, 310), maximum_size_y=720, image_path="../images/player1.png"):
        self.maximum_size_y = maximum_size_y
        self.position_x, self.position_y = start_position
        self.image = None
        self.image_path = image_path
        self.direct_move = None

    def move_player(self):
        if self.position_y + 146 < self.maximum_size_y and self.direct_move == pygame.K_DOWN:
            self.position_y += 10
        elif self.position_y >= 0 and self.direct_move == pygame.K_UP:
            self.position_y -= 10

    def load_player(self):
        self.image = pygame.image.load(self.image_path)


class FootballPong:
    def __init__(self):
        self.window = None
        self.field = None
        self.player1 = None
        self.player2 = None
        self.ball = None
        self.size_x_max = 1280
        self.size_y_max = 720
        self.size_window = [self.size_x_max, self.size_y_max]
        self.ball_x = 617
        self.ball_y = 337

    def move_ball(self):
        if self.ball_x < 1280:
            self.ball_x += 1
        else:
            self.ball_x = 0

    def draw(self):
        self.window.blit(self.field, (0, 0))
        self.window.blit(self.player1.image, (self.player1.position_x,
                                              self.player1.position_y))
        self.window.blit(self.player2.image, (self.player2.position_x,
                                              self.player2.position_y))
        self.window.blit(self.ball, (self.ball_x, self.ball_y))

    def play_pong(self):
        self.set_up()
        loop = True
        while loop:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    loop = False
                if events.type == pygame.KEYDOWN:
                    self.player1.direct_move = events.key
                if events.type == pygame.KEYUP:
                    self.player1.direct_move = None

            self.draw()
            self.move_ball()
            self.player1.move_player()
            pygame.display.update()

    def set_up(self):
        pygame.init()
        self.window = pygame.display.set_mode(self.size_window)
        pygame.display.set_caption("Football Pong")
        self.field = pygame.image.load("../images/field.png")

        self.player1 = Player(start_position=(50, 310),
                              image_path="../images/player1.png")
        self.player1.load_player()
        self.player2 = Player(start_position=(1150, 310),
                              image_path="../images/player2.png")
        self.player2.load_player()

        self.ball = pygame.image.load("../images/ball.png")


if __name__ == '__main__':
    football_pong = FootballPong()
    football_pong.play_pong()
