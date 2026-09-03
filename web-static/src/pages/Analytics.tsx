import { useEffect, useState, useCallback } from "react";
import { Layout } from "@/components/Layout";
import { seedPantryPalData } from "@/lib/seedData";
import { inventoryItemRepository } from "@/features/tables/inventory_item/repository";
import { ingredientRepository } from "@/features/tables/ingredient/repository";
import { recipeRepository } from "@/features/tables/recipe/repository";
import { InventoryItem } from "@/features/tables/inventory_item/model";
import { Ingredient } from "@/features/tables/ingredient/model";
import { Recipe } from "@/features/tables/recipe/model";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { PieChart, TrendingUp, Beef, BookOpen, CheckCircle2 } from "lucide-react";

export default function Analytics() {
  // State
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      seedPantryPalData();

      const [inventoryRes, ingredientsRes, recipesRes] = await Promise.all([
        inventoryItemRepository.getAll({ page: 1, size: 100 }),
        ingredientRepository.getAll({ page: 1, size: 100 }),
        recipeRepository.getAll({ page: 1, size: 100 }),
      ]);

      setInventory(inventoryRes.items);
      setIngredients(ingredientsRes.items);
      setRecipes(recipesRes.items);
    } catch (error) {
      console.error("Error loading analytics data:", error);
      toast.error("Failed to load analytics data");
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

  // Calculate Category Distribution
  const getCategoryDistribution = () => {
    const distribution: Record<string, number> = {
      "Proteins": 0,
      "Pantry": 0,
      "Aromatics": 0,
      "Produce": 0,
      "Grains": 0,
      "Dairy": 0,
    };

    inventory.forEach((item) => {
      const ing = ingredients.find((i) => i.id === item.ingredientId);
      if (ing) {
        const catId = ing.categoryId;
        if (catId === 1) distribution["Proteins"]++;
        else if (catId === 2) distribution["Pantry"]++;
        else if (catId === 3) distribution["Aromatics"]++;
        else if (catId === 4) distribution["Produce"]++;
        else if (catId === 5) distribution["Grains"]++;
        else if (catId === 6) distribution["Dairy"]++;
      }
    });

    return Object.entries(distribution).map(([name, count]) => ({
      name,
      count,
      percentage: inventory.length > 0 ? Math.round((count / inventory.length) * 100) : 0,
    })).sort((a, b) => b.count - a.count);
  };

  const categoryData = getCategoryDistribution();

  // Mocked Ingredient Usage Trends (Visualization Data Transformer)
  const usageTrends = [
    { name: "Garlic", usageCount: 12, status: "High Demand", color: "text-amber-600 bg-amber-50 dark:bg-zinc-800 dark:text-amber-400" },
    { name: "Olive Oil", usageCount: 9, status: "Stable", color: "text-green-600 bg-green-50 dark:bg-zinc-800 dark:text-green-400" },
    { name: "Spinach", usageCount: 8, status: "Expiring Soon", color: "text-red-600 bg-red-50 dark:bg-zinc-800 dark:text-red-400" },
    { name: "Chicken Breast", usageCount: 7, status: "High Demand", color: "text-amber-600 bg-amber-50 dark:bg-zinc-800 dark:text-amber-400" },
    { name: "Eggs", usageCount: 6, status: "Stable", color: "text-green-600 bg-green-50 dark:bg-zinc-800 dark:text-green-400" },
  ];

  return (
    <Layout>
      <div className="space-y-8" data-usecases="query-orchestration-service-77325352">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-amber-100 dark:border-zinc-800 pb-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
              Insights & Reporting Dashboard
            </h1>
            <p className="text-zinc-500 dark:text-zinc-400 mt-1">
              Visualize ingredient usage trends, pantry distribution, and recipe analytics.
            </p>
          </div>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Skeleton className="h-32 rounded-xl" />
            <Skeleton className="h-32 rounded-xl" />
            <Skeleton className="h-32 rounded-xl" />
          </div>
        ) : (
          <div className="space-y-8">
            {/* Key Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="border-amber-100 dark:border-zinc-800 shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-zinc-500 dark:text-zinc-400">
                    Pantry Stock
                  </CardTitle>
                  <Beef className="h-5 w-5 text-amber-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-zinc-900 dark:text-zinc-50">
                    {inventory.length}
                  </div>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
                    Active ingredients in your pantry
                  </p>
                </CardContent>
              </Card>

              <Card className="border-amber-100 dark:border-zinc-800 shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-zinc-500 dark:text-zinc-400">
                    Available Recipes
                  </CardTitle>
                  <BookOpen className="h-5 w-5 text-amber-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-zinc-900 dark:text-zinc-50">
                    {recipes.length}
                  </div>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
                    Recipes in the central database
                  </p>
                </CardContent>
              </Card>

              <Card className="border-amber-100 dark:border-zinc-800 shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between pb-2">
                  <CardTitle className="text-sm font-medium text-zinc-500 dark:text-zinc-400">
                    Pantry Health Score
                  </CardTitle>
                  <CheckCircle2 className="h-5 w-5 text-green-500" />
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-zinc-900 dark:text-zinc-50">
                    84%
                  </div>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
                    Excellent variety and low waste risk
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Detailed Analytics Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8" data-usecases="visualization-data-transformer-229c5d50">
              {/* Pantry Category Distribution */}
              <Card className="border-amber-100 dark:border-zinc-800 shadow-sm">
                <CardHeader>
                  <CardTitle className="text-lg font-bold text-zinc-900 dark:text-zinc-50 flex items-center gap-2">
                    <PieChart className="h-5 w-5 text-amber-500" />
                    Pantry Category Distribution
                  </CardTitle>
                  <CardDescription className="text-xs">
                    Breakdown of your current pantry items by food category.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {categoryData.map((cat) => (
                    <div key={cat.name} className="space-y-1.5">
                      <div className="flex justify-between text-xs font-medium">
                        <span className="text-zinc-700 dark:text-zinc-300">{cat.name}</span>
                        <span className="text-zinc-500 dark:text-zinc-400">
                          {cat.count} items ({cat.percentage}%)
                        </span>
                      </div>
                      <Progress value={cat.percentage} className="h-2 bg-amber-50 dark:bg-zinc-800" />
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Ingredient Usage Trends */}
              <Card className="border-amber-100 dark:border-zinc-800 shadow-sm">
                <CardHeader>
                  <CardTitle className="text-lg font-bold text-zinc-900 dark:text-zinc-50 flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-amber-500" />
                    Ingredient Usage Trends
                  </CardTitle>
                  <CardDescription className="text-xs">
                    Most frequently used ingredients and their current status.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    {usageTrends.map((trend) => (
                      <div
                        key={trend.name}
                        className="flex items-center justify-between p-3 rounded-xl border border-amber-50 dark:border-zinc-800/50 hover:bg-amber-50/30 dark:hover:bg-zinc-900/30 transition-colors"
                      >
                        <div className="space-y-0.5">
                          <p className="font-bold text-zinc-900 dark:text-zinc-100 text-sm">
                            {trend.name}
                          </p>
                          <p className="text-xs text-zinc-500 dark:text-zinc-400">
                            Used in {trend.usageCount} meals this month
                          </p>
                        </div>
                        <Badge className={`text-xs font-medium border-none ${trend.color}`}>
                          {trend.status}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
