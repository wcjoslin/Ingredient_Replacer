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
  const [dietSummaries, setDietSummaries] = useState<any[]>([]);
  const [enrichedIngredients, setEnrichedIngredients] = useState<any[]>([]);

  // --- Nutrition Label State ---
  const [nutritionLabelImage, setNutritionLabelImage] = useState<string | null>(null);

  // Fetch diet summaries on mount
  React.useEffect(() => {
    fetch("http://127.0.0.1:8000/diet_rules")
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

        // Fetch enriched ingredient data for highlighting
        try {
          const enrichRes = await fetch("http://127.0.0.1:8000/enrich_ingredients", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredients: cleanedIngredients }),
          });
          const enrichData = await enrichRes.json();
          setEnrichedIngredients(enrichData.ingredients || []);
        } catch {
          setEnrichedIngredients([]);
        }

        // Step 3: Send ingredients and diets to backend for swap suggestions
        const swapRes = await fetch("http://127.0.0.1:8000/suggestions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ingredients: cleanedIngredients, diets: selectedDiets }),
        });
        const swapData = await swapRes.json();
        setSwapSuggestions(swapData.suggestions || []);

        // --- Nutrition Label API Call Addition ---
        // Use cleanedIngredients and a default servings value (e.g., 4)
        try {
          const nutritionRes = await fetch("http://127.0.0.1:5001/nutrition-label", {
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
        // --- End Nutrition Label API Call Addition ---

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
      {/* Legend for highlight system */}
      <div className="mt-6 w-full max-w-md">
        <h2 className="text-md font-semibold mb-2">Legend</h2>
        <ul className="list-disc pl-6">
          <li>
            <span className="inline-block w-3 h-3 bg-yellow-100 border-l-4 border-yellow-500 align-middle mr-2"></span>
            <span className="align-middle">Ingredient flagged for dietary restriction</span>
          </li>
          <li>
            <span className="inline-block w-3 h-3 bg-transparent border-l-4 border-red-700 align-middle mr-2"></span>
            <span className="align-middle">Bullet highlighted in red: Reason for flag (nutrition/category)</span>
          </li>
          <li>
            <span className="inline-block w-3 h-3 bg-gray-200 border align-middle mr-2"></span>
            <span className="align-middle">No highlight: Ingredient is compliant</span>
          </li>
        </ul>
        <div className="text-xs text-gray-600 mt-1">
          <span className="font-semibold">Accessibility:</span> Icons and border styles are used in addition to color for users with color vision deficiency.
        </div>
      </div>
      {/* Diet summaries */}
      {selectedDiets.length > 0 && (
        <div className="mt-6 w-full max-w-md">
          <h2 className="text-lg font-semibold mb-2">Selected Diet Summaries:</h2>
          {dietSummaries
            .filter((diet) => selectedDiets.includes(diet.id))
            .map((diet) => (
              <div key={diet.id} className="mb-4 border rounded p-2 bg-gray-50">
                <div className="font-bold">{diet.name}</div>
                <div className="text-sm mb-1">{diet.description}</div>
                <div>
                  <span className="font-semibold">Category Restrictions:</span>
                  <ul className="list-disc pl-6">
                    {diet.category_restrictions.map((r: any, i: number) => (
                      <li key={i} title={r.full}>
                        {r.text}
                        {r.text !== r.full && (
                          <span className="ml-1 text-xs text-gray-500">(…)</span>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <span className="font-semibold">Macronutrient Restrictions:</span>
                  <ul className="list-disc pl-6">
                    {diet.macronutrient_restrictions.map((r: any, i: number) => (
                      <li key={i} title={r.full}>
                        {r.text}
                        {r.text !== r.full && (
                          <span className="ml-1 text-xs text-gray-500">(…)</span>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
        </div>
      )}
      {/* --- Nutrition Label Display Addition --- */}
      {nutritionLabelImage && (
        <div style={{ marginBottom: "2rem" }}>
          <img src={nutritionLabelImage} alt="Nutrition Label" style={{ maxWidth: "400px", border: "1px solid #333" }} />
        </div>
      )}
      {/* Enriched ingredient list with highlights */}
      {enrichedIngredients.length > 0 && (
        <div className="mt-6 w-full max-w-md">
          <h2 className="text-lg font-semibold mb-2">Ingredients & Nutrition:</h2>
          <ul className="list-disc pl-6">
            {enrichedIngredients.map((ing: any, i: number) => {
              const isFlagged = ing.swap_rationales && ing.swap_rationales.length > 0;
              return (
                <li
                  key={i}
                  className={isFlagged ? "bg-yellow-100 border-l-4 border-yellow-500 p-2 mb-2 rounded" : ""}
                  title={isFlagged ? ing.dietary_change_description : ""}
                >
                  <span className={isFlagged ? "font-bold text-black" : ""}>
                    {ing.ingredient}
                  </span>
                  <ul className="list-disc pl-6">
                    {ing.bullet_points.map((bp: string, j: number) => {
                      // Highlight bullet if it's a rationale
                      const isRationale = bp.startsWith("Flagged:");
                      // If flagged and not rationale, make text black for contrast
                      const bulletClass =
                        isRationale
                          ? "text-red-700 font-semibold"
                          : isFlagged
                          ? "text-black"
                          : "";
                      return (
                        <li
                          key={j}
                          className={bulletClass}
                          title={isRationale ? ing.swap_rationales.join("; ") : ""}
                        >
                          {bp}
                        </li>
                      );
                    })}
                  </ul>
                  {isFlagged && (
                    <div className="text-xs text-yellow-700 mt-1">
                      {ing.dietary_change_description}
                    </div>
                  )}
                </li>
              );
            })}
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
