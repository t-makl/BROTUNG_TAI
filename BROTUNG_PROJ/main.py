from abillities import *
from board import *
from player import *

def main():

    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE_WID, BOARD_SIZE_HIGHT))
    done = False
    end_turn = False
    list_of_players = [Player('fred', (255, 0, 0), pygame.K_a, pygame.K_d),
                       Player('greenlee', (0, 255, 0), pygame.K_LEFT, pygame.K_RIGHT),
                       Player('bluebell', (0, 0, 255), pygame.K_g, pygame.K_h)]

    pygame.draw.rect(screen, YELLOW, pygame.Rect(0, 0, BOARD_SIZE_WID * 3 / 4, BOARD_SIZE_HIGHT),BORDER_WIDTH)
    set_score_board(screen, BOARD_SIZE_WID, BOARD_SIZE_HIGHT, list_of_players)
    set_starting_players(list_of_players)
    set_of_dead = set()
    abillity_gen_timer = 0
    list_of_abilitties = list()

    while not done:

        update_score(screen, BOARD_SIZE_WID, BOARD_SIZE_HIGHT, list_of_players)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        for player in list_of_players:

            abillity_gen_timer = update_list_of_abilitties(list_of_abilitties, abillity_gen_timer, screen)
            #abilitties_update(list_of_abilitties, screen)
            
            if player.dead:
                set_of_dead.add(player)

            else:
                if len(set_of_dead) > player.dead_num:
                    player.dead_num += 1
                    player.score += 1

                player.update_effect()
                player.get_movment_input()
                player.draw(screen,list_of_abilitties)

        #start_new_turn
        if (len(list_of_players) - 1) == len(set_of_dead):
            end_turn = True
            continue

        if end_turn:
            screen.fill(BLACK)
            pygame.draw.rect(screen, YELLOW, pygame.Rect(0, 0, BOARD_SIZE_WID * 3 / 4, BOARD_SIZE_HIGHT), BORDER_WIDTH)
            set_score_board(screen, BOARD_SIZE_WID, BOARD_SIZE_HIGHT, list_of_players)
            set_starting_players(list_of_players)
            list_of_abilitties = list()
            abillity_gen_timer = 0
            set_of_dead = set()
            if check_win(screen, list_of_players):
                for player in list_of_players:
                    player.dead = True
            end_turn = False



        CLOCK.tick(30)

        pygame.display.flip()

if __name__ == '__main__':
    main()