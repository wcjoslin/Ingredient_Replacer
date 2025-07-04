# Ingredient Replacer PRD

## 1. Overview

**Objective:**  
Enhance recipe ingredient substitution by integrating foodBERT models with Suggestic's food/recipe data, enabling logical ingredient-level replacements.

## 2. Background

- Current platforms (e.g., Suggestic) offer recipe-level swaps based on dietary needs/preferences.
- foodBERT enables ingredient-level substitutions using food embeddings.
- Combining Suggestic's data with foodBERT can improve substitution logic.

## 3. Goals

1. **Set up foodBERT (multimodal and text) models**
   - Clone and install from [foodBERT repo](https://github.com/ChantalMP/Exploiting-Food-Embeddings-for-Ingredient-Substitution).
   - Follow [Colab install example](https://colab.research.google.com/drive/1tC7DRHUQx4qCrOAWhqdW1uuIwT1jyc1f?usp=sharing#scrollTo=Y60c1ZHJVtqu).
   - Train models on provided datasets.

2. **Set up Suggestic API**
   - Register and obtain API key.
   - Implement basic API calls (e.g., fetch recipes, ingredients).

3. **Integrate Suggestic data with foodBERT**
   - Use Suggestic's food/ingredient data to extend foodBERT's embedding space.
   - Validate improved substitution logic.

## 4. Steps & Deliverables

### Step 1: foodBERT Setup
- [ ] Clone foodBERT repo.
- [ ] Set up environment (dependencies, GPU support if needed).
- [ ] Run example notebooks to verify installation.
- [ ] Train both multimodal and text models.

### Step 2: Suggestic API Integration
- [ ] Register for Suggestic API access.
- [ ] Implement authentication and test API connectivity.
- [ ] Write scripts to fetch recipes and ingredient data.

### Step 3: Data Integration & Embedding Extension
- [ ] Analyze Suggestic data structure.
- [ ] Preprocess and format data for foodBERT.
- [ ] Extend foodBERT's embedding space with Suggestic data.
- [ ] Validate substitutions with test cases.

### Step 4: Documentation & Next Steps
- [ ] Document setup, integration, and usage instructions.
- [ ] Outline future improvements (e.g., UI, more data sources).

## 5. Useful Links

- [foodBERT GitHub](https://github.com/ChantalMP/Exploiting-Food-Embeddings-for-Ingredient-Substitution)
- [foodBERT Colab Example](https://colab.research.google.com/drive/1tC7DRHUQx4qCrOAWhqdW1uuIwT1jyc1f?usp=sharing#scrollTo=Y60c1ZHJVtqu)
- [Suggestic](https://suggestic.com/)
