
export interface ConsentJson {
  id: number;
  userId: number;
  consentType: string;
  consentGivenAt: string;
  consentRevokedAt: string | null;
  createdAt: string;
  updatedAt: string;
}

export class Consent {
  constructor(
    public readonly id: number,
    public readonly userId: number,
    public readonly consentType: string,
    public readonly consentGivenAt: string,
    public readonly consentRevokedAt: string | null,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): Consent {
    const data = json as ConsentJson;
    return new Consent(
      data.id,
      data.userId,
      data.consentType,
      data.consentGivenAt,
      data.consentRevokedAt,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): ConsentJson {
    return {
      id: this.id,
      userId: this.userId,
      consentType: this.consentType,
      consentGivenAt: this.consentGivenAt,
      consentRevokedAt: this.consentRevokedAt,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}