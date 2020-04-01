from consts import *

class Player(object):
    def __init__(self, name, color, left, right):
        """
        :param name: player name as string
        :param color: player color in rgb
        :param score: player score, get point 1 for each player that died 
        :param position: tuple cordination (x,y) on the board 
        :param angel: player angel of movment in degrees 
        :param left: pygame key object that represnt left for the player 
        :param right: pygame key object that represnt right for the player 
        :param space_counter: counter that count the num of frames until the player movment shoud draw blanks
        :param radius: radius of the player pointer == PATH_RAD
        :param list_of_effect: list of effect that effects the player 
        :param dead_num: number of othe player how died
        :param dead: booleen that checks if the player alive or not
        """
        self.name = name
        self.color = color
        self.score = 0
        self.position = (0, 0)
        self.angel = 0
        self.left = left
        self.right = right
        self.radius = PATH_RAD
        self.pace = PACE
        self.list_of_effects = list()
        self.squre = False
        self.space_counter = 0
        self.dead_num = 0
        self.dead = False
        self.ghost = False



    def gen(self):
        """
        generate player attribute that requires reset after each round
        :param: position = start the player position at random position
        :param: angel = random movment angel
        :param: dead = alive
        :param: dead_num = no dead
        :param: space_counter = rest
        :param: radius = PATH_RAD
        :return: 
        """
        self.position = (random.randint(10, BOARD_SIZE_WID * 3 / 4) - 5, random.randint(10, BOARD_SIZE_HIGHT) - 5)
        self.angel = random.randint(10, 350)
        self.dead = False
        self.dead_num = 0
        self.space_counter = 0
        self.radius = PATH_RAD
        self.list_of_effects = list()
        self.pace = PACE
        self.squre = False
        self.squre_counter = 0
        self.ghost = False


    def update_pos(self, x, y):
        """
        change player position 
        """
        self.position = (x, y)

    def update_angle(self, angle_factor):
        """
        update angel of movment by angel_factor
        :param angle_factor: the increement of the angle
        :return: 
        """
        if self.squre:
            if self.squre_counter == 4:
                angle_factor = 90 * (angle_factor / ANGEL_FACTOR)
                self.squre_counter = 0
            else:
                angle_factor = 0
                self.squre_counter += 1
        
        self.angel += angle_factor
        self.angel %= 360 # not needed but nice

    def move(self,next_move=False):
        """
        calculte the next position of a player by the furmola (x +(cos(a) * radius of movment),
                                                               y +(sin(a) * radius of movment))
        :param movment_radius: Dah
        :return: 
        """
        if next_move:
            return (self.position[0] + int(cos(radians(self.angel)) * self.pace * (self.radius / PATH_RAD) * 2),
                         self.position[1] + int(sin(radians(self.angel)) * self.pace * (self.radius / PATH_RAD) * 2))

        self.position = (self.position[0] + int(cos(radians(self.angel)) * self.pace),
                         self.position[1] + int(sin(radians(self.angel)) * self.pace))
        



    def activate_effect(self,abillity_list,screen,next_cord):
        for abillity in abillity_list:
            if next_cord in abillity.list_of_cord:
                if self.radius > 6:
                    print("oops")
                abillity.activet_abillity(self)
                abillity.disapear(screen,abillity_list)
                return 1
        return 0


    def update_effect(self):
        for effect in self.list_of_effects:
            if effect.counter == 0:
                if effect.effect == SIZE:
                    self.radius = effect.player_att
                    self.list_of_effects.remove(effect)
                elif effect.effect == CHANGE:
                    self.left = effect.player_att[0]
                    self.right = effect.player_att[1]
                    self.list_of_effects.remove(effect)
                elif effect.effect == PACE:
                    self.pace = effect.player_att
                    self.list_of_effects.remove(effect)
                elif effect.effect == SQURE:
                    self.squre = effect.player_att
                    self.squre_counter = 0
                    self.list_of_effects.remove(effect)
                elif effect.effect == GHOST:
                    self.ghost = effect.player_att
                    self.list_of_effects.remove(effect)
                
            else:
                effect.effect_tik()
    def path_drawer(self,screen,color):
        pace = self.pace
        cord = self.position
        self.pace = PACE

        for i in range(int(pace/PACE)):
            pygame.draw.circle(screen, color, self.position, self.radius)
            self.move()
        self.pace = pace
        self.position = cord

    def draw(self, screen,abillity_list):
        if (PLAYER_SPACE < self.space_counter < (PLAYER_SPACE + PLAYER_SPACE_RANGE)) or self.ghost:
            self.path_drawer(screen,BLACK)
        else:
             self.path_drawer(screen,self.color)

        if self.space_counter < (PLAYER_SPACE + PLAYER_SPACE_RANGE):
            self.space_counter += 1
        else:
            self.space_counter = 0

        self.move()
        next_cord = self.move(True)
         
        try:
            if screen.get_at(next_cord) != (0, 0, 0, 255):
                if(self.activate_effect(abillity_list,screen,next_cord)):
                    pass

                    if self.ghost:
                        if screen.get_at(next_cord) == (255, 255, 0, 255):
                            self.dead = True
                    else:
                        self.dead = True
                else:
                    self.dead = True

            pygame.draw.circle(screen, YELLOW, self.position, self.radius)
            
        except:
            self.dead = True

    def get_movment_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[self.left]:
            self.update_angle(ANGEL_FACTOR)
        elif pressed[self.right]:
            self.update_angle(-ANGEL_FACTOR)




