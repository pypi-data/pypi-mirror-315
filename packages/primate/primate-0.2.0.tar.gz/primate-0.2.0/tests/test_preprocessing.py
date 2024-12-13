from primate.nlp.preprocessing import TextPreprocessor, DataBatcher, split_data, EmbeddingGenerator
import torch


# Example input texts and labels
texts = [
    "I love programming in Python!",
    "PyTorch makes deep learning so much easier.",
    "Machine learning is fascinating!",
    "Transformers have revolutionized NLP."
]
labels = [1, 1, 1, 0]  # Example labels

# Initialize TextPreprocessor
print("Testing TextPreprocessor...")
preprocessor = TextPreprocessor(model_name="distilbert-base-uncased", max_length=16)

# Preprocess texts
preprocessed_data = preprocessor.preprocess(texts)
print("Tokenized Input IDs:", preprocessed_data["input_ids"])
print("Attention Masks:", preprocessed_data["attention_mask"])

# Split data
train_texts, test_texts, train_labels, test_labels = split_data(texts, labels)
print("Training Set:", train_texts)
print("Testing Set:", test_texts)

# Initialize DataBatcher
print("\nTesting DataBatcher...")
batcher = DataBatcher(batch_size=2)
batches = batcher.create_batches(
    preprocessed_data["input_ids"],
    preprocessed_data["attention_mask"],
    torch.tensor(labels)
)

for i, batch in enumerate(batches):
    print(f"Batch {i + 1}:")
    print("Input IDs:", batch["input_ids"])
    print("Attention Masks:", batch["attention_masks"])
    print("Labels:", batch["labels"])

# Generate embeddings
print("\nTesting EmbeddingGenerator...")
embedding_generator = EmbeddingGenerator(model_name="distilbert-base-uncased")
embeddings = embedding_generator.generate_embeddings(
    preprocessed_data["input_ids"],
    preprocessed_data["attention_mask"]
)
print("Generated Embeddings Shape:", embeddings.shape)
