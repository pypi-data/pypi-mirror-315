import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque


class DecisionNetwork(nn.Module):
    """
    Neural network for decision-making based on opponent behavior.
    """

    def __init__(self, input_dim=10, hidden_dim=32, output_dim=2):
        """
        Initialize the neural network.

        Parameters
        ----------
        input_dim : int
            Dimension of the input features.
        hidden_dim : int
            Number of hidden units.
        output_dim : int
            Number of output classes (e.g., cooperate or defect).
        """
        super(DecisionNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        self.softmax = nn.Softmax(dim=-1)

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
            Output probabilities.
        """
        x = torch.relu(self.fc1(x))
        x = self.softmax(self.fc2(x))
        return x


class DecisionAgent:
    """
    Represents an agent capable of learning and decision-making using dynamic strategies.

    Parameters
    ----------
    name : str
        The name of the agent.
    strategy : str, optional
        The decision strategy used by the agent. Options are 'random', 'neural_net', 'reinforcement_learning', or 'tit_for_tat'.
        Default is 'random'.
    cooperation_prob : float, optional
        Probability of cooperating (used in probabilistic strategies). Default is 0.5.
    """

    def __init__(self, name, strategy="random", cooperation_prob=0.5, history_size=10):
        self.name = name
        self.strategy = strategy
        self.cooperation_prob = cooperation_prob
        self.history = deque(maxlen=history_size)  # Circular history buffer
        self.score = 0
        self.network = None
        self.optimizer = None

        if strategy == "neural_net":
            self._initialize_neural_network(input_dim=2 * history_size)

    def _initialize_neural_network(self, input_dim):
        """
        Initialize the neural network and optimizer for the agent.
        """
        self.network = DecisionNetwork(input_dim=input_dim)
        self.optimizer = optim.Adam(self.network.parameters(), lr=0.001)

    def decide(self, opponent_action=None):
        """
        Make a decision based on the current strategy.

        Parameters
        ----------
        opponent_action : str, optional
            The opponent's last action ('cooperate', 'defect').

        Returns
        -------
        str
            The agent's decision ('cooperate', 'defect').
        """
        if self.strategy == "random":
            action = "cooperate" if np.random.rand() < self.cooperation_prob else "defect"
        elif self.strategy == "neural_net":
            action = self._neural_net_decision(opponent_action)
        elif self.strategy == "tit_for_tat":
            action = opponent_action if opponent_action else "cooperate"
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

        self.history.append((1 if action == "cooperate" else 0, 1 if opponent_action == "cooperate" else 0))
        return action

    def _neural_net_decision(self, opponent_action):
        """
        Use the neural network to decide the next action.

        Parameters
        ----------
        opponent_action : str
            The opponent's last action.

        Returns
        -------
        str
            The agent's decision ('cooperate', 'defect').
        """
        if len(self.history) < self.history.maxlen:
            # Default to cooperating until sufficient history is collected
            return "cooperate"

        # Prepare input for the neural network
        history_flattened = np.array(self.history).flatten()
        input_tensor = torch.tensor(history_flattened, dtype=torch.float32).unsqueeze(0)

        # Forward pass through the network
        with torch.no_grad():
            output_probs = self.network(input_tensor).squeeze()
            action_index = torch.argmax(output_probs).item()

        return "cooperate" if action_index == 0 else "defect"

    def train_neural_network(self, reward_matrix):
        """
        Train the neural network using history and reward feedback.

        Parameters
        ----------
        reward_matrix : dict
            Reward matrix for scoring decisions.
        """
        if len(self.history) < self.history.maxlen:
            return  # Not enough data to train

        # Prepare training data
        history_flattened = np.array(self.history).flatten()
        input_tensor = torch.tensor(history_flattened, dtype=torch.float32).unsqueeze(0)
        last_action, opponent_action = self.history[-1]
        reward = reward_matrix.get((last_action, opponent_action), 0)
        target = torch.tensor([reward], dtype=torch.float32)

        # Forward pass
        output_probs = self.network(input_tensor)
        predicted_reward = output_probs[:, last_action]

        # Compute loss
        loss = nn.MSELoss()(predicted_reward, target)

        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def reset(self):
        """
        Reset the agent's state, including history and scores.
        """
        self.history.clear()
        self.score = 0

    def print_history(self):
        """
        Print the decision history for debugging purposes.
        """
        print(f"History for {self.name}:")
        for i, (own_action, opponent_action) in enumerate(self.history):
            own_action_str = "cooperate" if own_action == 1 else "defect"
            opponent_action_str = "cooperate" if opponent_action == 1 else "defect"
            print(f"  Round {i + 1}: Own action = {own_action_str}, Opponent action = {opponent_action_str}")
