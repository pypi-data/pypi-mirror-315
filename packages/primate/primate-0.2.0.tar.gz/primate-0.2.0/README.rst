Primate AI: Tools for decision-making and NLP
=============================================

Primate AI is a Python package that bridges decision-making and natural language processing, inspired by intelligent behavior.

Features
--------

- **Decision-Making Models**:
  - Game-theoretic strategies (e.g., tit-for-tat).
  - Multi-agent simulations.
  - Reinforcement learning agents.

- **Natural Language Processing**:
  - Sentiment analysis.
  - Tokenization, text similarity, and vectorization.
  - Language evolution simulation.

- **Utility Tools**:
  - Logging and configuration management.
  - Performance profiling for PyTorch models.
  - Device helpers for GPU-accelerated computations.

Installation
------------

You can install the package via pip:

.. code-block:: bash

   pip install primate

Quick Start
-----------

Here are a few examples to get started:

### 1. Decision Agent

Simulate decision-making with game-theoretic strategies:

.. code-block:: python

   from primate.decision.agent import DecisionAgent

   # Create an agent with a strategy
   agent = DecisionAgent(strategy="tit_for_tat")
   decision = agent.decide(opponent_action="cooperate")
   print(f"Agent decided to: {decision}")

### 2. Sentiment Analysis

Analyze the sentiment of text data:

.. code-block:: python

   from primate.nlp.sentiment import SentimentAnalyzer

	# Initialize sentiment analyzer
	analyzer = SentimentAnalyzer()
	sentiment = analyzer.analyze("I love bananas!")
	print(f"Sentiment: {sentiment}")  # Output: "positive"

### 3. Tokenization with Transformers

Tokenize text using pre-trained transformer models:

.. code-block:: python

   from primate.nlp.tokenizer import Tokenizer

   # Initialize tokenizer
   tokenizer = Tokenizer(model_name="bert-base-uncased")
   tokenized = tokenizer.tokenize(["I love Python!", "NLP is fun."])
   print("Input IDs:", tokenized["input_ids"])
   print("Attention Masks:", tokenized["attention_mask"])

### 4. Model Profiling

Profile PyTorch models for parameter and operation details:

.. code-block:: python

   from primate.utils.helpers import PerformanceHelper
   import torch.nn as nn

   # Define a simple model
   class SimpleModel(nn.Module):
       def __init__(self):
           super(SimpleModel, self).__init__()
           self.linear = nn.Linear(10, 5)

       def forward(self, x):
           return self.linear(x)

   model = SimpleModel()
   profile = PerformanceHelper.profile_model(model, input_size=(1, 10))
   print(profile)

License
-------

This project is licensed under the MIT License.