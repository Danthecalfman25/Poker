import torch
from game import Game
from table import Table
from player import humanPlayer
from agent import Agent
from card import Card

MODEL_PATH = "poker_agent_final.pth"

def print_q_values(description, q_values, valid_actions):
    q_list = q_values.tolist()[0]
    print(q_list)

def main():
    table = Table()
    game = Game()

    agent = Agent(23, 7)
    game.reset()
    hero = game.players[0]

    hero.hand = [Card('A', 'S'), Card('A', 'H')]
    state = game.get_state()