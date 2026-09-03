
export interface ShoppingListItemJson {
  id: number;
  userId: number;
  itemName: string;
  quantity: string | null;
  notes: string | null;
  createdAt: string;
  updatedAt: string;
}

export class ShoppingListItem {
  constructor(
    public readonly id: number,
    public readonly userId: number,
    public readonly itemName: string,
    public readonly quantity: string | null,
    public readonly notes: string | null,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): ShoppingListItem {
    const data = json as ShoppingListItemJson;
    return new ShoppingListItem(
      data.id,
      data.userId,
      data.itemName,
      data.quantity,
      data.notes,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): ShoppingListItemJson {
    return {
      id: this.id,
      userId: this.userId,
      itemName: this.itemName,
      quantity: this.quantity,
      notes: this.notes,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}