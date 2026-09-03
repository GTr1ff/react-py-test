
export interface RecipeJson {
  id: number;
  recipeName: string;
  description: string | null;
  instructions: string | null;
  prepTimeMinutes: number | null;
  cookTimeMinutes: number | null;
  servings: number | null;
  createdAt: string;
  updatedAt: string;
}

export class Recipe {
  constructor(
    public readonly id: number,
    public readonly recipeName: string,
    public readonly description: string | null,
    public readonly instructions: string | null,
    public readonly prepTimeMinutes: number | null,
    public readonly cookTimeMinutes: number | null,
    public readonly servings: number | null,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): Recipe {
    const data = json as RecipeJson;
    return new Recipe(
      data.id,
      data.recipeName,
      data.description,
      data.instructions,
      data.prepTimeMinutes,
      data.cookTimeMinutes,
      data.servings,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): RecipeJson {
    return {
      id: this.id,
      recipeName: this.recipeName,
      description: this.description,
      instructions: this.instructions,
      prepTimeMinutes: this.prepTimeMinutes,
      cookTimeMinutes: this.cookTimeMinutes,
      servings: this.servings,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}