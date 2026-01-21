import torch
from game import Game
from table import Table
from player import humanPlayer 
from agent import Agent
EPISODES = 1000
STACK_SIZE = 1000
TARGET_UPDATE = 10

def main():
    table = Table()
    game = Game(table)
    Hero = humanPlayer("Hero", table)
    Villain = humanPlayer("Villain", table)
    game.players = [Hero, Villain]
    initial_state = game.reset()
    input_size = len(initial_state)
    agent = Agent(input_size, output_size = 7)
    
    print("Starting training...")
    
    for episode in range(EPISODES):
        for p in game.players:
            if p.chips <= 0:
                p.chips = STACK_SIZE

        state = game.reset()
        
        done = False
        while not done:
            pass

