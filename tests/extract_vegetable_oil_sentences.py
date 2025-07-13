def extract_sentences_with_ingredient(txt_path, ingredient, output_path, max_count=50):
    count = 0
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            if ingredient in line.lower():
                with open(output_path, "a", encoding="utf-8") as out_f:
                    out_f.write(line.strip() + "\n")
                count += 1
                if count >= max_count:
                    print(f"Extracted {max_count} sentences containing '{ingredient}'.")
                    return
    print(f"Extracted {count} sentences containing '{ingredient}'.")

if __name__ == "__main__":
    extract_sentences_with_ingredient(
        "foodBERT/foodbert/data/train_instructions.txt",
        "vegetable oil",
        "suggestic_ingredient_sentences_vegetable_oil.txt",
        max_count=50
    )
