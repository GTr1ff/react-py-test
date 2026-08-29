
export interface JobHistoryJson {
  employeeId: number;
  endDate: string | null;
  jobHistoryId: number;
  roleId: number;
  startDate: string;
}

export class JobHistory {
  constructor(
    public readonly employeeId: number,
    public readonly endDate: string | null,
    public readonly jobHistoryId: number,
    public readonly roleId: number,
    public readonly startDate: string,
  ) {}

  static fromJson(json: unknown): JobHistory {
    const data = json as JobHistoryJson;
    return new JobHistory(
      data.employeeId,
      data.endDate,
      data.jobHistoryId,
      data.roleId,
      data.startDate,
    );
  }

  toJson(): JobHistoryJson {
    return {
      employeeId: this.employeeId,
      endDate: this.endDate,
      jobHistoryId: this.jobHistoryId,
      roleId: this.roleId,
      startDate: this.startDate,
    };
  }
}