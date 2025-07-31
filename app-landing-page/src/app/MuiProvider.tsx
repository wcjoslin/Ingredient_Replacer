// MuiProvider.tsx
"use client";
import * as React from "react";
import { ThemeProvider, CssBaseline } from "@mui/material";
import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",
    background: {
      default: "#fdf6f3", // oklch(98% 0.016 73.684)
      paper: "#f5ede6",   // oklch(95% 0.038 75.164)
    },
    primary: {
      main: "#000000", // oklch(0% 0 0)
      contrastText: "#ffffff", // oklch(100% 0 0)
    },
    secondary: {
      main: "#3a2b23", // oklch(22.45% 0.075 37.85)
      contrastText: "#e5d9c6", // oklch(90% 0.076 70.697)
    },
    info: {
      main: "#5a5fd6", // oklch(42% 0.199 265.638)
      contrastText: "#e5d9c6",
    },
    success: {
      main: "#4bbf6b", // oklch(43% 0.095 166.913)
      contrastText: "#e5d9c6",
    },
    warning: {
      main: "#ffe59e", // oklch(82% 0.189 84.429)
      contrastText: "#6b4d2d", // oklch(41% 0.112 45.904)
    },
    error: {
      main: "#e07a5f", // oklch(70% 0.191 22.216)
      contrastText: "#6b3a2d", // oklch(39% 0.141 25.723)
    },
  },
  shape: {
    borderRadius: 16, // approx 1rem
  },
});

export default function MuiProvider({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}
