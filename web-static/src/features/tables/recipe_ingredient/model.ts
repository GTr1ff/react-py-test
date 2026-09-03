
export interface RecipeIngredientJson {
  recipeId: number;
  ingredientId: number;
  quantity: string;
  unit: string | null;
  createdAt: string;
  updatedAt: string;
}

export class RecipeIngredient {
  constructor(
    public readonly recipeId: number,
    public readonly ingredientId: number,
    public readonly quantity: string,
    public readonly unit: string | null,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): RecipeIngredient {
    const data = json as RecipeIngredientJson;
    return new RecipeIngredient(
      data.recipeId,
      data.ingredientId,
      data.quantity,
      data.unit,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): RecipeIngredientJson {
    return {
      recipeId: this.recipeId,
      ingredientId: this.ingredientId,
      quantity: this.quantity,
      unit: this.unit,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}