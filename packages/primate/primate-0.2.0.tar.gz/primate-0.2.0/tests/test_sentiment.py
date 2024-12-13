from primate.nlp.sentiment import PretrainedSentimentAnalyzer, CustomSentimentModel, SentimentTrainer
from torch.utils.data import DataLoader, TensorDataset
import torch
import torch.nn as nn  # Missing import added
import numpy as np


# Example Data
texts = [
    "I love this movie!",
    "This is the worst experience I've ever had.",
    "It's okay, nothing special but not bad either."
]
labels = [2, 0, 1]  # 2 = Positive, 0 = Negative, 1 = Neutral

# Testing PretrainedSentimentAnalyzer
print("Testing PretrainedSentimentAnalyzer...")
pretrained_analyzer = PretrainedSentimentAnalyzer(model_name="distilbert-base-uncased")
predictions = pretrained_analyzer.predict(texts)
print("Predicted Sentiments:", predictions)

# Testing CustomSentimentModel
print("\nTesting CustomSentimentModel...")
input_dim = 300  # Assume input embeddings are 300-dimensional
hidden_dim = 128
num_classes = 3
custom_model = CustomSentimentModel(input_dim, hidden_dim, num_classes)

# Create random synthetic data for testing
np.random.seed(42)
inputs = torch.tensor(np.random.rand(100, input_dim), dtype=torch.float32)
labels = torch.tensor(np.random.randint(0, num_classes, size=100), dtype=torch.long)

# Create DataLoader
dataset = TensorDataset(inputs, labels)
data_loader = DataLoader(dataset, batch_size=16, shuffle=True)

# Initialize Trainer
optimizer = torch.optim.Adam(custom_model.parameters(), lr=0.001)
loss_fn = nn.CrossEntropyLoss()
trainer = SentimentTrainer(custom_model, optimizer, loss_fn, device="cpu")

# Train the model
print("Training Custom Model...")
trainer.train(data_loader, epochs=5)

# Evaluate the model
print("\nEvaluating Custom Model...")
evaluation_report = trainer.evaluate(data_loader)
print("Evaluation Report:", evaluation_report)
