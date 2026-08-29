
export interface TaskJson {
  assignedTo: number | null;
  attachment: string | null;
  completed: boolean | null;
  dueDate: string | null;
  notes: string | null;
  projectId: number;
  taskId: number;
}

export class Task {
  constructor(
    public readonly assignedTo: number | null,
    public readonly attachment: string | null,
    public readonly completed: boolean | null,
    public readonly dueDate: string | null,
    public readonly notes: string | null,
    public readonly projectId: number,
    public readonly taskId: number,
  ) {}

  static fromJson(json: unknown): Task {
    const data = json as TaskJson;
    return new Task(
      data.assignedTo,
      data.attachment,
      data.completed,
      data.dueDate,
      data.notes,
      data.projectId,
      data.taskId,
    );
  }

  toJson(): TaskJson {
    return {
      assignedTo: this.assignedTo,
      attachment: this.attachment,
      completed: this.completed,
      dueDate: this.dueDate,
      notes: this.notes,
      projectId: this.projectId,
      taskId: this.taskId,
    };
  }
}