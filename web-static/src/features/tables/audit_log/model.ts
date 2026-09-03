
export interface AuditLogJson {
  id: number;
  userId: number;
  changeType: string;
  changedData: Record<string, unknown>;
  changeTimestamp: string;
  createdAt: string;
  updatedAt: string;
}

export class AuditLog {
  constructor(
    public readonly id: number,
    public readonly userId: number,
    public readonly changeType: string,
    public readonly changedData: Record<string, unknown>,
    public readonly changeTimestamp: string,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): AuditLog {
    const data = json as AuditLogJson;
    return new AuditLog(
      data.id,
      data.userId,
      data.changeType,
      data.changedData,
      data.changeTimestamp,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): AuditLogJson {
    return {
      id: this.id,
      userId: this.userId,
      changeType: this.changeType,
      changedData: this.changedData,
      changeTimestamp: this.changeTimestamp,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}