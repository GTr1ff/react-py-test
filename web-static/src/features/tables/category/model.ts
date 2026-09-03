
export interface CategoryJson {
  id: number;
  categoryName: string;
  description: string | null;
  createdAt: string;
  updatedAt: string;
}

export class Category {
  constructor(
    public readonly id: number,
    public readonly categoryName: string,
    public readonly description: string | null,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): Category {
    const data = json as CategoryJson;
    return new Category(
      data.id,
      data.categoryName,
      data.description,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): CategoryJson {
    return {
      id: this.id,
      categoryName: this.categoryName,
      description: this.description,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}