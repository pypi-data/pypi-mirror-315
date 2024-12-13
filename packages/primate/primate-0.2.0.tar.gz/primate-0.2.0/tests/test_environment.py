import torch
import torch.nn as nn
import torch.optim as optim
from primate.decision.agent import DecisionAgent
from primate.decision.environment import Environment


class PolicyModel(nn.Module):
    """
    Neural network for agent policy optimization.
    """

    def __init__(self, input_dim=4, hidden_dim=16, output_dim=1):
        super(PolicyModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)


# Define reward matrix
reward_matrix = {
    ("cooperate", "cooperate"): 3,
    ("cooperate", "defect"): 0,
    ("defect", "cooperate"): 5,
    ("defect", "defect"): 1,
}

# Create agents
agent1 = DecisionAgent(name="Agent1", strategy="random", cooperation_prob=0.7)
agent2 = DecisionAgent(name="Agent2", strategy="random", cooperation_prob=0.6)

# Initialize environment
env = Environment(agents=[agent1, agent2], reward_matrix=reward_matrix, rounds=20)

# Run simulation
history = env.run_simulation()

# Define a policy model and optimizer
policy_model = PolicyModel(input_dim=4)
optimizer = optim.Adam(policy_model.parameters(), lr=0.01)

# Train policies
env.batch_train_policies(policy_model, optimizer, batch_size=8, epochs=10)

# Summarize results
env.summarize_results()
