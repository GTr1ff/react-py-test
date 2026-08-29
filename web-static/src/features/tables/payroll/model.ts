
export interface PayrollJson {
  employeeId: number;
  hoursWorked: string | null;
  payPeriodEnd: string;
  payPeriodStart: string;
  payrollId: number;
  wages: string | null;
}

export class Payroll {
  constructor(
    public readonly employeeId: number,
    public readonly hoursWorked: string | null,
    public readonly payPeriodEnd: string,
    public readonly payPeriodStart: string,
    public readonly payrollId: number,
    public readonly wages: string | null,
  ) {}

  static fromJson(json: unknown): Payroll {
    const data = json as PayrollJson;
    return new Payroll(
      data.employeeId,
      data.hoursWorked,
      data.payPeriodEnd,
      data.payPeriodStart,
      data.payrollId,
      data.wages,
    );
  }

  toJson(): PayrollJson {
    return {
      employeeId: this.employeeId,
      hoursWorked: this.hoursWorked,
      payPeriodEnd: this.payPeriodEnd,
      payPeriodStart: this.payPeriodStart,
      payrollId: this.payrollId,
      wages: this.wages,
    };
  }
}