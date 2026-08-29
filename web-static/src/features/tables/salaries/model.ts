
export interface SalaryJson {
  currency: string;
  effectiveDate: string;
  employeeId: number;
  salary: string;
  salaryId: number;
}

export class Salary {
  constructor(
    public readonly currency: string,
    public readonly effectiveDate: string,
    public readonly employeeId: number,
    public readonly salary: string,
    public readonly salaryId: number,
  ) {}

  static fromJson(json: unknown): Salary {
    const data = json as SalaryJson;
    return new Salary(
      data.currency,
      data.effectiveDate,
      data.employeeId,
      data.salary,
      data.salaryId,
    );
  }

  toJson(): SalaryJson {
    return {
      currency: this.currency,
      effectiveDate: this.effectiveDate,
      employeeId: this.employeeId,
      salary: this.salary,
      salaryId: this.salaryId,
    };
  }
}