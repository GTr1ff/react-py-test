
export interface InventoryItemJson {
  id: number;
  userId: number;
  ingredientId: number;
  quantity: string;
  unit: string | null;
  createdAt: string;
  updatedAt: string;
}

export class InventoryItem {
  constructor(
    public readonly id: number,
    public readonly userId: number,
    public readonly ingredientId: number,
    public readonly quantity: string,
    public readonly unit: string | null,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): InventoryItem {
    const data = json as InventoryItemJson;
    return new InventoryItem(
      data.id,
      data.userId,
      data.ingredientId,
      data.quantity,
      data.unit,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): InventoryItemJson {
    return {
      id: this.id,
      userId: this.userId,
      ingredientId: this.ingredientId,
      quantity: this.quantity,
      unit: this.unit,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}