import React, { useEffect, useState, useCallback } from "react";
import { Layout } from "@/components/Layout";
import { seedPantryPalData } from "@/lib/seedData";
import { inventoryItemRepository } from "@/features/tables/inventory_item/repository";
import { ingredientRepository } from "@/features/tables/ingredient/repository";
import { categoryRepository } from "@/features/tables/category/repository";
import { InventoryItem } from "@/features/tables/inventory_item/model";
import { Ingredient } from "@/features/tables/ingredient/model";
import { Category } from "@/features/tables/category/model";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from "@/components/ui/sheet";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Plus, Search, Trash2, Edit2, AlertTriangle, Filter, RefreshCw, Calendar } from "lucide-react";

export default function Pantry() {
  // State
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  // Search & Filter State
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");

  // Add/Edit Drawer State
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<InventoryItem | null>(null);
  const [formIngredientId, setFormIngredientId] = useState("");
  const [formQuantity, setFormQuantity] = useState("1");
  const [formUnit, setFormUnit] = useState("unit");

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      seedPantryPalData();

      const [inventoryRes, ingredientsRes, categoriesRes] = await Promise.all([
        inventoryItemRepository.getAll({ page: 1, size: 100 }),
        ingredientRepository.getAll({ page: 1, size: 100 }),
        categoryRepository.getAll({ page: 1, size: 100 }),
      ]);

      setInventory(inventoryRes.items);
      setIngredients(ingredientsRes.items);
      setCategories(categoriesRes.items);
    } catch (error) {
      console.error("Error loading pantry data:", error);
      toast.error("Failed to load pantry data");
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

  // Helper: Get ingredient details
  const getIngredientDetails = (ingredientId: number) => {
    return ingredients.find((ing) => ing.id === ingredientId);
  };

  // Helper: Get category name
  const getCategoryName = (categoryId: number) => {
    const cat = categories.find((c) => c.id === categoryId);
    if (cat) return cat.categoryName;
    // Fallback names based on ID
    const fallbacks: Record<number, string> = {
      1: "Proteins",
      2: "Pantry",
      3: "Aromatics",
      4: "Produce",
      5: "Grains",
      6: "Dairy",
    };
    return fallbacks[categoryId] || "Other";
  };

  // Filtered Inventory
  const filteredInventory = inventory.filter((item) => {
    const ing = getIngredientDetails(item.ingredientId);
    if (!ing) return false;

    const matchesSearch = ing.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (ing.description && ing.description.toLowerCase().includes(searchQuery.toLowerCase()));

    const matchesCategory = selectedCategory === "all" || ing.categoryId.toString() === selectedCategory;

    return matchesSearch && matchesCategory;
  });

  // Handle Add/Edit Submit
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formIngredientId) {
      toast.error("Please select an ingredient");
      return;
    }

    try {
      const ingId = parseInt(formIngredientId);

      if (editingItem) {
        // Update
        await inventoryItemRepository.updateById(editingItem.id, {
          ingredientId: ingId,
          quantity: formQuantity,
          unit: formUnit,
        });
        toast.success("Pantry item updated successfully");
      } else {
        // Check if already exists
        const existing = inventory.find((item) => item.ingredientId === ingId);
        if (existing) {
          const newQty = (parseFloat(existing.quantity) + parseFloat(formQuantity)).toString();
          await inventoryItemRepository.updateById(existing.id, { quantity: newQty });
          toast.success(`Updated quantity for ${getIngredientDetails(ingId)?.name}`);
        } else {
          // Create
          const newItem = new InventoryItem(
            0,
            1, // userId
            ingId,
            formQuantity,
            formUnit,
            new Date().toISOString(),
            new Date().toISOString()
          );
          await inventoryItemRepository.create(newItem);
          toast.success("Added ingredient to pantry");
        }
      }

      setIsDrawerOpen(false);
      setEditingItem(null);
      resetForm();
      loadData();
    } catch (error) {
      console.error("Error saving pantry item:", error);
      toast.error("Failed to save pantry item");
    }
  };

  // Handle Delete
  const handleDelete = async (id: number, name: string) => {
    try {
      await inventoryItemRepository.deleteById(id);
      toast.success(`Removed ${name} from pantry`);
      loadData();
    } catch (error) {
      console.error("Error deleting pantry item:", error);
      toast.error("Failed to delete pantry item");
    }
  };

  // Open Edit Drawer
  const openEditDrawer = (item: InventoryItem) => {
    setEditingItem(item);
    setFormIngredientId(item.ingredientId.toString());
    setFormQuantity(item.quantity);
    setFormUnit(item.unit || "unit");
    setIsDrawerOpen(true);
  };

  // Reset Form
  const resetForm = () => {
    setFormIngredientId("");
    setFormQuantity("1");
    setFormUnit("unit");
  };

  // Helper: Get expiration status indicator
  const getExpirationStatus = (ingredientId: number) => {
    // Mocking expiration status based on ingredient ID
    if (ingredientId % 3 === 0) {
      return { label: "Expiring Soon", color: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400" };
    }
    if (ingredientId % 5 === 0) {
      return { label: "Use Within 3 Days", color: "bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400" };
    }
    return { label: "Fresh", color: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400" };
  };

  return (
    <Layout>
      <div className="space-y-8" data-usecases="inventory-view-aggregator-a4732472">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-amber-100 dark:border-zinc-800 pb-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
              Pantry Inventory Manager
            </h1>
            <p className="text-zinc-500 dark:text-zinc-400 mt-1">
              Add, edit, or remove ingredients with specific quantities and expiration dates.
            </p>
          </div>
          <div>
            <Button
              onClick={() => {
                setEditingItem(null);
                resetForm();
                setIsDrawerOpen(true);
              }}
              className="bg-amber-500 hover:bg-amber-600 text-white"
              data-usecases="quick-action-orchestrator-71f60a2e"
            >
              <Plus className="h-4 w-4 mr-2" />
              Add Ingredient
            </Button>
          </div>
        </div>

        {/* Search and Filter Controls */}
        <div className="flex flex-col md:flex-row gap-4 items-center justify-between bg-white dark:bg-zinc-900 p-4 rounded-xl border border-amber-100 dark:border-zinc-800" data-usecases="inventory-search-and-filter-engine-6995c7b2">
          <div className="relative w-full md:w-96">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-zinc-400" />
            <Input
              placeholder="Search pantry ingredients..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9 border-amber-200 dark:border-zinc-800 focus-visible:ring-amber-500"
            />
          </div>

          <div className="flex items-center gap-3 w-full md:w-auto justify-end">
            <div className="flex items-center gap-2 text-sm text-zinc-500 dark:text-zinc-400">
              <Filter className="h-4 w-4 text-amber-500" />
              <span>Category:</span>
            </div>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="rounded-md border border-amber-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 px-3 py-1.5 text-sm text-zinc-900 dark:text-zinc-50 focus:outline-none focus:ring-1 focus:ring-amber-500"
            >
              <option value="all">All Categories</option>
              <option value="1">Proteins</option>
              <option value="2">Pantry</option>
              <option value="3">Aromatics</option>
              <option value="4">Produce</option>
              <option value="5">Grains</option>
              <option value="6">Dairy</option>
            </select>

            <Button
              variant="ghost"
              size="icon"
              onClick={loadData}
              className="text-zinc-500 hover:text-amber-600 dark:hover:text-amber-400"
              title="Refresh Data"
            >
              <RefreshCw className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Main Content Table */}
        {loading ? (
          <div className="space-y-4">
            <Skeleton className="h-12 w-full" />
            <Skeleton className="h-12 w-full" />
            <Skeleton className="h-12 w-full" />
            <Skeleton className="h-12 w-full" />
          </div>
        ) : filteredInventory.length > 0 ? (
          <div className="bg-white dark:bg-zinc-900 rounded-xl border border-amber-100 dark:border-zinc-800 overflow-hidden">
            <Table>
              <TableHeader className="bg-amber-50/50 dark:bg-zinc-900/50">
                <TableRow>
                  <TableHead className="font-bold text-zinc-900 dark:text-zinc-100">Ingredient</TableHead>
                  <TableHead className="font-bold text-zinc-900 dark:text-zinc-100">Category</TableHead>
                  <TableHead className="font-bold text-zinc-900 dark:text-zinc-100">Quantity</TableHead>
                  <TableHead className="font-bold text-zinc-900 dark:text-zinc-100">Expiration Status</TableHead>
                  <TableHead className="text-right font-bold text-zinc-900 dark:text-zinc-100">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredInventory.map((item) => {
                  const ing = getIngredientDetails(item.ingredientId);
                  if (!ing) return null;
                  const exp = getExpirationStatus(item.ingredientId);

                  return (
                    <TableRow key={item.id} className="hover:bg-amber-50/10 dark:hover:bg-zinc-800/10 transition-colors">
                      <TableCell className="font-medium">
                        <div className="space-y-0.5">
                          <p className="text-zinc-900 dark:text-zinc-100 font-semibold">{ing.name}</p>
                          {ing.description && (
                            <p className="text-xs text-zinc-500 dark:text-zinc-400">{ing.description}</p>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline" className="border-amber-200 dark:border-zinc-800 text-zinc-700 dark:text-zinc-300">
                          {getCategoryName(ing.categoryId)}
                        </Badge>
                      </TableCell>
                      <TableCell className="font-semibold text-zinc-800 dark:text-zinc-200">
                        {item.quantity} {item.unit || "units"}
                      </TableCell>
                      <TableCell>
                        <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium ${exp.color}`}>
                          <Calendar className="h-3 w-3" />
                          {exp.label}
                        </span>
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Button
                            size="icon"
                            variant="ghost"
                            className="h-8 w-8 text-zinc-500 hover:text-amber-600 dark:hover:text-amber-400 hover:bg-amber-50 dark:hover:bg-zinc-800"
                            onClick={() => openEditDrawer(item)}
                            title="Edit Item"
                            data-usecases="quick-action-orchestrator-71f60a2e"
                          >
                            <Edit2 className="h-4 w-4" />
                          </Button>
                          <Button
                            size="icon"
                            variant="ghost"
                            className="h-8 w-8 text-zinc-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-zinc-800"
                            onClick={() => handleDelete(item.id, ing.name)}
                            title="Delete Item"
                            data-usecases="quick-action-orchestrator-71f60a2e"
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        ) : (
          <div className="text-center py-16 border border-dashed border-amber-200 dark:border-zinc-800 rounded-2xl bg-amber-50/10">
            <AlertTriangle className="h-12 w-12 text-amber-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">No ingredients found</h3>
            <p className="text-zinc-500 dark:text-zinc-400 max-w-md mx-auto mt-1">
              Try adjusting your search query or category filter, or add a new ingredient to your pantry.
            </p>
            <Button
              onClick={() => {
                setEditingItem(null);
                resetForm();
                setIsDrawerOpen(true);
              }}
              className="bg-amber-500 hover:bg-amber-600 text-white mt-4"
              data-usecases="quick-action-orchestrator-71f60a2e"
            >
              Add Your First Ingredient
            </Button>
          </div>
        )}
      </div>

      {/* Add/Edit Ingredient Drawer */}
      <Sheet open={isDrawerOpen} onOpenChange={setIsDrawerOpen}>
        <SheetContent className="w-full sm:max-w-md bg-white dark:bg-zinc-900">
          <form onSubmit={handleSubmit} className="space-y-6 py-4">
            <SheetHeader>
              <SheetTitle className="text-xl font-bold text-zinc-900 dark:text-zinc-50">
                {editingItem ? "Edit Pantry Ingredient" : "Add Pantry Ingredient"}
              </SheetTitle>
              <SheetDescription className="text-zinc-500 dark:text-zinc-400 text-xs">
                Specify the ingredient, quantity, and unit to track in your pantry.
              </SheetDescription>
            </SheetHeader>

            <div className="space-y-4">
              {/* Ingredient Selection */}
              <div className="space-y-2">
                <Label htmlFor="form-ingredient" className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
                  Ingredient
                </Label>
                <select
                  id="form-ingredient"
                  value={formIngredientId}
                  onChange={(e) => setFormIngredientId(e.target.value)}
                  className="w-full rounded-md border border-amber-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 px-3 py-2 text-sm text-zinc-900 dark:text-zinc-50 focus:outline-none focus:ring-1 focus:ring-amber-500"
                  disabled={!!editingItem}
                >
                  <option value="">Select Ingredient...</option>
                  {ingredients.map((ing) => (
                    <option key={ing.id} value={ing.id}>
                      {ing.name} ({getCategoryName(ing.categoryId)})
                    </option>
                  ))}
                </select>
              </div>

              {/* Quantity */}
              <div className="space-y-2">
                <Label htmlFor="form-qty" className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
                  Quantity
                </Label>
                <Input
                  id="form-qty"
                  type="number"
                  placeholder="e.g. 2"
                  value={formQuantity}
                  onChange={(e) => setFormQuantity(e.target.value)}
                  className="border-amber-200 dark:border-zinc-800 focus-visible:ring-amber-500"
                  min="0.1"
                  step="any"
                  required
                />
              </div>

              {/* Unit */}
              <div className="space-y-2">
                <Label htmlFor="form-unit" className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
                  Unit
                </Label>
                <Input
                  id="form-unit"
                  placeholder="e.g. pieces, grams, cups, bottle"
                  value={formUnit}
                  onChange={(e) => setFormUnit(e.target.value)}
                  className="border-amber-200 dark:border-zinc-800 focus-visible:ring-amber-500"
                  required
                />
              </div>
            </div>

            <div className="pt-4 border-t border-zinc-100 dark:border-zinc-800 flex justify-end gap-3">
              <Button
                type="button"
                variant="outline"
                onClick={() => setIsDrawerOpen(false)}
                className="border-amber-200 hover:bg-amber-50 dark:border-zinc-800 dark:hover:bg-zinc-800"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                className="bg-amber-500 hover:bg-amber-600 text-white"
                data-usecases="quick-action-orchestrator-71f60a2e"
              >
                {editingItem ? "Save Changes" : "Add to Pantry"}
              </Button>
            </div>
          </form>
        </SheetContent>
      </Sheet>
    </Layout>
  );
}
