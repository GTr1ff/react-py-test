
import { apiClient } from "@/api/apiClient";
import { PaginatedResponse } from "@/models/paginatedResponse";
import type { PaginationRequest } from "@/api/paginationRequest";
import { ApiException } from "@/exceptions/apiException";
import { appConfig } from "@/config/appConfig";
import { useMockDb } from "@/stores/mockDbStore";
import { PerformanceReview, type PerformanceReviewJson } from "./model";
import { performance_reviewsSchema } from "./schema";


const ENDPOINT = "/performance-reviews";
const TABLE = "performance_reviews";
const PK = "reviewId";

export const performance_reviewsRepository = {
  // ─── Create ──────────────────────────────────
  async create(record: PerformanceReview): Promise<PerformanceReview> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, performance_reviewsSchema);
      const inserted = db.insert(TABLE, record.toJson() as unknown as Record<string, unknown>, PK);
      return PerformanceReview.fromJson(inserted);
    }
    return apiClient.post(ENDPOINT, {
      data: record.toJson(),
      fromJson: (json) => PerformanceReview.fromJson(json),
    });
  },

  // ─── Read ────────────────────────────────────
  async getById(id: number): Promise<PerformanceReview> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, performance_reviewsSchema);
      const row = db.getById(TABLE, PK, id);
      if (!row) throw new ApiException("Not found", 404);
      return PerformanceReview.fromJson(row);
    }
    return apiClient.get(`${ENDPOINT}/${ id }`, {
      fromJson: (json) => PerformanceReview.fromJson(json),
    });
  },

  async getAll(pagination: PaginationRequest): Promise<PaginatedResponse<PerformanceReview>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, performance_reviewsSchema);
      const items = db.getAll(TABLE).map(PerformanceReview.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(ENDPOINT, {
      params: pagination,
      fromJson: (json) => PerformanceReview.fromJson(json),
    });
  },

  async search(
    filters: Record<string, unknown>,
    pagination: PaginationRequest,
  ): Promise<PaginatedResponse<PerformanceReview>> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, performance_reviewsSchema);
      const items = db
        .getAll(TABLE)
        .filter((row) =>
          Object.entries(filters).every(([key, value]) => row[key] === value),
        )
        .map(PerformanceReview.fromJson);
      return new PaginatedResponse(items, items.length, pagination.page ?? 1, pagination.size ?? items.length, 1);
    }
    return apiClient.getPaginated(`${ENDPOINT}/search`, {
      params: { ...filters, ...pagination },
      fromJson: (json) => PerformanceReview.fromJson(json),
    });
  },

  // ─── Update ──────────────────────────────────
  async updateById(
    id: number,
    updates: Partial<PerformanceReviewJson>,
  ): Promise<PerformanceReview> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, performance_reviewsSchema);
      const updated = db.update(TABLE, PK, id, updates as unknown as Record<string, unknown>);
      if (!updated) throw new ApiException("Not found", 404);
      return PerformanceReview.fromJson(updated);
    }
    return apiClient.put(`${ENDPOINT}/${ id }`, {
      data: updates,
      fromJson: (json) => PerformanceReview.fromJson(json),
    });
  },

  // ─── Delete ──────────────────────────────────
  async deleteById(id: number): Promise<void> {
    if (appConfig.useMocks) {
      const db = useMockDb.getState();
      db.seed(TABLE, performance_reviewsSchema);
      db.remove(TABLE, PK, id);
      return;
    }
    await apiClient.delete(`${ENDPOINT}/${ id }`);
  },
};
