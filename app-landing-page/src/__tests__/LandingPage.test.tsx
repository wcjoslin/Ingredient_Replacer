import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import LandingPage from "../app/page";

describe("LandingPage UI Mock", () => {
  it("renders the header and recipe input", () => {
    render(<LandingPage />);
    expect(screen.getByText(/Ingredient Replacer/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Paste your recipe or link/i)).toBeInTheDocument();
  });

  it("renders all 10 diet selection buttons", () => {
    render(<LandingPage />);
    const chips = screen.getAllByRole("button", { name: /Vegan|Vegetarian|Gluten-Free|Dairy-Free|Low Carb|Keto|Paleo|Halal|Kosher|Nut-Free/i });
    expect(chips.length).toBe(10);
  });

  it("allows selecting and deselecting diet chips", () => {
    render(<LandingPage />);
    const veganChip = screen.getByRole("button", { name: /Vegan/i });
    fireEvent.click(veganChip);
    expect(veganChip).toHaveClass("MuiChip-filledPrimary");
    fireEvent.click(veganChip);
    expect(veganChip).not.toHaveClass("MuiChip-filledPrimary");
  });

  it("shows loading bar after submitting", () => {
    render(<LandingPage />);
    fireEvent.change(screen.getByLabelText(/Paste your recipe or link/i), { target: { value: "Test Recipe" } });
    fireEvent.click(screen.getByRole("button", { name: /Submit/i }));
    expect(screen.getByText(/Analyzing your recipe/i)).toBeInTheDocument();
  });
});
