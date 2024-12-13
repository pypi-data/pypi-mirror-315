import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


class Environment:
    """
    A simulation environment for multi-agent interactions with reinforcement learning.

    Parameters
    ----------
    agents : list
        List of agents participating in the environment.
    reward_matrix : dict
        Reward matrix defining rewards for action pairs.
    rounds : int, optional
        Number of rounds to simulate. Default is 10.
    """

    def __init__(self, agents, reward_matrix, rounds=10):
        self.agents = agents
        self.reward_matrix = reward_matrix
        self.rounds = rounds
        self.history = []  # Record of all actions and rewards
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def run_round(self):
        """
        Execute a single round of interactions between agents.

        Returns
        -------
        dict
            Results of the round (actions, rewards, and scores).
        """
        round_results = {}
        actions = []
        rewards = []

        for i, agent in enumerate(self.agents):
            opponent = self.agents[(i + 1) % len(self.agents)]  # Round-robin opponent selection
            opponent_action = opponent.decide(agent.history[-1][0] if agent.history else None)
            action = agent.decide(opponent_action)

            # Reward calculation
            reward = self.reward_matrix.get((action, opponent_action), 0)
            agent.score += reward
            opponent.score += self.reward_matrix.get((opponent_action, action), 0)

            # Update history
            self.history.append((agent.name, action, opponent.name, opponent_action, reward))
            actions.append((agent.name, action))
            rewards.append(reward)

            # Log results
            round_results[agent.name] = {
                "action": action,
                "score": agent.score,
                "reward": reward,
            }

        return round_results

    def run_simulation(self):
        """
        Run the entire simulation for the specified number of rounds.

        Returns
        -------
        list
            Interaction history for the simulation.
        """
        for round_num in range(self.rounds):
            print(f"=== Round {round_num + 1} ===")
            results = self.run_round()
            for agent_name, data in results.items():
                print(f"Agent {agent_name}: Action = {data['action']}, Reward = {data['reward']}, Score = {data['score']}")

        return self.history

    def batch_train_policies(self, policy_model, optimizer, batch_size=32, epochs=5):
        """
        Train policies using PyTorch for multiple agents in a batched manner.

        Parameters
        ----------
        policy_model : nn.Module
            PyTorch model representing the policy.
        optimizer : torch.optim.Optimizer
            Optimizer for updating the policy.
        batch_size : int, optional
            Number of samples per batch. Default is 32.
        epochs : int, optional
            Number of training epochs. Default is 5.
        """
        print("Starting policy training...")
        data = self._prepare_training_data()

        for epoch in range(epochs):
            total_loss = 0
            for batch_start in range(0, len(data["inputs"]), batch_size):
                batch_end = batch_start + batch_size
                batch_inputs = torch.tensor(data["inputs"][batch_start:batch_end], dtype=torch.float32).to(self.device)
                batch_targets = torch.tensor(data["targets"][batch_start:batch_end], dtype=torch.float32).to(self.device)

                # Forward pass
                predictions = policy_model(batch_inputs)
                loss = nn.MSELoss()(predictions, batch_targets)

                # Backward pass
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss:.4f}")

    def _prepare_training_data(self):
        """
        Prepare training data for policy optimization.

        Returns
        -------
        dict
            Inputs and targets for training.
        """
        inputs = []
        targets = []

        for record in self.history:
            agent_name, action, opponent_name, opponent_action, reward = record

            # One-hot encode actions
            action_vector = [1 if action == "cooperate" else 0, 1 if action == "defect" else 0]
            opponent_vector = [1 if opponent_action == "cooperate" else 0, 1 if opponent_action == "defect" else 0]

            # Input: agent + opponent actions
            inputs.append(action_vector + opponent_vector)
            # Target: reward
            targets.append(reward)

        return {"inputs": inputs, "targets": targets}

    def summarize_results(self):
        """
        Summarize the simulation results.

        Returns
        -------
        dict
            Aggregated scores for each agent.
        """
        scores = {agent.name: agent.score for agent in self.agents}
        print("\n=== Simulation Summary ===")
        for name, score in scores.items():
            print(f"Agent {name}: Total Score = {score}")
        return scores
