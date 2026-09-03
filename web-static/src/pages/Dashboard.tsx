import React, { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
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
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from "@/components/ui/sheet";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Plus, Search, Check, ShoppingCart, Clock, Users, ArrowRight, AlertTriangle, Sparkles, BookOpen } from "lucide-react";

export default function Dashboard() {
  // State
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [recipeIngredients, setRecipeIngredients] = useState<RecipeIngredient[]>([]);
  const [loading, setLoading] = useState(true);

  // Quick Add Pantry State
  const [quickAddIngredientId, setQuickAddIngredientId] = useState<string>("");
  const [quickAddQuantity, setQuickAddQuantity] = useState<string>("1");
  const [quickAddUnit, setQuickAddUnit] = useState<string>("unit");

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
      console.error("Error loading dashboard data:", error);
      toast.error("Failed to load dashboard data");
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

  // Recommendation Engine: Calculate match percentage for each recipe
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

  // Sort recipes by match percentage (Relevance Ranking Engine)
  const rankedRecipes = recipes.map((recipe) => {
    const stats = getRecipeMatchStats(recipe.id);
    return {
      recipe,
      stats,
    };
  }).sort((a, b) => b.stats.percentage - a.stats.percentage);

  // Top Pick (highest match percentage)
  const topPick = rankedRecipes[0];
  // Other recommendations
  const otherRecommendations = rankedRecipes.slice(1);

  // Quick Add Ingredient to Pantry
  const handleQuickAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!quickAddIngredientId) {
      toast.error("Please select an ingredient");
      return;
    }

    try {
      const ingId = parseInt(quickAddIngredientId);
      // Check if already in pantry
      const existing = inventory.find((item) => item.ingredientId === ingId);

      if (existing) {
        // Update quantity
        const newQty = (parseFloat(existing.quantity) + parseFloat(quickAddQuantity)).toString();
        await inventoryItemRepository.updateById(existing.id, { quantity: newQty });
        toast.success(`Updated quantity for ${getIngredientName(ingId)}`);
      } else {
        // Create new
        const newItem = new InventoryItem(
          0,
          1, // userId
          ingId,
          quickAddQuantity,
          quickAddUnit || "unit",
          new Date().toISOString(),
          new Date().toISOString()
        );
        await inventoryItemRepository.create(newItem);
        toast.success(`Added ${getIngredientName(ingId)} to pantry`);
      }

      // Reset form and reload
      setQuickAddIngredientId("");
      setQuickAddQuantity("1");
      loadData();
    } catch (error) {
      console.error("Error adding ingredient:", error);
      toast.error("Failed to add ingredient");
    }
  };

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

  // Mark ingredient as used (decrease quantity or delete)
  const handleMarkAsUsed = async (itemId: number, ingredientName: string) => {
    try {
      await inventoryItemRepository.deleteById(itemId);
      toast.success(`Marked ${ingredientName} as used`);
      loadData();
    } catch (error) {
      console.error("Error marking as used:", error);
      toast.error("Failed to update pantry");
    }
  };

  return (
    <Layout>
      <div className="space-y-8" data-usecases="inventory-view-aggregator-a4732472">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-amber-100 dark:border-zinc-800 pb-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
              Meal Planning Dashboard
            </h1>
            <p className="text-zinc-500 dark:text-zinc-400 mt-1">
              Transform your pantry inventory into delicious culinary inspiration.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/pantry">
              <Button variant="outline" className="border-amber-200 hover:bg-amber-50 dark:border-zinc-800 dark:hover:bg-zinc-800">
                Manage Pantry
              </Button>
            </Link>
            <Link to="/recipes">
              <Button className="bg-amber-500 hover:bg-amber-600 text-white">
                <Search className="h-4 w-4 mr-2" />
                Find Recipes
              </Button>
            </Link>
          </div>
        </div>

        {loading ? (
          // Loading Skeletons
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 space-y-6">
              <Skeleton className="h-[300px] w-full rounded-xl" />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Skeleton className="h-[200px] rounded-xl" />
                <Skeleton className="h-[200px] rounded-xl" />
              </div>
            </div>
            <div className="space-y-6">
              <Skeleton className="h-[400px] rounded-xl" />
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column: Recipe Recommendations */}
            <div className="lg:col-span-2 space-y-8">
              {/* Top Picks Hero Section */}
              {topPick ? (
                <div className="relative overflow-hidden rounded-2xl border border-amber-100 dark:border-zinc-800 bg-gradient-to-br from-amber-500/10 via-amber-500/5 to-transparent p-6 md:p-8 shadow-sm">
                  <div className="absolute top-4 right-4">
                    <Badge className="bg-amber-500 text-white hover:bg-amber-600 flex items-center gap-1 px-3 py-1">
                      <Sparkles className="h-3.5 w-3.5" />
                      <span>Top Pick</span>
                    </Badge>
                  </div>

                  <div className="max-w-xl space-y-4">
                    <div className="space-y-2">
                      <span className="text-xs font-semibold text-amber-600 dark:text-amber-400 uppercase tracking-wider">
                        Based on your pantry
                      </span>
                      <h2 className="text-2xl md:text-3xl font-bold text-zinc-900 dark:text-zinc-50">
                        {topPick.recipe.recipeName}
                      </h2>
                      <p className="text-zinc-600 dark:text-zinc-300 text-sm md:text-base line-clamp-2">
                        {topPick.recipe.description}
                      </p>
                    </div>

                    {/* Match Progress */}
                    <div className="space-y-1.5" data-usecases="relevance-ranking-engine-5fc3d7c0">
                      <div className="flex justify-between text-xs font-medium">
                        <span className="text-zinc-500 dark:text-zinc-400">Pantry Match</span>
                        <span className="text-amber-600 dark:text-amber-400 font-bold">
                          {topPick.stats.percentage}% ({topPick.stats.ownedCount}/{topPick.stats.totalCount} ingredients)
                        </span>
                      </div>
                      <Progress value={topPick.stats.percentage} className="h-2 bg-amber-100 dark:bg-zinc-800" />
                    </div>

                    {/* Recipe Meta */}
                    <div className="flex flex-wrap gap-4 text-xs text-zinc-500 dark:text-zinc-400 pt-2">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3.5 w-3.5 text-amber-500" />
                        Prep: {topPick.recipe.prepTimeMinutes || 10}m | Cook: {topPick.recipe.cookTimeMinutes || 15}m
                      </span>
                      <span className="flex items-center gap-1">
                        <Users className="h-3.5 w-3.5 text-amber-500" />
                        Servings: {topPick.recipe.servings || 2}
                      </span>
                    </div>

                    {/* Actions */}
                    <div className="flex flex-wrap gap-3 pt-2">
                      <Button
                        onClick={() => {
                          setSelectedRecipe(topPick.recipe);
                          setIsRecipeDrawerOpen(true);
                        }}
                        className="bg-amber-500 hover:bg-amber-600 text-white"
                      >
                        View Recipe Instructions
                        <ArrowRight className="h-4 w-4 ml-2" />
                      </Button>

                      {topPick.stats.missing.length > 0 && (
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-zinc-500 dark:text-zinc-400">
                            Missing {topPick.stats.missing.length} items.
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-12 border border-dashed border-amber-200 dark:border-zinc-800 rounded-2xl bg-amber-50/10">
                  <BookOpen className="h-12 w-12 text-amber-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">No recipes found</h3>
                  <p className="text-zinc-500 dark:text-zinc-400 max-w-md mx-auto mt-1">
                    Add ingredients to your pantry to get personalized recipe recommendations.
                  </p>
                  <Link to="/pantry" className="inline-block mt-4">
                    <Button className="bg-amber-500 hover:bg-amber-600 text-white">
                      Add Pantry Ingredients
                    </Button>
                  </Link>
                </div>
              )}

              {/* Recipe Grid */}
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-zinc-900 dark:text-zinc-50">
                  More Recipe Suggestions
                </h3>

                {otherRecommendations.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {otherRecommendations.map(({ recipe, stats }) => (
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

                        <CardContent className="pb-3 flex-1 space-y-3">
                          {/* Progress */}
                          <div className="space-y-1">
                            <Progress value={stats.percentage} className="h-1.5 bg-amber-50 dark:bg-zinc-800" />
                            <p className="text-[10px] text-zinc-500 dark:text-zinc-400 text-right">
                              {stats.ownedCount} of {stats.totalCount} ingredients
                            </p>
                          </div>

                          {/* Missing Ingredients */}
                          {stats.missing.length > 0 && (
                            <div className="space-y-1">
                              <p className="text-[11px] font-semibold text-zinc-500 dark:text-zinc-400">
                                Missing:
                              </p>
                              <div className="flex flex-wrap gap-1">
                                {stats.missing.slice(0, 3).map((ri) => (
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
                                      <Plus className="h-3 w-3" />
                                    </button>
                                  </Badge>
                                ))}
                                {stats.missing.length > 3 && (
                                  <span className="text-[10px] text-zinc-400">
                                    +{stats.missing.length - 3} more
                                  </span>
                                )}
                              </div>
                            </div>
                          )}
                        </CardContent>

                        <CardFooter className="pt-0 border-t border-amber-50 dark:border-zinc-800/50 mt-auto flex justify-between items-center py-3">
                          <span className="text-[11px] text-zinc-400 flex items-center gap-1">
                            <Clock className="h-3 w-3" />
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
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-zinc-500 dark:text-zinc-400">
                    No other recipe suggestions available.
                  </p>
                )}
              </div>
            </div>

            {/* Right Column: Quick Pantry Rail */}
            <div className="space-y-6">
              {/* Quick Pantry Summary */}
              <Card className="border-amber-100 dark:border-zinc-800 shadow-sm">
                <CardHeader className="pb-4">
                  <div className="flex justify-between items-center">
                    <CardTitle className="text-lg font-bold text-zinc-900 dark:text-zinc-50">
                      Quick Pantry
                    </CardTitle>
                    <Badge className="bg-amber-100 text-amber-800 dark:bg-zinc-800 dark:text-amber-300">
                      {inventory.length} Items
                    </Badge>
                  </div>
                  <CardDescription className="text-xs">
                    Your current stock. Mark items as used or add new ones.
                  </CardDescription>
                </CardHeader>

                <CardContent className="space-y-4">
                  {/* Quick Add Form */}
                  <form onSubmit={handleQuickAdd} className="space-y-3 p-3 bg-amber-50/50 dark:bg-zinc-900/50 rounded-xl border border-amber-100/50 dark:border-zinc-800/50">
                    <p className="text-xs font-semibold text-amber-800 dark:text-amber-300">
                      Quick Add Ingredient
                    </p>
                    <div className="space-y-2">
                      <div>
                        <Label htmlFor="quick-ingredient" className="sr-only">Ingredient</Label>
                        <select
                          id="quick-ingredient"
                          value={quickAddIngredientId}
                          onChange={(e) => setQuickAddIngredientId(e.target.value)}
                          className="w-full rounded-md border border-amber-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 px-3 py-1.5 text-xs text-zinc-900 dark:text-zinc-50 focus:outline-none focus:ring-1 focus:ring-amber-500"
                        >
                          <option value="">Select Ingredient...</option>
                          {ingredients.map((ing) => (
                            <option key={ing.id} value={ing.id}>
                              {ing.name}
                            </option>
                          ))}
                        </select>
                      </div>

                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <Label htmlFor="quick-qty" className="sr-only">Quantity</Label>
                          <Input
                            id="quick-qty"
                            type="number"
                            placeholder="Qty"
                            value={quickAddQuantity}
                            onChange={(e) => setQuickAddQuantity(e.target.value)}
                            className="h-8 text-xs border-amber-200 dark:border-zinc-800"
                            min="0.1"
                            step="any"
                          />
                        </div>
                        <div>
                          <Label htmlFor="quick-unit" className="sr-only">Unit</Label>
                          <Input
                            id="quick-unit"
                            placeholder="Unit (e.g. pcs)"
                            value={quickAddUnit}
                            onChange={(e) => setQuickAddUnit(e.target.value)}
                            className="h-8 text-xs border-amber-200 dark:border-zinc-800"
                          />
                        </div>
                      </div>

                      <Button
                        type="submit"
                        className="w-full h-8 bg-amber-500 hover:bg-amber-600 text-white text-xs"
                        data-usecases="quick-action-orchestrator-71f60a2e"
                      >
                        <Plus className="h-3.5 w-3.5 mr-1" />
                        Add to Pantry
                      </Button>
                    </div>
                  </form>

                  {/* Pantry List */}
                  <div className="space-y-2 max-h-[300px] overflow-y-auto pr-1">
                    {inventory.length > 0 ? (
                      inventory.map((item) => {
                        const name = getIngredientName(item.ingredientId);
                        return (
                          <div
                            key={item.id}
                            className="flex items-center justify-between p-2 rounded-lg border border-amber-50 dark:border-zinc-800/50 hover:bg-amber-50/30 dark:hover:bg-zinc-900/30 transition-colors text-xs"
                          >
                            <div className="space-y-0.5">
                              <p className="font-semibold text-zinc-800 dark:text-zinc-200">
                                {name}
                              </p>
                              <p className="text-[10px] text-zinc-500 dark:text-zinc-400">
                                {item.quantity} {item.unit || "units"}
                              </p>
                            </div>
                            <Button
                              size="icon"
                              variant="ghost"
                              className="h-7 w-7 text-zinc-400 hover:text-amber-600 dark:hover:text-amber-400 hover:bg-amber-50 dark:hover:bg-zinc-800"
                              onClick={() => handleMarkAsUsed(item.id, name)}
                              title="Mark as Used"
                              data-usecases="quick-action-orchestrator-71f60a2e"
                            >
                              <Check className="h-3.5 w-3.5" />
                            </Button>
                          </div>
                        );
                      })
                    ) : (
                      <div className="text-center py-6 text-zinc-400 dark:text-zinc-500">
                        <p className="text-xs">Your pantry is empty.</p>
                      </div>
                    )}
                  </div>
                </CardContent>

                <CardFooter className="pt-0 border-t border-amber-50 dark:border-zinc-800/50 py-3">
                  <Link to="/pantry" className="w-full">
                    <Button variant="ghost" className="w-full text-xs text-amber-600 hover:text-amber-700 dark:text-amber-400 dark:hover:text-amber-300">
                      View Full Pantry Manager
                      <ArrowRight className="h-3.5 w-3.5 ml-1" />
                    </Button>
                  </Link>
                </CardFooter>
              </Card>

              {/* Expiration Alerts / Tips */}
              <Card className="border-amber-100 dark:border-zinc-800 bg-amber-50/20 dark:bg-zinc-900/20">
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-bold text-zinc-900 dark:text-zinc-50 flex items-center gap-1.5">
                    <AlertTriangle className="h-4 w-4 text-amber-500" />
                    Pantry Insights
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-xs text-zinc-600 dark:text-zinc-400 space-y-2">
                  <p>
                    You have <strong className="text-amber-700 dark:text-amber-300">Spinach</strong> and <strong className="text-amber-700 dark:text-amber-300">Eggs</strong> expiring soon. Try making the <strong className="font-semibold">Classic Cheddar Omelette</strong>!
                  </p>
                  <p className="text-[10px] text-zinc-400">
                    Tip: Keep your pantry updated to get the most accurate recipe recommendations.
                  </p>
                </CardContent>
              </Card>
            </div>
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
