# 1.) Set up
# --------------------------------------------------------------------------------------------------------------------------#
# Importane pizdarije
# import numpy as np
import random

# Define variables
from itertools import combinations


# --------------------------------------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------------------------------------#
# 2.) funkcija koja odreduje ko pobjeduje
# --------------------------------------------------------------------------------------------------------------------------#
def determine_winner(comp_shape, hum_shape):
    beat_relations = [[0, 2, 1], [1, 0, 2], [2, 1, 0]]  # usrana matrica
    w_p = beat_relations[comp_shape][hum_shape]
    if w_p == 2:  # pobjeda covjeka
        w_s, l_s = hum_shape, comp_shape
    elif w_p == 1:  # pobjeda kompa
        w_s, l_s = comp_shape, hum_shape
    else:  # draw
        w_s, l_s = 3, 3

    if w_s == 3:  # to je draw
        print("You both chose", comp_shape, "it's a draw")
    else:
        print(w_s, "beats", l_s, ", ", w_p, "wins")

    return w_p, w_s, l_s


# --------------------------------------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------------------------------------#
# 3.) Definiram komp igrace
# --------------------------------------------------------------------------------------------------------------------------#

class Strategy():  # superordinate class
    def play(self, win_play, win_answer):  # ovu metodu moram ubacit u svaku subklasu
        raise NotImplementedError  # ili dobijem ovaj error


# 1.) Random
class RandomStrategy(Strategy):
    def play(self, winner_player, winner_answer):
        return random.choices([0, 1, 2], [1 / 3, 1 / 3, 1 / 3], k=1)[0]


# 2.) Preferira jednu opciju
class SameMoveStrategy(Strategy):
    def play(self, winner_player, winner_answer):
        return random.choices([0, 1, 2], [2 / 3, 1 / 6, 1 / 6], k=1)[0]


# 3.) Preference ponavljanje izbora ako je pobijedio
class RepeatingStrategy(Strategy):
    def play(self, winner_player, winner_answer):
        if winner_player == 1:
            if winner_answer == 0:
                probs = [2 / 3, 1 / 6, 1 / 6]
            elif winner_answer == 1:
                probs = [1 / 6, 2 / 3, 1 / 6]
            elif winner_answer == 2:
                probs = [1 / 6, 1 / 6, 2 / 3]

                return random.choices([0, 1, 2], probs, k=1)[0]
        elif winner_player == 2 or winner_player == 0:
            probs = [1 / 3, 1 / 3, 1 / 3]
            return random.choices([0, 1, 2], probs, k=1)[0]


class VerySmartStrategy(Strategy):
    def play(self, winner_player, winner_answer):
        if winner_player == 2:
            if winner_answer == 0:
                probs = [1 / 6, 2 / 3, 1 / 6]
            elif winner_answer == 1:
                probs = [1 / 6, 1 / 6, 2 / 3]
            elif winner_answer == 2:
                probs = [2 / 3, 1 / 6, 1 / 6]
            return random.choices([0, 1, 2], probs, k=1)[0]
        elif winner_player == 1 or winner_player == 0:
            probs = [1 / 3, 1 / 3, 1 / 3]
            return random.choices([0, 1, 2], probs, k=1)[0]


# --------------------------------------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------------------------------------#
# 4.) human strat ovdje definiram
# --------------------------------------------------------------------------------------------------------------------------#


class HumanStrategy(Strategy):
    def play(self, win_player, win_something):
        elements = [0, 1, 2]
        while True:
            player_choice = int(
                input("Make your choice. 0 is Rock, 1 is Paper and 2 is Scissors\n"))  # 1 - ROCK 2 - PAPER 3 - SCISSORS
            if player_choice in elements:
                break

        return player_choice


# --------------------------------------------------------------------------------------------------------------------------#


# --------------------------------------------------------------------------------------------------------------------------#
# 5.) Game loop
# --------------------------------------------------------------------------------------------------------------------------#
def game_loop(total_players, schedule):
    total_players_nr = len(total_players)
    scoring_table = [0] * total_players_nr
    nr_of_rounds = int(input("How many rounds would you like to play?\n"))

    for match in schedule:
        rounds_played = 0
        winner_player = 0  # 0: draw, 1: computer player, 2: human player
        winner_answer = 0  # 3: draw, 0: rock, 1: paper, 2: scissors
        while rounds_played < int(nr_of_rounds):
            print("\n")
            player_1_idx, player_2_idx = schedule[schedule.index(match)]
            player_1 = total_players[player_1_idx]
            player_2 = total_players[player_2_idx]

            player_1_choice = player_1.play(winner_player, winner_answer)
            player_2_choice = player_2.play(winner_player, winner_answer)

            print(player_1_choice, player_2_choice)

            winner_player, winner_answer, l_s = determine_winner(player_1_choice, player_2_choice)

            rounds_played = rounds_played + 1
            if winner_player == 1:
                scoring_table[player_1_idx] = scoring_table[player_1_idx] + 1
            elif winner_player == 2:
                scoring_table[player_2_idx] = scoring_table[player_2_idx] + 1

    # End of game
    winning_index = scoring_table.index(max(scoring_table))
    print("Winning player was: ", winning_index + 1)


# --------------------------------------------------------------------------------------------------------------------------#
# 6.) Play
# --------------------------------------------------------------------------------------------------------------------------#
# SVE STRATEGIJE:
strategyA = RandomStrategy()
strategyB = SameMoveStrategy()
strategyC = RepeatingStrategy()
strategyD = VerySmartStrategy()
hp = HumanStrategy()  # OVO MI TREBA KAO ARGUMENT U GAME LOOPU

strategies = [strategyA, strategyB, strategyC, strategyD]
players = []

total_hp = int(input("How many human players are you?\n"))
for i in range(total_hp):
    players.append(hp)

total_cp = int(input("How many computer players are you?\n"))
for i in range(total_cp):
    while True:
        opponent = int(input("Which computer player you want to play against? Choose between 1, 2, 3 or 4 \n"))
        if (opponent <= 0) or (opponent > 4):
            print("Your choice was invalid. It has to be a number between 1-4")
            continue
        players.append(strategies[opponent - 1])
        break

player_indices = [i * 1 for i in range(total_hp + total_cp)]  # list of player indices, total_players_nr in total
game_schedule = [comb for comb in combinations(player_indices, 2)]  # every unique, 2-element combination
print("The tournament schedule is as following: ", game_schedule)

# Initiate the game
game_loop(players, game_schedule)
