
export interface PerformanceReviewJson {
  details: Record<string, unknown> | null;
  employeeId: number;
  reviewDate: string;
  reviewId: number;
}

export class PerformanceReview {
  constructor(
    public readonly details: Record<string, unknown> | null,
    public readonly employeeId: number,
    public readonly reviewDate: string,
    public readonly reviewId: number,
  ) {}

  static fromJson(json: unknown): PerformanceReview {
    const data = json as PerformanceReviewJson;
    return new PerformanceReview(
      data.details,
      data.employeeId,
      data.reviewDate,
      data.reviewId,
    );
  }

  toJson(): PerformanceReviewJson {
    return {
      details: this.details,
      employeeId: this.employeeId,
      reviewDate: this.reviewDate,
      reviewId: this.reviewId,
    };
  }
}