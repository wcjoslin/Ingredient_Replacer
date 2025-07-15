import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from foodBERT.foodbert_embeddings.helpers.generate_ingredient_embeddings import generate_food_embedding_dict
import matplotlib.pyplot as plt
import numpy as np

def analyze_embedding_space(min_threshold=100):
    embedding_dict = generate_food_embedding_dict(max_sentence_count=100)
    counts = [v.shape[0] for v in embedding_dict.values()]
    plt.figure(figsize=(10,6))
    plt.hist(counts, bins=50, color='skyblue', edgecolor='black')
    plt.axvline(min_threshold, color='red', linestyle='dashed', linewidth=2, label=f'Threshold: {min_threshold}')
    plt.xlabel('Sentence Count per Ingredient')
    plt.ylabel('Number of Ingredients')
    plt.title('Distribution of Sentence Counts for FoodBERT Ingredient Embeddings')
    plt.legend()
    plt.tight_layout()
    plt.savefig('sentence_count_distribution.png')
    print("Histogram saved as sentence_count_distribution.png")
    print(f"Median sentence count: {int(np.median(counts))}")
    print(f"Mean sentence count: {int(np.mean(counts))}")

if __name__ == "__main__":
    analyze_embedding_space(min_threshold=100)
