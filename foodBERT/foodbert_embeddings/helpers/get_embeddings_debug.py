"""
Debug version of ingredient embedding generation.
Uses simplified BERT-style model without dependencies.
"""
import json
from pathlib import Path
import torch
import numpy as np

def load_vocab(vocab_file):
    """Load vocabulary from file."""
    print(f"Loading vocabulary from {vocab_file}")
    vocab = {}
    with open(vocab_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            token = line.strip()
            vocab[token] = i
    print(f"Loaded {len(vocab)} tokens")
    return vocab

def load_bert_model(config_path, model_path):
    """Load BERT model configuration and weights."""
    print(f"Loading config from {config_path}")
    with open(config_path, 'r') as f:
        config = json.load(f)
    print("Successfully loaded config")

    print(f"Loading model weights from {model_path}")
    class BertEmbeddings(torch.nn.Module):
        def __init__(self, config):
            super().__init__()
            print("Initializing model layers...")
            self.word_embeddings = torch.nn.Embedding(config["vocab_size"], config["hidden_size"])
            self.position_embeddings = torch.nn.Embedding(512, config["hidden_size"])
            self.LayerNorm = torch.nn.LayerNorm(config["hidden_size"], eps=1e-12)
            self.dropout = torch.nn.Dropout(config["hidden_dropout_prob"])
            print("Model layers initialized")

        def forward(self, input_ids):
            seq_length = input_ids.size(1)
            position_ids = torch.arange(seq_length, dtype=torch.long, device=input_ids.device)
            position_ids = position_ids.unsqueeze(0).expand_as(input_ids)
            
            words_embeddings = self.word_embeddings(input_ids)
            position_embeddings = self.position_embeddings(position_ids)
            
            embeddings = words_embeddings + position_embeddings
            embeddings = self.LayerNorm(embeddings)
            embeddings = self.dropout(embeddings)
            return embeddings

    model = BertEmbeddings(config)
    print("Loading state dict...")
    state_dict = torch.load(str(model_path), map_location='cpu')
    
    # Convert state dict keys to match our simplified model
    print("Processing state dict keys...")
    new_state_dict = {}
    for key, value in state_dict.items():
        if key.startswith('bert.embeddings.'):
            new_key = key.replace('bert.embeddings.', '')
            new_state_dict[new_key] = value
            print(f"Converting key: {key} -> {new_key}")
    
    try:
        print("Attempting strict loading...")
        model.load_state_dict(new_state_dict, strict=True)
        print("Successfully loaded model (strict mode)")
    except RuntimeError as e:
        print(f"Warning: Strict loading failed ({str(e)}), attempting flexible loading")
        model.load_state_dict(new_state_dict, strict=False)
        print("Successfully loaded model (flexible mode)")
    
    return model, config

def tokenize_text(text, vocab, max_length=512):
    """Simple whitespace tokenization and vocabulary lookup."""
    print(f"Tokenizing text: {text[:50]}...")  # Show first 50 chars
    tokens = ['[CLS]'] + text.lower().split() + ['[SEP]']
    if len(tokens) > max_length:
        print(f"Truncating tokens from {len(tokens)} to {max_length}")
        tokens = tokens[:max_length-1] + ['[SEP]']
    
    input_ids = []
    for token in tokens:
        # Get token ID from vocab, use [UNK] ID for unknown tokens
        token_id = vocab.get(token, vocab.get('[UNK]'))
        input_ids.append(token_id)
        print(f"Token: {token} -> ID: {token_id}")
    
    # Pad sequence
    padding_length = max_length - len(input_ids)
    input_ids.extend([0] * padding_length)
    print(f"Added {padding_length} padding tokens")
    
    return torch.tensor([input_ids])

def get_embeddings_debug(ingredients):
    """
    Generate embeddings for ingredients using simplified BERT model.
    
    Args:
        ingredients: List of ingredient names
        
    Returns:
        torch.Tensor of shape [num_ingredients, sequence_length, hidden_size]
    """
    print(f"\nGenerating embeddings for {len(ingredients)} ingredients")
    
    try:
        print("Loading BERT model and tokenizer...")
        model_path = Path('foodBERT/foodbert/data')
        config_path = model_path / "config.json"
        model_weights_path = model_path / "pytorch_model.bin"
        vocab_path = model_path / "bert-base-cased-vocab.txt"
        
        # Load model and vocab
        model, config = load_bert_model(config_path, model_weights_path)
        vocab = load_vocab(vocab_path)
        
        # Move model to device and set to eval mode
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)
        model.eval()
        print(f"Model ready on device: {device}")
        
        print("Processing ingredients...")
        all_embeddings = []
        
        with torch.no_grad():
            for i, ingredient in enumerate(ingredients):
                print(f"\nProcessing ingredient {i+1}/{len(ingredients)}: {ingredient}")
                # Tokenize ingredient
                input_ids = tokenize_text(ingredient, vocab).to(device)
                print(f"Input shape: {input_ids.shape}")
                
                # Get embeddings
                embedding = model(input_ids)
                print(f"Embedding shape: {embedding.shape}")
                all_embeddings.append(embedding)
        
        # Stack all embeddings
        print("Stacking embeddings...")
        embeddings = torch.cat(all_embeddings, dim=0)
        print(f"Final embedding shape: {embeddings.shape}")
        
        return embeddings

    except Exception as e:
        print(f"Error during embedding generation: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
