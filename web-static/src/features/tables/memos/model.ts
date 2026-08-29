
export interface MemoJson {
  ccEmployees: unknown | null;
  createdAt: string | null;
  memoId: number;
  message: string;
}

export class Memo {
  constructor(
    public readonly ccEmployees: unknown | null,
    public readonly createdAt: string | null,
    public readonly memoId: number,
    public readonly message: string,
  ) {}

  static fromJson(json: unknown): Memo {
    const data = json as MemoJson;
    return new Memo(
      data.ccEmployees,
      data.createdAt,
      data.memoId,
      data.message,
    );
  }

  toJson(): MemoJson {
    return {
      ccEmployees: this.ccEmployees,
      createdAt: this.createdAt,
      memoId: this.memoId,
      message: this.message,
    };
  }
}