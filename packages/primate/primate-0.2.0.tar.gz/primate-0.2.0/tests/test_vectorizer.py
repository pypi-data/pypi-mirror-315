from primate.nlp.vectorizer import BagOfWordsVectorizer, TfidfVectorizerWrapper, EmbeddingVectorizer, CombinedVectorizer

# Example texts
texts = [
    "I love machine learning!",
    "Transformers have revolutionized natural language processing.",
    "Deep learning is fascinating."
]

# Test Bag of Words Vectorizer
print("Testing Bag of Words Vectorizer...")
bow_vectorizer = BagOfWordsVectorizer(max_features=10)
bow_features = bow_vectorizer.fit_transform(texts)
print("Bag of Words Features:", bow_features)
print("Feature Names:", bow_vectorizer.feature_names())

# Test TF-IDF Vectorizer
print("\nTesting TF-IDF Vectorizer...")
tfidf_vectorizer = TfidfVectorizerWrapper(max_features=10)
tfidf_features = tfidf_vectorizer.fit_transform(texts)
print("TF-IDF Features:", tfidf_features)
print("Feature Names:", tfidf_vectorizer.feature_names())

# Test Embedding Vectorizer
print("\nTesting Embedding Vectorizer...")
embedding_vectorizer = EmbeddingVectorizer(model_name="distilbert-base-uncased")
embedding_features = embedding_vectorizer.vectorize(texts)
print("Embedding Features Shape:", embedding_features.shape)

# Test Combined Vectorizer
print("\nTesting Combined Vectorizer...")
combined_vectorizer = CombinedVectorizer(bow_max_features=10, tfidf_max_features=10, model_name="distilbert-base-uncased")
combined_features = combined_vectorizer.fit_transform(texts)
print("Combined Features Shapes:")
print("Bag of Words:", combined_features["bow"].shape)
print("TF-IDF:", combined_features["tfidf"].shape)
print("Embeddings:", combined_features["embeddings"].shape)
