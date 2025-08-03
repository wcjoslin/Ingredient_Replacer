# Ingredient Replacer Frontend – Recipe Upload

---

**Migration Note:**  
This project has been migrated from Tailwind CSS to [Material UI MCP](https://mui.com/material-ui/getting-started/mcp/) for all UI components and layout.  
- All major UI code now uses Material UI components and theming.
- Tailwind and custom CSS have been removed.
- See `Material_UI_MCP_Migration_Checklist.md` for migration details and checklist.

---

## UI Development with Material UI MCP

This project uses [Material UI MCP](https://mui.com/material-ui/getting-started/mcp/) for all UI components and layout.

### Key Guidelines
- Use Material UI components for all new UI features.
- Wrap new UI in MUI's `Box`, `Stack`, `Card`, `Typography`, `Button`, etc.
- Use the `sx` prop for custom styling and spacing.
- Theme customization is handled in `src/app/MuiProvider.tsx`.
- Accessibility: Use MUI's built-in accessibility features and ARIA props.
- See `Material_UI_MCP_Migration_Checklist.md` for a step-by-step migration and development checklist.

### Useful References
- [Material UI Documentation](https://mui.com/material-ui/getting-started/overview/)
- [Material UI MCP Guide](https://mui.com/material-ui/getting-started/mcp/)
- [Theming](https://mui.com/material-ui/customization/theming/)
- [Component Demos](https://mui.com/material-ui/react-button/)

### Project Structure for UI
- `src/app/components/` – All reusable UI components (use MUI)
- `src/app/page.tsx` – Main page layout (uses MUI)
- `src/app/MuiProvider.tsx` – ThemeProvider and CssBaseline setup

---

## Overview

This is the Next.js/React frontend for the Ingredient Replacer project.  
It allows users to upload recipes and view ingredient suggestions, nutrition labels, and swap suggestions.

---

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
3. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## API Integration

- The frontend calls the backend FastAPI endpoints for ingredient enrichment and swap suggestions:
  - `/suggestions` for swap suggestions (uses precomputed foodBERT cache)
  - `/enrich_ingredients` for ingredient enrichment
- For nutrition label generation, the frontend calls the Flask API endpoint:
  - `/nutrition-label` for FDA-style nutrition label images

- Configure API endpoint in `.env.local`:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

---

## Features

- Upload a recipe URL and extract ingredients
- Highlight ingredients flagged for dietary restrictions
- Suggest ingredient swaps for selected diets (cache-based, instant)
- Display diet summaries and ingredient nutrition
- Generate and display FDA-style nutrition label for uploaded recipes

---

## Testing

- Run frontend tests:
   ```bash
   npm test
   ```
- Minimal tests are included as a baseline. Add real tests for your components as needed.

---

## Deployment Guide

### Local Development

1. Start backend APIs:
   - FastAPI (swap suggestions, enrichment):  
     ```
     uvicorn src.ingredient_suggestion_api:app --reload
     ```
   - Flask (nutrition label):  
     ```
     python src/nutrition_label_api.py
     ```

2. Start frontend:
   ```
   npm run dev
   ```

### Production Deployment

- **Frontend:**  
  Deploy to [Vercel](https://vercel.com/) or [Netlify](https://www.netlify.com/) for Next.js apps.
  - Set `NEXT_PUBLIC_API_URL` to your backend's public URL.

- **Backend:**  
  Deploy FastAPI and Flask APIs to [Render](https://render.com/), [Heroku](https://www.heroku.com/), or [AWS](https://aws.amazon.com/).
  - Ensure all required data files (swap cache, nutrition data) are included.
  - Set up CORS and environment variables as needed.

- **Cache Regeneration:**  
  If you update ingredients, regenerate the swap cache and redeploy the backend.

---

## API Reference

See [../API_DOCS.md](../API_DOCS.md) for backend API documentation.

---

## Contributing

- Do not commit `node_modules` or build output.
- Document new features and changes.

---

## License

MIT
