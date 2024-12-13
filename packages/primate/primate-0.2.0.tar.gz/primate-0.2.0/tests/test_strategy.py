import torch
import torch.optim as optim
from primate.decision.strategy import (
    RandomStrategy,
    TitForTatStrategy,
    PolicyGradientStrategy,
    AdaptiveStrategy,
)


# Test Random Strategy
random_strategy = RandomStrategy(cooperation_prob=0.7)
for _ in range(10):
    print(f"Random Strategy Decision: {random_strategy.decide()}")

# Test Tit-for-Tat Strategy
tit_for_tat_strategy = TitForTatStrategy()
opponent_actions = ["cooperate", "defect", "cooperate", None]
for opponent_action in opponent_actions:
    print(f"Tit-for-Tat Decision: {tit_for_tat_strategy.decide(opponent_action)}")

# Test Policy Gradient Strategy
policy_strategy = PolicyGradientStrategy(input_dim=4, hidden_dim=16, action_space=2)
optimizer = optim.Adam(policy_strategy.parameters(), lr=0.01)

# Simulate interactions and train
states = [torch.rand(4) for _ in range(20)]
actions = [torch.randint(0, 2, (1,)).item() for _ in range(20)]
rewards = [1 if a == 0 else -1 for a in actions]  # Reward structure

for state, action, reward in zip(states, actions, rewards):
    policy_strategy.store_transition(state, action, reward)

print("Training Policy Gradient Strategy...")
policy_strategy.train_policy(optimizer)

# Test Adaptive Strategy
adaptive_strategy = AdaptiveStrategy(cooperation_threshold=0.6)
for opponent_action in ["cooperate", "defect", "cooperate"]:
    action = adaptive_strategy.decide(opponent_action)
    adaptive_strategy.update_history(action, opponent_action)
    print(f"Adaptive Strategy Decision: {action}")
