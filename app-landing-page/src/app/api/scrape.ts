import { NextRequest, NextResponse } from "next/server";
import * as cheerio from "cheerio";

export async function POST(req: NextRequest) {
  try {
    // DEBUG: Hardcoded ingredient list for outbound fetch test
    const cleanedIngredients = [
      "ricotta cheese",
      "egg",
      "mozzarella cheese",
      "parmesan cheese",
      "italian seasoning",
      "salt",
      "pepper",
      "olive oil",
      "yellow onion",
      "ground beef",
      "ground italian sausage",
      "garlic",
      "chicken broth",
      "marinara sauce",
      "tomato paste",
      "hot sauce",
      "worcestershire sauce",
      "lasagna noodles",
      "debug-test-ingredient"
    ];
    console.log("Cleaned ingredients for enrichment (hardcoded):", cleanedIngredients);

    // TEST: Fetch public API to verify outbound connectivity
    try {
      const testRes = await fetch("https://jsonplaceholder.typicode.com/todos/1");
      const testJson = await testRes.json();
      console.log("Public API fetch result:", testJson);
    } catch (testErr) {
      console.error("Public API fetch error:", testErr);
    }

    // POST cleaned ingredients to backend extraction API for normalization
    const backendUrl = "https://ingredient-replacer.onrender.com";
    console.log("Calling enrich at:", backendUrl + "/enrich");
    let enrichRes;
    try {
      enrichRes = await fetch(backendUrl + "/enrich", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients: cleanedIngredients }),
        // Add timeout for debugging network issues
        signal: AbortSignal.timeout ? AbortSignal.timeout(10000) : undefined
      });
      console.log("enrich fetch completed");
    } catch (fetchErr) {
      console.error("Error calling enrich_ingredients:", fetchErr);
      return NextResponse.json({ error: "Network error calling enrich_ingredients", details: String(fetchErr) }, { status: 500 });
    }

    if (!enrichRes.ok) {
      const errText = await enrichRes.text();
      console.error("enrich_ingredients failed:", errText);
      return NextResponse.json({
        error: "Failed to enrich ingredients: " + errText,
        ingredients: cleanedIngredients,
        enrichedIngredients: []
      }, { status: 500 });
    }

    const enriched = await enrichRes.json();
    console.log("Enrich response:", enriched);

    // Return both raw and enriched ingredients to frontend
    return NextResponse.json({
      ingredients: cleanedIngredients,
      enrichedIngredients: enriched.ingredients || []
    });
  } catch (err: any) {
    console.error("Top-level scrape API error:", err);
    return NextResponse.json({ error: err.message || "Scraping error", details: String(err) }, { status: 500 });
  }
}
