import torch
from foodBERT.foodbert.helpers.prediction_model import PredictionModel

# Initialize model
model = PredictionModel()

# Print device info
print(f"\nModel device: {next(model.model.parameters()).device}")

# Test with a sample ingredient
test_ingredient = "chicken breast"
print(f"\nTesting with ingredient: {test_ingredient}")

# Get embedding using tokenizer.encode
encoded = model.tokenizer.encode(test_ingredient)
input_ids = encoded['input_ids'].to(model.device)

# Generate embedding
with torch.no_grad():
    embeddings = model.model(input_ids)
    embedding = embeddings.mean(dim=1)  # Average over token embeddings
    
print(f"Embedding device: {embedding.device}")
print(f"Embedding shape: {embedding.shape}")
