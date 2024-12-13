import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np


class BagOfWordsVectorizer:
    """
    Bag of Words (BoW) vectorizer for text data.

    Parameters
    ----------
    max_features : int, optional
        Maximum number of features to consider. Default is 5000.
    """

    def __init__(self, max_features=5000):
        self.vectorizer = CountVectorizer(max_features=max_features)

    def fit_transform(self, texts):
        """
        Fits the vectorizer on texts and transforms them into feature vectors.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        np.ndarray
            Bag of Words feature matrix.
        """
        return self.vectorizer.fit_transform(texts).toarray()

    def transform(self, texts):
        """
        Transforms texts into feature vectors using a fitted vectorizer.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        np.ndarray
            Bag of Words feature matrix.
        """
        return self.vectorizer.transform(texts).toarray()

    def feature_names(self):
        """
        Returns the feature names extracted by the vectorizer.

        Returns
        -------
        list of str
            List of feature names.
        """
        return self.vectorizer.get_feature_names_out()


class TfidfVectorizerWrapper:
    """
    TF-IDF vectorizer for text data.

    Parameters
    ----------
    max_features : int, optional
        Maximum number of features to consider. Default is 5000.
    """

    def __init__(self, max_features=5000):
        self.vectorizer = TfidfVectorizer(max_features=max_features)

    def fit_transform(self, texts):
        """
        Fits the vectorizer on texts and transforms them into TF-IDF vectors.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        np.ndarray
            TF-IDF feature matrix.
        """
        return self.vectorizer.fit_transform(texts).toarray()

    def transform(self, texts):
        """
        Transforms texts into TF-IDF vectors using a fitted vectorizer.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        np.ndarray
            TF-IDF feature matrix.
        """
        return self.vectorizer.transform(texts).toarray()

    def feature_names(self):
        """
        Returns the feature names extracted by the vectorizer.

        Returns
        -------
        list of str
            List of feature names.
        """
        return self.vectorizer.get_feature_names_out()


class EmbeddingVectorizer:
    """
    Embedding-based vectorizer using pre-trained transformer models.

    Parameters
    ----------
    model_name : str
        Name of the transformer model to use.
    """

    def __init__(self, model_name="bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def vectorize(self, texts):
        """
        Generates embeddings for input texts.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        torch.Tensor
            Embedding matrix for input texts.
        """
        embeddings = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
                embeddings.append(outputs.last_hidden_state[:, 0, :])  # CLS token
        return torch.cat(embeddings, dim=0)

    def batch_vectorize(self, texts, batch_size=8):
        """
        Generates embeddings for input texts in batches.

        Parameters
        ----------
        texts : list of str
            List of input texts.
        batch_size : int
            Size of each batch.

        Returns
        -------
        torch.Tensor
            Embedding matrix for input texts.
        """
        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            inputs = self.tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
                embeddings.append(outputs.last_hidden_state[:, 0, :])
        return torch.cat(embeddings, dim=0)


class CombinedVectorizer:
    """
    Combines Bag of Words, TF-IDF, and Embedding vectorizers.

    Parameters
    ----------
    bow_max_features : int, optional
        Maximum number of features for Bag of Words. Default is 5000.
    tfidf_max_features : int, optional
        Maximum number of features for TF-IDF. Default is 5000.
    model_name : str, optional
        Transformer model for embeddings. Default is "bert-base-uncased".
    """

    def __init__(self, bow_max_features=5000, tfidf_max_features=5000, model_name="bert-base-uncased"):
        self.bow_vectorizer = BagOfWordsVectorizer(max_features=bow_max_features)
        self.tfidf_vectorizer = TfidfVectorizerWrapper(max_features=tfidf_max_features)
        self.embedding_vectorizer = EmbeddingVectorizer(model_name=model_name)

    def fit_transform(self, texts):
        """
        Fits and transforms texts using all vectorizers.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        dict
            Combined feature matrices from all vectorizers.
        """
        bow_features = self.bow_vectorizer.fit_transform(texts)
        tfidf_features = self.tfidf_vectorizer.fit_transform(texts)
        embedding_features = self.embedding_vectorizer.vectorize(texts)
        return {
            "bow": bow_features,
            "tfidf": tfidf_features,
            "embeddings": embedding_features
        }
