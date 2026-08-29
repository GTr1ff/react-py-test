
export interface BenefitJson {
  benefitId: number;
  benefitName: string;
  benefitType: string | null;
  coverageDetails: Record<string, unknown> | null;
  createdAt: string | null;
  monthlyCost: string | null;
}

export class Benefit {
  constructor(
    public readonly benefitId: number,
    public readonly benefitName: string,
    public readonly benefitType: string | null,
    public readonly coverageDetails: Record<string, unknown> | null,
    public readonly createdAt: string | null,
    public readonly monthlyCost: string | null,
  ) {}

  static fromJson(json: unknown): Benefit {
    const data = json as BenefitJson;
    return new Benefit(
      data.benefitId,
      data.benefitName,
      data.benefitType,
      data.coverageDetails,
      data.createdAt,
      data.monthlyCost,
    );
  }

  toJson(): BenefitJson {
    return {
      benefitId: this.benefitId,
      benefitName: this.benefitName,
      benefitType: this.benefitType,
      coverageDetails: this.coverageDetails,
      createdAt: this.createdAt,
      monthlyCost: this.monthlyCost,
    };
  }
}