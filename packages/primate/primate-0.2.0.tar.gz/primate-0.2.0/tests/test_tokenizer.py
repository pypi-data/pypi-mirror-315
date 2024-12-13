from primate.nlp.tokenizer import Tokenizer

# Initialize Tokenizer
print("Testing Tokenizer...")
tokenizer = Tokenizer(model_name="distilbert-base-uncased", max_length=16)

# Example Texts
texts = [
    "Hello, how are you?",
    "PyTorch is great for deep learning.",
    "Transformers have revolutionized NLP."
]

# Tokenize Texts
print("\nTokenizing texts...")
tokenized = tokenizer.tokenize(texts)
print("Input IDs:", tokenized["input_ids"])
print("Attention Masks:", tokenized["attention_mask"])

# Detokenize Input IDs
print("\nDetokenizing input IDs...")
detokenized_texts = tokenizer.detokenize(tokenized["input_ids"])
print("Detokenized Texts:", detokenized_texts)

# Test Encode/Decode
print("\nTesting encode/decode...")
text = "I love natural language processing!"
encoded = tokenizer.encode(text)
print("Encoded Text:", encoded)
decoded = tokenizer.decode(encoded)
print("Decoded Text:", decoded)

# Test Batch Encode/Decode
print("\nTesting batch encode/decode...")
batch_encoded = tokenizer.batch_encode(texts)
print("Batch Encoded Input IDs:", batch_encoded["input_ids"])
batch_decoded = tokenizer.batch_decode(batch_encoded["input_ids"])
print("Batch Decoded:", batch_decoded)

# Test Padding
print("\nTesting padding...")
input_ids = [tokenizer.encode(text) for text in texts]
padded = tokenizer.pad_sequences(input_ids)
print("Padded Sequences:", padded)

# Special Tokens
print("\nSpecial Tokens...")
special_tokens = tokenizer.special_tokens()
print("Special Tokens:", special_tokens)
