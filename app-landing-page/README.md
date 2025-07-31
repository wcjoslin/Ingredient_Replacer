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
It allows users to upload recipes and view ingredient suggestions.

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

## Testing

- Run frontend tests:
   ```bash
   npm test
   ```
- Minimal tests are included as a baseline. Add real tests for your components as needed.

---

## Environment Variables

- Configure API endpoint in `.env.local`:
  ```
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

---

## Main Components

- `src/app/page.tsx` – Main upload page
- `src/app/api/` – API route handlers (if any)
- `src/app/components/` – UI components

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
