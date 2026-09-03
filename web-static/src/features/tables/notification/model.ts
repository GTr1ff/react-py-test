
export interface NotificationJson {
  id: number;
  userId: number;
  title: string;
  message: string;
  isRead: boolean;
  sentAt: string;
  createdAt: string;
  updatedAt: string;
}

export class Notification {
  constructor(
    public readonly id: number,
    public readonly userId: number,
    public readonly title: string,
    public readonly message: string,
    public readonly isRead: boolean,
    public readonly sentAt: string,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): Notification {
    const data = json as NotificationJson;
    return new Notification(
      data.id,
      data.userId,
      data.title,
      data.message,
      data.isRead,
      data.sentAt,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): NotificationJson {
    return {
      id: this.id,
      userId: this.userId,
      title: this.title,
      message: this.message,
      isRead: this.isRead,
      sentAt: this.sentAt,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}