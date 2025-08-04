// page.tsx (Material UI MCP Modernized)
"use client";
import React, { useState } from "react";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import Divider from "@mui/material/Divider";
import Alert from "@mui/material/Alert";
import CircularProgress from "@mui/material/CircularProgress";
import IngredientCard from "./components/IngredientCard";
import SwapSuggestionCard from "./components/SwapSuggestionCard";

const DIET_OPTIONS = [
  { key: "vegan", label: "Vegan" },
  { key: "vegetarian", label: "Vegetarian" },
  { key: "glutenfree", label: "Gluten-Free" },
  { key: "dairyfree", label: "Dairy-Free" },
  { key: "lowcarb", label: "Low-Carb" },
  { key: "paleo", label: "Paleo" },
  { key: "keto", label: "Keto" },
];

// Improved cleaning function (no filtering, just normalization)
function cleanIngredient(ingredient: string) {
  let cleaned = ingredient.replace(/^▢\s*/, "");
  cleaned = cleaned.replace(/^\d+([\/\d\s\.]*)?\s*(oz\.|ounce[s]?|cup[s]?|lb\.|pound[s]?|tsp\.|tbsp\.|clove[s]?|large|small|medium|teaspoon[s]?|tablespoon[s]?|fresh|finely|diced|grated|minced|extra|plus|extra|in case of breakage)?\s*/i, "");
  cleaned = cleaned.replace(/[,].*$/, "");
  cleaned = cleaned.replace(/\s*see notes.*/i, "");
  cleaned = cleaned.trim();
  cleaned = cleaned.toLowerCase();
  cleaned = cleaned.replace(/\s+/g, " ");
  return cleaned;
}

