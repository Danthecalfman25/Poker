import torch
from game import Game
from table import Table
from player import humanPlayer 
from agent import Agent

# --- CONFIGURATION ---
EPISODES = 1000000       # The Million Run
STACK_SIZE = 1000
TARGET_UPDATE = 1000     # Update target net less frequently (stability)

def main():
    print("Setting up the table...")
    table = Table()
    game = Game(table)
    
    # Create players
    # We use humanPlayer but we control them manually in the loop
    p1 = humanPlayer("Hero", table)
    p2 = humanPlayer("Villain", table)
    game.players = [p1, p2]
    
    # Run once to get dimensions
    initial_state = game.reset()
    input_size = len(initial_state)
    
    # Initialize Agent
    agent = Agent(input_size, output_size=7)
    print("Agent initialized.")
    print("Starting Marathon Training...")

    wins = 0
    best_win_rate = 0.0
    
    for episode in range(EPISODES):
        for p in game.players:
            if p.chips <= 0:
                p.chips = STACK_SIZE

        state = game.reset()
        
        hero = game.players[0]
        prev_chips = hero.chips
        
        done = False
        while not done:
            action = agent.select_action(state)
            next_state, reward, done = game.step(action)
            
            agent.memory.append((state, action, reward, next_state, done))
            agent.optimize_model()

            state = next_state

            if done:
                print(f"Start {starting_stack} -> End {hero.chips}")
                if hero.chips > starting_stack:
                    wins += 1

        
        if episode % TARGET_UPDATE == 0:
            agent.target_net.load_state_dict(agent.policy_net.state_dict())

        if agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay

        if episode % 1000 == 0 and episode > 0:
            current_win_rate = wins / 1000
            print(f"Episode {episode}: Win Rate {current_win_rate:.1%} | Epsilon {agent.epsilon:.4f}")
            
            if current_win_rate > best_win_rate and episode > 50000:
                best_win_rate = current_win_rate
                torch.save(agent.policy_net.state_dict(), "poker_shark_best.pth")
                print(f"   >>> New High Score! Saved 'poker_shark_best.pth' ({current_win_rate:.1%})")

            wins = 0 

        if episode % 100000 == 0 and episode > 0:
            torch.save(agent.policy_net.state_dict(), f"checkpoint_{episode}.pth")
            print(f"   [Checkpoint saved]")

    print("Training Complete. Saving final model...")
    torch.save(agent.policy_net.state_dict(), "poker_agent_final.pth")
    print("Model saved as 'poker_agent_final.pth'.")

if __name__ == "__main__":
    main()