
export interface EmployeeBenefitJson {
  benefitId: number;
  employeeBenefitId: number;
  employeeId: number;
  enrollmentDate: string;
}

export class EmployeeBenefit {
  constructor(
    public readonly benefitId: number,
    public readonly employeeBenefitId: number,
    public readonly employeeId: number,
    public readonly enrollmentDate: string,
  ) {}

  static fromJson(json: unknown): EmployeeBenefit {
    const data = json as EmployeeBenefitJson;
    return new EmployeeBenefit(
      data.benefitId,
      data.employeeBenefitId,
      data.employeeId,
      data.enrollmentDate,
    );
  }

  toJson(): EmployeeBenefitJson {
    return {
      benefitId: this.benefitId,
      employeeBenefitId: this.employeeBenefitId,
      employeeId: this.employeeId,
      enrollmentDate: this.enrollmentDate,
    };
  }
}