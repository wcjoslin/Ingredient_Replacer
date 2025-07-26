"use client";

import React, { useState } from "react";
import {
  Container,
  Typography,
  TextField,
  Button,
  Box,
  CircularProgress,
  Chip,
  Avatar,
  Alert,
  Tooltip,
  IconButton,
} from "@mui/material";
import Grid from "@mui/material/Grid";
import RestaurantMenuIcon from "@mui/icons-material/RestaurantMenu";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";

export default function LandingPage() {
  const [recipe, setRecipe] = useState("");
  const [selectedDiets, setSelectedDiets] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [swapSuggestions, setSwapSuggestions] = useState<any[]>([]);
  const [swapError, setSwapError] = useState<string | null>(null);
  const [unmatchedIngredients, setUnmatchedIngredients] = useState<string[]>([]);

  // Example diet presets (replace with dietary_restriction_presets.json data)
  const dietPresets = [
    { key: "vegan", name: "Vegan", desc: "No animal products" },
    { key: "vegetarian", name: "Vegetarian", desc: "No meat" },
    { key: "glutenfree", name: "Gluten-Free", desc: "No gluten" },
    { key: "dairyfree", name: "Dairy-Free", desc: "No dairy" },
    { key: "lowcarb", name: "Low Carb", desc: "Reduced carbs" },
    { key: "keto", name: "Keto", desc: "High fat, low carb" },
    { key: "paleo", name: "Paleo", desc: "Whole foods only" },
    { key: "halal", name: "Halal", desc: "Meets halal rules" },
    { key: "kosher", name: "Kosher", desc: "Meets kosher rules" },
    { key: "nutfree", name: "Nut-Free", desc: "No nuts" },
  ];

  // Cache swap suggestions after first fetch
  const [allSuggestions, setAllSuggestions] = useState<any[]>([]);

  const handleDietToggle = (key: string) => {
    setSelectedDiets((prev) =>
      prev.includes(key) ? prev.filter((d) => d !== key) : [...prev, key]
    );
  };

  // Simple ingredient extraction (replace with NLP for production)
  function extractIngredients(recipeText: string): string[] {
    // Split by lines, remove empty, trim, remove quantities (very basic)
    return recipeText
      .split("\n")
      .map((line) => line.replace(/^[\d\/\.\-\s]+/, "").trim())
      .filter((line) => line.length > 0);
  }

  async function fetchAllSuggestions(diets: string[]) {
    // Replace with your FastAPI server URL if not localhost
    let url = "http://localhost:8000/suggestions";
    if (diets.length > 0) {
      url += "?" + diets.map(d => `diets=${encodeURIComponent(d)}`).join("&");
    }
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to fetch swap suggestions");
    return await res.json();
  }

  function getBestSwap(swapSuggestion: any) {
    // Try to get the best ranked swap from swap_suggestion.ranked_swaps
    if (
      swapSuggestion &&
      swapSuggestion.swap_suggestion &&
      Array.isArray(swapSuggestion.swap_suggestion.ranked_swaps) &&
      swapSuggestion.swap_suggestion.ranked_swaps.length > 0
    ) {
      return swapSuggestion.swap_suggestion.ranked_swaps[0].substitute;
    }
    return null;
  }

  function findSwapsForIngredients(ingredients: string[], suggestions: any[]) {
    // Match ingredients case-insensitively
    const swaps = [];
    const unmatched = [];
    for (const ing of ingredients) {
      const match = suggestions.find(
        (entry) => entry.ingredient.toLowerCase().trim() === ing.toLowerCase().trim()
      );
      if (match) {
        swaps.push(match);
      } else {
        unmatched.push(ing);
      }
    }
    return { swaps, unmatched };
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSwapError(null);
    setSwapSuggestions([]);
    setUnmatchedIngredients([]);
    try {
      let suggestions = allSuggestions;
      // Always refetch if diets change, so don't cache across diet changes
      suggestions = await fetchAllSuggestions(selectedDiets);
      setAllSuggestions(suggestions);
      const ingredients = extractIngredients(recipe);
      const { swaps, unmatched } = findSwapsForIngredients(ingredients, suggestions);
      setSwapSuggestions(swaps);
      setUnmatchedIngredients(unmatched);
      if (swaps.length === 0 && unmatched.length > 0) {
        setSwapError("No swap suggestions found for your recipe ingredients.");
      }
    } catch (err: any) {
      setSwapError(err.message || "Error fetching swap suggestions.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ py: 6 }}>
      <Box textAlign="center" mb={4}>
        <RestaurantMenuIcon color="primary" sx={{ fontSize: 48 }} />
        <Typography variant="h4" component="h1" gutterBottom>
          Ingredient Replacer
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Upload your recipe and select dietary restrictions
        </Typography>
      </Box>
      <Box component="form" onSubmit={handleSubmit} mb={4}>
        <TextField
          label="Paste your recipe or link"
          variant="outlined"
          fullWidth
          value={recipe}
          onChange={(e) => setRecipe(e.target.value)}
          required
          margin="normal"
          InputProps={{
            sx: {
              bgcolor: "#fff",
              color: "text.primary",
              borderRadius: 2,
            },
          }}
        />
        <Box mt={3} mb={2}>
          <Typography variant="subtitle2" gutterBottom>
            Select dietary restrictions:
          </Typography>
          <Grid
            container
            direction="column"
            spacing={2}
            justifyContent="center"
            alignItems="center"
          >
            {[0, 1, 2, 3, 4].map((rowIdx) => (
              <Grid container key={rowIdx} spacing={2} justifyContent="center">
                {[0, 1].map((colIdx) => {
                  const dietIdx = rowIdx * 2 + colIdx;
                  const diet = dietPresets[dietIdx];
                  if (!diet) return null;
                  return (
                    <Grid
                      key={diet.key}
                      sx={{
                        display: "flex",
                        justifyContent: "center",
                      }}
                    >
                      <Chip
                        avatar={
                          <Avatar
                            sx={{
                              width: 56,
                              height: 56,
                              fontSize: 28,
                              bgcolor: selectedDiets.includes(diet.key)
                                ? "primary.dark"
                                : "#e0e0e0",
                              color: selectedDiets.includes(diet.key)
                                ? "common.white"
                                : "text.primary",
                            }}
                          >
                            {diet.name[0]}
                          </Avatar>
                        }
                        label={
                          <Box
                            sx={{
                              display: "flex",
                              flexDirection: "column",
                              alignItems: "center",
                              justifyContent: "center",
                              width: "100%",
                              textAlign: "center",
                              px: 1,
                            }}
                          >
                            <Typography
                              variant="body1"
                              sx={{ fontWeight: 500, textAlign: "center" }}
                            >
                              {diet.name}
                            </Typography>
                            <Typography
                              variant="caption"
                              color="text.secondary"
                              sx={{ textAlign: "center" }}
                            >
                              {diet.desc}
                            </Typography>
                          </Box>
                        }
                        color={selectedDiets.includes(diet.key) ? "primary" : "default"}
                        variant={selectedDiets.includes(diet.key) ? "filled" : "outlined"}
                        onClick={() => handleDietToggle(diet.key)}
                        sx={{
                          width: 180,
                          height: 120,
                          minHeight: 120,
                          py: 2,
                          px: 2,
                          fontSize: 18,
                          bgcolor: selectedDiets.includes(diet.key)
                            ? "primary.main"
                            : "#f5f5f5",
                          color: selectedDiets.includes(diet.key)
                            ? "common.white"
                            : "text.primary",
                          border: selectedDiets.includes(diet.key)
                            ? "none"
                            : "1px solid #ccc",
                          alignItems: "center",
                          justifyContent: "center",
                          textAlign: "center",
                        }}
                      />
                    </Grid>
                  );
                })}
              </Grid>
            ))}
          </Grid>
        </Box>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          disabled={loading}
          sx={{ mt: 3 }}
        >
          {loading ? <CircularProgress size={24} /> : "Submit"}
        </Button>
      </Box>
      {loading && (
        <Box textAlign="center" mt={4}>
          <CircularProgress />
          <Typography variant="body2" mt={2}>
            Analyzing your recipe...
          </Typography>
        </Box>
      )}
      {swapError && (
        <Box mt={2}>
          <Alert severity="warning">{swapError}</Alert>
        </Box>
      )}
      {swapSuggestions.length > 0 && (
        <Box mt={4}>
          <Typography variant="h6" gutterBottom>
            Swap Suggestions:
          </Typography>
          {swapSuggestions.map((swap, idx) => {
            const bestSwap = getBestSwap(swap);
            return (
              <Box key={idx} mb={2} sx={{ bgcolor: "#f5f5f5", p: 2, borderRadius: 2 }}>
                <Box display="flex" alignItems="center">
                  <Typography variant="subtitle1" sx={{ mr: 1 }}>
                    <strong>{swap.ingredient}</strong> &rarr;{" "}
                    <strong>{bestSwap ? bestSwap : <span style={{ color: "#aaa" }}>No swap found</span>}</strong>
                  </Typography>
                  {swap.rationale && swap.rationale.length > 0 && (
                    <Tooltip title={swap.rationale.join(" ")} arrow>
                      <IconButton size="small" sx={{ ml: 1 }}>
                        <InfoOutlinedIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  )}
                </Box>
              </Box>
            );
          })}
        </Box>
      )}
      {unmatchedIngredients.length > 0 && (
        <Box mt={4}>
          <Typography variant="h6" gutterBottom color="warning.main">
            Unmatched Ingredients:
          </Typography>
          {unmatchedIngredients.map((ing, idx) => (
            <Box key={idx} mb={1} sx={{ bgcolor: "#fffbe6", p: 1.5, borderRadius: 2 }}>
              <Typography variant="body1" color="warning.main">
                {ing}
              </Typography>
            </Box>
          ))}
          <Typography variant="body2" color="text.secondary" mt={2}>
            No swap suggestions found for these ingredients. You may try editing them or provide feedback.
          </Typography>
        </Box>
      )}
    </Container>
  );
}
