import time

import pygame


class Player:
    def __init__(self,
                 start_position=(50, 310),
                 maximum_size_y=720,
                 image_path="../images/player1.png",
                 score_path="../images/score/",
                 score_position=(500, 50)):
        self.maximum_size_y = maximum_size_y
        self.position_x, self.position_y = start_position
        self.image = None
        self.image_path = image_path
        self.direct_move = None
        self.score_path = score_path
        self.score = 0
        self.score_position = score_position

    def move(self, step=10):
        if self.position_y + 146 < self.maximum_size_y and self.direct_move == pygame. K_DOWN:
            self.position_y += step
        elif self.position_y >= 0 and self.direct_move == pygame.K_UP:
            self.position_y -= step

    def load(self):
        self.image = pygame.image.load(self.image_path)

    def draw(self, window):
        window.blit(self.image, (self.position_x, self.position_y))
        if self.score < 10:
            score_image = pygame.image.load(fr"{self.score_path}/{self.score}.png")
            window.blit(score_image, self.score_position)
        else:
            print("Finish game")
            quit()

    def bot_move(self, step):
        if step <= 720 - 146:
            self.position_y = step


class Ball:
    def __init__(self, image_path="../images/ball.png"):
        self.position_x = 617
        self.position_y = 337
        self.image_path = image_path
        self.image = None
        self.direct_x = -30
        self.direct_y = -30

    def move(self):
        if self.position_x < 1280:
            self.position_x += self.direct_x
        if self.position_x <= 0:
            self.change_direction()
        elif self.position_x + 46 >= 1280:
            self.change_direction()

        if self.position_y + 46 >= 720:
            self.change_direction_y()
        elif self.position_y <= 5:
            self.change_direction_y()
        self.position_y -= self.direct_y

    def change_direction(self):
        self.change_direction_x()
        self.change_direction_y()

    def change_direction_x(self):
        self.direct_x *= -1

    def change_direction_y(self):
        self.direct_y *= -1

    def load(self):
        self.image = pygame.image.load(self.image_path)

    def draw(self, window):
        window.blit(self.image, (self.position_x, self.position_y))

    def restart_game(self):
        self.position_x = 617
        self.position_y = 337
        self.change_direction()


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
                if events.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(f"position mouse {pos}")

            self.collision()
            self.check_score()
            self.draw()
            self.player2.bot_move(self.ball.position_y)
            self.ball.move()
            self.player1.move()
            pygame.display.update()

    def set_up(self):
        pygame.init()
        self.window = pygame.display.set_mode(self.size_window)
        pygame.display.set_caption("Football Pong")
        self.field = pygame.image.load("../images/field.png")

        self.player1 = Player(start_position=(50, 310),
                              image_path="../images/player1.png",
                              score_position=(500, 50))
        self.player1.load()
        self.player2 = Player(start_position=(1150, 310),
                              image_path="../images/player2.png",
                              score_position=(710, 50))
        self.player2.load()

        self.ball = Ball(image_path="../images/ball.png")
        self.ball.load()

    def collision(self):
        # Collision player 1
        if self.ball.position_x < 120:
            if self.player1.position_y < self.ball.position_y + 23:
                if self.player1.position_y + 146 > self.ball.position_y:
                    self.ball.change_direction()

        # Collision player 2
        if self.ball.position_x > 1100:
            if self.player2.position_y < self.ball.position_y + 23:
                if self.player2.position_y + 146 > self.ball.position_y:
                    self.ball.change_direction()

    def check_score(self):
        # Check score for player 1
        if self.ball.position_x < 50:
            if 221 < self.ball.position_y < 500:  # beam area
                self.player2.score += 1
                self.ball.restart_game()
        elif self.ball.position_x > 1100:
            if 221 < self.ball.position_y < 500:  # beam area
                self.player1.score += 1
                self.ball.restart_game()


if __name__ == '__main__':
    football_pong = FootballPong()
    football_pong.play_pong()
