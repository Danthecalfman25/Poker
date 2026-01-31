import torch
from game import Game
from table import Table
from player import humanPlayer 
from agent import Agent
import random
from calling_station import calling_station_action
EPISODES = 300000
STACK_SIZE = 1000
TARGET_UPDATE = 1000
RESUME_FILE_PATH = "poker_agent_final.pth"

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
    
    agent = Agent(input_size=44, output_size=7)

    try:
        
        saved_weights = torch.load(RESUME_FILE_PATH)
        
        agent.policy_net.load_state_dict(saved_weights)
        agent.target_net.load_state_dict(saved_weights)
        
        agent.epsilon = 0.2
        
        start_episode = 200001
        print(f">>> SUCCESS: Resuming from Episode {start_episode}")

    except FileNotFoundError:
        print(">>> WARNING: Save file not found. Starting from scratch.")
        start_episode = 0

    print("Starting Training...")
    print("PHASE 1")

    total_profit = 0
    best_profit = -float('inf')
    
    for episode in range(start_episode, EPISODES):
        if game.players[0].chips <= 0 or game.players[1].chips <= 0:
            for p in game.players:
                p.chips = STACK_SIZE
        
        if episode < 20000:
            opponent_is_station = True

        elif episode == 20000:
            print("\n" + "="*50)
            print(">>> PHASE 2 STARTED: Strategy Generalization")
            print(">>> Switching to Mixed Opponents (Soup) & Slow Decay")
            print("="*50 + "\n")
            
            agent.epsilon = 0.30   
            agent.epsilon_decay = 0.99999 
            
            opponent_is_station = (random.random() < 0.5)

        else:
            opponent_is_station = (random.random() < 0.5)

        state = game.reset()
        hero = game.players[0]
        starting_stack = hero.chips
        hero_state = None
        hero_action = None
        hero_stack_at_action = 0
        
        done = False
        while not done:
            curr_player_index = game.current_player_index
            valid_actions = game.get_valid_actions()
            
            if curr_player_index == 0:
                if hero_state is not None:
                    reward = hero.chips - hero_stack_at_action
                    
                    agent.memory.append((hero_state, hero_action, reward, state, False))
                    agent.optimize_model()
                
                hero_state = state
                hero_stack_at_action = hero.chips
                hero_action = agent.select_action(state, valid_actions)
                
                next_state, _, done = game.step(hero_action)
                
                if done:
                    reward = hero.chips - hero_stack_at_action
                    agent.memory.append((hero_state, hero_action, reward, None, True))
                    agent.optimize_model()
                
                state = next_state

            else:
                if opponent_is_station:
                    action = calling_station_action(valid_actions)
                else:
                    action = agent.select_action(state, valid_actions)
                
                next_state, _, done = game.step(action)
                
                if done:
                    if hero_state is not None:
                        reward = hero.chips - hero_stack_at_action
                        agent.memory.append((hero_state, hero_action, reward, None, True))
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
            mode_str = "Station" if opponent_is_station else "Self-Play" # Just shows last hand's mode
            
            print(f"Ep {episode}: Avg Profit: {avg_profit:.2f} | Epsilon: {agent.epsilon:.4f}")
            
            # Save "Best" Model (Only after Phase 1 is done to avoid saving a 'Nit' bot)
            if avg_profit > best_profit and episode > 20000:
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