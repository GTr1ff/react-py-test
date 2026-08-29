
export interface DepartmentJson {
  budget: string | null;
  createdAt: string | null;
  departmentId: number;
  departmentName: string;
  location: string | null;
  managerId: number | null;
  updatedAt: string | null;
}

export class Department {
  constructor(
    public readonly budget: string | null,
    public readonly createdAt: string | null,
    public readonly departmentId: number,
    public readonly departmentName: string,
    public readonly location: string | null,
    public readonly managerId: number | null,
    public readonly updatedAt: string | null,
  ) {}

  static fromJson(json: unknown): Department {
    const data = json as DepartmentJson;
    return new Department(
      data.budget,
      data.createdAt,
      data.departmentId,
      data.departmentName,
      data.location,
      data.managerId,
      data.updatedAt,
    );
  }

  toJson(): DepartmentJson {
    return {
      budget: this.budget,
      createdAt: this.createdAt,
      departmentId: this.departmentId,
      departmentName: this.departmentName,
      location: this.location,
      managerId: this.managerId,
      updatedAt: this.updatedAt,
    };
  }
}