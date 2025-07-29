# Ingredient Replacer Frontend – Recipe Upload

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