export default function Home() {
  const [url, setUrl] = useState("");
  const [ingredients, setIngredients] = useState<string[]>([]);
  const [swapSuggestions, setSwapSuggestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedDiets, setSelectedDiets] = useState<string[]>([]);
  const [dietSummaries, setDietSummaries] = useState<any[]>([]);
  const [enrichedIngredients, setEnrichedIngredients] = useState<any[]>([]);
  const [nutritionLabelImage, setNutritionLabelImage] = useState<string | null>(null);

  React.useEffect(() => {
fetch("https://ingredient-replacer.onrender.com/diet_rules")
      .then((res) => res.json())
      .then((data) => setDietSummaries(data.diets || []))
      .catch(() => setDietSummaries([]));
  }, []);

  function handleDietToggle(diet: string) {
    setSelectedDiets((prev) =>
      prev.includes(diet)
        ? prev.filter((d) => d !== diet)
        : [...prev, diet]
    );
  }

  async function handleScrape(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setIngredients([]);
    setSwapSuggestions([]);
    try {
      const res = await fetch("/api/scrape", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await res.json();
      if (data.ingredients) {
        setIngredients(data.ingredients);
        const cleanedIngredients = data.ingredients.map(cleanIngredient);

        try {
const enrichRes = await fetch("https://ingredient-replacer.onrender.com/enrich_ingredients", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredients: cleanedIngredients }),
          });
          const enrichData = await enrichRes.json();
          setEnrichedIngredients(enrichData.ingredients || []);
        } catch {
          setEnrichedIngredients([]);
        }

const swapRes = await fetch("https://ingredient-replacer.onrender.com/suggestions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ingredients: cleanedIngredients, diets: selectedDiets }),
        });
        const swapData = await swapRes.json();
        setSwapSuggestions(swapData.suggestions || []);

        try {
const nutritionRes = await fetch("https://ingredient-replacer.onrender.com/nutrition-label", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredients: cleanedIngredients, servings: 4 }),
          });
          if (nutritionRes.ok) {
            const nutritionData = await nutritionRes.json();
            setNutritionLabelImage("data:image/png;base64," + nutritionData.nutrition_label_image);
          }
        } catch (nutritionError) {
          console.error("Failed to fetch nutrition label:", nutritionError);
        }
      } else {
        setError(data.error || "No ingredients found.");
      }
    } catch (err: any) {
      setError(err.message || "Error scraping ingredients.");
    }
    setLoading(false);
  }

  return (
    <Box
      sx={{
        minHeight: "100vh",
        bgcolor: "#fafafa",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        p: 4,
      }}
    >
      <Typography variant="h4" fontWeight={700} mb={3}>
        Recipe Ingredient Replacer
      </Typography>
      <Box
        component="form"
        onSubmit={handleScrape}
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 2,
          width: "100%",
          maxWidth: 400,
          mb: 2,
        }}
      >
        <TextField
          fullWidth
          label="Paste recipe URL here"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          variant="outlined"
          size="small"
        />
        <Stack direction="row" spacing={1} flexWrap="wrap" mt={1}>
          {DIET_OPTIONS.map((diet) => (
            <Chip
              key={diet.key}
              label={diet.label}
              color={selectedDiets.includes(diet.key) ? "success" : "default"}
              variant={selectedDiets.includes(diet.key) ? "filled" : "outlined"}
              onClick={() => handleDietToggle(diet.key)}
              sx={{ mb: 1 }}
            />
          ))}
        </Stack>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
          sx={{ fontWeight: 600, width: "100%" }}
        >
          {loading ? <CircularProgress size={22} color="inherit" /> : "Get Ingredient Swaps"}
        </Button>
      </Box>
      {error && (
        <Alert severity="error" sx={{ mb: 2, width: "100%", maxWidth: 400 }}>
          {error}
        </Alert>
      )}

      {/* Legend */}
      <Card sx={{ mt: 4, width: "100%", maxWidth: 400 }}>
        <CardContent>
          <Typography variant="subtitle1" fontWeight={600} mb={1}>
            Legend
          </Typography>
          <List dense>
            <ListItem>
              <Box
                sx={{
                  display: "inline-block",
                  width: 12,
                  height: 12,
                  bgcolor: "#fffde7",
                  borderLeft: "4px solid #ed6c02",
                  mr: 1,
                  verticalAlign: "middle",
                }}
              />
              <Typography variant="body2" component="span">
                Ingredient flagged for dietary restriction
              </Typography>
            </ListItem>
            <ListItem>
              <Box
                sx={{
                  display: "inline-block",
                  width: 12,
                  height: 12,
                  bgcolor: "transparent",
                  borderLeft: "4px solid #d32f2f",
                  mr: 1,
                  verticalAlign: "middle",
                }}
              />
              <Typography variant="body2" component="span">
                Bullet highlighted in red: Reason for flag (nutrition/category)
              </Typography>
            </ListItem>
            <ListItem>
              <Box
                sx={{
                  display: "inline-block",
                  width: 12,
                  height: 12,
                  bgcolor: "#e0e0e0",
                  border: "1px solid #bdbdbd",
                  mr: 1,
                  verticalAlign: "middle",
                }}
              />
              <Typography variant="body2" component="span">
                No highlight: Ingredient is compliant
              </Typography>
            </ListItem>
          </List>
          <Typography variant="caption" color="text.secondary" mt={1} display="block">
            <b>Accessibility:</b> Icons and border styles are used in addition to color for users with color vision deficiency.
          </Typography>
        </CardContent>
      </Card>

      {/* Diet summaries */}
      {selectedDiets.length > 0 && (
        <Box sx={{ mt: 4, width: "100%", maxWidth: 400 }}>
          <Typography variant="h6" fontWeight={600} mb={1}>
            Selected Diet Summaries:
          </Typography>
          {dietSummaries
            .filter((diet) => selectedDiets.includes(diet.id))
            .map((diet) => (
              <Card key={diet.id} sx={{ mb: 2, bgcolor: "#f5f5f5" }}>
                <CardContent>
                  <Typography fontWeight={700}>{diet.name}</Typography>
                  <Typography variant="body2" mb={1}>
                    {diet.description}
                  </Typography>
                  <Typography variant="subtitle2" fontWeight={600}>
                    Category Restrictions:
                  </Typography>
                  <List dense>
                    {diet.category_restrictions.map((r: any, i: number) => (
                      <ListItem key={i} title={r.full} sx={{ pl: 2, fontSize: "1rem" }} disableGutters>
                        {r.text}
                        {r.text !== r.full && (
                          <Typography component="span" variant="caption" sx={{ ml: 1, color: "text.secondary" }}>
                            (…)
                          </Typography>
                        )}
                      </ListItem>
                    ))}
                  </List>
                  <Typography variant="subtitle2" fontWeight={600}>
                    Macronutrient Restrictions:
                  </Typography>
                  <List dense>
                    {diet.macronutrient_restrictions.map((r: any, i: number) => (
                      <ListItem key={i} title={r.full} sx={{ pl: 2, fontSize: "1rem" }} disableGutters>
                        {r.text}
                        {r.text !== r.full && (
                          <Typography component="span" variant="caption" sx={{ ml: 1, color: "text.secondary" }}>
                            (…)
                          </Typography>
                        )}
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            ))}
        </Box>
      )}

      {/* Nutrition Label */}
      {nutritionLabelImage && (
        <Box sx={{ my: 4 }}>
          <img src={nutritionLabelImage} alt="Nutrition Label" style={{ maxWidth: "400px", border: "1px solid #333" }} />
        </Box>
      )}

      {/* Enriched ingredient list with highlights */}
      {enrichedIngredients.length > 0 && (
        <Box sx={{ mt: 4, width: "100%", maxWidth: 400 }}>
          <Typography variant="h6" fontWeight={600} mb={1}>
            Ingredients & Nutrition:
          </Typography>
          {enrichedIngredients.map((ing: any, i: number) => (
            <IngredientCard
              key={i}
              ingredient={ing.ingredient}
              bulletPoints={ing.bullet_points}
              isFlagged={!!(ing.swap_rationales && ing.swap_rationales.length > 0)}
              dietaryChangeDescription={ing.dietary_change_description}
              swapRationales={ing.swap_rationales}
            />
          ))}
        </Box>
      )}

      {/* Swap Suggestions */}
      {swapSuggestions.length > 0 && (
        <Box sx={{ mt: 4, width: "100%", maxWidth: 400 }}>
          <Typography variant="h6" fontWeight={600} mb={1}>
            Swap Suggestions:
          </Typography>
          {swapSuggestions.map((swap, i) => (
            <SwapSuggestionCard
              key={i}
              original={swap.original}
              rankedSwaps={
                swap.swap_suggestion && swap.swap_suggestion.ranked_swaps
                  ? swap.swap_suggestion.ranked_swaps
                  : []
              }
            />
          ))}
        </Box>
      )}
    </Box>
  );
}
