import { NextRequest, NextResponse } from "next/server";
import * as cheerio from "cheerio";

export async function POST(req: NextRequest) {
  try {
    const { url } = await req.json();
    if (!url || typeof url !== "string") {
      return NextResponse.json({ error: "Missing or invalid URL" }, { status: 400 });
    }

    // Fetch the HTML content of the recipe page
    const res = await fetch(url, { method: "GET" });
    if (!res.ok) {
      return NextResponse.json({ error: "Failed to fetch recipe site" }, { status: 400 });
    }
    const html = await res.text();

    // Use cheerio to parse and extract ingredient names
    const $ = cheerio.load(html);
    let ingredients: string[] = [];

    // Try common selectors for ingredient lists
    // 1. All <li> elements containing "ingredient" in parent class/id
    $("li").each((_, el) => {
      const parent = $(el).parent();
      const parentClass = parent.attr("class") || "";
      const parentId = parent.attr("id") || "";
      if (
        /ingredient/i.test(parentClass) ||
        /ingredient/i.test(parentId) ||
        /ingredient/i.test($(el).attr("class") || "") ||
        /ingredient/i.test($(el).attr("id") || "")
      ) {
        const text = $(el).text().trim();
        if (text.length > 0) ingredients.push(text);
      }
    });

    // 2. Fallback: any <span> or <div> with "ingredient" in class/id
    if (ingredients.length === 0) {
      $("[class*=ingredient], [id*=ingredient]").each((_, el) => {
        const text = $(el).text().trim();
        if (text.length > 0) ingredients.push(text);
      });
    }

    // Remove duplicates and filter out non-ingredient lines
    ingredients = Array.from(new Set(ingredients)).filter(
      (line) => line.length > 0 && line.split(" ").length <= 20
    );

    // Clean ingredient names before enrichment (less aggressive)
    const cleanedIngredients = ingredients.map(line =>
      line.replace(/^▢\s*/, "")
          .replace(/^\s*\d+([\/\d\s\.]*)?\s*/i, "")
          .replace(/[,].*$/, "")
          .replace(/\s*see notes.*/i, "")
          .trim()
          .toLowerCase()
          .replace(/\s+/g, " ")
    );
    console.log("Cleaned ingredients for enrichment:", cleanedIngredients);

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
        ingredients,
        enrichedIngredients: []
      }, { status: 500 });
    }

    const enriched = await enrichRes.json();
    console.log("Enrich response:", enriched);

    // Return both raw and enriched ingredients to frontend
    return NextResponse.json({
      ingredients,
      enrichedIngredients: enriched.ingredients || []
    });
  } catch (err: any) {
    console.error("Top-level scrape API error:", err);
    return NextResponse.json({ error: err.message || "Scraping error", details: String(err) }, { status: 500 });
  }
}
