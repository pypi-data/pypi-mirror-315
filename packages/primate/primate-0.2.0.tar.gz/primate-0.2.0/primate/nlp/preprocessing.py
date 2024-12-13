import torch
from transformers import AutoTokenizer
from sklearn.model_selection import train_test_split
import re
import numpy as np


class TextPreprocessor:
    """
    Handles text preprocessing tasks, including cleaning, tokenization, and batching.
    """

    def __init__(self, model_name="bert-base-uncased", max_length=128):
        """
        Initialize the TextPreprocessor with a tokenizer and max sequence length.

        Parameters
        ----------
        model_name : str
            Name of the transformer model tokenizer.
        max_length : int
            Maximum sequence length for tokenization.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_length = max_length

    def clean_text(self, text):
        """
        Cleans the input text by removing special characters and extra spaces.

        Parameters
        ----------
        text : str
            The input text.

        Returns
        -------
        str
            The cleaned text.
        """
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, texts):
        """
        Tokenize and encode a list of texts using the tokenizer.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        dict
            Tokenized output with input IDs and attention masks.
        """
        return self.tokenizer(
            texts,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

    def preprocess(self, texts):
        """
        Clean and tokenize input texts.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        dict
            Preprocessed data with input IDs and attention masks.
        """
        cleaned_texts = [self.clean_text(text) for text in texts]
        return self.tokenize(cleaned_texts)


class DataBatcher:
    """
    Handles batching and preparing data for deep learning models.
    """

    def __init__(self, batch_size=32):
        """
        Initialize the DataBatcher with a specified batch size.

        Parameters
        ----------
        batch_size : int
            Number of samples per batch.
        """
        self.batch_size = batch_size

    def create_batches(self, input_ids, attention_masks, labels=None):
        """
        Create batches from tokenized input data and labels.

        Parameters
        ----------
        input_ids : torch.Tensor
            Tokenized input IDs.
        attention_masks : torch.Tensor
            Attention masks corresponding to the input IDs.
        labels : torch.Tensor, optional
            Labels for the input data.

        Returns
        -------
        list of dict
            List of batches containing input IDs, attention masks, and labels.
        """
        dataset = []
        for i in range(0, len(input_ids), self.batch_size):
            batch = {
                "input_ids": input_ids[i:i + self.batch_size],
                "attention_masks": attention_masks[i:i + self.batch_size],
            }
            if labels is not None:
                batch["labels"] = labels[i:i + self.batch_size]
            dataset.append(batch)
        return dataset


def split_data(input_texts, labels, test_size=0.2):
    """
    Split data into training and testing sets.

    Parameters
    ----------
    input_texts : list of str
        List of input texts.
    labels : list
        List of labels corresponding to the input texts.
    test_size : float
        Fraction of data to be used for testing.

    Returns
    -------
    tuple
        Training and testing sets (texts and labels).
    """
    return train_test_split(input_texts, labels, test_size=test_size, random_state=42)


class EmbeddingGenerator:
    """
    Generates embeddings for input texts using a transformer model.

    Parameters
    ----------
    model_name : str
        Name of the transformer model to use.
    """

    def __init__(self, model_name="bert-base-uncased"):
        from transformers import AutoModel
        self.model = AutoModel.from_pretrained(model_name)

    def generate_embeddings(self, input_ids, attention_masks):
        """
        Generate embeddings for input texts.

        Parameters
        ----------
        input_ids : torch.Tensor
            Tokenized input IDs.
        attention_masks : torch.Tensor
            Attention masks corresponding to the input IDs.

        Returns
        -------
        torch.Tensor
            Generated embeddings.
        """
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_masks)
            return outputs.last_hidden_state[:, 0, :]  # CLS token embeddings
