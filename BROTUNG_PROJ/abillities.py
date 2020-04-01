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

class Effect(object):

    def __init__(self,player_att,effect):
        """
        the effect of the abillity
        :param player_att: before abillity value of player att
        :param effect: the effect value 1-5
        :param counter: count frames until effect disapears
        """
        self.player_att = player_att
        self.effect = effect
        self.counter = EFFECT_COUNTER
    def effect_tik(self):
        self.counter -= 1

class Ability(object):

    def __init__(self,path,type):
        """
        The abillity
        :param image: the pygame imgage object
        :param cord: cordination of left corner of image 
        :param type: type of abillity 1-5
        :param counter: counter that checks when the abillity will dissapear
        :param exist: is the abillity need to be erased 
        :param list_of_cord: all the cordantions on the board that this abillity takes  
        """
        self.image = set_pic(path,PIC_PROP)
        self.cord = tuple()
        self.type = type
        self.counter = int()
        self.exist = True
        self.list_of_cord = list()

    def gen_cord(self,wid,hight,list_of_player=False,list_of_abillities=False):
        """
        generate the coordantions of the abillity by PIC_PROPORTIONS
        #TODO make sure that abillity isnt created on another abillity or player#
        :param wid: board width 
        :param hight: board hight
        :param list_of_player: Dah
        :param list_of_abillities: Dah
        :return: create the abillity cordinations
        """

        self.cord = (random.randint(50,wid),random.randint(50,hight))
        for i in range(PIC_PROP[0]):
            for j in range(PIC_PROP[1]):
                self.list_of_cord.append((self.cord[0]+i,self.cord[1] + j))

    def disapear(self,screen,list_of_abillities):
        """
        paint the abillity squre in black and make it disappear
        :param screen: game board
        :return: paint the abillity squre on the board in black
        """
        bye_rect = pygame.Rect((self.cord),PIC_PROP)
        pygame.draw.rect(screen,BLACK,bye_rect)
        list_of_abillities.remove(self)
        self.existe = False

    def update(self,screen):
        """
        checks if the abillity shoud disapeer
        :param screen: game screen 
        :return: 
        """
        self.counter += 1
        if self.counter == ABILLITY_GONE_TIMER:
            self.disapear(screen)



    def activet_abillity(self,player):
        """
        activate the abillity, checks the type of the abillity and then activate her by changing
        player attrebiutes
        :param player: player object
        :return: change player attrebiutes
        """
        if self.type == SIZE:
            player.list_of_effects.append(Effect(player.radius,SIZE))
            player.radius *= 2
        if self.type == CHANGE:
            player.list_of_effects.append(Effect((player.left,player.right),CHANGE))
            ezer = player.left
            player.left = player.right
            player.right = ezer
        if self.type == SPEED:
            player.list_of_effects.append(Effect(player.pace,SPEED))
            player.pace *= 2
        if self.type == SQURE:
            player.list_of_effects.append(Effect(player.squre,SQURE))
            player.squre = True
        if self.type == GHOST:
            player.list_of_effects.append(Effect(player.ghost,GHOST))
            player.ghost = True


def update_list_of_abilitties(list_of_abillity,abilitty_gen_timer,screen):
    """
    In main each FRAME a list of abillities that right now on the board is checked and removed if needed
    this function generate for each ABILLITY_GEN_TIMER amount of time an abillity object and draw it on the board

    :param list_of_abillity: Dah
    :param abilitty_gen_timer: how MUCH frame till an abillity should be drawn 
    :param screen: game screen
    :return: create on board new abillity object and append it to the abillity_list
    """
    abilitty_gen_timer += 1
    if abilitty_gen_timer == ABILLITY_GEN_TIMER:
        att = GHOST#random.randint(CHANGE,SIZE)
        abillity = Ability(ATT_DICT[att],att)
        abillity.gen_cord(BOARD_SIZE_WID * 3 / 4 - 50, BOARD_SIZE_HIGHT - 50)
        screen.blit(abillity.image, abillity.cord)
        list_of_abillity.append(abillity)
        abilitty_gen_timer = 0
    return abilitty_gen_timer

def abilitties_update(list_of_abillity,screen):
    """
    this function update the abillity list and remove any abillity that need to be removed
    :param list_of_abillity: Dah
    :param screen: game board
    """
    if len(list_of_abillity) > 1:
        for abillity in list_of_abillity:
            if not abillity.exist:
                list_of_abillity.remove(abillity)
            abillity.update(screen)