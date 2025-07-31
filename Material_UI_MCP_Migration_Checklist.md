# Material UI MCP Migration Checklist

## 1. Project Preparation
- [x] Ensure `@mui/material` and `@mui/mcp` are installed in `app-landing-page`
- [x] Review current UI components and layouts

## 2. Component Mapping
- [x] Inventory all components in `app-landing-page/src/app/components/`
- [x] Map each custom/Tailwind component to the closest MUI component

## 3. Refactor Components
- [x] Refactor `IngredientCard.tsx` to use `Card`, `CardContent`, `Typography`, `List`, `ListItem`
- [x] Refactor `DietSummaryCard.tsx` to use `Card`, `CardContent`, `Typography`, `List`, `ListItem`
- [x] Refactor `SwapSuggestionCard.tsx` to use `Card`, `CardContent`, `Typography`, `List`, `ListItem`

## 4. Refactor Main Layout
- [x] Refactor `page.tsx` to use MUI layout components (`Box`, `Stack`, `Typography`, `TextField`, `Button`, `List`, `Card`)
- [x] Replace Tailwind classes with MUI props and `sx` styling

## 5. Theming and Provider Setup
- [x] Wrap app with `ThemeProvider` and `CssBaseline` in root layout
- [ ] Configure custom theme if needed

## 6. Accessibility and Icons
- [x] Use MUI accessibility features and icons where appropriate

## 7. Testing and Validation
- [x] Test all UI flows for correct appearance and behavior
- [x] Validate accessibility and responsiveness
- [x] Remove unused Tailwind/custom CSS

## 8. Documentation
- [ ] Document all changes and new component usage
- [ ] Provide migration notes for future development
