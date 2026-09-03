
export interface IngredientJson {
  id: number;
  name: string;
  description: string | null;
  categoryId: number;
  createdAt: string;
  updatedAt: string;
}

export class Ingredient {
  constructor(
    public readonly id: number,
    public readonly name: string,
    public readonly description: string | null,
    public readonly categoryId: number,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): Ingredient {
    const data = json as IngredientJson;
    return new Ingredient(
      data.id,
      data.name,
      data.description,
      data.categoryId,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): IngredientJson {
    return {
      id: this.id,
      name: this.name,
      description: this.description,
      categoryId: this.categoryId,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}