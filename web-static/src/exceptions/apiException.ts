export class ApiException extends Error {
  constructor(
    message: string,
    public readonly statusCode?: number,
    public readonly data?: unknown,
  ) {
    super(message);
    this.name = 'ApiException';
    Object.setPrototypeOf(this, ApiException.prototype);
  }

  override toString(): string {
    return `ApiException: ${this.message}${this.statusCode != null ? ` (Status: ${this.statusCode})` : ''}`;
  }

  get isNotFound(): boolean {
    return this.statusCode === 404;
  }
  get isUnauthorized(): boolean {
    return this.statusCode === 401;
  }
  get isForbidden(): boolean {
    return this.statusCode === 403;
  }
  get isServerError(): boolean {
    return this.statusCode != null && this.statusCode >= 500;
  }
  get isClientError(): boolean {
    return this.statusCode != null && this.statusCode >= 400 && this.statusCode < 500;
  }
}