from consts import *
def set_pic(path,prop):
    """
    :param path: pic path
    :param prop: proportions
    :return: image object
    """
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, prop)
    return image
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