import torch
from game import Game
from table import Table
from player import humanPlayer 
from agent import Agent

# --- CONFIGURATION ---
EPISODES = 1000000
STACK_SIZE = 1000
TARGET_UPDATE = 1000

def main():
    print("Setting up the table...")
    table = Table()
    game = Game(table)
    
    Hero = humanPlayer("Hero", table)
    Villain = humanPlayer("Villain", table)
    game.players = [Hero, Villain]
    
    initial_state = game.reset()
    input_size = len(initial_state)
    
    agent = Agent(input_size, output_size=7)
    print("Agent initialized.")

    print("Starting training...")
    wins = 0
    
    for episode in range(EPISODES):
        for p in game.players:
            if p.chips <= 0:
                p.chips = STACK_SIZE

        state = game.reset()
        
        done = False
        while not done:
            
            action = agent.select_action(state)

            next_state, reward, done = game.step(action)
            if reward > 0:
                wins += 1
            
            agent.memory.append((state, action, reward, next_state, done))

            agent.optimize_model()

            state = next_state

        
        if episode % TARGET_UPDATE == 0:
            agent.target_net.load_state_dict(agent.policy_net.state_dict())

        if agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay

        if episode % 50 == 0:
            print(f"Episode {episode}/{EPISODES} completed. Epsilon: {agent.epsilon:.3f}")
        if episode % 1000 == 0:
            print(f"Episode {episode}: Win Rate {wins/1000:.2%}, Epsilon {agent.epsilon:.4f}")
            wins = 0
    print("Training Complete. Saving the model...")
    torch.save(agent.policy_net.state_dict(), "poker_agent.pth")
    print("Model saved as 'poker_agent.pth'.")    

if __name__ == "__main__":
    main()