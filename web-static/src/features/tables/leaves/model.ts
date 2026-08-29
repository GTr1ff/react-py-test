
export interface LeafJson {
  approvalStatus: string | null;
  approvedBy: number | null;
  employeeId: number;
  endDate: string;
  leaveId: number;
  reason: string | null;
  startDate: string;
}

export class Leaf {
  constructor(
    public readonly approvalStatus: string | null,
    public readonly approvedBy: number | null,
    public readonly employeeId: number,
    public readonly endDate: string,
    public readonly leaveId: number,
    public readonly reason: string | null,
    public readonly startDate: string,
  ) {}

  static fromJson(json: unknown): Leaf {
    const data = json as LeafJson;
    return new Leaf(
      data.approvalStatus,
      data.approvedBy,
      data.employeeId,
      data.endDate,
      data.leaveId,
      data.reason,
      data.startDate,
    );
  }

  toJson(): LeafJson {
    return {
      approvalStatus: this.approvalStatus,
      approvedBy: this.approvedBy,
      employeeId: this.employeeId,
      endDate: this.endDate,
      leaveId: this.leaveId,
      reason: this.reason,
      startDate: this.startDate,
    };
  }
}