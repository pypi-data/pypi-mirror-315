from primate.decision.agent import DecisionAgent

# Define reward matrix
reward_matrix = {
    (1, 1): 3,  # Both cooperate
    (1, 0): 0,  # Agent cooperates, opponent defects
    (0, 1): 5,  # Agent defects, opponent cooperates
    (0, 0): 1,  # Both defect
}

# Create agents
agent1 = DecisionAgent(name="Agent1", strategy="neural_net", history_size=10)
agent2 = DecisionAgent(name="Agent2", strategy="random", cooperation_prob=0.7)

# Simulate rounds
for round_num in range(20):
    opponent_action = agent2.decide()
    action = agent1.decide(opponent_action)

    # Train neural network with feedback
    agent1.train_neural_network(reward_matrix)

    # Print round results
    print(f"Round {round_num + 1}: Agent1 = {action}, Agent2 = {opponent_action}")

# Debug histories
agent1.print_history()
agent2.print_history()
