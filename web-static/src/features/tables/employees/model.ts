
export interface EmployeeJson {
  birthDate: string | null;
  createdAt: string | null;
  departmentId: number | null;
  email: string | null;
  employeeId: number;
  firstName: string;
  hireDate: string;
  isActive: boolean | null;
  lastName: string;
  phone: string | null;
  updatedAt: string | null;
}

export class Employee {
  constructor(
    public readonly birthDate: string | null,
    public readonly createdAt: string | null,
    public readonly departmentId: number | null,
    public readonly email: string | null,
    public readonly employeeId: number,
    public readonly firstName: string,
    public readonly hireDate: string,
    public readonly isActive: boolean | null,
    public readonly lastName: string,
    public readonly phone: string | null,
    public readonly updatedAt: string | null,
  ) {}

  static fromJson(json: unknown): Employee {
    const data = json as EmployeeJson;
    return new Employee(
      data.birthDate,
      data.createdAt,
      data.departmentId,
      data.email,
      data.employeeId,
      data.firstName,
      data.hireDate,
      data.isActive,
      data.lastName,
      data.phone,
      data.updatedAt,
    );
  }

  toJson(): EmployeeJson {
    return {
      birthDate: this.birthDate,
      createdAt: this.createdAt,
      departmentId: this.departmentId,
      email: this.email,
      employeeId: this.employeeId,
      firstName: this.firstName,
      hireDate: this.hireDate,
      isActive: this.isActive,
      lastName: this.lastName,
      phone: this.phone,
      updatedAt: this.updatedAt,
    };
  }
}