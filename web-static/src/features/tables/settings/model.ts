
export interface SettingJson {
  settingId: number;
  settingKey: string;
  settingValue: Record<string, unknown> | null;
  updatedAt: string | null;
}

export class Setting {
  constructor(
    public readonly settingId: number,
    public readonly settingKey: string,
    public readonly settingValue: Record<string, unknown> | null,
    public readonly updatedAt: string | null,
  ) {}

  static fromJson(json: unknown): Setting {
    const data = json as SettingJson;
    return new Setting(
      data.settingId,
      data.settingKey,
      data.settingValue,
      data.updatedAt,
    );
  }

  toJson(): SettingJson {
    return {
      settingId: this.settingId,
      settingKey: this.settingKey,
      settingValue: this.settingValue,
      updatedAt: this.updatedAt,
    };
  }
}