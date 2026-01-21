import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import deque

EPSILON_DECAY = .995
EPSILON_MIN = 0.01
GAMMA = .99
BATCH_SIZE = 64


class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.input_layer = nn.Linear(input_size, 128)
        self.hidden_layer = nn.Linear(128,128)
        self.output_layer = nn.Linear(128, output_size)

    def forward(self, x):
        x = self.input_layer(x)
        x = F.leaky_relu(x)

        x = self.hidden_layer(x)
        x = F.leaky_relu(x)

        x = self.output_layer(x)

        return x

class Agent:
    def __init__(self, input_size, output_size):
        self.policy_net = DQN(input_size, output_size)
        self.target_net = DQN(input_size, output_size)

        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=0.001)
        self.memory = deque(maxlen=10000)

        self.epsilon = 1.0
        self.epsilon_min = EPSILON_MIN
        self.epsilon_decay = EPSILON_DECAY
        self.gamma = GAMMA
        self.batch_size = BATCH_SIZE


    def select_action(self, state):
        roll = random.random()
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        if roll < self.epsilon:
            return random.randint(0,6)
        else:
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            with torch.no_grad():
                Q_values = self.policy_net(state_tensor)
            return Q_values.argmax().item()
        
    def optimize_model(self,):
        if len(self.memory) < BATCH_SIZE:
            return
        
        experiences = random.sample(self.memory, BATCH_SIZE)

        batch_state, batch_action, batch_reward, batch_next_state, batch_done = zip(*experiences)
        
        state_batch = torch.FloatTensor(batch_state)
        action_batch = torch.LongTensor(batch_action).unsqueeze(1)
        reward_batch = torch.FloatTensor(batch_reward)
        next_state_batch = torch.FloatTensor(batch_next_state)
        done_batch = torch.FloatTensor(batch_done)

        q_values = self.policy_net(state_batch).gather(1, action_batch)
        prediction = self.target_net(next_state_batch).max(1)[0].detach()
        expected_state_action_values = reward_batch + (GAMMA * prediction * (1-done_batch))

        loss = F.smooth_l1_loss(q_values, expected_state_action_values.unsqueeze(1))
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()



