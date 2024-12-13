import torch
import torch.nn as nn
import torch.optim as optim
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, classification_report


class SentimentAnalyzer:
    """
    Wrapper for sentiment analysis using a pre-trained transformer model.
    """

    def __init__(self, model_name="distilbert-base-uncased"):
        self.analyzer = PretrainedSentimentAnalyzer(model_name=model_name)

    def analyze(self, text):
        """
        Analyzes the sentiment of a single text.

        Parameters
        ----------
        text : str
            Input text.

        Returns
        -------
        str
            Sentiment label ("positive", "negative", "neutral").
        """
        label_map = {0: "negative", 1: "neutral", 2: "positive"}
        prediction = self.analyzer.predict([text])[0]
        return label_map[prediction]


class PretrainedSentimentAnalyzer:
    """
    Sentiment analyzer using pre-trained transformer models.

    Parameters
    ----------
    model_name : str
        Name of the pre-trained transformer model to use.
    """

    def __init__(self, model_name="distilbert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

    def predict(self, texts):
        """
        Predict sentiment for a list of texts.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        list
            Predicted sentiment labels.
        """
        inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
        return predictions.tolist()


class CustomSentimentModel(nn.Module):
    """
    Custom PyTorch model for sentiment analysis.
    """

    def __init__(self, input_dim, hidden_dim, num_classes):
        super(CustomSentimentModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, num_classes)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        """
        Forward pass through the model.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor.

        Returns
        -------
        torch.Tensor
            Class probabilities.
        """
        x = torch.relu(self.fc1(x))
        x = self.softmax(self.fc2(x))
        return x


class SentimentTrainer:
    """
    Trainer for the custom sentiment analysis model.

    Parameters
    ----------
    model : nn.Module
        PyTorch model for sentiment analysis.
    optimizer : torch.optim.Optimizer
        Optimizer for training the model.
    loss_fn : nn.Module
        Loss function for training.
    device : torch.device
        Device to train on (CPU or GPU).
    """

    def __init__(self, model, optimizer, loss_fn, device="cpu"):
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.device = device
        self.model.to(self.device)

    def train(self, data_loader, epochs=5):
        """
        Train the sentiment model.

        Parameters
        ----------
        data_loader : torch.utils.data.DataLoader
            DataLoader for training data.
        epochs : int
            Number of training epochs.

        Returns
        -------
        list
            Training loss for each epoch.
        """
        self.model.train()
        losses = []
        for epoch in range(epochs):
            total_loss = 0
            for batch in data_loader:
                inputs, labels = batch
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                # Forward pass
                outputs = self.model(inputs)
                loss = self.loss_fn(outputs, labels)

                # Backward pass
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()

            avg_loss = total_loss / len(data_loader)
            losses.append(avg_loss)
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")
        return losses

    def evaluate(self, data_loader):
        """
        Evaluate the sentiment model.

        Parameters
        ----------
        data_loader : torch.utils.data.DataLoader
            DataLoader for evaluation data.

        Returns
        -------
        dict
            Evaluation metrics.
        """
        self.model.eval()
        all_labels = []
        all_preds = []

        with torch.no_grad():
            for batch in data_loader:
                inputs, labels = batch
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                predictions = torch.argmax(outputs, dim=-1)

                all_labels.extend(labels.cpu().numpy())
                all_preds.extend(predictions.cpu().numpy())

        accuracy = accuracy_score(all_labels, all_preds)
        report = classification_report(all_labels, all_preds, output_dict=True)
        print("Evaluation Accuracy:", accuracy)
        return report
