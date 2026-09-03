
export interface UserPreferenceJson {
  id: number;
  userId: number;
  theme: string | null;
  language: string | null;
  notificationsEnabled: boolean;
  createdAt: string;
  updatedAt: string;
}

export class UserPreference {
  constructor(
    public readonly id: number,
    public readonly userId: number,
    public readonly theme: string | null,
    public readonly language: string | null,
    public readonly notificationsEnabled: boolean,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): UserPreference {
    const data = json as UserPreferenceJson;
    return new UserPreference(
      data.id,
      data.userId,
      data.theme,
      data.language,
      data.notificationsEnabled,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): UserPreferenceJson {
    return {
      id: this.id,
      userId: this.userId,
      theme: this.theme,
      language: this.language,
      notificationsEnabled: this.notificationsEnabled,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}