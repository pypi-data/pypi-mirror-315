import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel


class StaticEmbedding:
    """
    Handles static embeddings like GloVe or FastText.

    Parameters
    ----------
    embedding_file : str
        Path to the pre-trained embedding file.
    """

    def __init__(self, embedding_file):
        self.embedding_file = embedding_file
        self.word_to_index = {}
        self.index_to_vector = []

        self._load_embeddings()

    def _load_embeddings(self):
        """
        Load static embeddings from a file.
        """
        print(f"Loading embeddings from {self.embedding_file}...")
        with open(self.embedding_file, "r", encoding="utf-8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = torch.tensor([float(x) for x in values[1:]], dtype=torch.float32)
                self.word_to_index[word] = len(self.index_to_vector)
                self.index_to_vector.append(vector)
        self.index_to_vector = torch.stack(self.index_to_vector)
        print(f"Loaded {len(self.word_to_index)} embeddings.")

    def get_embedding(self, word):
        """
        Get the embedding for a given word.

        Parameters
        ----------
        word : str
            The word to retrieve the embedding for.

        Returns
        -------
        torch.Tensor
            The embedding vector.
        """
        index = self.word_to_index.get(word, None)
        if index is None:
            raise ValueError(f"Word '{word}' not found in the embedding vocabulary.")
        return self.index_to_vector[index]

    def similarity(self, word1, word2):
        """
        Compute cosine similarity between two word embeddings.

        Parameters
        ----------
        word1 : str
            The first word.
        word2 : str
            The second word.

        Returns
        -------
        float
            Cosine similarity score.
        """
        embedding1 = self.get_embedding(word1)
        embedding2 = self.get_embedding(word2)
        return torch.nn.functional.cosine_similarity(embedding1.unsqueeze(0), embedding2.unsqueeze(0)).item()


class ContextualEmbedding:
    """
    Handles contextual embeddings using transformer models like BERT.

    Parameters
    ----------
    model_name : str
        Name of the transformer model to use.
    """

    def __init__(self, model_name="bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def get_embedding(self, sentence):
        """
        Get contextual embeddings for a given sentence.

        Parameters
        ----------
        sentence : str
            The input sentence.

        Returns
        -------
        torch.Tensor
            The embedding for the sentence.
        """
        inputs = self.tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
        outputs = self.model(**inputs)
        # Return the CLS token's embedding
        return outputs.last_hidden_state[:, 0, :]

    def sentence_similarity(self, sentence1, sentence2):
        """
        Compute cosine similarity between two sentence embeddings.

        Parameters
        ----------
        sentence1 : str
            The first sentence.
        sentence2 : str
            The second sentence.

        Returns
        -------
        float
            Cosine similarity score.
        """
        embedding1 = self.get_embedding(sentence1)
        embedding2 = self.get_embedding(sentence2)
        return torch.nn.functional.cosine_similarity(embedding1, embedding2).item()


class CustomEmbedding(nn.Module):
    """
    Custom embedding layer for specific NLP tasks.

    Parameters
    ----------
    vocab_size : int
        Size of the vocabulary.
    embedding_dim : int
        Dimension of the embeddings.
    """

    def __init__(self, vocab_size, embedding_dim):
        super(CustomEmbedding, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)

    def forward(self, input_ids):
        """
        Forward pass to retrieve embeddings for input IDs.

        Parameters
        ----------
        input_ids : torch.Tensor
            Tensor of input token IDs.

        Returns
        -------
        torch.Tensor
            Embedding vectors.
        """
        return self.embedding(input_ids)

    def freeze_embeddings(self):
        """
        Freeze the embedding weights (useful for fine-tuning).
        """
        self.embedding.weight.requires_grad = False

    def unfreeze_embeddings(self):
        """
        Unfreeze the embedding weights.
        """
        self.embedding.weight.requires_grad = True
