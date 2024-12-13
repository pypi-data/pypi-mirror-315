import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque


class StrategyBase(nn.Module):
    """
    Base class for strategies using PyTorch.

    This serves as a foundation for building various strategies, including neural networks
    and reinforcement learning-based strategies.
    """

    def __init__(self, input_dim, hidden_dim, output_dim):
        super(StrategyBase, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        """
        Forward pass through the network.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor.

        Returns
        -------
        torch.Tensor
            Output logits.
        """
        x = torch.relu(self.fc1(x))
        return self.fc2(x)


class RandomStrategy:
    """
    Random strategy that selects actions based on a fixed probability distribution.
    """

    def __init__(self, cooperation_prob=0.5):
        self.cooperation_prob = cooperation_prob

    def decide(self):
        """
        Decide an action based on a fixed probability distribution.

        Returns
        -------
        str
            "cooperate" or "defect".
        """
        return "cooperate" if np.random.rand() < self.cooperation_prob else "defect"


class TitForTatStrategy:
    """
    Tit-for-tat strategy that mimics the opponent's previous action.
    """

    def decide(self, opponent_action=None):
        """
        Decide an action based on the opponent's previous action.

        Parameters
        ----------
        opponent_action : str, optional
            The opponent's last action.

        Returns
        -------
        str
            "cooperate" or "defect".
        """
        return opponent_action if opponent_action else "cooperate"


class PolicyGradientStrategy(nn.Module):
    """
    Policy Gradient strategy implemented using PyTorch.

    This strategy learns a policy for choosing actions based on a reward signal.
    """

    def __init__(self, input_dim, hidden_dim, action_space):
        super(PolicyGradientStrategy, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, action_space)
        self.softmax = nn.Softmax(dim=-1)

        # Reinforcement learning memory
        self.memory = []

    def forward(self, x):
        """
        Forward pass through the policy network.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor.

        Returns
        -------
        torch.Tensor
            Probability distribution over actions.
        """
        x = torch.relu(self.fc1(x))
        x = self.softmax(self.fc2(x))
        return x

    def store_transition(self, state, action, reward):
        """
        Store a transition in memory for policy gradient updates.

        Parameters
        ----------
        state : torch.Tensor
            The state vector.
        action : int
            The action index taken.
        reward : float
            The reward received.
        """
        self.memory.append((state, action, reward))

    def compute_returns(self, gamma=0.99):
        """
        Compute discounted rewards for the stored transitions.

        Parameters
        ----------
        gamma : float
            Discount factor for future rewards.

        Returns
        -------
        list
            List of discounted rewards.
        """
        discounted_rewards = []
        cumulative = 0
        for _, _, reward in reversed(self.memory):
            cumulative = reward + gamma * cumulative
            discounted_rewards.insert(0, cumulative)
        return discounted_rewards

    def train_policy(self, optimizer, gamma=0.99):
        """
        Train the policy using stored transitions and policy gradient.

        Parameters
        ----------
        optimizer : torch.optim.Optimizer
            Optimizer for updating the policy network.
        gamma : float
            Discount factor for future rewards.
        """
        if not self.memory:
            return

        states, actions, rewards = zip(*self.memory)
        states = torch.stack(states)
        actions = torch.tensor(actions)
        returns = torch.tensor(self.compute_returns(gamma))

        # Normalize returns for better gradient stability
        returns = (returns - returns.mean()) / (returns.std() + 1e-5)

        optimizer.zero_grad()
        probs = self.forward(states)
        action_probs = probs.gather(1, actions.unsqueeze(1)).squeeze()
        loss = -torch.sum(torch.log(action_probs) * returns)
        loss.backward()
        optimizer.step()

        # Clear memory
        self.memory = []


class AdaptiveStrategy:
    """
    Adaptive strategy that adjusts its decision logic based on performance.
    """

    def __init__(self, cooperation_threshold=0.7):
        self.cooperation_threshold = cooperation_threshold
        self.history = deque(maxlen=10)

    def decide(self, opponent_action=None):
        """
        Decide an action based on historical performance.

        Parameters
        ----------
        opponent_action : str, optional
            The opponent's last action.

        Returns
        -------
        str
            "cooperate" or "defect".
        """
        if len(self.history) < self.history.maxlen:
            return "cooperate"  # Default to cooperation initially

        # Calculate cooperation ratio
        cooperation_ratio = sum(1 for _, op_action in self.history if op_action == "cooperate") / len(self.history)
        return "cooperate" if cooperation_ratio >= self.cooperation_threshold else "defect"

    def update_history(self, action, opponent_action):
        """
        Update the history with the latest action pair.

        Parameters
        ----------
        action : str
            The agent's action.
        opponent_action : str
            The opponent's action.
        """
        self.history.append((action, opponent_action))
