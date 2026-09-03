import { useEffect, useState, useCallback } from "react";
import { Layout } from "@/components/Layout";
import { seedPantryPalData } from "@/lib/seedData";
import { recipeRepository } from "@/features/tables/recipe/repository";
import { inventoryItemRepository } from "@/features/tables/inventory_item/repository";
import { ingredientRepository } from "@/features/tables/ingredient/repository";
import { recipeIngredientRepository } from "@/features/tables/recipe_ingredient/repository";
import { shoppingListItemRepository } from "@/features/tables/shopping_list_item/repository";
import { Recipe } from "@/features/tables/recipe/model";
import { InventoryItem } from "@/features/tables/inventory_item/model";
import { Ingredient } from "@/features/tables/ingredient/model";
import { RecipeIngredient } from "@/features/tables/recipe_ingredient/model";
import { ShoppingListItem } from "@/features/tables/shopping_list_item/model";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from "@/components/ui/sheet";
import { toast } from "sonner";
import { Search, Filter, Clock, ArrowRight, ShoppingCart, BookOpen } from "lucide-react";

export default function Recipes() {
  // State
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [recipeIngredients, setRecipeIngredients] = useState<RecipeIngredient[]>([]);
  const [loading, setLoading] = useState(true);

  // Search & Filter State
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedDiet, setSelectedDiet] = useState("all");

  // Selected Recipe for Drawer
  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);
  const [isRecipeDrawerOpen, setIsRecipeDrawerOpen] = useState(false);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      seedPantryPalData();

      const [recipesRes, inventoryRes, ingredientsRes, recipeIngredientsRes] = await Promise.all([
        recipeRepository.getAll({ page: 1, size: 100 }),
        inventoryItemRepository.getAll({ page: 1, size: 100 }),
        ingredientRepository.getAll({ page: 1, size: 100 }),
        recipeIngredientRepository.getAll({ page: 1, size: 100 }),
      ]);

      setRecipes(recipesRes.items);
      setInventory(inventoryRes.items);
      setIngredients(ingredientsRes.items);
      setRecipeIngredients(recipeIngredientsRes.items);
    } catch (error) {
      console.error("Error loading recipes data:", error);
      toast.error("Failed to load recipes data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadData();
    }, 0);
    return () => clearTimeout(timer);
  }, [loadData]);

  // Helper: Get ingredient name by ID
  const getIngredientName = (id: number) => {
    return ingredients.find((ing) => ing.id === id)?.name || "Unknown Ingredient";
  };

  // Helper: Check if ingredient is in pantry
  const isIngredientInPantry = (ingredientId: number) => {
    return inventory.some((item) => item.ingredientId === ingredientId);
  };

  // Helper: Get required ingredients for a recipe
  const getRecipeIngredients = (recipeId: number) => {
    return recipeIngredients.filter((ri) => ri.recipeId === recipeId);
  };

  // Helper: Get recipe match percentage
  const getRecipeMatchStats = (recipeId: number) => {
    const required = getRecipeIngredients(recipeId);
    if (required.length === 0) return { percentage: 0, ownedCount: 0, totalCount: 0, missing: [] };

    let ownedCount = 0;
    const missing: RecipeIngredient[] = [];

    required.forEach((ri) => {
      if (isIngredientInPantry(ri.ingredientId)) {
        ownedCount++;
      } else {
        missing.push(ri);
      }
    });

    const percentage = Math.round((ownedCount / required.length) * 100);
    return {
      percentage,
      ownedCount,
      totalCount: required.length,
      missing,
    };
  };

  // Helper: Get dietary tags for a recipe
  const getDietaryTags = (recipeId: number) => {
    const tags: string[] = [];
    if (recipeId === 1) tags.push("High-Protein");
    if (recipeId === 2) tags.push("Vegetarian", "Gluten-Free");
    if (recipeId === 3) tags.push("Low-Carb");
    if (recipeId === 4) tags.push("Gluten-Free", "Low-Carb", "High-Protein");
    if (recipeId === 5) tags.push("Vegetarian", "Gluten-Free", "Low-Carb");
    if (recipeId === 6) tags.push("Gluten-Free", "Low-Carb", "High-Protein");
    return tags;
  };

  // Filtered Recipes
  const filteredRecipes = recipes.filter((recipe) => {
    const matchesSearch = recipe.recipeName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (recipe.description && recipe.description.toLowerCase().includes(searchQuery.toLowerCase()));

    const tags = getDietaryTags(recipe.id);
    const matchesDiet = selectedDiet === "all" || tags.includes(selectedDiet);

    return matchesSearch && matchesDiet;
  });

  // Add missing ingredient to shopping list
  const handleAddToShoppingList = async (ingredientId: number, recipeName: string) => {
    try {
      const name = getIngredientName(ingredientId);
      const newItem = new ShoppingListItem(
        0,
        1, // userId
        name,
        "1 unit",
        `Needed for ${recipeName}`,
        new Date().toISOString(),
        new Date().toISOString()
      );
      await shoppingListItemRepository.create(newItem);
      toast.success(`Added ${name} to shopping list`);
    } catch (error) {
      console.error("Error adding to shopping list:", error);
      toast.error("Failed to add to shopping list");
    }
  };

  return (
    <Layout>
      <div className="space-y-8" data-usecases="query-parser-and-normalizer-2b747fac">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-amber-100 dark:border-zinc-800 pb-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
              Recipe Catalog & Discovery
            </h1>
            <p className="text-zinc-500 dark:text-zinc-400 mt-1">
              Explore recipes, filter by dietary needs, and see how well they match your current pantry.
            </p>
          </div>
        </div>

        {/* Search and Filter Controls */}
        <div className="flex flex-col md:flex-row gap-4 items-center justify-between bg-white dark:bg-zinc-900 p-4 rounded-xl border border-amber-100 dark:border-zinc-800" data-usecases="faceted-filter-processor-121fab1a">
          <div className="relative w-full md:w-96">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-zinc-400" />
            <Input
              placeholder="Search recipes by name or description..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 border-amber-200 dark:border-zinc-800 focus-visible:ring-amber-500"
            />
          </div>

          <div className="flex items-center gap-3 w-full md:w-auto justify-end">
            <div className="flex items-center gap-2 text-sm text-zinc-500 dark:text-zinc-400">
              <Filter className="h-4 w-4 text-amber-500" />
              <span>Dietary Needs:</span>
            </div>
            <select
              value={selectedDiet}
              onChange={(e) => setSelectedDiet(e.target.value)}
              className="rounded-md border border-amber-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 px-3 py-1.5 text-sm text-zinc-900 dark:text-zinc-50 focus:outline-none focus:ring-1 focus:ring-amber-500"
            >
              <option value="all">All Diets</option>
              <option value="Vegetarian">Vegetarian</option>
              <option value="Gluten-Free">Gluten-Free</option>
              <option value="Low-Carb">Low-Carb</option>
              <option value="High-Protein">High-Protein</option>
            </select>
          </div>
        </div>

        {/* Recipe Grid */}
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Skeleton className="h-[300px] rounded-xl" />
            <Skeleton className="h-[300px] rounded-xl" />
            <Skeleton className="h-[300px] rounded-xl" />
          </div>
        ) : filteredRecipes.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" data-usecases="relevance-ranking-engine-5fc3d7c0">
            {filteredRecipes.map((recipe) => {
              const stats = getRecipeMatchStats(recipe.id);
              const tags = getDietaryTags(recipe.id);

              return (
                <Card
                  key={recipe.id}
                  className="group border-amber-100 dark:border-zinc-800 hover:shadow-md transition-all duration-200 hover:-translate-y-0.5 flex flex-col"
                >
                  <CardHeader className="pb-3">
                    <div className="flex justify-between items-start gap-2">
                      <CardTitle className="text-lg font-bold text-zinc-900 dark:text-zinc-50 group-hover:text-amber-600 dark:group-hover:text-amber-400 transition-colors line-clamp-1">
                        {recipe.recipeName}
                      </CardTitle>
                      <Badge variant="secondary" className="bg-amber-50 text-amber-700 dark:bg-zinc-800 dark:text-amber-300 shrink-0">
                        {stats.percentage}% Match
                      </Badge>
                    </div>
                    <CardDescription className="line-clamp-2 text-xs mt-1">
                      {recipe.description}
                    </CardDescription>
                  </CardHeader>

                  <CardContent className="pb-3 flex-1 space-y-4">
                    {/* Dietary Tags */}
                    <div className="flex flex-wrap gap-1">
                      {tags.map((tag) => (
                        <Badge
                          key={tag}
                          variant="outline"
                          className="text-[10px] bg-amber-50/50 dark:bg-zinc-900/50 border-amber-100 dark:border-zinc-800 text-amber-700 dark:text-amber-300"
                        >
                          {tag}
                        </Badge>
                      ))}
                    </div>

                    {/* Match Progress */}
                    <div className="space-y-1">
                      <div className="flex justify-between text-[10px] text-zinc-500 dark:text-zinc-400">
                        <span>Pantry Match</span>
                        <span>{stats.ownedCount} of {stats.totalCount} ingredients</span>
                      </div>
                      <div className="w-full bg-amber-50 dark:bg-zinc-800 h-1.5 rounded-full overflow-hidden">
                        <div
                          className="bg-amber-500 h-full rounded-full transition-all duration-500"
                          style={{ width: `${stats.percentage}%` }}
                        />
                      </div>
                    </div>

                    {/* Missing Ingredients */}
                    {stats.missing.length > 0 && (
                      <div className="space-y-1">
                        <p className="text-[11px] font-semibold text-zinc-500 dark:text-zinc-400">
                          Missing:
                        </p>
                        <div className="flex flex-wrap gap-1">
                          {stats.missing.map((ri) => (
                            <Badge
                              key={ri.ingredientId}
                              variant="outline"
                              className="text-[10px] border-amber-200 dark:border-zinc-800 text-zinc-600 dark:text-zinc-400 flex items-center gap-1"
                            >
                              {getIngredientName(ri.ingredientId)}
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleAddToShoppingList(ri.ingredientId, recipe.recipeName);
                                }}
                                className="hover:text-amber-600 dark:hover:text-amber-400"
                                title="Add to Shopping List"
                                data-usecases="shopping-list-generator-3a1a4ea9"
                              >
                                <ShoppingCart className="h-3 w-3" />
                              </button>
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </CardContent>

                  <CardFooter className="pt-0 border-t border-amber-50 dark:border-zinc-800/50 mt-auto flex justify-between items-center py-3">
                    <span className="text-[11px] text-zinc-400 flex items-center gap-1">
                      <Clock className="h-3.5 w-3.5 text-amber-500" />
                      {recipe.prepTimeMinutes ? recipe.prepTimeMinutes + recipe.cookTimeMinutes! : 25} mins
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        setSelectedRecipe(recipe);
                        setIsRecipeDrawerOpen(true);
                      }}
                      className="text-amber-600 hover:text-amber-700 dark:text-amber-400 dark:hover:text-amber-300 text-xs font-semibold p-0 h-auto hover:bg-transparent"
                    >
                      View Recipe
                      <ArrowRight className="h-3 w-3 ml-1" />
                    </Button>
                  </CardFooter>
                </Card>
              );
            })}
          </div>
        ) : (
          <div className="text-center py-16 border border-dashed border-amber-200 dark:border-zinc-800 rounded-2xl bg-amber-50/10">
            <BookOpen className="h-12 w-12 text-amber-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">No recipes found</h3>
            <p className="text-zinc-500 dark:text-zinc-400 max-w-md mx-auto mt-1">
              Try adjusting your search query or dietary filter to find recipes.
            </p>
          </div>
        )}
      </div>

      {/* Recipe Instructions Drawer */}
      <Sheet open={isRecipeDrawerOpen} onOpenChange={setIsRecipeDrawerOpen}>
        <SheetContent className="w-full sm:max-w-lg overflow-y-auto bg-white dark:bg-zinc-900">
          {selectedRecipe && (
            <div className="space-y-6 py-4">
              <SheetHeader>
                <div className="flex justify-between items-start">
                  <Badge className="bg-amber-500 text-white">Recipe Details</Badge>
                </div>
                <SheetTitle className="text-2xl font-bold text-zinc-900 dark:text-zinc-50 mt-2">
                  {selectedRecipe.recipeName}
                </SheetTitle>
                <SheetDescription className="text-zinc-500 dark:text-zinc-400 text-sm">
                  {selectedRecipe.description}
                </SheetDescription>
              </SheetHeader>

              {/* Recipe Meta */}
              <div className="grid grid-cols-3 gap-4 p-3 bg-amber-50/50 dark:bg-zinc-900/50 rounded-xl text-center text-xs">
                <div>
                  <p className="text-zinc-400">Prep Time</p>
                  <p className="font-bold text-zinc-800 dark:text-zinc-200">
                    {selectedRecipe.prepTimeMinutes || 10} mins
                  </p>
                </div>
                <div>
                  <p className="text-zinc-400">Cook Time</p>
                  <p className="font-bold text-zinc-800 dark:text-zinc-200">
                    {selectedRecipe.cookTimeMinutes || 15} mins
                  </p>
                </div>
                <div>
                  <p className="text-zinc-400">Servings</p>
                  <p className="font-bold text-zinc-800 dark:text-zinc-200">
                    {selectedRecipe.servings || 2}
                  </p>
                </div>
              </div>

              {/* Ingredients List */}
              <div className="space-y-3">
                <h4 className="font-bold text-zinc-900 dark:text-zinc-50 text-sm">
                  Required Ingredients
                </h4>
                <div className="space-y-2">
                  {getRecipeIngredients(selectedRecipe.id).map((ri) => {
                    const inPantry = isIngredientInPantry(ri.ingredientId);
                    return (
                      <div
                        key={ri.ingredientId}
                        className="flex items-center justify-between p-2 rounded-lg border border-zinc-100 dark:border-zinc-800 text-xs"
                      >
                        <div className="flex items-center gap-2">
                          <div className={`h-2 w-2 rounded-full ${inPantry ? "bg-green-500" : "bg-amber-500"}`} />
                          <span className="font-medium text-zinc-800 dark:text-zinc-200">
                            {getIngredientName(ri.ingredientId)}
                          </span>
                        </div>
                        <div className="flex items-center gap-3">
                          <span className="text-zinc-500 dark:text-zinc-400">
                            {ri.quantity} {ri.unit || "units"}
                          </span>
                          {!inPantry && (
                            <Button
                              size="icon"
                              variant="ghost"
                              className="h-7 w-7 text-amber-600 hover:text-amber-700 hover:bg-amber-50 dark:hover:bg-zinc-800"
                              onClick={() => handleAddToShoppingList(ri.ingredientId, selectedRecipe.recipeName)}
                              title="Add to Shopping List"
                              data-usecases="shopping-list-generator-3a1a4ea9"
                            >
                              <ShoppingCart className="h-3.5 w-3.5" />
                            </Button>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Instructions */}
              <div className="space-y-3">
                <h4 className="font-bold text-zinc-900 dark:text-zinc-50 text-sm">
                  Cooking Instructions
                </h4>
                <div className="bg-zinc-50 dark:bg-zinc-950 p-4 rounded-xl border border-zinc-100 dark:border-zinc-800 text-xs text-zinc-700 dark:text-zinc-300 whitespace-pre-line leading-relaxed">
                  {selectedRecipe.instructions || "No instructions provided."}
                </div>
              </div>

              <div className="pt-4 border-t border-zinc-100 dark:border-zinc-800 flex justify-end">
                <Button
                  onClick={() => setIsRecipeDrawerOpen(false)}
                  className="bg-amber-500 hover:bg-amber-600 text-white"
                >
                  Close Details
                </Button>
              </div>
            </div>
          )}
        </SheetContent>
      </Sheet>
    </Layout>
  );
}
