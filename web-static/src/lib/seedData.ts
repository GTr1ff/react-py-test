import { useMockDb } from "@/stores/mockDbStore";

export const seedPantryPalData = () => {
  const db = useMockDb.getState();

  // Seed ingredients
  const existingIngredients = db.getAll("ingredient");
  const isRandomOrEmpty = existingIngredients.length === 0 || (existingIngredients[0] && typeof existingIngredients[0].name === "string" && (existingIngredients[0].name as string).startsWith("text_"));

  if (isRandomOrEmpty) {
    // Clear existing random data
    db.tables["ingredient"] = [];
    db.tables["recipe"] = [];
    db.tables["recipe_ingredient"] = [];
    db.tables["inventory_item"] = [];
    db.tables["shopping_list_item"] = [];

    const ingredients = [
      { id: 1, name: "Chicken Breast", description: "Lean protein", category_id: 1, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 2, name: "Olive Oil", description: "Healthy cooking oil", category_id: 2, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 3, name: "Garlic", description: "Aromatic bulb", category_id: 3, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 4, name: "Onion", description: "Sweet and savory aromatic", category_id: 3, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 5, name: "Tomato", description: "Juicy red fruit/vegetable", category_id: 4, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 6, name: "Pasta", description: "Semolina wheat pasta", category_id: 5, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 7, name: "Rice", description: "Long grain white rice", category_id: 5, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 8, name: "Salt", description: "Essential mineral", category_id: 2, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 9, name: "Black Pepper", description: "Ground spice", category_id: 2, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 10, name: "Spinach", description: "Leafy green vegetable", category_id: 4, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 11, name: "Parmesan Cheese", description: "Hard, aged cheese", category_id: 6, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 12, name: "Lemon", description: "Citrus fruit", category_id: 4, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 13, name: "Butter", description: "Creamy dairy fat", category_id: 6, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 14, name: "Eggs", description: "Farm fresh eggs", category_id: 1, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 15, name: "Bacon", description: "Smoked pork belly", category_id: 1, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 16, name: "Avocado", description: "Creamy green fruit", category_id: 4, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 17, name: "Cheddar Cheese", description: "Sharp cheddar cheese", category_id: 6, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 18, name: "Salmon Fillet", description: "Rich omega-3 fish", category_id: 1, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 19, name: "Bell Pepper", description: "Sweet bell pepper", category_id: 4, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 20, name: "Soy Sauce", description: "Savory fermented sauce", category_id: 2, created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
    ];

    ingredients.forEach((ing) => {
      db.insert("ingredient", ing, "id");
    });

    // Seed recipes
    const recipes = [
      {
        id: 1,
        recipe_name: "Garlic Butter Chicken Pasta",
        description: "A quick and delicious pasta tossed with sautéed chicken, fresh spinach, and parmesan cheese in a rich garlic butter sauce.",
        instructions: "1. Cook pasta in salted boiling water according to package instructions.\n2. Season chicken breast pieces with salt and black pepper.\n3. Melt butter in a large skillet over medium-high heat. Add minced garlic and sauté for 1 minute.\n4. Add chicken and cook until golden brown and cooked through (about 6-8 minutes).\n5. Stir in fresh spinach and cook until wilted.\n6. Drain pasta and toss with the chicken, spinach, and a generous handful of grated parmesan cheese. Squeeze fresh lemon juice on top before serving.",
        prep_time_minutes: 10,
        cook_time_minutes: 15,
        servings: 4,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 2,
        recipe_name: "Creamy Tomato Spinach Rice",
        description: "A comforting, one-pan rice dish loaded with tomatoes, spinach, and a touch of butter and parmesan.",
        instructions: "1. Cook rice according to package instructions.\n2. In a pan, heat olive oil over medium heat. Sauté chopped onions and minced garlic until soft.\n3. Add diced tomatoes and cook for 5 minutes until they break down.\n4. Stir in fresh spinach and cook until wilted.\n5. Add the cooked rice, butter, and parmesan cheese. Stir well until creamy and heated through.\n6. Season with salt and black pepper to taste.",
        prep_time_minutes: 5,
        cook_time_minutes: 20,
        servings: 3,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 3,
        recipe_name: "Avocado Bacon Egg Toast",
        description: "The ultimate breakfast or brunch toast featuring creamy mashed avocado, crispy bacon, and a perfectly fried egg.",
        instructions: "1. Cook bacon in a skillet until crispy. Drain on paper towels.\n2. Toast your bread slices until golden brown.\n3. Mash avocado in a bowl with a squeeze of lemon juice, salt, and black pepper.\n4. Fry eggs in the bacon fat or butter to your desired doneness.\n5. Spread mashed avocado evenly over the toast.\n6. Top with crispy bacon and the fried egg. Garnish with extra black pepper.",
        prep_time_minutes: 5,
        cook_time_minutes: 5,
        servings: 2,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 4,
        recipe_name: "Lemon Garlic Pan-Seared Salmon",
        description: "Perfectly flaky salmon fillets seared in olive oil and basted with a bright lemon garlic butter sauce.",
        instructions: "1. Pat salmon fillets dry and season both sides with salt and black pepper.\n2. Heat olive oil in a skillet over medium-high heat. Add salmon skin-side up and sear for 4-5 minutes until golden.\n3. Flip salmon, add butter, minced garlic, and lemon juice to the pan.\n4. Spoon the melted garlic butter over the salmon as it cooks for another 3-4 minutes.\n5. Serve hot with a drizzle of the pan sauce.",
        prep_time_minutes: 10,
        cook_time_minutes: 10,
        servings: 2,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 5,
        recipe_name: "Classic Cheddar Omelette",
        description: "A fluffy, buttery omelette stuffed with sharp cheddar cheese and fresh bell peppers.",
        instructions: "1. Whisk eggs in a bowl with a pinch of salt and black pepper.\n2. Melt butter in a non-stick skillet over medium heat.\n3. Add chopped bell peppers and onions, sautéing for 2-3 minutes until soft. Remove and set aside.\n4. Pour whisked eggs into the skillet. Let cook for 1-2 minutes, lifting the edges to let uncooked egg flow underneath.\n5. When the eggs are mostly set, sprinkle cheddar cheese and the sautéed peppers over one half.\n6. Fold the omelette in half and slide onto a plate.",
        prep_time_minutes: 5,
        cook_time_minutes: 5,
        servings: 1,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      },
      {
        id: 6,
        recipe_name: "Chicken and Vegetable Stir-Fry",
        description: "A healthy, high-protein stir-fry with chicken breast, bell peppers, onions, and spinach in a savory soy sauce glaze.",
        instructions: "1. Cut chicken breast into bite-sized pieces.\n2. Heat olive oil in a large skillet or wok over high heat.\n3. Add chicken and cook until browned and cooked through (about 5-6 minutes). Remove from pan.\n4. Add a bit more oil, then sauté sliced bell peppers and onions for 3-4 minutes until tender-crisp.\n5. Return chicken to the pan, add fresh spinach, and pour in soy sauce.\n6. Toss everything together for 1-2 minutes until spinach is wilted and sauce coats the ingredients.",
        prep_time_minutes: 10,
        cook_time_minutes: 10,
        servings: 3,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
    ];

    recipes.forEach((rec) => {
      db.insert("recipe", rec, "id");
    });

    // Seed recipe ingredients
    const recipeIngredients = [
      // Garlic Butter Chicken Pasta (Recipe 1)
      { recipeId: 1, ingredientId: 1, quantity: "2", unit: "pieces" }, // Chicken Breast
      { recipeId: 1, ingredientId: 6, quantity: "250", unit: "grams" }, // Pasta
      { recipeId: 1, ingredientId: 13, quantity: "3", unit: "tbsp" }, // Butter
      { recipeId: 1, ingredientId: 3, quantity: "4", unit: "cloves" }, // Garlic
      { recipeId: 1, ingredientId: 10, quantity: "2", unit: "cups" }, // Spinach
      { recipeId: 1, ingredientId: 11, quantity: "0.5", unit: "cup" }, // Parmesan
      { recipeId: 1, ingredientId: 12, quantity: "1", unit: "piece" }, // Lemon

      // Creamy Tomato Spinach Rice (Recipe 2)
      { recipeId: 2, ingredientId: 7, quantity: "1", unit: "cup" }, // Rice
      { recipeId: 2, ingredientId: 5, quantity: "2", unit: "pieces" }, // Tomato
      { recipeId: 2, ingredientId: 10, quantity: "2", unit: "cups" }, // Spinach
      { recipeId: 2, ingredientId: 13, quantity: "2", unit: "tbsp" }, // Butter
      { recipeId: 2, ingredientId: 11, quantity: "0.25", unit: "cup" }, // Parmesan
      { recipeId: 2, ingredientId: 4, quantity: "0.5", unit: "piece" }, // Onion
      { recipeId: 2, ingredientId: 3, quantity: "2", unit: "cloves" }, // Garlic

      // Avocado Bacon Egg Toast (Recipe 3)
      { recipeId: 3, ingredientId: 16, quantity: "1", unit: "piece" }, // Avocado
      { recipeId: 3, ingredientId: 15, quantity: "4", unit: "slices" }, // Bacon
      { recipeId: 3, ingredientId: 14, quantity: "2", unit: "pieces" }, // Eggs
      { recipeId: 3, ingredientId: 12, quantity: "0.5", unit: "piece" }, // Lemon

      // Lemon Garlic Pan-Seared Salmon (Recipe 4)
      { recipeId: 4, ingredientId: 18, quantity: "2", unit: "fillets" }, // Salmon
      { recipeId: 4, ingredientId: 13, quantity: "2", unit: "tbsp" }, // Butter
      { recipeId: 4, ingredientId: 3, quantity: "3", unit: "cloves" }, // Garlic
      { recipeId: 4, ingredientId: 12, quantity: "1", unit: "piece" }, // Lemon
      { recipeId: 4, ingredientId: 2, quantity: "1", unit: "tbsp" }, // Olive Oil

      // Classic Cheddar Omelette (Recipe 5)
      { recipeId: 5, ingredientId: 14, quantity: "3", unit: "pieces" }, // Eggs
      { recipeId: 5, ingredientId: 17, quantity: "0.5", unit: "cup" }, // Cheddar
      { recipeId: 5, ingredientId: 19, quantity: "0.5", unit: "piece" }, // Bell Pepper
      { recipeId: 5, ingredientId: 4, quantity: "0.25", unit: "piece" }, // Onion
      { recipeId: 5, ingredientId: 13, quantity: "1", unit: "tbsp" }, // Butter

      // Chicken and Vegetable Stir-Fry (Recipe 6)
      { recipeId: 6, ingredientId: 1, quantity: "2", unit: "pieces" }, // Chicken Breast
      { recipeId: 6, ingredientId: 19, quantity: "1", unit: "piece" }, // Bell Pepper
      { recipeId: 6, ingredientId: 4, quantity: "0.5", unit: "piece" }, // Onion
      { recipeId: 6, ingredientId: 10, quantity: "2", unit: "cups" }, // Spinach
      { recipeId: 6, ingredientId: 20, quantity: "3", unit: "tbsp" }, // Soy Sauce
      { recipeId: 6, ingredientId: 2, quantity: "1", unit: "tbsp" }, // Olive Oil
    ];

    recipeIngredients.forEach((ri) => {
      db.insert("recipe_ingredient", ri, "recipeId");
    });

    // Seed initial inventory items (Pantry)
    const initialInventory = [
      { id: 1, userId: 1, ingredientId: 1, quantity: "2", unit: "pieces", created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, // Chicken Breast
      { id: 2, userId: 1, ingredientId: 2, quantity: "1", unit: "bottle", created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, // Olive Oil
      { id: 3, userId: 1, ingredientId: 3, quantity: "5", unit: "cloves", created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, // Garlic
      { id: 4, userId: 1, ingredientId: 6, quantity: "500", unit: "grams", created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, // Pasta
      { id: 5, userId: 1, ingredientId: 10, quantity: "3", unit: "cups", created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, // Spinach
      { id: 6, userId: 1, ingredientId: 13, quantity: "250", unit: "grams", created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, // Butter
      { id: 7, userId: 1, ingredientId: 14, quantity: "6", unit: "pieces", created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, // Eggs
      { id: 8, userId: 1, ingredientId: 16, quantity: "2", unit: "pieces", created_at: new Date().toISOString(), updated_at: new Date().toISOString() }, // Avocado
    ];

    initialInventory.forEach((inv) => {
      db.insert("inventory_item", inv, "id");
    });

    // Seed initial shopping list items
    const initialShoppingList = [
      { id: 1, userId: 1, itemName: "Bacon", quantity: "1 pack", notes: "For Avocado Bacon Egg Toast", created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 2, userId: 1, itemName: "Parmesan Cheese", quantity: "1 block", notes: "For Pasta and Rice", created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
      { id: 3, userId: 1, itemName: "Salmon Fillet", quantity: "2 fillets", notes: "For Lemon Garlic Salmon", created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
    ];

    initialShoppingList.forEach((item) => {
      db.insert("shopping_list_item", item, "id");
    });
  }
};
