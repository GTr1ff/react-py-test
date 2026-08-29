
export interface ProjectJson {
  budget: string | null;
  createdAt: string | null;
  endDate: string | null;
  projectId: number;
  projectName: string;
  startDate: string | null;
  status: string;
  tags: unknown | null;
}

export class Project {
  constructor(
    public readonly budget: string | null,
    public readonly createdAt: string | null,
    public readonly endDate: string | null,
    public readonly projectId: number,
    public readonly projectName: string,
    public readonly startDate: string | null,
    public readonly status: string,
    public readonly tags: unknown | null,
  ) {}

  static fromJson(json: unknown): Project {
    const data = json as ProjectJson;
    return new Project(
      data.budget,
      data.createdAt,
      data.endDate,
      data.projectId,
      data.projectName,
      data.startDate,
      data.status,
      data.tags,
    );
  }

  toJson(): ProjectJson {
    return {
      budget: this.budget,
      createdAt: this.createdAt,
      endDate: this.endDate,
      projectId: this.projectId,
      projectName: this.projectName,
      startDate: this.startDate,
      status: this.status,
      tags: this.tags,
    };
  }
}