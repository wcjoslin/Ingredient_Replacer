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

    // POST scraped ingredients to backend extraction API for normalization
    const enrichRes = await fetch(process.env.BACKEND_URL + "/enrich_ingredients", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredients }),
    });

    if (!enrichRes.ok) {
      return NextResponse.json({ error: "Failed to enrich ingredients" }, { status: 500 });
    }

    const enriched = await enrichRes.json();

    // Return normalized/enriched ingredients to frontend
    return NextResponse.json(enriched);
  } catch (err: any) {
    return NextResponse.json({ error: err.message || "Scraping error" }, { status: 500 });
  }
}
