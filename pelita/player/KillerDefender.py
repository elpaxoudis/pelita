
from pelita.player import AbstractPlayer
from pelita.datamodel import north, south, west, east, stop
from pelita.graph import AdjacencyList, NoPathException, diff_pos
import numpy as np
# use relative imports for things inside your module
from .utils import utility_function

class GreedyAttacker(AbstractPlayer):

    def __init__(self):
        # Do some basic initialisation here. You may also accept additional
        # parameters which you can specify in your factory.
        # Note that any other game variables have not been set yet. So there is
        # no ``self.current_uni`` or ``self.current_state``
        self.sleep_rounds = 0

    def goto_pos(self, pos):
        return self.adjacency.a_star(self.current_pos, pos)[-1]

    def set_initial(self):
        # Now ``self.current_uni`` and ``self.current_state`` are known.
        # ``set_initial`` is always called before ``get_move``, so we can do some
        # additional initialisation here

        # Just printing the universe to give you an idea, please remove all
        # print statements in the final player.
        #self.universe_states = []
        #print(self.current_uni)
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.next_food = None

    def check_pause(self):
        # make a pause every fourth step because whatever :)
        if self.sleep_rounds <= 0:
            if self.rnd.random() > 0.75:
                self.sleep_rounds = 3

        if self.sleep_rounds > 0:
            self.sleep_rounds -= 1
            texts = ["Too much Μαστίχα", "#aspp2017", "Python School Νικήτη"]
            self.say(self.rnd.choice(texts))
            return stop

    def find_distance(self, pos, pos_list, minimum=True):
        '''
        Uses current position and list of all enemy food positions to calculate
        nearest food based on euclidean dist.
        returns the position of the
        '''
        pos_dict = {}
        for pos_option in pos_list:
            pos_dict[pos_option] = np.linalg.norm(np.array(pos_option)-np.array(pos))

        if minimum:
            return min(pos_dict, key=pos_dict.get)
        else:
            return max(pos_dict, key=pos_dict.get)

    def get_move(self):
        #utility_function()
        my_current_pos = self.current_pos
        enemy_food_map = self.enemy_food

        self.next_food = self.find_distance(my_current_pos, enemy_food_map,minimum=True)
        next_pos = self.goto_pos(self.next_food)

        move = diff_pos(self.current_pos, next_pos)
        return move

class KillerDefender(AbstractPlayer):

    def __init__(self):
        # Do some basic initialisation here. You may also accept additional
        # parameters which you can specify in your factory.
        # Note that any other game variables have not been set yet. So there is
        # no ``self.current_uni`` or ``self.current_state``
        self.sleep_rounds = 0

    def goto_pos(self, pos):
        return self.adjacency.a_star(self.current_pos, pos)[-1]

    def set_initial(self):
        # Now ``self.current_uni`` and ``self.current_state`` are known.
        # ``set_initial`` is always called before ``get_move``, so we can do some
        # additional initialisation here

        # Just printing the universe to give you an idea, please remove all
        # print statements in the final player.
        #self.universe_states = []
        #print(self.current_uni)
        self.adjacency = AdjacencyList(self.current_uni.reachable([self.initial_pos]))
        self.next_food = None
        self.history_pos = [None]*4
        self.is_goal_set = False
        self.border_list = self.team_border

    def set_goal(self, pos, pos_list, flag=False):
        self.goal_border = self.find_closest_position(pos,
                                            pos_list,
                                            minimum=flag)
        self.is_goal_set = True

    def find_closest_position(self, pos, pos_list, minimum=True):
        '''
        Uses current position and list of all enemy food positions to calculate
        nearest food based on euclidean dist.
        returns the position and the distance of the nearest or furthest point in pos_list
        '''
        pos_dict = {}
        for pos_option in pos_list:
            pos_dict[pos_option] = np.linalg.norm(np.array(pos_option)-np.array(pos))

        if minimum:
            min_pos = min(pos_dict, key=pos_dict.get)
            return min_pos
        else:
            max_pos = max(pos_dict, key=pos_dict.get)
            return max_pos

    def get_move(self):
        #utility_function()
        #getting my current positions
        my_current_pos = self.current_pos
        enemies_eater_positions = [bot.current_pos
                               for bot in self.enemy_bots if not bot.is_destroyer]
        #print(enemy_eater_pos)
        if not self.is_goal_set:
            self.say("Hmm...")
            #set a the furthest border position as goal
            self.set_goal(my_current_pos,self.border_list)
            #we always need to return a move
            #we return stop until next border goal is set
            return stop

        if enemies_eater_positions:
            self.say("Get the $%!@^& out!!!")
            closest_enemy_pos = self.find_closest_position(my_current_pos,
                                                        enemies_eater_positions)
            next_pos = self.goto_pos(closest_enemy_pos)
            move = diff_pos(my_current_pos, next_pos)
            return move

        else:
            self.say("Trolling...")
            next_pos = self.goto_pos(self.goal_border)
            move = diff_pos(my_current_pos, next_pos)
            if next_pos in self.border_list or my_current_pos in self.border_list:
                self.is_goal_set = False
                return stop

            return move

def factory():
    return SimpleTeam("VS TEAM", KillerDefende(), KillerDefender())
