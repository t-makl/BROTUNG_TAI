import pygame
import random
from math import sin, cos, pi, radians
import time

# ratio between game and score board 3/4
BOARD_SIZE_WID = 700
BOARD_SIZE_HIGHT = 500
BORDER_WIDTH = 5
WINNING_SIZE = 75
PATH_RAD = 3
LINE_WID = 3
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_YELLOW = (255, 254, 0)
CLOCK = pygame.time.Clock()
ANGEL_FACTOR = 5.5
RADIUS = 3


class Player(object):
    def __init__(self, name, color, left, right):
        self.name = name
        self.color = color
        self.score = 0
        self.position = (0, 0)
        self.angel = 0
        self.dead_num = 0
        self.dead = False
        self.left = left
        self.right = right
        self.space_counter = 0

    def gen(self):
        self.position = (random.randint(10, BOARD_SIZE_WID * 3 / 4) - 5, random.randint(10, BOARD_SIZE_HIGHT) - 5)
        self.angel = random.randint(10, 350)
        self.dead = False
        self.dead_num = 0
        self.space_counter = 0

    def update_pos(self, x, y):
        self.position = (x, y)

    def update_angle(self, angle_factor):
        self.angel += angle_factor
        self.angel %= 360

    def move(self, radius):
        self.position = (self.position[0] + int(cos(radians(self.angel)) * radius),
                         self.position[1] + int(sin(radians(self.angel)) * radius))

    def draw(self, screen, radius, pointer_radius):
        if 80 < self.space_counter < 90:
            pygame.draw.circle(screen, BLACK, self.position, pointer_radius)
        else:
            pygame.draw.circle(screen, self.color, self.position, pointer_radius)
        if self.space_counter < 90:
            self.space_counter += 1
        else:
            self.space_counter = 0

        self.move(radius)
        next_cord = ((self.position[0] + int(cos(radians(self.angel)) * radius * 2)
                      , self.position[1] + int(sin(radians(self.angel)) * radius * 2)))
        try:
            if screen.get_at(next_cord) != (0, 0, 0, 255):
                self.dead = True
            pygame.draw.circle(screen, YELLOW, self.position, pointer_radius)
        except:
            self.dead = True


def board_formated_text(screen, sb_wid, sb_hight, text, font_size, hight, rgb, middle=True, left=False, right=False,
                        font=None, ):
    """
    the function gets a text and format it to the game score board
    :param screen: the game screen
    :param sb_wid: the score board widtgh
    :param sb_hight: the score board hight
    :param text: obvius
    :param font_size: size of text - empiri
    :param hight: empiri
    :param r: red out of RGB
    :param g: green out of RGB
    :param b: blue out of RGB
    :param middle: condition that determains if the text will be in the middle
    :param left: condition that determains if the text will be in the left
    :param right: condition that determains if the text will be in the right
    :param font: type of font, usally is system font - None
    :return: nothing
    """
    obj_font = pygame.font.SysFont(font, font_size)
    obj_text = obj_font.render(text, True, rgb)
    if middle:
        text_x = (sb_wid - int(sb_wid / 8)) - int(obj_text.get_width() / 2)

    elif left:
        text_x = sb_wid - int(sb_wid / 4) + 5
    elif right:
        text_x = sb_wid - 20

    screen.blit(obj_text, (text_x, hight))


def update_score(screen, sb_wid, sb_hight, list_of_players):
    """
    the function updates the player scores by they cuurent score
    :param screen: game screen 
    :param sb_wid: score board widtgh
    :param sb_hight: score board hight
    :param list_of_players: list of player objects
    :return: None
    """
    counter = 140
    for player in list_of_players:
        if player.score == 0:
            board_formated_text(screen, sb_wid, sb_hight, str(player.score), 20, counter, player.color, middle=False,
                                right=True)
        else:
            board_formated_text(screen, sb_wid, sb_hight, str(player.score - 1), 20, counter, BLACK, middle=False,
                                right=True)
            board_formated_text(screen, sb_wid, sb_hight, str(player.score), 20, counter, player.color, middle=False,
                                right=True)
        counter += 20


