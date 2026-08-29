
export interface RoleJson {
  privileges: unknown | null;
  roleId: number;
  roleName: string;
}

export class Role {
  constructor(
    public readonly privileges: unknown | null,
    public readonly roleId: number,
    public readonly roleName: string,
  ) {}

  static fromJson(json: unknown): Role {
    const data = json as RoleJson;
    return new Role(
      data.privileges,
      data.roleId,
      data.roleName,
    );
  }

  toJson(): RoleJson {
    return {
      privileges: this.privileges,
      roleId: this.roleId,
      roleName: this.roleName,
    };
  }
}