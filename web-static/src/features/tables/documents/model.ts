
export interface DocumentJson {
  docContent: string | null;
  docName: string | null;
  docType: string | null;
  documentId: number;
  employeeId: number;
}

export class Document {
  constructor(
    public readonly docContent: string | null,
    public readonly docName: string | null,
    public readonly docType: string | null,
    public readonly documentId: number,
    public readonly employeeId: number,
  ) {}

  static fromJson(json: unknown): Document {
    const data = json as DocumentJson;
    return new Document(
      data.docContent,
      data.docName,
      data.docType,
      data.documentId,
      data.employeeId,
    );
  }

  toJson(): DocumentJson {
    return {
      docContent: this.docContent,
      docName: this.docName,
      docType: this.docType,
      documentId: this.documentId,
      employeeId: this.employeeId,
    };
  }
}