def set_score_board(screen, sb_wid, sb_hight, list_of_players):
    """
    the function set the start board
    the followings texts: "goal", number of pints to win(10 * players num),"two points diff",player names and scores
    which is for the begining zero
    :param screen: screen
    :param sb_wid: score board widtgh
    :param sb_hight: score board hight
    :param list_of_players: list of player objects
    :return: None
    """
    board_formated_text(screen, sb_wid, sb_hight, "goal", 30, 30, WHITE)
    board_formated_text(screen, sb_wid, sb_hight, (str(len(list_of_players) * 10)), 60, 60, WHITE)
    board_formated_text(screen, sb_wid, sb_hight, "Two points diff", 20, 120, WHITE)
    counter = 140
    for player in list_of_players:
        board_formated_text(screen, sb_wid, sb_hight, player.name, 20, counter,
                            player.color, middle=False, left=True)
        counter += 20
    update_score(screen, sb_wid, sb_hight, list_of_players)


def set_starting_players(list_of_players):
    for player in list_of_players:
        player.gen()


def set_of_player(list_of_players):
    set_p = set()
    for player in list_of_players:
        set_p.add(player)
    return set_p

def print_win(screen,player,font=None):
    win_font = pygame.font.SysFont(font, WINNING_SIZE)
    win_text = win_font.render("{} WON !!!".format(player.name), True, player.color)
    screen.blit(win_text, ((BOARD_SIZE_WID * (3/4) - win_text.get_width()) / 2 , BOARD_SIZE_HIGHT / 2))
    return True

def check_win(screen,list_of_players):
    list_of_scores = list()
    for player in list_of_players:
        if player.score >= len(list_of_players) * 10:
            list_of_scores.append((player.score,player))

    if len(list_of_scores) > 1:
        list_of_scores.sort()
        if list_of_scores[-1][0] > list_of_scores[-2][0] + 1:
            return print_win(screen,list_of_scores[-1][1])
    elif len(list_of_scores) == 1:
        return print_win(screen, list_of_scores[0][1])
    else:
        return False











def main():

    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE_WID, BOARD_SIZE_HIGHT))
    done = False
    list_of_players = [Player('fred', (255, 0, 0), pygame.K_a, pygame.K_d),
                       Player('greenlee', (0, 255, 0), pygame.K_LEFT, pygame.K_RIGHT),
                       Player('bluebell', (0, 0, 255), pygame.K_g, pygame.K_h)]

    set_of_players = set_of_player(list_of_players)
    pygame.draw.rect(screen, BOARD_YELLOW, pygame.Rect(0, 0, BOARD_SIZE_WID * 3 / 4, BOARD_SIZE_HIGHT),BORDER_WIDTH)
    set_score_board(screen, BOARD_SIZE_WID, BOARD_SIZE_HIGHT, list_of_players)
    set_starting_players(list_of_players)
    set_of_dead = set()

    while not done:

        update_score(screen, BOARD_SIZE_WID, BOARD_SIZE_HIGHT, list_of_players)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        for player in list_of_players:


            if player.dead:
                set_of_dead.add(player)

            else:
                if len(set_of_dead) > player.dead_num:
                    player.dead_num += 1
                    player.score += 1

                pressed = pygame.key.get_pressed()
                if pressed[player.left]:
                    player.update_angle(ANGEL_FACTOR)
                elif pressed[player.right]:
                    player.update_angle(-ANGEL_FACTOR)
                player.draw(screen, RADIUS, PATH_RAD)
        #start_new_turn
        if (len(list_of_players) - 1) == len(set_of_dead):
            list(set_of_players - set_of_dead)[0].score += 1
            screen.fill(BLACK)
            pygame.draw.rect(screen, BOARD_YELLOW, pygame.Rect(0, 0, BOARD_SIZE_WID * 3 / 4, BOARD_SIZE_HIGHT), BORDER_WIDTH)
            set_score_board(screen, BOARD_SIZE_WID, BOARD_SIZE_HIGHT, list_of_players)
            set_starting_players(list_of_players)
            set_of_dead = set()
            if check_win(screen, list_of_players):
                for player in list_of_players:
                    player.dead = True



        CLOCK.tick(30)

        pygame.display.flip()


if __name__ == '__main__':
    main()