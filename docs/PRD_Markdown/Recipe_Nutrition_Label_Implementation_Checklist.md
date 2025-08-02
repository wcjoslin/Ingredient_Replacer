# Recipe Nutrition Label Implementation Checklist

## Branch & Setup
- [ ] Create feature branch (e.g., `feature/recipe-nutrition-label`)
- [ ] Ensure access to `data enrichment/enriched_ingredient_data_nutritionix.json`
- [ ] Obtain nutrition label template image (provided by user)

## Core Logic
- [ ] Parse uploaded recipe for ingredient list and servings
- [ ] Retrieve nutrition data for each ingredient
- [ ] Sum nutrition facts for whole recipe, adjusting for servings

## Image Generation (FDA-style)
- [ ] Generate FDA-style nutrition label image using Pillow (stylized, right-aligned numbers)

## Backend Integration
- [ ] Add backend API endpoint (e.g., `/nutrition-label`) to trigger nutrition label generation
- [ ] Modify endpoint to return nutrition label image (base64 string or image URL) in API response

## Frontend Integration
- [ ] Update frontend to call `/nutrition-label` endpoint after recipe upload
- [ ] Display returned nutrition label image above parsed ingredients list

## Testing
- [ ] Unit tests for nutrition summing logic
- [ ] Integration tests for image generation and overlay
- [ ] API endpoint tests for nutrition label generation
- [ ] Manual testing with sample recipes and ingredient data

## Documentation & PR
- [ ] Update README with usage instructions
- [ ] Document new scripts/modules/endpoints
- [ ] Open PR to `main` after testing and documentation
- [ ] Ensure review and successful checks before merging
