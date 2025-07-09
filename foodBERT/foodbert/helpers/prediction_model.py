"""
Custom BERT model for ingredient predictions.
"""

import json
from pathlib import Path

import torch
import numpy as np

def load_vocab(vocab_path):
    """Load vocabulary from file."""
    vocab = {}
    with open(vocab_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            token = line.strip()
            vocab[token] = i
    return vocab

class SimpleTokenizer:
    """Basic tokenizer implementation."""
    def __init__(self, vocab_path):
        self.vocab = load_vocab(vocab_path)
        self.ids_to_tokens = {v: k for k, v in self.vocab.items()}
        
    def tokenize(self, text):
        """Simple tokenization by splitting on whitespace."""
        return text.split()
        
    def convert_tokens_to_ids(self, tokens):
        """Convert tokens to vocabulary IDs."""
        return [self.vocab.get(token, self.vocab['[UNK]']) for token in tokens]
        
    def encode(self, text, max_length=512, pad_to_max_length=True):
        """Encode text to model inputs."""
        tokens = ['[CLS]'] + self.tokenize(text) + ['[SEP]']
        if len(tokens) > max_length:
            tokens = tokens[:max_length-1] + ['[SEP]']
            
        input_ids = self.convert_tokens_to_ids(tokens)
        attention_mask = [1] * len(input_ids)
        
        if pad_to_max_length:
            padding_length = max_length - len(input_ids)
            input_ids = input_ids + [0] * padding_length
            attention_mask = attention_mask + [0] * padding_length
            
        return {
            'input_ids': torch.tensor([input_ids], dtype=torch.long),
            'attention_mask': torch.tensor([attention_mask], dtype=torch.long)
        }

class BertEmbeddings(torch.nn.Module):
    """Custom BERT embeddings module."""
    def __init__(self, config):
        super().__init__()
        self.word_embeddings = torch.nn.Embedding(config['vocab_size'], config['hidden_size'])
        self.position_embeddings = torch.nn.Embedding(512, config['hidden_size'])
        self.LayerNorm = torch.nn.LayerNorm(config['hidden_size'], eps=1e-12)
        self.dropout = torch.nn.Dropout(config['hidden_dropout_prob'])

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

class PredictionModel:
    """Model for generating ingredient embeddings."""
    def __init__(self):
        print("Initializing PredictionModel...")
        
        # Setup paths
        model_path = Path('foodBERT/foodbert/data')
        config_path = model_path / "config.json"
        model_bin_path = model_path / "pytorch_model.bin"
        vocab_path = model_path / "bert-base-cased-vocab.txt"
        
        # Load tokenizer
        print(f"Loading tokenizer from {vocab_path}")
        self.tokenizer = SimpleTokenizer(str(vocab_path))
        print("Tokenizer loaded successfully")
        
        # Load config
        print("Loading config...")
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialize model
        print("Loading BERT model...")
        self.model = BertEmbeddings(self.config)
        state_dict = torch.load(str(model_bin_path), map_location='cpu')
        
        # Convert state dict keys to match our model
        new_state_dict = {}
        for key, value in state_dict.items():
            if key.startswith('bert.embeddings.'):
                new_key = key.replace('bert.embeddings.', '')
                new_state_dict[new_key] = value
        
        try:
            self.model.load_state_dict(new_state_dict, strict=True)
            print("Successfully loaded model (strict mode)")
        except RuntimeError as e:
            print(f"Warning: Strict loading failed, attempting flexible loading: {str(e)}")
            self.model.load_state_dict(new_state_dict, strict=False)
            print("Successfully loaded model (flexible mode)")
        
        self.model.eval()
        print("Model set to evaluation mode")
        
        # Use GPU if available
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        self.model = self.model.to(self.device)
        print("Model moved to device successfully")

    def predict_embeddings(self, sentences):
        """Generate embeddings for ingredients in given sentences."""
        # Tokenize all sentences using encode
        input_ids_list = []
        for sentence in sentences:
            encoded = self.tokenizer.encode(sentence)
            input_ids_list.append(encoded['input_ids'][0])
        input_ids = torch.stack(input_ids_list).to(self.device)
        with torch.no_grad():
            embeddings = self.model(input_ids)
        return embeddings, input_ids

    def get_ingredient_embedding(self, ingredient):
        """Get embedding for a single ingredient."""
        # Tokenize ingredient
        tokens = self.tokenizer(ingredient, return_tensors='pt')
        tokens = {k: v.to(self.device) for k, v in tokens.items()}
        
        # Generate embedding
        with torch.no_grad():
            embeddings = self.model(tokens['input_ids'])
            embedding = embeddings.mean(dim=1)  # Average over token embeddings
            
        return embedding
