import { useEffect, useState, useCallback } from "react";
import { Layout } from "@/components/Layout";
import { seedPantryPalData } from "@/lib/seedData";
import { shoppingListItemRepository } from "@/features/tables/shopping_list_item/repository";
import { inventoryItemRepository } from "@/features/tables/inventory_item/repository";
import { ingredientRepository } from "@/features/tables/ingredient/repository";
import { ShoppingListItem } from "@/features/tables/shopping_list_item/model";
import { InventoryItem } from "@/features/tables/inventory_item/model";
import { Ingredient } from "@/features/tables/ingredient/model";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { Plus, Trash2, Check, ShoppingCart, RefreshCw, FileText } from "lucide-react";

export default function ShoppingList() {
  // State
  const [shoppingList, setShoppingList] = useState<ShoppingListItem[]>([]);
  const [ingredients, setIngredients] = useState<Ingredient[]>([]);
  const [loading, setLoading] = useState(true);

  // Add Item Form State
  const [formItemName, setFormItemName] = useState("");
  const [formQuantity, setFormQuantity] = useState("1");
  const [formNotes, setFormNotes] = useState("");

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      seedPantryPalData();

      const [shoppingRes, ingredientsRes] = await Promise.all([
        shoppingListItemRepository.getAll({ page: 1, size: 100 }),
        ingredientRepository.getAll({ page: 1, size: 100 }),
      ]);

      setShoppingList(shoppingRes.items);
      setIngredients(ingredientsRes.items);
    } catch (error) {
      console.error("Error loading shopping list data:", error);
      toast.error("Failed to load shopping list data");
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

  // Handle Add Item
  const handleAddItem = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formItemName.trim()) {
      toast.error("Please enter an item name");
      return;
    }

    try {
      const newItem = new ShoppingListItem(
        0,
        1, // userId
        formItemName.trim(),
        formQuantity || "1 unit",
        formNotes.trim() || null,
        new Date().toISOString(),
        new Date().toISOString()
      );

      await shoppingListItemRepository.create(newItem);
      toast.success(`Added ${formItemName} to shopping list`);
      setFormItemName("");
      setFormQuantity("1");
      setFormNotes("");
      loadData();
    } catch (error) {
      console.error("Error adding shopping list item:", error);
      toast.error("Failed to add item");
    }
  };

  // Handle Delete Item
  const handleDeleteItem = async (id: number, name: string) => {
    try {
      await shoppingListItemRepository.deleteById(id);
      toast.success(`Removed ${name} from shopping list`);
      loadData();
    } catch (error) {
      console.error("Error deleting shopping list item:", error);
      toast.error("Failed to delete item");
    }
  };

  // Handle Mark as Purchased (Inventory Reconciliation Service)
  const handleMarkAsPurchased = async (item: ShoppingListItem) => {
    try {
      // 1. Delete from shopping list
      await shoppingListItemRepository.deleteById(item.id);

      // 2. Try to match with existing ingredient to add to pantry
      const matchedIngredient = ingredients.find(
        (ing) => ing.name.toLowerCase() === item.itemName.toLowerCase()
      );

      if (matchedIngredient) {
        // Check if already in pantry
        const pantryItems = await inventoryItemRepository.getAll({ page: 1, size: 100 });
        const existing = pantryItems.items.find((pi) => pi.ingredientId === matchedIngredient.id);

        if (existing) {
          // Update quantity
          const currentQty = parseFloat(existing.quantity) || 0;
          const addedQty = parseFloat(item.quantity || "1") || 1;
          const newQty = (currentQty + addedQty).toString();
          await inventoryItemRepository.updateById(existing.id, { quantity: newQty });
        } else {
          // Create new pantry item
          const newPantryItem = new InventoryItem(
            0,
            1, // userId
            matchedIngredient.id,
            item.quantity || "1",
            "unit",
            new Date().toISOString(),
            new Date().toISOString()
          );
          await inventoryItemRepository.create(newPantryItem);
        }
        toast.success(`Purchased ${item.itemName} and added to pantry!`);
      } else {
        toast.success(`Purchased ${item.itemName}!`);
      }

      loadData();
    } catch (error) {
      console.error("Error marking item as purchased:", error);
      toast.error("Failed to complete purchase");
    }
  };

  return (
    <Layout>
      <div className="space-y-8" data-usecases="shopping-list-generator-3a1a4ea9">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-amber-100 dark:border-zinc-800 pb-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50">
              Shopping List Integration
            </h1>
            <p className="text-zinc-500 dark:text-zinc-400 mt-1">
              Track items needed for recipes that are not currently in your pantry.
            </p>
          </div>
          <div>
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

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Add Item Form */}
          <div className="space-y-6">
            <Card className="border-amber-100 dark:border-zinc-800 shadow-sm">
              <CardHeader>
                <CardTitle className="text-lg font-bold text-zinc-900 dark:text-zinc-50">
                  Add Custom Item
                </CardTitle>
                <CardDescription className="text-xs">
                  Add items manually to your shopping list.
                </CardDescription>
              </CardHeader>

              <CardContent>
                <form onSubmit={handleAddItem} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="item-name" className="text-xs font-semibold text-zinc-700 dark:text-zinc-300">
                      Item Name
                    </Label>
                    <Input
                      id="item-name"
                      placeholder="e.g. Milk, Bacon, Cheese"
                      value={formItemName}
                      onChange={(e) => setFormItemName(e.target.value)}
                      className="border-amber-200 dark:border-zinc-800 focus-visible:ring-amber-500"
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="item-qty" className="text-xs font-semibold text-zinc-700 dark:text-zinc-300">
                      Quantity / Unit
                    </Label>
                    <Input
                      id="item-qty"
                      placeholder="e.g. 1 pack, 500g, 2 bottles"
                      value={formQuantity}
                      onChange={(e) => setFormQuantity(e.target.value)}
                      className="border-amber-200 dark:border-zinc-800 focus-visible:ring-amber-500"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="item-notes" className="text-xs font-semibold text-zinc-700 dark:text-zinc-300">
                      Notes
                    </Label>
                    <Input
                      id="item-notes"
                      placeholder="e.g. For breakfast omelette"
                      value={formNotes}
                      onChange={(e) => setFormNotes(e.target.value)}
                      className="border-amber-200 dark:border-zinc-800 focus-visible:ring-amber-500"
                    />
                  </div>

                  <Button
                    type="submit"
                    className="w-full bg-amber-500 hover:bg-amber-600 text-white"
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Add to List
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Right Column: Shopping List Items */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="border-amber-100 dark:border-zinc-800 shadow-sm">
              <CardHeader className="pb-4">
                <div className="flex justify-between items-center">
                  <CardTitle className="text-lg font-bold text-zinc-900 dark:text-zinc-50">
                    Your Shopping List
                  </CardTitle>
                  <Badge className="bg-amber-100 text-amber-800 dark:bg-zinc-800 dark:text-amber-300">
                    {shoppingList.length} Items
                  </Badge>
                </div>
                <CardDescription className="text-xs">
                  Items marked as purchased will automatically reconcile with your pantry if they match known ingredients.
                </CardDescription>
              </CardHeader>

              <CardContent className="space-y-4">
                {loading ? (
                  <div className="space-y-3">
                    <Skeleton className="h-12 w-full" />
                    <Skeleton className="h-12 w-full" />
                    <Skeleton className="h-12 w-full" />
                  </div>
                ) : shoppingList.length > 0 ? (
                  <div className="space-y-3" data-usecases="shopping-list-categorizer-ceddc312">
                    {shoppingList.map((item) => {
                      const isKnown = ingredients.some(
                        (ing) => ing.name.toLowerCase() === item.itemName.toLowerCase()
                      );

                      return (
                        <div
                          key={item.id}
                          className="flex items-center justify-between p-4 rounded-xl border border-amber-50 dark:border-zinc-800/50 hover:bg-amber-50/30 dark:hover:bg-zinc-900/30 transition-all duration-200"
                        >
                          <div className="space-y-1">
                            <div className="flex items-center gap-2">
                              <p className="font-bold text-zinc-900 dark:text-zinc-100">
                                {item.itemName}
                              </p>
                              {isKnown ? (
                                <Badge variant="outline" className="text-[10px] border-green-200 text-green-700 bg-green-50/50 dark:border-green-900/30 dark:text-green-400">
                                  Matches Ingredient
                                </Badge>
                              ) : (
                                <Badge variant="outline" className="text-[10px] border-zinc-200 text-zinc-500 bg-zinc-50/50 dark:border-zinc-800 dark:text-zinc-400">
                                  Custom Item
                                </Badge>
                              )}
                            </div>
                            <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-zinc-500 dark:text-zinc-400">
                              <span className="font-semibold text-amber-700 dark:text-amber-400">
                                Qty: {item.quantity || "1 unit"}
                              </span>
                              {item.notes && (
                                <span className="flex items-center gap-1">
                                  <FileText className="h-3.5 w-3.5 text-zinc-400" />
                                  {item.notes}
                                </span>
                              )}
                            </div>
                          </div>

                          <div className="flex items-center gap-2">
                            <Button
                              size="sm"
                              className="bg-green-600 hover:bg-green-700 text-white h-8 px-3 text-xs flex items-center gap-1"
                              onClick={() => handleMarkAsPurchased(item)}
                              data-usecases="inventory-reconciliation-service-3e8b1387"
                            >
                              <Check className="h-3.5 w-3.5" />
                              <span>Purchased</span>
                            </Button>
                            <Button
                              size="icon"
                              variant="ghost"
                              className="h-8 w-8 text-zinc-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-zinc-800"
                              onClick={() => handleDeleteItem(item.id, item.itemName)}
                              title="Delete Item"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div className="text-center py-12 border border-dashed border-amber-200 dark:border-zinc-800 rounded-2xl bg-amber-50/10">
                    <ShoppingCart className="h-12 w-12 text-amber-400 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Your shopping list is empty</h3>
                    <p className="text-zinc-500 dark:text-zinc-400 max-w-md mx-auto mt-1">
                      Add items manually or click the shopping cart icon on any recipe to add missing ingredients.
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
}
