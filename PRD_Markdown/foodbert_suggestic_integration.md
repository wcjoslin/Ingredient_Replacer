# Integrating Suggestic Data with foodBERT

## Overview

This document outlines the process for using Suggestic food/ingredient data to extend the embedding space of the foodBERT model.

## Steps

1. **Analyze Suggestic Data Structure**
   - Identify relevant endpoints and data fields (e.g., ingredient names, categories, nutrition).

2. **Preprocess Suggestic Data**
   - Normalize ingredient names and formats to match foodBERT expectations.
   - Handle duplicates, synonyms, and missing values.

3. **Prepare Data for foodBERT**
   - Convert Suggestic ingredient data into a format compatible with foodBERT embedding scripts.
   - Save as JSON or CSV as needed.

4. **Extend foodBERT Embedding Space**
   - Use or adapt foodBERT scripts to incorporate new ingredient data.
   - Validate by generating embeddings for Suggestic ingredients.

5. **Testing and Validation**
   - Run test cases to ensure new ingredients are embedded and substitutions are logical.

## Requirements

- Access to Suggestic API and ingredient data.
- foodBERT environment set up and ready for embedding generation.

## Next Steps

- Implement scripts for data extraction and preprocessing.
- Document integration results and any issues encountered.
