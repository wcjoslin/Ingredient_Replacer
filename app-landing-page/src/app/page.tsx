"use client";
import React, { useState } from "react";

// Remove hardcoded ingredient list. We'll fetch the model's ingredient list from the backend.

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
  // Remove leading bullet and whitespace
  let cleaned = ingredient.replace(/^▢\s*/, "");
  // Remove quantity and units (e.g., "15 oz.", "2 cups", "¾ lb.", etc.)
  cleaned = cleaned.replace(/^\d+([\/\d\s\.]*)?\s*(oz\.|ounce[s]?|cup[s]?|lb\.|pound[s]?|tsp\.|tbsp\.|clove[s]?|large|small|medium|teaspoon[s]?|tablespoon[s]?|fresh|finely|diced|grated|minced|extra|plus|extra|in case of breakage)?\s*/i, "");
  // Remove everything after a comma
  cleaned = cleaned.replace(/[,].*$/, "");
  // Remove everything after "see notes" or similar
  cleaned = cleaned.replace(/\s*see notes.*/i, "");
  // Remove trailing whitespace
  cleaned = cleaned.trim();
  // Lowercase for matching
  cleaned = cleaned.toLowerCase();
  // Remove duplicate spaces
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

  function handleDietToggle(diet: string) {
    setSelectedDiets((prev) =>
      prev.includes(diet)
        ? prev.filter((d) => d !== diet)
        : [...prev, diet]
    );
  }

  // Step 1: Scrape ingredients from recipe URL
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
        // Step 2: Clean ingredients (no filtering)
        const cleanedIngredients = data.ingredients.map(cleanIngredient);
        // Step 3: Send ingredients and diets to backend for swap suggestions
        const swapRes = await fetch("http://127.0.0.1:8000/suggestions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ingredients: cleanedIngredients, diets: selectedDiets }),
        });
        const swapData = await swapRes.json();
        setSwapSuggestions(swapData.suggestions || []);
      } else {
        setError(data.error || "No ingredients found.");
      }
    } catch (err: any) {
      setError(err.message || "Error scraping ingredients.");
    }
    setLoading(false);
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-4">Recipe Ingredient Replacer</h1>
      <form onSubmit={handleScrape} className="flex flex-col items-center gap-2 w-full max-w-md">
        <input
          type="text"
          placeholder="Paste recipe URL here"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="border rounded px-2 py-1 w-full"
        />
        <div className="flex flex-wrap gap-2 mt-2">
          {DIET_OPTIONS.map((diet) => (
            <button
              key={diet.key}
              type="button"
              className={`px-3 py-1 rounded border ${
                selectedDiets.includes(diet.key)
                  ? "bg-green-600 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
              onClick={() => handleDietToggle(diet.key)}
            >
              {diet.label}
            </button>
          ))}
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? "Processing..." : "Get Ingredient Swaps"}
        </button>
      </form>
      {error && <div className="text-red-600 mt-2">{error}</div>}
      {ingredients.length > 0 && (
        <div className="mt-6 w-full max-w-md">
          <h2 className="text-lg font-semibold mb-2">Extracted Ingredients:</h2>
          <ul className="list-disc pl-6">
            {ingredients.map((ing, i) => (
              <li key={i}>{ing}</li>
            ))}
          </ul>
        </div>
      )}
      {swapSuggestions.length > 0 && (
        <div className="mt-6 w-full max-w-md">
          <h2 className="text-lg font-semibold mb-2">Swap Suggestions:</h2>
          <ul className="list-disc pl-6">
            {swapSuggestions.map((swap, i) => (
              <li key={i}>
                <strong>{swap.original}:</strong> {swap.swap_suggestion && swap.swap_suggestion.ranked_swaps
                  ? swap.swap_suggestion.ranked_swaps.map((s: any, idx: number) => (
                      <span key={idx}>
                        {s.substitute} (score: {s.score.toFixed(2)})
                        {idx < swap.swap_suggestion.ranked_swaps.length - 1 ? ", " : ""}
                      </span>
                    ))
                  : "No swap found"}
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}
