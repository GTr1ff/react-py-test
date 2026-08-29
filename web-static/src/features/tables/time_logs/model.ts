
export interface TimeLogJson {
  clockIn: string;
  clockOut: string | null;
  employeeId: number;
  location: string | null;
  timeLogId: number;
}

export class TimeLog {
  constructor(
    public readonly clockIn: string,
    public readonly clockOut: string | null,
    public readonly employeeId: number,
    public readonly location: string | null,
    public readonly timeLogId: number,
  ) {}

  static fromJson(json: unknown): TimeLog {
    const data = json as TimeLogJson;
    return new TimeLog(
      data.clockIn,
      data.clockOut,
      data.employeeId,
      data.location,
      data.timeLogId,
    );
  }

  toJson(): TimeLogJson {
    return {
      clockIn: this.clockIn,
      clockOut: this.clockOut,
      employeeId: this.employeeId,
      location: this.location,
      timeLogId: this.timeLogId,
    };
  }
}