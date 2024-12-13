import torch
from transformers import AutoTokenizer


class Tokenizer:
    """
    Tokenizer class for text tokenization and detokenization.

    Parameters
    ----------
    model_name : str
        Name of the pre-trained model's tokenizer to use.
    max_length : int
        Maximum sequence length for tokenization.
    """

    def __init__(self, model_name="bert-base-uncased", max_length=128):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_length = max_length

    def tokenize(self, texts):
        """
        Tokenizes a list of texts.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        dict
            Tokenized outputs including input IDs and attention masks.
        """
        return self.tokenizer(
            texts,
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt"
        )

    def detokenize(self, input_ids):
        """
        Detokenizes input IDs back into text.

        Parameters
        ----------
        input_ids : torch.Tensor
            Token IDs.

        Returns
        -------
        list of str
            List of detokenized texts.
        """
        return self.tokenizer.batch_decode(input_ids, skip_special_tokens=True)

    def special_tokens(self):
        """
        Returns the special tokens of the tokenizer.

        Returns
        -------
        dict
            Dictionary of special tokens.
        """
        return self.tokenizer.special_tokens_map

    def encode(self, text):
        """
        Encodes a single text into input IDs.

        Parameters
        ----------
        text : str
            Input text.

        Returns
        -------
        torch.Tensor
            Encoded input IDs.
        """
        return torch.tensor(self.tokenizer.encode(text, truncation=True, max_length=self.max_length))

    def decode(self, input_ids):
        """
        Decodes input IDs back into text.

        Parameters
        ----------
        input_ids : torch.Tensor
            Token IDs.

        Returns
        -------
        str
            Decoded text.
        """
        return self.tokenizer.decode(input_ids, skip_special_tokens=True)

    def batch_encode(self, texts):
        """
        Batch encodes a list of texts.

        Parameters
        ----------
        texts : list of str
            List of input texts.

        Returns
        -------
        dict
            Tokenized outputs including input IDs and attention masks, all padded to uniform length.
        """
        return self.tokenize(texts)

    def batch_decode(self, batch_input_ids):
        """
        Batch decodes a list of input IDs back into texts.

        Parameters
        ----------
        batch_input_ids : torch.Tensor
            Batch of input IDs.

        Returns
        -------
        list of str
            Decoded texts.
        """
        return self.detokenize(batch_input_ids)

    def pad_sequences(self, input_ids, padding_value=0):
        """
        Pads sequences to the maximum length in the batch.

        Parameters
        ----------
        input_ids : list of torch.Tensor
            List of input ID tensors.
        padding_value : int, optional
            Value used for padding. Default is 0.

        Returns
        -------
        torch.Tensor
            Padded tensor.
        """
        max_len = max(len(ids) for ids in input_ids)
        padded = torch.stack([
            torch.cat([ids, torch.full((max_len - len(ids),), padding_value, dtype=torch.long)]) for ids in input_ids
        ])
        return padded

    def truncate_sequences(self, input_ids, max_length):
        """
        Truncates sequences to a specific maximum length.

        Parameters
        ----------
        input_ids : list of torch.Tensor
            List of input ID tensors.
        max_length : int
            Maximum sequence length.

        Returns
        -------
        list of torch.Tensor
            Truncated input IDs.
        """
        return [ids[:max_length] for ids in input_ids]
