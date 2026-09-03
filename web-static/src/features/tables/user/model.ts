
export interface UserJson {
  id: number;
  username: string;
  email: string;
  hashedPassword: string;
  isActive: boolean;
  lastLoginAt: string | null;
  createdAt: string;
  updatedAt: string;
}

export class User {
  constructor(
    public readonly id: number,
    public readonly username: string,
    public readonly email: string,
    public readonly hashedPassword: string,
    public readonly isActive: boolean,
    public readonly lastLoginAt: string | null,
    public readonly createdAt: string,
    public readonly updatedAt: string,
  ) {}

  static fromJson(json: unknown): User {
    const data = json as UserJson;
    return new User(
      data.id,
      data.username,
      data.email,
      data.hashedPassword,
      data.isActive,
      data.lastLoginAt,
      data.createdAt,
      data.updatedAt,
    );
  }

  toJson(): UserJson {
    return {
      id: this.id,
      username: this.username,
      email: this.email,
      hashedPassword: this.hashedPassword,
      isActive: this.isActive,
      lastLoginAt: this.lastLoginAt,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}