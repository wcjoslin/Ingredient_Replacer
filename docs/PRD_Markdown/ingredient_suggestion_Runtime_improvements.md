# Ingredient Suggestion Runtime Improvements PRD

## Objective
Reduce runtime and improve efficiency of the ingredient replacement workflow for dietary restriction-based recipe modification, with minimal codebase disruption.

## Key Steps & Recommendations

### 1. Early Filtering
- **Move all filtering (dietary restriction, category, spices, nutrition) before expensive calls (foodBERT, ML models).**
- Reuse: Enhance filtering logic in `ingredient_workflow.py` and `ingredient_swap_suggestions.py` to ensure only relevant ingredients are processed.

### 2. Caching
- **Cache nutrition profiles and embedding lookups in-memory during workflow execution.**
- Reuse: Add caching dictionaries to `ingredient_swap_suggestions.py` and `nutritional_analysis.py` to avoid redundant API calls and disk reads.

### 3. Parallel Processing
- **Process flagged ingredients in parallel using Python's multiprocessing or concurrent.futures.**
- Reuse: Refactor swap suggestion loop in `ingredient_swap_suggestions.py` to use `ProcessPoolExecutor` or similar.

### 4. Reduce I/O
- **Minimize file reads/writes inside loops; aggregate results and write once at the end.**
- Reuse: Ensure all data is loaded at the start and results are written after batch processing.

### 5. Profiling & Bottleneck Identification
- **Use profiling tools (cProfile, line_profiler) to identify and optimize slowest workflow steps.**
- Reuse: Profile `ingredient_workflow.py` and `ingredient_swap_suggestions.py` to focus optimization efforts.

### 6. Precompute & Vectorize
- **Precompute embeddings and nearest neighbors for common ingredients. Use numpy/pandas for filtering and scoring.**
- Reuse: Store precomputed data in existing embedding files; refactor filtering/scoring to use vectorized operations.

### 7. Ingredient Grouping
- **Group similar flagged ingredients and process together to reduce redundant work.**
- Reuse: Implement grouping logic in `ingredient_workflow.py` before swap suggestion step.

## Implementation Notes
- All changes should be made by modifying existing scripts (`ingredient_workflow.py`, `ingredient_swap_suggestions.py`, etc.) rather than creating new files.
- Document any new functions or major changes inline for maintainability.
- Test runtime improvements using representative recipes and dietary restrictions.

## Expected Outcomes
- Significant reduction in total workflow runtime.
- Improved scalability for large recipes and ingredient lists.
- Easier maintenance and extension of the workflow.
