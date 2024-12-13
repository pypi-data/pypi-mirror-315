from primate.nlp.embedding import StaticEmbedding, ContextualEmbedding, CustomEmbedding
import torch


# Test Static Embedding
print("Testing Static Embedding...")
# Simulate loading embeddings from a file (example format for real usage)
with open("example_glove.txt", "w") as f:
    f.write("word1 0.1 0.2 0.3 0.4\n")
    f.write("word2 0.4 0.3 0.2 0.1\n")
    f.write("word3 0.5 0.5 0.5 0.5\n")

static_embedding = StaticEmbedding("example_glove.txt")
print("Embedding for 'word1':", static_embedding.get_embedding("word1"))
print("Similarity between 'word1' and 'word2':", static_embedding.similarity("word1", "word2"))

# Test Contextual Embedding
print("\nTesting Contextual Embedding...")
contextual_embedding = ContextualEmbedding(model_name="distilbert-base-uncased")
sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "A fast brown fox leapt over a sleeping dog."
embedding1 = contextual_embedding.get_embedding(sentence1)
embedding2 = contextual_embedding.get_embedding(sentence2)
print("Sentence Embedding Shape:", embedding1.shape)
print("Similarity between sentences:", contextual_embedding.sentence_similarity(sentence1, sentence2))

# Test Custom Embedding
print("\nTesting Custom Embedding...")
vocab_size = 1000
embedding_dim = 50
custom_embedding = CustomEmbedding(vocab_size, embedding_dim)
input_ids = torch.randint(0, vocab_size, (10,))
embeddings = custom_embedding(input_ids)
print("Custom Embedding Shape:", embeddings.shape)

# Test freezing and unfreezing
custom_embedding.freeze_embeddings()
print("Embedding weights frozen:", not custom_embedding.embedding.weight.requires_grad)
custom_embedding.unfreeze_embeddings()
print("Embedding weights unfrozen:", custom_embedding.embedding.weight.requires_grad)
