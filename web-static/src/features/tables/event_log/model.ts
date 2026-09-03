
export interface EventLogJson {
  id: number;
  userId: number;
  eventType: string;
  eventTimestamp: string;
  eventData: Record<string, unknown> | null;
  createdAt: string;
  updatedAt: string;
}

export class EventLog {
  constructor(
    public readonly id: number,
    public readonly userId: number,
    public readonly eventType: string,
    public readonly eventTimestamp: string,
    public readonly eventData: Record<string, unknown> | null,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): EventLog {
    const data = json as EventLogJson;
    return new EventLog(
      data.id,
      data.userId,
      data.eventType,
      data.eventTimestamp,
      data.eventData,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): EventLogJson {
    return {
      id: this.id,
      userId: this.userId,
      eventType: this.eventType,
      eventTimestamp: this.eventTimestamp,
      eventData: this.eventData,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}