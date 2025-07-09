# foodBERT Setup Instructions

## 1. Install Requirements

Already completed:
```sh
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

## 2. Download Pretrained Data and Models

Download the following files and extract/place them in the specified directories:

- [food2vec_models.zip](https://github.com/ChantalMP/Exploiting-Food-Embeddings-for-Ingredient-Substitution/releases/download/0.1/food2vec_models.zip) → `./food2vec/models`
- [foodbert_data.zip](https://github.com/ChantalMP/Exploiting-Food-Embeddings-for-Ingredient-Substitution/releases/download/0.1/foodbert_data.zip) → `./foodbert/data`
- [foodbert_embeddings_data.zip](https://github.com/ChantalMP/Exploiting-Food-Embeddings-for-Ingredient-Substitution/releases/download/0.1/foodbert_embeddings_data.zip) → `./foodbert_embeddings/data`
- [multimodal_data.zip](https://github.com/ChantalMP/Exploiting-Food-Embeddings-for-Ingredient-Substitution/releases/download/0.1/multimodal_data.zip) → `./multimodal/data`
- [relation_extraction_models.zip](https://github.com/ChantalMP/Exploiting-Food-Embeddings-for-Ingredient-Substitution/releases/download/0.1/relation_extraction_models.zip) → `./relation_extraction/models`

Unzip each file into the corresponding directory.

## 3. (Optional) Generate Data for FoodBERT and RE Training

- Download the [Recipe1M+ dataset](http://pic2recipe.csail.mit.edu) (login required).
- Unzip, rename `layer1.json` to `recipe1m.json` and place in `.data/`.
- Run:
  ```sh
  python -m normalisation.normalize_recipe_instructions
  python -m foodbert.preprocess_instructions
  ```

## 4. Next Steps

Once the data is in place, you can proceed with running or training the models as described in the main README.
