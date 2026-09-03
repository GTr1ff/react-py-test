
export interface TagJson {
  id: number;
  tagName: string;
  description: string | null;
  createdAt: string;
  updatedAt: string;
}

export class Tag {
  constructor(
    public readonly id: number,
    public readonly tagName: string,
    public readonly description: string | null,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): Tag {
    const data = json as TagJson;
    return new Tag(
      data.id,
      data.tagName,
      data.description,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): TagJson {
    return {
      id: this.id,
      tagName: this.tagName,
      description: this.description,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}