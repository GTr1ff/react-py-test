export class PaginatedResponse<T> {
  constructor(
    public readonly items: T[],
    public readonly total: number,
    public readonly page: number,
    public readonly size: number,
    public readonly pages: number,
  ) {}

  static fromJson<T>(
    json: Record<string, unknown>,
    fromJsonT: (item: unknown) => T,
  ): PaginatedResponse<T> {
    return new PaginatedResponse(
      (json.items as unknown[]).map(fromJsonT),
      json.total as number,
      json.page as number,
      json.size as number,
      json.pages as number,
    );
  }

  get hasNextPage(): boolean {
    return this.page < this.pages;
  }

  get hasPreviousPage(): boolean {
    return this.page > 1;
  }
}