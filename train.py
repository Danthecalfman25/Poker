import torch
from game import Game
from table import Table
from player import humanPlayer 
from agent import Agent

EPISODES = 200000
STACK_SIZE = 1000
TARGET_UPDATE = 1000

def main():
    print("Setting up the table...")
    table = Table()
    game = Game(table)
    
    p1 = humanPlayer("Hero", table)
    p2 = humanPlayer("Villain", table)
    game.players = [p1, p2]
    
    initial_state = game.reset()
    input_size = len(initial_state) 
    print(f"State Size: {input_size}")
    
    agent = Agent(input_size, output_size=7)
    print("Starting Training...")

    total_profit = 0
    best_profit = -float('inf')
    
    for episode in range(EPISODES):
        if game.players[0].chips <= 0 or game.players[1].chips <= 0:
            for p in game.players:
                p.chips = STACK_SIZE

        state = game.reset()
        hero = game.players[0]
        starting_stack = hero.chips
        
        done = False
        while not done:
            valid_actions = game.get_valid_actions()
            action = agent.select_action(state, valid_actions)
            
            next_state, reward, done = game.step(action)
            
            agent.memory.append((state, action, reward, next_state, done))
            agent.optimize_model()

            state = next_state

        profit = hero.chips - starting_stack
        total_profit += profit

        if episode % TARGET_UPDATE == 0:
            agent.target_net.load_state_dict(agent.policy_net.state_dict())

        if agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay

        if episode % 1000 == 0 and episode > 0:
            avg_profit = total_profit / 1000
            print(f"Ep {episode}: Avg Profit/Hand: {avg_profit:.2f} | Epsilon {agent.epsilon:.4f}")
            
            if avg_profit > best_profit and episode > 10000:
                best_profit = avg_profit
                torch.save(agent.policy_net.state_dict(), "poker_shark_best.pth")
                print(f"   >>> New Record! Saved best model.")
            
            total_profit = 0

        if episode % 50000 == 0 and episode > 0:
            torch.save(agent.policy_net.state_dict(), f"checkpoint_{episode}.pth")

    print("Training Complete.")
    torch.save(agent.policy_net.state_dict(), "poker_agent_final.pth")

if __name__ == "__main__":
    main()