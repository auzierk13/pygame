import pygame


class Player:
    def __init__(self, start_position=(50, 310), maximum_size_y=720, image_path="../images/player1.png"):
        self.maximum_size_y = maximum_size_y
        self.position_x, self.position_y = start_position
        self.image = None
        self.image_path = image_path
        self.direct_move = None

    def move(self, step=10):
        if self.position_y + 146 < self.maximum_size_y and self.direct_move == pygame.K_DOWN:
            self.position_y += step
        elif self.position_y >= 0 and self.direct_move == pygame.K_UP:
            self.position_y -= step

    def load(self):
        self.image = pygame.image.load(self.image_path)

    def draw(self, window):
        window.blit(self.image, (self.position_x, self.position_y))

    def bot_move(self, step):
        if step <= 720 - 146:
            self.position_y = step


class Ball:
    def __init__(self, image_path="../images/ball.png"):
        self.ball_x = 617
        self.ball_y = 337
        self.image_path = image_path
        self.image = None
        self.direct_x = -3
        self.direct_y = -3

    def move(self):
        if self.ball_x < 1280:
            self.ball_x += self.direct_x
        if self.ball_x <= 0:
            self.change_direction()
        elif self.ball_x + 46 >= 1280:
            self.change_direction()

        if self.ball_y + 46 >= 720:
            self.change_direction_y()
        elif self.ball_y <= 5:
            self.change_direction_y()
        self.ball_y -= self.direct_y

    def change_direction(self):
        print("Call for collision")
        self.change_direction_x()
        self.change_direction_y()

    def change_direction_x(self):
        self.direct_x *= -1

    def change_direction_y(self):
        self.direct_y *= -1

    def load(self):
        self.image = pygame.image.load(self.image_path)

    def draw(self, window):
        window.blit(self.image, (self.ball_x, self.ball_y))


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

    def draw(self):
        self.window.blit(self.field, (0, 0))
        self.player1.draw(self.window)
        self.player2.draw(self.window)
        self.ball.draw(self.window)

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

            self.collision()
            self.draw()
            self.player2.bot_move(self.ball.ball_y)
            self.ball.move()
            self.player1.move()
            pygame.display.update()

    def set_up(self):
        pygame.init()
        self.window = pygame.display.set_mode(self.size_window)
        pygame.display.set_caption("Football Pong")
        self.field = pygame.image.load("../images/field.png")

        self.player1 = Player(start_position=(50, 310),
                              image_path="../images/player1.png")
        self.player1.load()
        self.player2 = Player(start_position=(1150, 310),
                              image_path="../images/player2.png")
        self.player2.load()

        self.ball = Ball(image_path="../images/ball.png")
        self.ball.load()

    def collision(self):
        # Collision player 1
        if self.ball.ball_x < 120:
            if self.player1.position_y < self.ball.ball_y + 23:
                if self.player1.position_y + 146 > self.ball.ball_y:
                    self.ball.change_direction()

        # Collision player 2
        if self.ball.ball_x > 1100:
            if self.player2.position_y < self.ball.ball_y + 23:
                if self.player2.position_y + 146 > self.ball.ball_y:
                    self.ball.change_direction()


if __name__ == '__main__':
    football_pong = FootballPong()
    football_pong.play_pong()
