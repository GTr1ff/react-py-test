
export interface EmployeeProjectJson {
  assignedDate: string | null;
  employeeId: number;
  employeeProjectId: number;
  projectId: number;
  roleName: string | null;
}

export class EmployeeProject {
  constructor(
    public readonly assignedDate: string | null,
    public readonly employeeId: number,
    public readonly employeeProjectId: number,
    public readonly projectId: number,
    public readonly roleName: string | null,
  ) {}

  static fromJson(json: unknown): EmployeeProject {
    const data = json as EmployeeProjectJson;
    return new EmployeeProject(
      data.assignedDate,
      data.employeeId,
      data.employeeProjectId,
      data.projectId,
      data.roleName,
    );
  }

  toJson(): EmployeeProjectJson {
    return {
      assignedDate: this.assignedDate,
      employeeId: this.employeeId,
      employeeProjectId: this.employeeProjectId,
      projectId: this.projectId,
      roleName: this.roleName,
    };
  }
}