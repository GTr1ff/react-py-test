
export interface SessionJson {
  id: number;
  userId: number;
  sessionToken: string;
  ipAddress: string | null;
  userAgent: string | null;
  expiresAt: string;
  createdAt: string;
  updatedAt: string;
}

export class Session {
  constructor(
    public readonly id: number,
    public readonly userId: number,
    public readonly sessionToken: string,
    public readonly ipAddress: string | null,
    public readonly userAgent: string | null,
    public readonly expiresAt: string,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): Session {
    const data = json as SessionJson;
    return new Session(
      data.id,
      data.userId,
      data.sessionToken,
      data.ipAddress,
      data.userAgent,
      data.expiresAt,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): SessionJson {
    return {
      id: this.id,
      userId: this.userId,
      sessionToken: this.sessionToken,
      ipAddress: this.ipAddress,
      userAgent: this.userAgent,
      expiresAt: this.expiresAt,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}